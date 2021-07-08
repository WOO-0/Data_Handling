# JSON을 이용한 네이버 블로그 동적 크롤링
# 멀티프로세스를 사용하여 크롤링 속도를 높임

import json
import os
import requests
from bs4 import BeautifulSoup
import re
from pandas import DataFrame
from datetime import datetime
import multiprocessing


def get_blog_list_url(keyword, pageNum):
    keyword = keyword.encode('utf-8')
    url = 'https://section.blog.naver.com/ajax/SearchList.naver'

    params = {
        'countPerPage':'7',
        'currentPage' : pageNum,
        'endDate' : '',
        'orderBy':'sim',
        'keyword': keyword,
        'startDate' : '',
        'type' : 'post'
    }

    headers = {
        "Referer": 'https://section.blog.naver.com/Search/Post.naver?pageNo={}&rangeType=ALL&orderBy=sim&keyword={}'.format(pageNum, keyword)
    }
    data = requests.get(url,params = params, headers=headers).text
    data = json.loads(data[5:])
    url_list = []
    for d in data['result']['searchList']:
        url_list.append(d['postUrl'])
    return url_list

def real_link(link):
    req = requests.get(link)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    real_url = soup.find('iframe').get('src')
    real_url = 'https://blog.naver.com' + str(real_url)
    return real_url

def get_content(link):
    req = requests.get(link)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    contents = str(soup.find_all('p',{'class': re.compile('se-text-paragraph .*')}))
    contents = re.sub('<.+?>', '', contents, 0).strip()
    contents = re.sub('\u200b, ', '', contents, 0).strip()
    return contents

def save_data(b_dict, b_query):
    date = str(datetime.now())
    date = date[:date.rfind(':')].replace(' ', '_')
    date = date.replace(':','시') + '분'
    
    blog_df = DataFrame(b_dict)
    folder_path = os.getcwd()
    xlsx_file_name = '네이버 블로그_{}_{}.xlsx'.format(b_query, date)
    
    blog_df.to_excel(xlsx_file_name)
    print('엑셀 저장 완료 | 경로 : {}\\{}'.format(folder_path, xlsx_file_name))
    os.startfile(folder_path)

if __name__ == "__main__":

    query = input('검색 키워드를 입력하세요 : ')
    query = query.replace(' ', '+')

    blog_page_num = int(input('총 필요한 페이지 수를 입력해주세요(숫자만 입력, 한 페이지당 7개의 게시글) : '))

    print()
    print("크롤링 중...")
    idx = 1
    blog_dict = list({})
    pool = multiprocessing.Pool(multiprocessing.cpu_count())

    while idx <= blog_page_num:
        blog_list_url = get_blog_list_url(query, idx)
        for blog_url in blog_list_url:
            r_link = real_link(blog_url)
            content = pool.map(get_content, (r_link,))
            blog_dict.append({
                'url' : blog_url,
                'content' : content
            })
        idx += 1
    
    print('크롤링 완료 총 {}개의 블로그 저장'.format(blog_page_num * 7))
    save_data(blog_dict, query)