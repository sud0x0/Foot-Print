import json
import os

class random_funtions:
    
    def __init__(self):
        a = os.getcwd()
        with open(a +'/config.json') as json_file:
            self.data = json.load(json_file)

    def SHODAN_API_KEY(self):
        SHODAN_API_KEY = self.data['API']['Shodan']
        if (SHODAN_API_KEY == ''):
            return False
        else:
            return SHODAN_API_KEY

    def HACKER_TARGET_API_KEY(self):
        HACKERTARGET_API_KEY = self.data['API']['Hacker_Target']
        if (HACKERTARGET_API_KEY == ''):
            return False
        else:
            return HACKERTARGET_API_KEY

    def remove_dup(self, rlist):
        no_duplicate_list = []
        for i in rlist:
            item_exist = False
            if no_duplicate_list:
                for x in no_duplicate_list:
                    if i[0] == x[0]:
                        item_exist = True
                if item_exist == False:
                    no_duplicate_list.append(i)
            else:
                no_duplicate_list.append(i)
        return no_duplicate_list   



