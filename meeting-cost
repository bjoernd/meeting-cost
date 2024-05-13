#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from io import StringIO
import time
import pandas as pd

SDE_URL="https://www.levels.fyi/companies/amazon/salaries/software-engineer?country=254"
SDM_URL="https://www.levels.fyi/companies/amazon/salaries/software-engineering-manager?country=254"


def extract_salaries(url):
    # Set up Chrome webdriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # To run Chrome in headless mode
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    service = Service('/usr/bin/chromedriver')  # Path to your ChromeDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Load the webpage
    driver.get(url)

    # Wait for the content to load
    wait = WebDriverWait(driver, 10)
    div_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiTableContainer-root.job-family_tableContainer__MOxEY.css-kge0eu")))

    # Find the link to Click
    link_to_click = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".MuiButton-root.MuiButton-text.MuiButton-textNeutral.MuiButton-sizeLarge.MuiButton-textSizeLarge.MuiButtonBase-root.css-1t9hmlk")))
    # Click the link
    link_to_click.click()
    time.sleep(3)

    # Get the page content
    page_content = driver.page_source.replace('\n', ' ')

    # Quit the driver
    driver.quit()

    with open("./amazon_salaries.html", "w") as f:
        f.write(page_content)

    tables = pd.read_html(StringIO(page_content))

    return tables[0]


def create_salary_dict(df):
    ret = {}

    for key in ["L4", "L5", "L6", "L7", "L8"]:
        data = df[df["Level Name"].str.contains(key)]
        if not data.empty:
            salary = data["Total"].values[0]
            salary = salary.replace('€', '')
            salary = salary.replace('K', '')
            salary = int(salary, 10) * 1000
            ret[key] = salary

    return ret


if __name__ == "__main__":
    salaries = {}

    print("Getting salary data...")
    for title, short, url in [ ("Software Engineering Managers", "SDM", SDM_URL),
                        ("Software Developers", "SDE", SDE_URL)]:
        print(f"  ... {short} ...")
        df = extract_salaries(url)
        salaries[short] = create_salary_dict(df)

    print("Got salary data.")
