import numpy as np
from bs4 import BeautifulSoup
import re
import os
import glob
# 对每一个文件，提取名字中的时间

"""
Order:
1. parse_html_to_txt.py
2. make_directories.py
3. make_json_file.py

"""

class ParseHTML():
    """
    Input: input path and output path, parse html from input path and generated txt files to the output directory
    input path format:
    DataOriginals -> A, AA etc -> A-2019-q1-earning-call.html, A-2019-q2-earning-call.html
    output path format:
    DataTest/ticker/ALl/ **.txt
    """

    def __init__(self, inputPath, outputpath):
        self.inputPath = inputPath

        self.content = None
        self.tickers = []
        self.outputPath = outputpath

    def get_tickers(self):
        for ticker in glob.glob(self.inputPath):
            self.tickers.append(ticker.split('/')[1])


    def read_html(self,filename):
        # read html and get file content, ticker, as well as date
        with open(filename, 'r') as f:
            soup = BeautifulSoup(f.read(), 'lxml')
            try:
                self.content = soup.find('div', class_='sa-art article-width ').text
            except:
                self.content = ''


    def check_date(self,filename):
        headline = filename.split('/')[2]
        if not re.search('q\d\-\d{4}', headline):
            return False
        else:
            date = re.search('q\d\-\d{4}', headline).group()
            return date



    def output_file(self,ticker,date):
        path = self.outputPath+ ticker + '/ALL'
        if not os.path.exists(path):
            os.makedirs(path)

        name = ticker + '-' + date+'-earning-all-transcript.txt'
        file = open(os.path.join(path, name), "w")

        file.write(self.content)
        file.close()
        # return

    def generateData(self):
        self.get_tickers()
        for i, ticker in enumerate(self.tickers):
            for filename in glob.glob(self.inputPath + ticker + '/*.html'):

                if self.check_date(filename):
                    date = self.check_date(filename)
                    # print(date)
                    self.read_html(filename)
                    self.output_file(ticker,date)
                # break


if __name__ == "__main__":

    inputPath = 'DataOriginals/*'
    outputPath = 'DataTest/'

    gd = ParseHTML(inputPath,outputPath)
    gd.generateData()
    print(gd.tickers)
    print('Done!')

