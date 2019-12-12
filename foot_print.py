import argparse
import sys
import os
import socket
import pandas
from modules.hackertarget import hackertarget_result_gen
from modules.bufferover import bufferover_result_gen
from modules.shodan import shodan_data
from modules.functions import random_funtions
from modules.dnsdumpster import dnsdmpstr


def banner():
    print("""
         _____           _       ____       _       _     
        |  ___|__   ___ | |_    |  _ \ _ __(_)_ __ | |_   
        | |_ / _ \ / _ \| __|   | |_) | '__| | '_ \| __|  
        |  _| (_) | (_) | |_    |  __/| |  | | | | | |_ _ 
        |_|  \___/ \___/ \__|___|_|   |_|  |_|_| |_|\__(_)
                          |_______| A Project By Sudhara                 
    """)



def parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--domain", help="Check a domain.", action='store', metavar="[Domain]" , nargs=1)
    parser.add_argument("-f", "--file", help="Add the domain list", action="store" , metavar="[Domain List]" , nargs=1)
    parser.add_argument("-n", "--name", help="File Name.", action='store', metavar="[Name]" , nargs=1, required=True)
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        return False

    else:
        return args


def search(domain):
    try:
        if domain[:4] == 'www.':
            domain = domain[4:]
        elif domain[:4] == 'ww2.':
            domain = domain[4:]
        else:
            domain = domain
        socket.gethostbyname(domain)
    except socket.gaierror:
        return False

    #Gathering Data DNS dumpster and hacker target
    dumpstr = dnsdmpstr()
    ht_res = hackertarget_result_gen(domain)
    rand = random_funtions()

    dump_results,state = dumpstr.dump(domain)
    if dump_results:
        dns_data = []
        for i in dump_results['dns']:
            if not dump_results['dns'] == {}:
                dns_data.append(dump_results['dns'][i]['host'])

        mx_data = []
        for i in dump_results['mx']:
            if not dump_results['mx'] == {}:
                hostn = (dump_results['mx'][i]['host'])
                ip = (dump_results['mx'][i]['ip'])
                mx_data.append([hostn,ip])

        txt_data = []
        for i in dump_results['txt']:
            if not dump_results['txt'] == {}:
                txt_data.append(dump_results['txt'][i])  

        host_data = []
        for i in dump_results['host']:
            if not dump_results['host'] == {}:
                hostn = (dump_results['host'][i]['host'])
                hostn = str(hostn).split("HTTP")[0]
                hostn = str(hostn).split("SSH")[0]
                hostn = str(hostn).split("FTP")[0]
                ip = (dump_results['host'][i]['ip'])
                host_data.append([hostn,ip]) 


        #if there is more data than dnsdumpster limit
        if state == False: 
            print ('More domains than DNSDumster limit so checking via Hacker Target')
            host_search= ht_res.result_host_search()
            if host_search == False:
                print ('\nHacker Target cannot be used to get host data because API limit is exceeded.\n')
            else:
                for x in host_search:
                    host_data.append(x)
                host_data = rand.remove_dup(host_data)
    else:
        print ('The Program uses DNSdumpster as the main module. You reached the daily limit for the IP')
        return False, False #DNS Dumpster Limit is over

    reverse_dns = ht_res.result_reverse_dns()
    reverse_ip = ht_res.result_reverse_ip()
    
    if not reverse_ip:
        reverse_ip = []

    if not reverse_dns:
        reverse_dns = []
    '''
    #Buffer Over Run
    bo_res = bufferover_result_gen(domain)
    data = bo_res.api_call()

    if not data == False:
        fdns_data = bo_res.fdns_res()
        rdns_data = bo_res.rdns_res()
        if rdns_data == False and fdns_data == False:
            print ('No data in Buffer Over RUN')
            bo_list = []
        elif fdns_data == False:
            bo_list = rdns_data
        elif rdns_data == False:
            bo_list = fdns_data

        else:
            bo_list = rdns_data + fdns_data
    '''
    bo_list = []
    if host_data == []:
        Full_list_D = bo_list
       
    elif bo_list == []:
        Full_list_D = host_data

    elif bo_list and host_data == []:
        Full_list_D = []

    else:
        Full_list_D = bo_list + host_data
    
    if not Full_list_D == []:
        Full_list = rand.remove_dup(Full_list_D)
    
    print ('\nDomain List\n')
    for i in Full_list:
        print (str(i[0]) + ' : ' + str(i[1]))
    print ('\n')

    domain_data = [domain, dns_data, mx_data, txt_data, reverse_ip, reverse_dns]
    return Full_list, domain_data



