
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import xlsxwriter
from datetime import datetime


def scrape_data(asins):

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-extensions')

    driver = webdriver.Chrome('/usr/bin/chromedriver', chrome_options=chrome_options, service_args=["--verbose", "--log-path=/tmp/chromedriver.log"])

    vendor_list = []
    price_list = []
    product_code = []
    imports = []

    print(asins)

    for asin in asins:
        stripped_asin = asin.strip()

        driver.get('https://www.amazon.ae/dp/' + stripped_asin + '/ref=olp_aod_redir?_encoding=UTF8&aod=1')
        try:
            see_more = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, 'aod-pinned-offer-show-more-link'))
            )
            see_more.click()
            print(stripped_asin)

        except:
            pass

        try:

            prices = WebDriverWait(driver, 5).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "a-price"))
            )

            for price in prices:
                print(price.text)
                price_list.append(price.text.replace('\n', '.'))
                product_code.append(stripped_asin)

            vendors = WebDriverWait(driver, 5).until(
                EC.presence_of_all_elements_located((By.ID, "aod-offer-shipsFrom"))
            )

            for vendor in vendors:
                vendor_name = vendor.find_element(By.CLASS_NAME, 'a-col-right')
                print(vendor_name.text)
                vendor_list.append(vendor_name.text)

            sold_by = WebDriverWait(driver, 5).until(
                EC.presence_of_all_elements_located((By.ID, "aod-offer-soldBy"))
            )

            for sold in sold_by:
                try:
                    import_badge = sold.find_element(By.ID, 'aod-import-badge')
                    print("Yes")
                    imports.append(import_badge.text)
                except:
                    imports.append("Does not import internationally")

        except:
            pass
    # dateTimeObj = datetime.now()
    # timestampStr = dateTimeObj.strftime("%d-%b-%Y-%H-%M-%S-%f")

    out_workbook = xlsxwriter.Workbook("amazon-prices.xlsx")
    out_sheet = out_workbook.add_worksheet()

    out_sheet.write("A1", "asin")
    out_sheet.write("B1", "Vendor")
    out_sheet.write("C1", "Price")
    out_sheet.write("D1", "Imports")

    for item in range(len(vendor_list)):
        out_sheet.write(item + 1, 0, product_code[item])
        out_sheet.write(item + 1, 1, vendor_list[item])
        out_sheet.write(item + 1, 2, price_list[item])
        out_sheet.write(item + 1, 3, imports[item])

    out_workbook.close()
    driver.quit()

    if not vendor_list:
        return "There are no vendors for this asin or product is currently not available."
    return product_code, vendor_list, price_list, imports
