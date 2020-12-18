import os
import glob
import time

class MakeDir():
    """
    Order:
    1. parse_html_to_txt.py
    2. make_directories.py

    """
    def __init__(self, files_location):
        """
        :param files_location: 'DataTest/'
        output:
        make directories:
            'files_by_company/**/ALL'
            'files_by_company/**/Analyst'
            'files_by_company/**/CEO'
            'files_by_company/**/CFO'

        inside files_location: 'DataTest/**/ALL'

        """

        self.path = files_location


    def get_tickers(self,files_location):
        tickers = []
        for ticker in glob.glob(files_location + '*'):
            tickers.append(ticker.split('/')[1])
        return tickers


    def make_company_dir(self):
        """
        input: original files_location, ex: 'data/'

        Params:
        1. path: 'files_by_company/AACG'
        2. mkdir:
            'files_by_company/AACG/ALL'
            'files_by_company/AACG/Analyst'
            'files_by_company/AACG/CEO'
            'files_by_company/AACG/CFO'

        """
        files_location = self.path
        company_names = self.get_tickers(files_location)

        for company in company_names:
            path = files_location + company
            if not os.path.exists(path):
                os.mkdir(path)
            if not os.path.exists(path + '/ALL'):
                os.mkdir(path + '/ALL')
            if not os.path.exists(path + '/Analyst'):
                os.mkdir(path + '/Analyst')
            if not os.path.exists(path + '/CEO'):
                os.mkdir(path + '/CEO')
            if not os.path.exists(path + '/CFO'):
                os.mkdir(path + '/CFO')

        print('done creating directories')

if __name__ == '__main__':
    start_time = time.time()
    path = 'DataTest/'
    make_dir = MakeDir(path)
    make_dir.make_company_dir()

    print("--- %s seconds ---" % (time.time() - start_time))