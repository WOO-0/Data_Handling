# 스레딩을 사용한 구글 큰 사이즈 이미지 크롤링

# # 모듈 가져오기 
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
import time 
import urllib.request
import traceback
import threading

# 크롬 열고 검색하기 
binary = 'C:/Users/woomj/OneDrive/바탕 화면/chromedriver.exe'
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(binary, options=options) 
driver.get("https://www.google.co.kr/imghp?hl=ko&tab=wi&ogbl")
elem = driver.find_element_by_name("q") 
elem.send_keys("마스크")
elem.send_keys(Keys.RETURN)

SCROLL_PAUSE_TIME = 1

last_height = driver.execute_script("return document.body.scrollHeight")

while True: 
    # 스크롤 끝까지 내리기 
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # 페이지 로딩 기다리기 
    time.sleep(SCROLL_PAUSE_TIME) 
    # 더 보기 요소 있을 경우 클릭하기 
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height: 
        try: 
            driver.find_element_by_css_selector(".mye4qd").click() 
        except: 
            break 
    last_height = new_height

def downloadImage(imagePath, fileName):
    print("Downloading Image from ", imagePath)
    urllib.request.urlretrieve(imagePath, fileName)
    print("Completed Download")

def executeThread(i, url): 
  imageName = "images1/" + str(i) + ".jpg"
  downloadImage(url, imageName)

threads = []


images = driver.find_elements_by_css_selector(".rg_i.Q4LuWd")
count = 75
for image in images: 
    try: 
        image.click() 
        time.sleep(2) 
        element = driver.find_elements_by_class_name('v4dQwb')
        if count == 0:
            imgUrl = element[0].find_element_by_class_name('n3VNCb').get_attribute("src")
        else:
           imgUrl = element[1].find_element_by_class_name('n3VNCb').get_attribute("src")
        print(imgUrl)
        for i in range(10):
            thread = threading.Thread(target=executeThread, args=(count,imgUrl))
            threads.append(thread)
            thread.start()
        count = count + 1 
    except:
        # traceback.print_exc()
        pass

for i in threads:
    i.join()
          
#프로그램 종료 
driver.close()

