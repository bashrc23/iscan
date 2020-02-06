import gevent
from gevent import monkey
monkey.patch_all()
import nmap
import os
import sys
import configparser
import json
from queue import Queue

rootpath = os.path.dirname(__file__).replace("plugins","")
conf = configparser.ConfigParser()
conf.read(rootpath+"/config/plugins.conf")


def test_alive(domain):  # 检测端口数量判断主机存活
    print(f"[+] Detecting {domain} Survival ... ")
    scanner = nmap.PortScanner()
    tester = scanner.scan(hosts=domain, arguments="-F -sS -T5 -Pn")
    scan = tester['scan']

    ip = None
    for keys in scan:
        ip = keys
        break
    if ip:
        if len(scan[ip]['tcp']) > 0:
            return True
    else:
        return False


class Port_scanner:
    def __init__(self,domain):
        self.result = []
        self.ips = []
        self.domain = domain
        self.load_sub_domain_ips()



    def load_sub_domain_ips(self):
        self.ips = [ip.strip() for ip in open(rootpath+"/result/"+self.domain+"/"+self.domain+"_ips.txt",'r').readlines()]



    def scan(self,ip):
        sys.stdout.write("\r"+f"[+ portscanner +] checking {ip}'s ports ...")
        sys.stdout.flush()
        portscan = nmap.PortScanner()
        try:
            p = portscan.scan(hosts=ip,arguments=conf.get("nmap","argv"),ports=conf.get("nmap","ports"))
            self.result.append(portscan)
        except Exception as e:
            print(f"[- portscanner -] {e}")



    def save_result(self):
        res_file = open(rootpath+"/result/"+self.domain+"/"+self.domain+"_port_info.csv",'w')
        for p in self.result:
            res_file.write(p.csv())
            res_file.write("\n")
        res_file.close()
        print(f"\n[+ portscanner +] complete! ")


    def check_sub_domain_ports(self):
        print("[+ portscanner +] checking ports ...")
        coroutine = [gevent.spawn(self.scan,ip) for ip in self.ips]
        try:
            gevent.joinall(coroutine)
            self.save_result()

        except Exception as e:
            print(f"[- portscanner -] {e}")

# if __name__ == '__main__':
#     p = nmap.PortScanner()
#     s = p.scan(hosts="my.srat1999.top",arguments=conf.get("nmap","argv"))
#     print(s)
    # p.check_sub_domain_ports()
    # print(conf.get("nmap","argv"))







