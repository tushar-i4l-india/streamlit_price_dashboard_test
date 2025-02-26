import pandas as pd # type: ignore
import streamlit # type: ignore
from bs4 import BeautifulSoup # type: ignore
import requests # type: ignore
import time
import re
from selenium.webdriver.support.ui import Select # type: ignore
from selenium.webdriver.common.by import By # type: ignore
from selenium import webdriver # type: ignore
from datetime import datetime
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager # type: ignore

def scrape_online_insulation_sales(url):
    try:
        print(f"Processing URL {url}")
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        price_element = soup.find("small", class_ = re.compile("ex-vat"))  
        if price_element:
            return price_element.text.split()[0].strip()
        return 'Price Not Found'
    except Exception as e:
        return f'Error: {str(e)}'

# Function to scrape ex-VAT price from Building Materials
def scrape_building_materials(url, series):
    try:
        print(f"Processing URL {url}")
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)  
        thickness_div = driver.find_element(By.CLASS_NAME, "product-options-wrapper")
        if thickness_div:
            dropdown = Select(driver.find_element(By.CLASS_NAME, "super-attribute-select"))
            time.sleep(5)
            options = [option.text for option in dropdown.options]
            for option in options:
                dropdown.select_by_visible_text(option)
                updated_html = driver.page_source
                s1 = BeautifulSoup(updated_html, "html.parser") 
                title = s1.find("h1", class_ = re.compile("page-title")).text.strip() 
                if series in title:
                    price_element = s1.find("span", class_ = "price-wrapper price-excluding-tax")
                    break
        if price_element:
            return price_element.text.strip()
        return 'Price Not Found'
    except Exception as e:
        return f'Error: {str(e)}'
    finally:
        driver.quit()

# Function to scrape ex-VAT price from Insulation Superstore
def scrape_insulation_superstore(url):
    try:
        print(f"Processing URL {url}")
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        price_element = soup.find("strong", class_ = re.compile("ex-vat"))  
        if price_element:
            return price_element.text.strip()
        return 'Price Not Found'
    except Exception as e:
        return f'Error: {str(e)}'

# Function to scrape ex-VAT price from I4L
def scrape_i4l(url):
    try:
        print(f"Processing URL {url}")
        time.sleep(3)
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        price_element = soup.find("span", class_ = re.compile("ex_vat_price"))  
        if price_element:
            return price_element.text.strip()
        return 'Price Not Found'
    except Exception as e:
        return f'Error: {str(e)}'

def scrape_insulationhub(url):
    print(f"Processing URL {url}")
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    driver.quit() 
    try:
        price_div = soup.find("div", class_ = "price-wrapper")
        price_elements = price_div.find_all("span", class_ = "woocommerce-Price-amount amount")
        if len(price_elements) > 2:
            price_element = price_elements[2]
            old_price = float(price_elements[0].text.strip().replace("£", ""))
            return f"{price_element.text.strip()}-Sale Price"+f" old Price: £{round(old_price/1.2, 2)}"
        else:
            price_element = price_elements[1]
            return price_element.text.strip()
        return 'Price Not Found'
    except Exception as e:
        return f'Error: {str(e)}'

def scrape_planetinsulation(url):
    try:
        print(f"Processing URL {url}")
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        price_element = soup.find("span", class_ = "price-item price-item--sale price-item--last")  
        if price_element:
            return price_element.text.strip()
        return 'Price Not Found'
    except Exception as e:
        return f'Error: {str(e)}'

def scrape_insulationonline(url):
    try:
        print(f"Processing URL {url}")
        response = requests.get(url)
        response.raise_for_status()
        time.sleep(3)
        soup = BeautifulSoup(response.text, 'html.parser')
        price_element = soup.find("span", class_ = "woocommerce-Price-amount amount")  
        if price_element:
            return price_element.text.strip()
        return 'Price Not Found'
    except Exception as e:
        return f'Error: {str(e)}'

def scrape_insulationshop(url):
    try:
        print(f"Processing URL {url}")
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        price_element = soup.find("div", class_ = "product-price").text.split()[1].strip()
        if price_element == "Price:":
            price_elements = soup.find("div", class_ = "product-price").text.split()[2].strip()
            return price_elements
        else: 
            return price_element
        return 'Price Not Found'
    except Exception as e:
        return f'Error: {str(e)}'

def scrape_directinsulation(url):
    try:
        print(f"Processing URL {url}")
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        price_element = soup.find("span", attrs={"data-hook": "formatted-primary-price"}) 
        if price_element:
            return price_element.text.strip()
        return 'Price Not Found'
    except Exception as e:
        return f'Error: {str(e)}'

