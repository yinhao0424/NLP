import numpy as np
from bs4 import BeautifulSoup
import re
import os
import glob
# 对每一个文件，提取名字中的时间

class generateDataFile():

    def __init__(self, inputPath, outputpath):
        self.inputPath = inputPath

        self.content = None
        self.tickers = []
        self.outputPath = outputpath

    def getTickers(self):
        for ticker in glob.glob(self.inputPath):
            self.tickers.append(ticker.split('/')[1])


    def readHtml(self,filename):
        # read html and get file content, ticker, as well as date
        with open(filename, 'r') as f:
            soup = BeautifulSoup(f.read(), 'lxml')
            try:
                self.content = soup.find('div', class_='sa-art article-width ').text
            except:
                self.content = ''


    def checkDate(self,filename):
        headline = filename.split('/')[2]
        if not re.search('q\d\-\d{4}', headline):
            return False
        else:
            date = re.search('q\d\-\d{4}', headline).group()
            return date



    def outputFile(self,ticker,date):
        path = self.outputPath+ ticker
        if not os.path.exists(path):
            os.makedirs(path)

        name = ticker + '-' + date+'.txt'
        file = open(os.path.join(path, name), "w")

        file.write(self.content)
        file.close()
        # return

    def generateData(self):
        self.getTickers()
        for i, ticker in enumerate(self.tickers):
            for filename in glob.glob(self.inputPath + ticker + '/*.html'):

                if self.checkDate(filename):
                    date = self.checkDate(filename)
                    # print(date)
                    self.readHtml(filename)
                    self.outputFile(ticker,date)
                # break





if __name__ == "__main__":
    inputPath = 'dataOrigins/*'
    outputPath = 'dataTest/'

    gd = generateDataFile(inputPath,outputPath)
    gd.generateData()

    print('Done!')

