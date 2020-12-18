import os
import re
import json
import time

"""
Order:
1. parse_html_to_txt.py
2. make_directories.py
3. make_json_file.py
4. split_by_parties
"""
class make_json():

    def __init__(self, input,output):
        """

        :param input: 'DataTest'
        :param output: 'company_profile_test.json'
        """
        self.input = input
        self.output = output
        self.companies = []

        self.data = {}

    def get_companies(self):
        """
        Get a list of company names
        :return:
        """
        for f in os.listdir(self.input):
            if f != '.DS_Store':
                company_path = self.input + '/' + f + '/ALL'
                self.companies.append(company_path)

    def comany_parties(self,info,lines, call_start_index, call_end_index):
        # Create single companies info
        quarter = {}
        quarter['name'] = info[0]
        quarter['year'] = info[2]
        quarter['quarter'] = info[1]
        quarter['participants'] = {}

        # loop through each line in the call participants section
        mark = None
        for i in range(call_start_index, call_end_index):
            if lines[i] != '\n':
                line = re.sub(r'\n', "", lines[i])
                if line == 'Analysts' or line == 'Conference Call Participants':
                    mark = 'Analysts'
                    continue
                elif line == 'Executives' or line == 'Company Participants':
                    continue
                if line in quarter['participants']:  # Find lines start with the name of CEO or CFO
                    break

                if len(line.split('-')) > 1:
                    name = line.split('-')[0].strip()
                    title = line.split('-')[1].strip()
                    quarter['participants'][name] = title if not mark else mark
                elif len(line.split('–')) > 1:
                    name = line.split('–')[0].strip()
                    title = line.split('–')[1].strip()
                    quarter['participants'][name] = title if not mark else mark
                else:
                    name = line.split('-')[0].strip()
                    quarter['participants'][name] = 'Analysts'
        return quarter

    def create_company_info(self,file, filepath):

        with open(filepath, 'r') as f:
            lines = f.readlines()
            # find the line index where call participants start and end
            call_start_index = 1
            call_end_index = 20

            if 'Operator\n' in lines:
                call_end_index = lines.index('Operator\n')  # Find the first Operator

            call_end_index = min(20, call_end_index, len(lines))
            # set up each quarter's entry in json
            info = file.split('-')
            quarter = self.comany_parties(info,lines, call_start_index, call_end_index)
            self.data['company_profile'].append(quarter)
            with open(self.output, 'w') as outfile:
                json.dump(self.data, outfile, indent=4)


    def create_metadata(self):
        # put all companies in a list
        self.get_companies()

        self.data['company_profile'] = []

        for company in self.companies:
            for file in os.listdir(company):
                # print(file)
                if file != '.DS_Store':
                    filepath = company + '/' + file
                    # filepath: DataTest/BF.B/ALL/BF.B-q3-2019-earning-all-transcript.txt
                    if os.path.getsize(filepath) == 0:
                        continue

                    self.create_company_info(file,filepath)


if __name__ == '__main__':
    start_time = time.time()
    input = 'DataTest'
    output = 'company_profile_test.json'

    mkjson = make_json(input, output)
    mkjson.create_metadata()

    print("--- %s seconds ---" % (time.time() - start_time))

