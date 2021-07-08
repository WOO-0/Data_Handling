# from selenium import webdriver
# import time

# options = webdriver.ChromeOptions()
# options.add_experimental_option("excludeSwitches", ["enable-logging"])

# chromedriver = 'C:/Users/woomj/OneDrive/바탕 화면/chromedriver.exe'
# driver = webdriver.Chrome(chromedriver, options=options)

# driver.get('https://search.naver.com/search.naver?sm=tab_hty.top&where=image&query=마스크')
import urllib.request
from  bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
binary = 'C:/Users/woomj/OneDrive/바탕 화면/chromedriver.exe'
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
browser = webdriver.Chrome(binary, options=options)

browser.implicitly_wait(10)
browser.get("https://search.naver.com/search.naver?where=image&amp;sm=stb_nmr&amp;")

elem = browser.find_element_by_id('nx_query')
elem.send_keys("마스크")
elem.submit()
for i in range(1, 5):
    browser.find_element_by_xpath("//body").send_keys(Keys.END)
    time.sleep(10)
time.sleep(10)
html = browser.page_source
soup = BeautifulSoup(html, "lxml")
def fetch_list_url():
    params = []
    imgList = soup.find_all("img", class_="_image")
    for im in imgList:
        try :
            params.append(im["src"])
        except KeyError:
            params.append(im["data-src"])
    return params
def fetch_detail_url():
    params = fetch_list_url()
    for idx,p in enumerate(params,1):
        urllib.request.urlretrieve(p, "images7/" + str(idx) + ".jpg")
fetch_detail_url()
browser.quit()