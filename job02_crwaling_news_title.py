#지시사항

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import pandas as pd
import re
import datetime
import time

category = ['Politics','Economic','social','Culture','World','It']


options=ChromeOptions()
user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
options.add_argument('user_agent='+user_agent)
options.add_argument('lang=ko_KR')
#options.add_argument('--start-fullscreen')     #full_screen
#options.add_argument('--blink-settings=imagesEnabled=false')       #이미지를 없이 보여준다
#options.add_argument('incognito')              #시크릿모드
#options.add_argument('headless')               #브라우저가띄지않고 실행
#options.add_argument('--window-size= x, y')     #크기지정
#options.add_argument('--start-maximized')       #꽉찬화면으로 실행

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
page = [105,105,105,81,105,81]

df_titles = pd.DataFrame()
for l in range(2):      #카테고리에 따른 페이지
    section_url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=10{}'.format(l)
    titles=[]
    for k in range(1,page[l]):        #카테고리안의 페이지를 정하는 것
        url = section_url + '#&date=%2000:00:00&page={}'.format(k)
        try:
            driver.get(url)
            time.sleep(0.5)
        except:
            print('driver.get',l,k)

        for i in range(1,5):        #//*[@id="section_body"]/ul[{}]/li[{}]/dl/dt[2]/a {}안의 숫자에 따라 기사표현
            for j in range(1,6):
                try:
                    title =driver.find_element('xpath', '//*[@id="section_body"]/ul[{}]/li[{}]/dl/dt[2]/a'.format(i, j)).text
                    title = re.compile('[^가-힣]').sub(' ',title)     #한글만
                    titles.append(title)
                except:
                    print('find element',l,k,i,j)
            if k % 5 ==0:
            #print(titles)
            #print(len(titles))
                df_section_title = pd.DataFrame(titles,columns=['titles'])
                df_section_title['category'] = category[l]
                df_section_title.to_csv('./crawling_data/data_{}_{}.csv'.format(l,k))
                #df_titles = pd.concat([df_titles,df_section_title] , axis='rows' , ignore_index=True)

driver.close()

    #df_titles.to_csv()
