import requests
from bs4 import BeautifulSoup
import os
import sys

SAVE_FOLDER = 'images6'

def main():
    if not os.path.exists(SAVE_FOLDER):
        os.mkdir(SAVE_FOLDER)
        
    data = input('What are you looking for? ')

    for start in range(0,20,20):
        download_images(data, start)
    
def download_images(data, start):
    # ask for user input

    print('Start searching...')
    
    GOOGLE_IMAGE  ="https://www.google.com/search?q={}&source=lnms&tbm=isch&start={}"
    # get url query string
    searchurl = GOOGLE_IMAGE.format(data,start)
    print(searchurl)

    # request url, without usr_agent the permission gets denied
    response = requests.get(searchurl)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.findAll('div', {'class': 'svla5d'})
    if(len(results)==0):
        print("No Data")
        sys.exit(1)

    # extract the link from the div tag
    imagelinks= []
    for re in results:
        img = re.find('img')
        href = img.attrs['src']
        imagelinks.append(href)

    print(f'found {len(imagelinks)} images')
    print('Start downloading...')

    for i, imagelink in enumerate(imagelinks):
        # open image link and save as file
        params =  {
            "cse_image": [
                {
                    "src": "https://www.google.com/search?q={}".format(data)
                }
            ],
                "cse_thumbnail": [
                {
                    "width": "400",
                    "height": "400",
                    "src": href
                }
            ]
        }
        print(imagelink)
        response = requests.get(imagelink, params = params)
        imagename = SAVE_FOLDER + '/' + data + str(start+i) + '.jpg'
        with open(imagename, 'wb') as file:
            file.write(response.content)

    print('Done')


if __name__ == '__main__':
    main()