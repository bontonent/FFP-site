# Parsing lib
import requests
from lxml import html

# Work with data lib
import numpy as np
import re 

# Export in excel
import pandas as pd

# Work with threading
from concurrent.futures import ThreadPoolExecutor, as_completed

# Visual load
from tqdm import tqdm

# Sup python script with def
import google_key

# Stop work
import sys

# Main class
class main_exercise:
    def __init__(self,url):
        # Check such work url
        self.url = url
        respons = requests.get(self.url)
        if str(respons) != "<Response [200]>":
            sys.exit(0)

        # Search max people
        page_search = html.fromstring(respons.content)
        count_people_page = page_search.xpath('//strong/text()')
        count_people = int(str(count_people_page[0]).replace(" resultaten",""))

        # In page 20 peaople. People/20 = pages
        if float(count_people/20) != int(count_people/20):
            max_page = int(count_people/20)+1
        print("Max page:",max_page)
        
        # Array pages
        self.range_page = np.array(range(max_page+1))[1:]
        
        # Create 
        self.df = pd.DataFrame(columns = ['Name','Email','Telephone','Address','Google address','Photo','Web-Site'])

        # Save main data
        self.all_url_users = []
        self.datas=[]
        
        
    # Main round
    def main(self):
        
        # Run Treading element for get users
        with ThreadPoolExecutor(max_workers=5) as thread_position:
            list(
               tqdm(
                   thread_position.map(self.get_pages,self.range_page)
                   , total=len(self.range_page)        
               )
        )

        # self.all_url_users = ['https://ffp.nl/planner/nmvessies', 'https://ffp.nl/planner/jejverweij', 'https://ffp.nl/planner/dntvo', 'https://ffp.nl/planner/rrjvleugels', 'https://ffp.nl/planner/stmvinkvanliemt', 'https://ffp.nl/planner/pverkuijlvinkcfp', 'https://ffp.nl/planner/geverhoefba', 'https://ffp.nl/planner/avisbeen', 'https://ffp.nl/planner/jverheij', 'https://ffp.nl/planner/accmverploeghcfp', 'https://ffp.nl/planner/ljmversantvoort', 'https://ffp.nl/planner/pbdevethcfp', 'https://ffp.nl/planner/kversluijsentius', 'https://ffp.nl/planner/caavandervleutencfp', 'https://ffp.nl/planner/hmphvincken', 'https://ffp.nl/planner/adevisser', 'https://ffp.nl/planner/pahverstappenmfpcfpbc', 'https://ffp.nl/planner/jddevlugtcfp', 'https://ffp.nl/planner/ajjverstegen', 'https://ffp.nl/planner/rgahverheijen']
        # print(len(self.all_url_users))
        
        max_workers = 3
        time_delay = 3
        retries_work = 3
        futures = {}

        with ThreadPoolExecutor(max_workers) as thread:
            for user in tqdm(self.all_url_users):
                futures[thread.submit(self.data_person,user)] = user
            try:
                for fut in tqdm(as_completed(futures),total =len(futures)):
                    src = futures[fut]
                    result_data = {
                            "Name": None
                            , "Photo" : None
                            , "Telephone": None
                            , "Web-Site": None
                            , "Email": None
                            , "Address": None
                            , "Google address": None
                            , "Page_person" : src
                        }
                    
                    
                    try:
                        result_data = fut.result(timeout=time_delay)
                        # print()
                    except Exception as e:
                        # error if Retries == 0
                        if retries_work > 0: 
                            for n in range(retries_work):
                                try:
                                    retry_res = thread.submit(self.data_person, user).result(timeout=time_delay)
                                    print(retry_res)
                                    result_data = retry_res
                                    print("don't work such")
                                    break
                                except Exception as e2:
                                    continue
                    self.datas.append(result_data)
                    
            except KeyboardInterrupt:
                # user cancellation: try to cancel pending futures
                for f in futures:
                    f.cancel()
                raise
        
        # Write data
        for data in self.datas:
            self.df.loc[len(self.df)] = data

        
        self.df.to_excel("answer.xlsx")

    # Catalog peoples get data
    def get_pages(self,i):
        # Parsing url number i
        url_work = "".join([self.url[:len(self.url)-1],str(i)])
        request = requests.get(url_work)
        page_search = html.fromstring(request.content)

        # Get each people
        pages_oneclick = page_search.xpath('//div[@class="inner-block"]/@onclick')
        urls = []
        for page_oneclick in pages_oneclick:
            url = str(page_oneclick).split("'")[1]
            url_people = "".join(["https://ffp.nl",url])
            urls.append(url_people)

            # Save data
            self.all_url_users.append(url_people)
        print(urls)

    # Get data person
    def data_person(self, url_person):
        # Open url
        respons = requests.get(url_person)
        page_people = html.fromstring(respons.content)

        # Need data get
        data = {
            "Name": None
            , "Photo" : None
            , "Telephone": None
            , "Web-Site": None
            , "Email": None
            , "Address": None
            , "Google address": None
            , "Page_person" : url_person
        }

        # Get photo if have
        url_photos = page_people.xpath('//div[@class="profile-wrap"]/img/@src')
        for photo in url_photos:
            if photo == photo.replace("https://ffp.nl/wp-content/uploads",""):
                data["Photo"] = photo

        # Get url block if have
        url_btnes = page_people.xpath('//div[@class="btn-wrap"]/a/@href')
        for block in url_btnes:
            if block != block.replace("tel:",""):
                data["Telephone"] = block.replace("tel:","")
            elif block != block.replace("https:",""):
                data["Web-Site"] = block
            elif block != block.replace("mailto:",""):
                data["Email"] = block.replace("mailto:","")

        # Get name
        page_h = page_people.xpath('//div[@class="default-content"]/h1/text()')
        if page_h != []:
            data["Name"] = page_h[0]

        # Get Adresss
        page_h = page_people.xpath('//div[@class="default-content"]/p/text()')
        if page_h != []:
            s_text = "".join(page_h)
            addrs = re.sub(r'\s+', ' ', s_text).strip()
            data["Address"] = addrs

        # Get google key for get address
        ifram_googles = page_people.xpath('//div/iframe/@src')
        for ifram_google in ifram_googles:
            url_google = ifram_google

            # Get google key
            google_address = google_key.get_address_google(url_google)
            data["Google address"] = str(google_address)
        return data


# Run
if __name__ == "__main__":
    # Url search(we can change on another)
    url = "https://ffp.nl/vind-een-planner/?gespecialiseerd_vermogensopbouw=vermogensopbouw&pageNumber=1"
    work = main_exercise(url)
    work.main()
