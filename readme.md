# This is a walkthrough of the EzeeAssist Web Scraping Engineer Assignment
## 1. How to Run the Script.
### a. Open the command line in the code editor (preferably VSCode)
### b. Create a virtualenv with by typing command _pipenv --python 3.11_ in CLI.
### c. Then run command _pipenv shell_
### d. Then run the command _pip install -r requirements.txt_
### e. At the root directory of the project, run the command _python client.py_

## 2. Logic
### As per the assignment, EzeeAssist is looking for all the data that is available in the website https://franchisesuppliernetwork.com . Broadly there are two types of data, text and image. This project has scraped text data using three scripts, fns_supplier_scraper.py, home_scraper.py, and resources_scraper.py
### FNS Supplier has 95 pages
### resources scraper has 144 pages
### Home Page Scraper has 14 pages.

## 3. Detailed Description
### a. FNS Supplier Scraper has two levels of hierarchy alongwith pagination, each page has been scraped and stored into a csv file. Both text and images scraped.
### b. Likewise, Resources Scraper has a single level hierarchy with pagination, each page has been scraped and stored into a csv file. Both text and images scraped.
### c. Home page has 13 major links, one for each page. All of those pages have been scraped. The text data is scraped and stored alongith image data.

## 4. Image Scraping
### All the images collected from the previous scraping stages are stored into a list. Then, we convert each image into a bytes object by using IO module, then we convert that bytes object into a RGB file using PIL module. Finally, each image is saved as a .PNG file by specifying the path  