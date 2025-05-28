from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logininfo
import time

browser = webdriver.Chrome()
browser.get("https://x.com/")
time.sleep(3)

giris_yap = browser.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[1]/div/div/div[3]/div[4]/a')
giris_yap.click()
time.sleep(3)


username = browser.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[4]/label/div/div[2]/div/input')
username.send_keys(logininfo.username)
time.sleep(3)

ileri = browser.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/button[2]')
ileri.click()
time.sleep(1)

uname = browser.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input')
uname.send_keys("mfyagmur")
time.sleep(1)

ileri2 = browser.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/button')
ileri2.click()
time.sleep(1)

password = browser.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input')
password.send_keys(logininfo.password)
time.sleep(1)

run = browser.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/button')
run.click()
time.sleep(5)


# arama kısmından hashtag gonderme
serach = WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div/div[1]/div/div/div/form/div[1]/div/div/div/div/div[2]/div/input")))
serach.clear()
serach.send_keys("5YıldızlıŞampiyon", Keys.ENTER)
time.sleep(5)

#Sayfa Sonuna gitme scripti
lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
match=False
while(match==False):
    lastCount = lenOfPage
    time.sleep(3)
    lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    if lastCount == lenOfPage:
        match=True
time.sleep(5)

elements = browser.find_elements(By.CSS_SELECTOR, "css-175oi2r.r-1777fci.r-bt1l66.r-bztko3.r-lrvibr.r-1loqt21.r-1ny4l3l")
for element in elements:
    try:
        element.click()
        time.sleep(2)
    except Exception:
        print ("Bir Soru8n oluştu.")


browser.close()