import requests
import json
import os
import configparser


rootpath = os.path.dirname(__file__).replace("plugins","")
conf = configparser.ConfigParser()
conf.read(rootpath+"/config/plugins.conf")

url = conf.get("whois","url")
def whois(domain):
    whois_result = open(rootpath+"/result/"+domain+f"/{domain}_whois.txt",'w')
    print("\n[+ whois +] 正在查询...")
    res = requests.get(url+domain).text
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







    
    
    

    
