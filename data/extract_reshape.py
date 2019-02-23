
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os


#This code is magic - wide to long
# df1 = pd.read_csv('returns_largesample.csv')  
# df = df1.iloc[:, 2:]

# print df.columns.values
# df = df[(df['QE']!=0) &(df['time']<1000)]

# df = df.pivot_table(columns=['asset'], index=['QE', 'seed', 'time'], values='val')



import os

import requests
from lxml import html

print 'hey'

class ImageScraper:
    def __init__(self, url, download_path):
        self.url = url
        self.download_path = download_path

        self.session = requests.Session()

    def scrape_images(self):
        response = self.session.get(self.url).text

        tree = html.fromstring(response)
        for movie in tree.xpath('//div[@class="mv"]'):
            title = movie.findtext('.//h3/a')

            image_url = "https:" + movie.xpath('.//img/@src')[0]
            image_name = image_url.split('/')[-1]

            self.save_image(title, image_name, image_url)

    def save_image(self, movie_name, file_name, item_link):
        response = self.session.get(item_link, stream=True)

        if response.status_code == 200:
            with open(os.path.join(self.download_path, file_name), 'wb') as image_file:
                for chunk in response.iter_content(1024):
                    image_file.write(chunk)

        print(movie_name, file_name)



scraper = ImageScraper(url="https://solarmoviez.ru/movie/the-secret-life-of-pets-14600/watching.html",
                           download_path="/Users/Tina/git_repos")
scraper.scrape_images()

print 'done?'
# l = []
# for i in range(50,2500, 100):
# 	l.append(i)
# print len(l)
# print l 

# #Sampling
# path1='/Users/Tina/Dropbox/International Spillovers/Data/results/'
# path2='/Users/Tina/git_repos/qe-financial-spillover/data/'

# #df=pd.read_csv('returns_ls.csv')
# df=pd.read_csv(path2+'summary_largesample.csv') 
# df1=df.sample(frac=0.1, replace=True, random_state=1)
# df1.to_csv(path2+'resample_state1_01.csv')

# df2 = df.iloc[0::100,:]

# df2.to_csv('resample.csv')
###LATEX
# df = pd.read_excel('/Users/Tina/Dropbox/International Spillovers/Data/results/prices.xlsx')  
# df.replace(np.nan, '', inplace=True)

# df = pd.read_csv('dom_bonds.csv')  

# df = df.pivot_table(columns=['time'])
# print df.head()
# df.to_latex('test.tex')