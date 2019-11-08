import subprocess
import json
import copy
import ipaddress
import socket

class bufferover_result_gen:

    def __init__(self,domain):
        self.domain = domain

    def api_call(self):
        try:
            search = ["curl", "http://dns.bufferover.run/dns?q="+self.domain]
            results = subprocess.check_output(search).decode("utf-8")
            results= json.loads(results)
            return results
        except:
            print ('Error')
            return False

    def fdns_res(self):
        fdns_sheet = []
        results = self.api_call()
        if not results == False:
            fdns = results['FDNS_A']
            if not fdns == None:
                for i in fdns:
                    ip = i.split(',')[0]
                    
                    fdomain = i.split(',')[1]
                    if fdomain[:4] == 'www.':
                        domain = fdomain[4:]
                    elif fdomain[:4] == 'ww2.':
                        domain = fdomain[4:]
                    else:
                        domain = fdomain
                    try:
                        ip = ipaddress.ip_address(ip)
                    except ValueError:
                        if ip[:4] == 'www.':
                            ip = ip[4:]
                        elif ip[:4] == 'ww2.':
                            ip = ip[4:]
                        else:
                            ip = ip
                        try:        
                            IP = socket.gethostbyname(ip)
                        except:
                            continue
                        Domainx = ip 
                        results = [Domainx,IP] 
                        fdns_sheet.append(results)
                        try:
                            ip = socket.gethostbyname(domain)                    
                        except:
                            continue
                    results = [domain,ip]
                    fdns_sheet.append(results)
                if not (len(fdns_sheet) == 0): 
                    return fdns_sheet
                else:
                    print ('No results Found')
                    return False
            else: 
                return False
        else:
            return False

    def rdns_res(self):
        rdns_sheet = []
        results = self.api_call()
        if not results == False:
            rdns = results['RDNS']
            if not rdns == None:
                for i in rdns:
                    ip = i.split(',')[0]
                    fdomain = i.split(',')[1]
                    if fdomain[:4] == 'www.':
                        domain = fdomain[4:]
                    elif fdomain[:4] == 'ww2.':
                        domain = fdomain[4:]
                    else:
                        domain = fdomain
                    try:
                        ip = ipaddress.ip_address(ip)
                    except ValueError:
                        if ip[:4] == 'www.':
                            ip = ip[4:]
                        elif ip[:4] == 'ww2.':
                            ip = ip[4:]
                        else:
                            ip = ip
                        try:        
                            IP = socket.gethostbyname(ip)
                        except:
                            continue
                        Domainx = ip 
                        results = [Domainx,IP] 
                        rdns_sheet.append(results)
                        try:
                            ip = socket.gethostbyname(domain)                    
                        except:
                            continue 

                    results = [domain,ip]
                    rdns_sheet.append(results)
                if not (len(rdns_sheet) == 0): 
                    return (rdns_sheet)
                else:
                    print ('No results Found')
                    return False
            else: 
                return False
        else:
            return False
