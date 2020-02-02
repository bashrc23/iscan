from plugins.domainbrute import *
import argparse
from plugins.portscan import *
from multiprocessing import Process
from plugins.whois import *
from plugins.whatweb import *
from plugins.portscanner_alt import *
import json
import os
import sys


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d","--domain",help="target domain",required=True)
    parser.add_argument("-fc","--force_check_port",help="force check subdomain port",choices=['y','n'])
    parser.add_argument("-p","--plugins",help="choose the plugins you want to use",default="domainbrute")
    args = parser.parse_args()


    domain = args.domain
    plugins = args.plugins
    force_check_port = True if args.force_check_port == 'y' else False

    processes = []
    if "whatweb" in plugins:
        whatweb = Process(target=whatweb, args=(domain,))
        processes.append(whatweb)
    if "whois" in plugins:
        whois = Process(target=whois, args=(domain,))
        processes.append(whois)
    if "domainbrute" in plugins:
        domainbruter = DomainBruter(domain)


    if test_alive(domain):
        domainbruter.run()

        for p in processes:
            p.start()

        if force_check_port:
            portscaner = Port_scanner(domain)
            portscaner.check_sub_domain_ports()
    else:
        print("[-] the target seems dead,please check your input somthing like : baidu.com (without http!)")
        sys.exit(0)










    
