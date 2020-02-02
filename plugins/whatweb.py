import requests
import zlib
import json
import os
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

rootpath = os.path.dirname(__file__).replace("plugins","")

def whatweb(domain):
    result = open(rootpath+"/result/"+domain+f"/{domain}_whatweb.txt",'w',encoding="GBK")
    url = "http://"+domain
    try:
        response = requests.post(url,timeout=5)
    except Exception as e:
        print(f"[+ whatweb +] {e}")

    whatweb_dict = {"url":response.url,"text":response.text,"headers":dict(response.headers)}
    whatweb_dict = json.dumps(whatweb_dict)
    whatweb_dict = whatweb_dict.encode()
    whatweb_dict = zlib.compress(whatweb_dict)
    data = {"info":whatweb_dict}
    res = requests.post("http://whatweb.bugscaner.com/api.go",files=data).text
    info_dict = json.loads(res)
    for keys in info_dict:
        print(f"[+ whatweb +] {keys}:{info_dict[keys]}")
        result.write(f"{keys}:{info_dict[keys]}"+"\n")
    result.close()
    print("[+ whatweb +] complete!")




    

