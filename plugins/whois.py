import requests
import json
import os
 

key = "xxxxxxxxxxxxxxxxxxx"
url = "http://apidata.chinaz.com/CallAPI/Whois?key=%s&domainName=%s"

rootpath = os.path.dirname(__file__).replace("plugins","")
def whois(domain):
    whois_result = open(rootpath+"/result/"+domain+f"/{domain}_whois.txt",'w')
    print("[+ whois +] 正在查询...")
    res = requests.get(url%(key,domain)).text
    data = json.loads(res)
    # print(res)
    if data.get('StateCode')==1:
        result = data.get('Result')
        for keys in result:
            print(f"[+ whois +] {keys}:{result[keys]}")
            whois_result.write(f"{keys}:{result[keys]}"+"\n")
        whois_result.close()

        print('[+ whois +] complete! ')
    else:
        print('[- whois -] 查询失败！')
        whois_result.close()







    
    
    

    
