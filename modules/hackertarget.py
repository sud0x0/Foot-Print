import subprocess
import sys
import socket
from modules.functions import random_funtions

class hackertarget_result_gen:

    def __init__ (self,domain):
        func = random_funtions()
        API = func.HACKER_TARGET_API_KEY()
        if API:
            self.domain = domain + '&apikey=' + API
            self.api = API
        else:
            self.domain = domain
            self.api = False


    def result_asn(self):
        try:
            ip = socket.gethostbyname(self.domain.split('&')[0])
        except socket.gaierror:
            print ('Invalid Domain')
            return False
        if self.api:
            hr_asn_number = ["curl", "https://api.hackertarget.com/aslookup/?q="+ip+'&apikey='+self.api]
        else:
            hr_asn_number = ["curl", "https://api.hackertarget.com/aslookup/?q="+ip]
        try:
            hr_asn_result = subprocess.check_output(hr_asn_number).decode("utf-8").splitlines()
        except:
            print ('Error')
            return False
        if not 'API count exceeded - Increase Quota with Membership' in hr_asn_result:
            result = hr_asn_result[0].replace('"','').split (",")
            return result
        else:
            print ('API limit Exceeded for the day')
            return False


    def result_net_blocks(self,asn):
        asn = str(asn)
        if self.api:
            hr_asn_number = ["curl", "https://api.hackertarget.com/aslookup/?q="+'AS'+asn+'&apikey='+self.api]
        else:
            hr_asn_number = ["curl", "https://api.hackertarget.com/aslookup/?q="+'AS'+asn]
        try:
            hr_asn_result = subprocess.check_output(hr_asn_number).decode("utf-8").splitlines()
        except:
            print ('Error')
            return False
        if not 'API count exceeded - Increase Quota with Membership' in hr_asn_result:
            hr_asn_result.remove(hr_asn_result[0])
            return hr_asn_result
        else:
            print ('API limit Exceeded for the day')
            return False


    def result_host_search(self):
        hr_host_search = ["curl", "https://api.hackertarget.com/hostsearch/?q=" + self.domain]
        try:
            hr_host_search_result = subprocess.check_output(hr_host_search).decode("utf-8").splitlines()
        except:
            print ('Error')
            return False
        hr_host_search_list = []
        if not 'API count exceeded - Increase Quota with Membership' in hr_host_search_result[0]:
            try:
                if not 'error check your search parameter' in hr_host_search_result[0]:
                    for i in hr_host_search_result:
                        fdomain = i.split(',')[0]
                        if fdomain[:4] == 'www.':
                            domain = fdomain[4:]
                        else:
                            domain = fdomain
                        ip = i.split(',')[1]
                        new_list = [domain,ip]
                        hr_host_search_list.append(new_list)
                return hr_host_search_list
            except IndexError:
                print ('Invalid API')
                return False
        else:
            print ('API limit Exceeded for the day')
            return False
    

    def result_reverse_dns(self):
        hr_reverse_dns = ["curl", "https://api.hackertarget.com/reversedns/?q=" + self.domain]
        try:
            hr_reverse_dns_result = subprocess.check_output(hr_reverse_dns).decode("utf-8").splitlines()
        except:
            print ('Error')
            return False
        hr_reverse_dns_list = []
        if not 'API count exceeded - Increase Quota with Membership' in hr_reverse_dns_result[0]:
            try:
                if not 'error input is invalid' in hr_reverse_dns_result[0]:
                    for i in hr_reverse_dns_result:
                        fdomain = i.split(',')[0]
                        if fdomain[:4] == 'www.':
                            domain = fdomain[4:]
                        else:
                            domain = fdomain
                        ip = i.split(',')[1]
                        new_list = [domain,ip]
                        hr_reverse_dns_list.append(new_list)
                return hr_reverse_dns_list
            except IndexError:
                print ('Invalid API')
                return False
        else:
            print ('API limit Exceeded for the day')
            return False


    def result_reverse_ip(self):
        hr_reverse_ip = ["curl", "https://api.hackertarget.com/reverseiplookup/?q=" + self.domain]
        try:
            hr_reverse_ip_result = subprocess.check_output(hr_reverse_ip).decode("utf-8").splitlines()
        except:
            print ('Error')
            return False
        hr_reverse_ip_list = []
        if not 'API count exceeded - Increase Quota with Membership' in hr_reverse_ip_result[0]:
            try:
                if not 'error check your search parameter' in hr_reverse_ip_result[0]:
                    for i in hr_reverse_ip_result:
                        fdomain = i
                        if fdomain[:4] == 'www.':
                            domain = fdomain[4:]
                        else:
                            domain = fdomain
                        new_list = [domain]
                        hr_reverse_ip_list.append(new_list)  
                return hr_reverse_ip_list             
            except IndexError:
                print ('Invalid API')
                return False
        else:
            print ('API limit Exceeded for the day')
            return False


    def result_whois(self):
        hr_whois = ["curl", "https://api.hackertarget.com/whois/?q=" + self.domain]
        try:
            hr_whois_result = subprocess.check_output(hr_whois).decode("utf-8").splitlines()
        except:
            print ('Error')
            return False
        if not 'API count exceeded - Increase Quota with Membership' in hr_whois_result[0]:
            try:
                if not 'error check your search parameter' in hr_whois_result:
                    registrar_name = hr_whois_result[5].replace('Registrar Name: ','')
                    registrar_contact = hr_whois_result[13].replace('Tech Contact Name: ','')
                    registrar = [registrar_name, registrar_contact]
                return registrar
            except IndexError:
                print ('Invalid API')
                return False
        else:
            print ('API limit Exceeded for the day')
            return False


