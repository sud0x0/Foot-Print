import shodan
import time
from modules.functions import random_funtions


class shodan_data:

    def __init__(self):
        func = random_funtions()
        API = func.SHODAN_API_KEY()
        if API:
            self.api = shodan.Shodan(API)
        else:
            print ('Check the Shodan API Key.')


    def shodan_IP(self,ip_list):
        sheet1 = []
        sheet2 = []
        sheet3 = []
        sheet4 = []
        extra = []
        ip_list_new = []
        for k in ip_list:
            IP = k[1]
            domain_org = k[0]
            print ('Checking IP: '+str(IP))
            if not IP in ip_list_new:
                ip_list_new.append(str(IP))
                try:
                    time.sleep(0.5)
                    results = self.api.host(IP)

                except Exception as e:
                    if 'Invalid API key' in str(e):
                        print('Cannot Connect to Shodan, Check your API key and Internet')
                        return False
                    else:
                        s1 = [IP,'-', domain_org, '-', '-', '-', '-', '-', '-', '-', '-']
                        extra.append(s1)
                        continue
                if isinstance(results.get('hostnames'), list):    
                    hostname = ', '.join(results.get('hostnames'))
                else:
                    hostname = results.get('hostnames')
                asn = results.get('asn')
                org = results.get('org')
                isp = results.get('isp')
                country = results.get('country_name')
                city = results.get('city')
                ports = ','.join([str(i) for i in results.get('ports')]) 
                if isinstance(results.get('vulns'), list):
                    vul = ', '.join(results.get('vulns'))
                else:
                    vul = results.get('vulns')
                update = results.get('last_update')
                s1 = [IP, hostname, domain_org, org, isp, country, city, asn, ports, vul, update]
                sheet1.append(s1)    
                for i in results['data']:
                    port = str(i['port'])
                    protocol =  str(i['transport'])
                    service = str(i['_shodan']['module'])
                    application = str(i.get('product'))
                    cpe = str(i.get('cpe'))
                    domains = ', '.join(i.get('domains'))
                    os = str(i.get('os'))
                    ssl_info = str(i.get('info'))
                    s2 = [IP, port, protocol, service, application, cpe, os, domains, domain_org, ssl_info]
                    sheet2.append(s2)
                    if (i.get('ssl')):
                        ssl_expired = str(i['ssl']['cert']['expired'])
                        ssl_exp = str(i['ssl']['cert']['expires'])
                        ssl_ver = str(i['ssl']['cipher']['version'])
                        ssl_name = str(i['ssl']['cipher']['name'])
                        ssl_bits = str(i['ssl']['cipher']['bits'])
                        s3 = [IP, port, ssl_exp, ssl_expired, ssl_name, ssl_ver, ssl_bits]
                        sheet3.append(s3)
                    if (i.get('vulns')):
                        names = [*i.get('vulns')]
                        for l in names:
                            cvss = str(i['vulns'][l]['cvss'])
                            varified = str(i['vulns'][l]['verified'])
                            summary = str(i['vulns'][l]['summary'])
                            s4 = [IP, port, l, cvss, varified, summary]
                            sheet4.append(s4)
        if not (len(extra) == 0):              
            sheet1 = sheet1 + extra                
        book = [sheet1, sheet2, sheet3, sheet4]
        return book
   

    def Shodan_Search(self,code):
        sheet1 = []
        try:
            results = self.api.search(code)
        except:
            print('Cannot Connect to Shodan, Check your API key and Internet')
            return False
        if not len(results['matches']) == 0:
            for i in results['matches']:
                dataset = []
                ip =i.get('ip_str')
                if results.get('domains') == '':
                    domain = ', '.join(results.get('domains'))
                else:
                    domain =  results.get('domains')
                asn = i.get('asn')
                port = i.get('port')
                product = i.get('product')
                dataset = [ip,domain,asn,port,product]
                sheet1.append(dataset)
            return sheet1  
        else:
            print ('No Result')
            return False  


