import re
import os
import json
import time

"""
Order:
1. parse_html_to_txt.py
2. make_directories.py
3. make_json_file.py
4. split_by_parties.py
5. remove_files and create empty files

"""

# Final Version for generating data
class SplitParties():
    def __init__(self, input_path, json_file):

        self.path = input_path
        self.metadata = json_file

        self.data = None

    def load_json(self):
        with open(self.metadata, 'r') as json_file:
            self.data = json.load(json_file)

    def get_info(self,quarter):
        file_name = quarter['name'] + '-' + quarter['quarter'] + '-' + quarter['year'] + '-earning-all-transcript.txt'
        file_path = self.path + '/' + quarter['name'] + '/ALL/' + file_name
        seperators = list(quarter['participants'].keys()) + ['Operator']
        return file_name,file_path,seperators

    def get_res(self,lines,seperators):
    #     {'CEO': [line1, line2, line7, 8], 'B': [line5, 6, 9]}

        category = None
        res = {}
        for line in lines:
            line = re.sub(r'\n', "", line)
            line = line.strip()
            if line != "":
                #         print(line)
                #         print(category)
                if line not in res and line in seperators:
                    category = line
                    res[category] = []
                #                     print(category)
                elif line in seperators:
                    category = line
                    continue
                else:
                    if not category:
                        continue
                    res[category].append(line)
                    continue
        return res

    def output_file(self,quarter, res):
        for key in res:
            # key: ['Operator', 'Kim Collins', 'Keith Dunleavy', 'Jonathan Boldt', 'Sandy Draper']
            if key in quarter['participants']:
                title = quarter['participants'][key]
                #         title: ['Senior Vice President', 'Chief Executive Officer and Chairman', 'Chief Financial Officer', 'Analysts']

                if 'chief executive' in title.lower() or 'executive officer' in title.lower() or 'ceo' in title.lower() or 'c.e.o' in title.lower():
                    file_name_new = quarter['name'] + '-' + quarter['quarter'] + '-' + quarter[
                        'year'] + '-earning-ceo-transcript.txt'
                    file_path_new = self.path + '/' + quarter['name'] + '/CEO/' + file_name_new
                    if not os.path.exists(file_path_new):
                        with open(file_path_new, 'a') as f_ceo:
                            for line in res[key]:
                                f_ceo.write(line + '\n\n')

                elif 'chief financial' in title.lower() or 'financial officer' in title.lower() or 'finance' in title.lower() or 'cfo' in title.lower() or 'c.f.o' in title.lower():
                    file_name_new = quarter['name'] + '-' + quarter['quarter'] + '-' + quarter[
                        'year'] + '-earning-cfo-transcript.txt'
                    file_path_new = self.path + '/' + quarter['name'] + '/CFO/' + file_name_new
                    if not os.path.exists(file_path_new):
                        with open(file_path_new, 'a') as f_cfo:
                            for line in res[key]:
                                f_cfo.write(line + '\n\n')


                elif 'analysts' in title.lower():
                    file_name_new = quarter['name'] + '-' + quarter['quarter'] + '-' + quarter[
                        'year'] + '-earning-analyst-transcript.txt'
                    file_path_new = self.path + '/' + quarter['name'] + '/Analyst/' + file_name_new
                    if not os.path.exists(file_path_new):
                        with open(file_path_new, 'a') as f_an:
                            for line in res[key]:
                                f_an.write(line + '\n\n')

    def separate_text(self):
        self.load_json()

        for quarter in self.data['company_profile']:
            file_name, file_path, seperators = self.get_info(quarter)

            with open(file_path, 'r') as file:
                lines = file.readlines()
                res = self.get_res(lines, seperators)
                self.output_file(quarter, res)

        print('done')

if __name__ == '__main__':
    start_time = time.time()
    path = 'DataTest'

    metadata = 'company_profile_test.json'

    sp = SplitParties(path,metadata)
    sp.separate_text()

    print("--- %s seconds ---" % (time.time() - start_time))