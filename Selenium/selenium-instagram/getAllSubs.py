from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import loginInfo

browser = webdriver.Chrome()
browser.get("https://www.instagram.com/")
time.sleep(3)

username = browser.find_element(By.NAME, 'username').send_keys(loginInfo.username)
password = browser.find_element(By.NAME, "password").send_keys(loginInfo.password)
time.sleep(3)
loginButton = browser.find_element(By.XPATH, '//*[@id="loginForm"]/div[1]/div[3]/button').click()
time.sleep(3)

notNow = browser.find_element(By., ' _acan._acap._acas._aj1-._ap30').click()
time.sleep(3)



time.sleep(10)
browser.close()