def scrape_insulationbee(url):
    print(f"Processing URL {url}")
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    driver.quit() 
    try:
        price_element = soup.find("span", id = "price-old")
        if price_element:
            return price_element.text.split()[0].strip()
        return 'Price Not Found'
    except Exception as e:
        return f'Error: {str(e)}'
    except Exception as e:
        return f'Error: {str(e)}'

def scrape_tradeinsulation(url):
    try:
        print(f"Processing URL {url}")
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        price_element = soup.find_all("span", class_ = "woocommerce-Price-amount amount")[3] 
        if price_element:
            return price_element.text.strip()
        return 'Price Not Found'
    except Exception as e:
        return f'Error: {str(e)}'

def scrape_materialmarket(url):
    try:
        print(f"Processing URL {url}")
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        price_elements = soup.find("span", class_ = "c-product-information__price col l12 s6") 
        price_element = price_elements.find("span")["data-product-price-single-unit"]
        if price_element:
            return price_element
        return 'Price Not Found'
    except Exception as e:
        return f'Error: {str(e)}'

def scrape_insulationuk(url):
    try:
        print(f"Processing URL {url}")
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        price_element = soup.find("span", class_ = "iprice-ex") 
        if price_element:
            return price_element.text.split()[0].strip()
        return 'Price Not Found'
    except Exception as e:
        return f'Error: {str(e)}'

def scrape_diybuildingsupplies(url):
    try:
        print(f"Processing URL {url}")
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        price_element = soup.find("strong", class_ = "price__current") 
        if price_element:
            return price_element.text.split()[0].strip()
        return 'Price Not Found'
    except Exception as e:
        return f'Error: {str(e)}'

def scrape_insulationwholesale(url):
    print(f"Processing URL {url}")
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    driver.quit() 
    try:
        price_element = soup.find_all("span", class_ = "woocommerce-Price-amount amount")[2]
        if price_element:
            return price_element.text.strip()
        return 'Price Not Found'
    except Exception as e:
        return f'Error: {str(e)}'
        
df = pd.read_excel("Celotex & Recticel Links.xlsx", sheet_name="Celotex")

result_data = []
for index, row in df.iterrows():
    sku = row["SKU"]
    product = row["Products"]
    series = row["Series"]
    scraped_prices = {
        "I4L": scrape_i4l(row["I4L"]) if pd.notna(row["I4L"]) else 'No Link',
        "Insulation Superstore": scrape_insulation_superstore(row["Insulation Superstore"]) if pd.notna(row["Insulation Superstore"]) else 'No Link',
        "InsulationUK": scrape_insulationuk(row["InsulationUK"]) if pd.notna(row["InsulationUK"]) else 'No Link',
        "Online Insulation Sales": scrape_online_insulation_sales(row["Online Insulation Sales"]) if pd.notna(row["Online Insulation Sales"]) else 'No Link',
        "Insulation Hub": scrape_insulationhub(row["Insulation Hub"]) if pd.notna(row["Insulation Hub"]) else 'No Link',
        "Building Materials": scrape_building_materials(row["Building Materials"], series) if pd.notna(row["Building Materials"]) else 'No Link',
        "Insulation Online": scrape_insulationonline(row["Insulation Online"]) if pd.notna(row["Insulation Online"]) else 'No Link',
        "Planet Insulation": scrape_planetinsulation(row["Planet Insulation"]) if pd.notna(row["Planet Insulation"]) else 'No Link',
        "Insulation Shop": scrape_insulationshop(row["Insulation Shop"]) if pd.notna(row["Insulation Shop"]) else 'No Link',
        "Building Materials Direct": scrape_directinsulation(row["Building Materials Direct"]) if pd.notna(row["Building Materials Direct"]) else 'No Link',
        "Insulation Bee": scrape_insulationbee(row["Insulation Bee"]) if pd.notna(row["Insulation Bee"]) else 'No Link',
        "Trade Insulations": scrape_tradeinsulation(row["Trade Insulations"]) if pd.notna(row["Trade Insulations"]) else 'No Link',
        "Materials Market": scrape_materialmarket(row["Materials Market"]) if pd.notna(row["Materials Market"]) else 'No Link',
        "Insulation Wholesale": scrape_insulationwholesale(row["Insulation Wholesale"]) if pd.notna(row["Insulation Wholesale"]) else 'No Link',
        "DIY Building supplies": scrape_diybuildingsupplies(row["DIY Building supplies"]) if pd.notna(row["DIY Building supplies"]) else 'No Link'
    }
    
    result_data.append({"SKU": sku, "Product": product, **scraped_prices})
        
result_df = pd.DataFrame(result_data)
current_date = datetime.now().strftime("%d-%m-%Y")  # Format: DD-MM-YYYY
output_file_name = f"Compititor's_Price\\Celotex_Prices\\Celotex_Prices_{current_date}.xlsx"
result_df.to_excel(output_file_name)
result_df
