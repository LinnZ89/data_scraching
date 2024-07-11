from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

service = Service(executable_path='C:/chromedriver/chromedriver.exe')
options = Options()
driver = webdriver.Chrome(service=service, options=options)

url = 'https://meteostat.net/en/place/vn/thu-uc?s=48900&t=2024-05-19/2024-05-26' #Đổi URL sang từ ngày 19-5 đến 26-5
driver.get(url)

WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="cookieModal"]/div/div/div[3]/button[2]'))
).click()

WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/main/div/div/div/div[1]/div[1]/div[1]/button[2]'))
).click()
time.sleep(2)

def show_more_button_until_done():
    max_attempts = 100
    attempts = 0
    while attempts < max_attempts:
        try:
            show_more_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="details-modal"]/div/div/div[2]/div[2]/button'))
            )
            show_more_button.click()
            time.sleep(2)

            rows = driver.find_elements(By.XPATH, '//div[@class="v-data-table__wrapper"]//table//tbody//tr')
            if len(rows) >= 1000:
                break

            attempts += 1
        except Exception as e:
            print(f"No more 'Show More' button or an error occurred: {e}")
            break

def main():
    table = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/main/div/div/div/div[1]/div[3]/div[6]/div/div/div[2]/div[1]'))
    )

    rows = table.find_elements(By.XPATH, './/tr')

    table_data = []

    for row in rows:
        cells = row.find_elements(By.XPATH, './/th | .//td')
        cell_data = [cell.text for cell in cells]
        table_data.append(cell_data)

    with open('19-26 May.csv', mode='w', newline='', encoding='utf-8') as file: #Đổi tên file csv
        writer = csv.writer(file)
        writer.writerows(table_data)

    print("Successfully!")

if __name__ == "__main__":
    show_more_button_until_done()
    main()
    driver.quit()