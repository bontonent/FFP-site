# Parsing lib
import requests
from bs4 import BeautifulSoup

# Work with data lib
import re

# Get address google
def get_address_google(url_google):
    # Open google key
    respons = requests.get(url_google)
    soup = BeautifulSoup(respons.content,'lxml')

    # Get necessary data (a lot of data work)
    masive = str(soup).split("initEmbed")[1].split(";")[0]
    elements = masive.replace("null,","")
    work_element = True
    google_address = ""
    for element in elements.split('"'):
        data = re.finditer(r"\S+\s\S+\s\S+",element)
        for dat in data:
            if google_address == "":
                google_address = dat.group(0)
            else:
                google_address = " ".join([google_address, dat.group(0)])
            work_element = False
        if work_element != True:
            break

    # return google address
    return google_address

if __name__ == '__main__':
    url_google = "https://www.google.com/maps/embed/v1/place?key=AIzaSyDYxfDTHwtcSZEZvkSsyRhjoF1xHdbmvxc&q=3502MA,Stadsplateau 20"
    print(get_address_google(url_google))