def writer(data_list,name):
    try:
        data0 = pandas.DataFrame(data_list[0] ,columns=['IP', 'Hostname', 'Identified_Domain', 'Org', 'ISP', 'Country', 'City', 'ASN', 'Ports', 'Vul', 'Ipdate'])
        data1 = pandas.DataFrame(data_list[1] ,columns=['IP','Port','Protocol','Service','Application', 'Cpe', 'OS', 'Domains', 'Identified_Domain', 'SSL_Info'])
        data2 = pandas.DataFrame(data_list[2] ,columns=['IP', 'Port', 'SSL_exp', 'SSL_expired', 'SSL_name', 'SSL_ver', 'SSL_bits'])
        data3 = pandas.DataFrame(data_list[3] ,columns=['IP', 'Port', 'l', 'CVSS', 'Verified', 'Summary'])
        with pandas.ExcelWriter(name + '_A_Records_Shodan_Analysis'+'.xlsx') as writer:
            data0.to_excel(writer, sheet_name='General', index=False)
            data1.to_excel(writer, sheet_name='By_Port', index=False)
            data2.to_excel(writer, sheet_name='By_Cert', index=False)
            data3.to_excel(writer, sheet_name='By_Vul', index=False)
        return True
    except:
        return False

def shodan_ip_check(Full_list):
    print ('\nChecking With Shodan\n')  
    sh_check = shodan_data()
    data = sh_check.shodan_IP(Full_list)
    return data

def text_writer(data_list, name):
    
    try:
        with open (name + '_other_data.txt', "w") as file:
            for x in data_list:
                file.write ("Domain: " + x[0] + '\n')
                file.write ("\nDNS Data:\n")
                file.writelines ( "%s\n" % item for item in x[1])
                file.write ('\n')
                file.write ("\nMX Data:\n")
                file.writelines( "%s\n" % item for item in x[2])
                file.write ('\n')
                file.write ("\nTXT Data:\n")
                file.writelines ( "%s\n" % item for item in x[3])
                file.write ('\n')
                file.write ("\nReverse IP:\n")
                file.writelines ( "%s\n" % item for item in x[4])
                file.write ('\n')
                file.write ("\nReverse DNS:\n")
                file.writelines( "%s\n" % item for item in x[5])
                file.write ('\n')
            return True
    except:
        return False                            



def main():
    rand = random_funtions()
    sh = rand.SHODAN_API_KEY()
    banner()
    args = parser()
    domain = args.domain
    if domain:
        try:
            socket.gethostbyname(domain[0]) 
        except:
            print ('Invalid Domain: '+ domain[0])
            return False
    if args.file:
        if not os.path.isfile(args.file[0]):
                print ("File does not exist")
                quit()
        else:
            f = open(args.file[0], "r")
            if not args.file[0].endswith('.txt'):
                print ('Only support for .txt files')
                return False
            elif f == '':
                print ('File is Empty')
                return False
            else:
                dom_list = []
                for x in f:
                    x = x.strip()
                    if len(x) > 0:
                        try:
                            socket.gethostbyname(x) 
                            dom_list.append(x)
                        except:
                            print ('Invalid Domain: '+ x)
                            pass        
    try:
        if domain:
            a_data, o_data = search(args.domain[0])
            if a_data and o_data:
                write = text_writer([o_data],args.name[0])
                if sh:
                    shodan_g = shodan_ip_check(a_data)
                    shodan_r = writer(shodan_g,args.name[0])
                else:
                    print ('\nCannot check the A Records with Shodan. Add the API Key\n')
                    return False
                if write and shodan_r:
                    print ('\nDone Please check the file\n')
            else:
                return False

        elif args.file:
            o_data_list = []
            a_data_list = []
            for x in dom_list:
                print ('\n'+x+'\n')
                a_data, o_data = search(x)
                if a_data and o_data:
                    o_data_list = o_data_list + [o_data]
                    for y in a_data:
                        a_data_list.append(y)    
                else:
                    return False
            write = text_writer(o_data_list,args.name[0])
            if sh:
                shodan_g = shodan_ip_check(a_data_list)
                shodan_r = writer(shodan_g,args.name[0]) 
            else:
                    print ('\nCannot check the A Records with Shodan. Add the API Key\n')
                    return False
            if write and shodan_r:
                print ('\nDone Please check the file\n')   
        else:
            return False

    except Exception as e:
        print (e)
        print ('Error')

if __name__ == "__main__":
    main()
