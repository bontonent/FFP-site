# Project

## Describe

### Type
- url: https://ffp.nl/vind-een-planner/
- speed page search: 17 it/s
- speed page people: 3.7 it/s
- All time: 913 items 5 min and less

---
### User library
requirements.txt
```bash
- pandas
- bs4
- lxml
- requests
- tqdm
- openpyxl
```

### How run project themselves

##### Get project
```bash
git copy https://github.com/bontonent/FFP-site.git
cd ./FFP-site
```

##### Make environment with library
```bash
python -m venv .venv
source ./.venv/bin/activate # for linux
pip install -r requirements.txt
```

##### Run project
```bash
python main.py
```

---
## Exercise

#### Summary
We are seeking a skilled web scraper to extract all contact information, including email addresses, from the following page: https://ffp.nl/vind-een-planner/

We only need the contacts categorized under 'Vermogensopbouw' (169 contacts) The ideal candidate will have experience with data scraping tools and techniques. You will be responsible for collecting accurate email data from each relevant pages.

Each contact has its own individual page with phone number, website, email and address. We want to extract that as well.

#### Deliverables
A CSV/Excel file containing 169 contacts from the FFP page including contact details.

##### Complete in answer.xlsx