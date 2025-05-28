from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import logininfo

browser = webdriver.Chrome()
browser.get("https://x.com/")

login = browser.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[1]/div[1]/div/div[3]/div[4]/a').click()
sleep(3)

username = browser.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[4]/label/div/div[2]/div/input')
username.send_keys(logininfo.username)
sleep(3)
go = browser.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/button[2]').click()
sleep(1)
uname = browser.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input').send_keys("mfyagmur")
sleep(3)
go1 = browser.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/button').click()
sleep(3)

password = browser.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input').send_keys(logininfo.password)
sleep(3)
go = browser.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/button').click()
sleep(3)

search = WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div/div[1]/div/div/div/form/div[1]/div/div/div/div/div[2]/div/input')))
search.clear()
search.send_keys("Kandilli Rasathanesi", Keys.ENTER)
sleep(5)

count = 1
elements = browser.find_elements(By.CSS_SELECTOR, '.css-1jxf684.r-bcqeeo.r-1ttztb7.r-qvutc0.r-poiln3')
with open("text.txt", "w", encoding="UTF-8") as file:
    for element in elements:
        file.write(str(count) + ".\n" + element.text + "\n")
        file.write("*********************************************************\n")
        count += 1


sleep(5)
browser.back()
sleep(10)
browser.close()