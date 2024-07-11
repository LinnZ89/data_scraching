#Thêm thư viện làm việc Selenium + Time + CSV
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

#Setup google driver cho trình duyệt web
service = Service(executable_path='C:/chromedriver/chromedriver.exe') #Thêm đường dẫn tới bản chromedriver binary trong máy
options = Options() #Set biến options là cài đặt của chrome
driver = webdriver.Chrome(service=service, options=options) #Tạo đối tượng driver để tương tác với page

url = 'https://meteostat.net/en/station/48900?t=2022-01-01/2022-12-31' #Đường dẫn tới trang
driver.get(url) #driver lấy đường dẫn để request tương tác với trang html

WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="cookieModal"]/div/div/div[3]/button[2]'))
).click() #Tìm và click vào nút accept cookie 

WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/main/div/div/div/div[1]/div[1]/div[1]/button[2]'))
).click()
time.sleep(2) #Tìm và click vào nút detail -> hiện bảng

def show_more_button_until_done(): #Hàm bấm nút show more tới khi sổ hết bảng
    max_attempts = 100 #Giới hạn lần bấm sổ là 100
    attempts = 0 #Số lần đã thực hiện
    while attempts < max_attempts: #Cho vòng while chạy tới khi lần thử vượt giới hạn
        try:
            show_more_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="details-modal"]/div/div/div[2]/div[2]/button'))
            ) #Tạo biến tương đương với nút show more bằng tìm nút show more thông qua đường dẫn xpath
            show_more_button.click() #click vào nút để sổ bảng
            time.sleep(2) #dừng python 2s để đợi bảng load hoàn toàn

            rows = driver.find_elements(By.XPATH, '//div[@class="v-data-table__wrapper"]//table//tbody//tr') #Đếm số dòng
            if len(rows) >= 1000: #vượt quá 1000 dòng thì dừng
                break

            attempts += 1 #Sau khi bấm show more xong thì tăng lần thực hiện lên 1
        except Exception as e: #Exceptiont tương đương với việc k tìm được nút show more nào nữa và break vòng lập
            print(f"No more 'Show More' button or an error occurred: {e}")
            break

def main():
    table = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/main/div/div/div/div[1]/div[3]/div[5]/div/div/div[2]/div[1]'))
    ) #Dò tìm bảng bằng đường dẫn xpath trong vòng 10s

    rows = table.find_elements(By.XPATH, './/tr') #Thực hiện dò tìm dòng theo xpath từ bảng đã tìm thấy

    table_data = [] #tạo array chứa dữ liệu

    for row in rows: #Chạy từng dòng 
        cells = row.find_elements(By.XPATH, './/th | .//td') #Lấy tất cả những dòng có loại <th và <td thuộc dòng
        cell_data = [cell.text for cell in cells] #Đẩy những dữ liệu dạng chữ của các cell của dòng vào 1 mảng
        table_data.append(cell_data) #Đẩy mảng trên vào array chứa dữ liệu

    with open('2022.csv', mode='w', newline='', encoding='utf-8') as file: #Mở file để ghi
        writer = csv.writer(file) #Ghi theo tuýp csv
        writer.writerows(table_data) #Từ table_data array ghi dữ liệu vào csv

    print("Successfully") #In đã ghi thành công

if __name__ == "__main__":
    show_more_button_until_done()
    main()
    driver.quit()