from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random

browser = webdriver.Chrome()
url = "https://eksisozluk.com/1959-oncesi-sampiyonluklar--5824104?p="
pageCount=1
entry = []
entryCount = 1

while pageCount <= 10:
    randomPage = random.randint(1,150)
    newUrl = url + str(randomPage)
    browser.get(newUrl)
    elements = browser.find_elements(By.CSS_SELECTOR, ".content")
    for elemnt in elements:
        entry.append(elemnt.text)
    time.sleep(5)
    pageCount += 1
    

with open("entries.txt", "w", encoding="UTF-8") as file:
    for ent in entry:
        file.write(str(entryCount) + ".\n" + ent + "\n")
        file.write("************************************\n")
        entryCount += 1
            
browser.close()
