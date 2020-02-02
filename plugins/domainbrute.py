import gevent
from gevent import monkey,pool
monkey.patch_all()

import dns
from queue import Queue
import dns.resolver as resolver
import sys
import time
import random
import os
this_rootpath = os.path.dirname(__file__).replace("plugins","")


class DomainBruter:
    def __init__(self,domain):
        self.domain = domain
        self.domain_dict = dict()
        self.domain_queue = Queue()
        self.generate_dict()
        self.resolver = resolver.Resolver()
        self.pool = pool.Pool(1000)
        self.cname_record = dict()


        self.resolver.nameservers = ["182.254.116.116"]
        # self.get_faster_nameserver()

    def query(self,domain):
        sys.stdout.write("\r"+f"[+ domainbruter +] scanning {domain} ...")
        sys.stdout.flush()
        ip_list = []
        try:
            record = self.resolver.query(domain)
            for A_CNAME in record.response.answer:
                for item in A_CNAME.items:
                    if item.rdtype == self.get_type_id('A'):
                        ip_list.append(str(item))
                    if item.rdtype == self.get_type_id("CNAME"):
                        self.cname_record[domain] = str(item)
                        print(f"\n[+ domainbruter +] cname {domain} =====> {str(item)}")
                self.domain_dict[domain] = ",".join(ip_list)
        except dns.exception.Timeout:
            self.domain_queue.put(domain)
        except Exception as e:
            # print( e )
            pass

    # 不太稳定
    def get_faster_nameserver(self):
        print("[+ domainbruter +]  determining the fastest nameserver ...\n")
        # nameservers = open("D:\\share\\iscan\\plugins\\nameservers.txt").readlines()
        nameservers = open("dict/nameservers.txt").readlines()
        ser_info = {}
        for nameserver in nameservers:
            print(f"testing {nameserver}")
            self.resolver.nameservers = [nameserver]
            self.resolver.lifetime = 3
            start_time = time.time()
            for _ in range(2):
                random_str = str(random.randint(1, 1000))
                domain_list = [random_str + "testnamservspeed.com" for _ in range(200)]
                coroutines = [self.pool.spawn(self.query, l) for l in domain_list]
                gevent.joinall(coroutines)
            end_time = time.time()
            cost = end_time-start_time
            print(cost)
            ser_info[nameserver] = cost
        fast_nameserver = sorted(ser_info,key=lambda ser_info: ser_info[1])[0]
        print(fast_nameserver)
        self.resolver.nameservers = [fast_nameserver.strip()]
        self.resolver.lifetime = 10
        print(f"\n[+ domainbruter +] the fast nameserver is {fast_nameserver}")









    def generate_dict(self):
        try:
            # domains = open("D:\share\iscan\plugins\sub_full.txt",'r',encoding="utf-8").readlines()
            domains = open(this_rootpath+"/dict/sub_full.txt", 'r', encoding="utf-8").readlines()
            for domain in domains:
                self.domain_queue.put(domain.strip()+"."+self.domain)
            print(f"\n[+ domainbruter +] dict size {self.domain_queue.qsize()}")
        except FileNotFoundError as e:
            print(e)
            sys.exit(0)


    def get_type_id(self, name):
        return dns.rdatatype.from_text(name)

    def save_result(self):
        if not os.path.exists(this_rootpath+"result"):
            os.mkdir(this_rootpath+"result")
        try:
            os.mkdir(this_rootpath+"result/"+self.domain)
        except:
            pass
        resultpath = this_rootpath+"result/"+self.domain+"/"
        ips = []
        try:
            result_cname = open(resultpath + self.domain + "_cnames.txt", 'w')
            result = open(resultpath+self.domain+".txt",'w')
            result_ips = open(resultpath+self.domain+"_ips.txt",'w')
            result_subdomains = open(resultpath+self.domain+"_subs.txt",'w')

            for keys in self.domain_dict:
                result_subdomains.write(keys+"\n")
                if len(self.domain_dict[keys]) >19:
                    tmp_ips = self.domain_dict[keys].split(",")
                    for t_i in tmp_ips:
                        ips.append(t_i)
                else:
                    ips.append(self.domain_dict[keys])
                result.write(f"{keys}      {self.domain_dict[keys]}  ")
                result.write("\n")
            ips = list(set(ips))
            for ip in ips:
                result_ips.write(ip + "\n")

            for keys in self.cname_record:
                result_cname.write(f"{keys}    {self.cname_record[keys]}" + "\n")
        except Exception as e:
            print(f"\033[0;31;40m{e}\033[0m")
        finally:
            result.close()
            result_subdomains.close()
            result_ips.close()
            result_cname.close()

        # 记录cname


        print("\n[+ domainbruter +] save success "+self.domain+".txt")

    def run(self):
        print(f"[+ domainbruter +] nameserver : {self.resolver.nameservers}")
        while True:
            # sys.stdout.write("\r"+f"[+ domainbruter +] left {self.domain_queue.qsize()}")
            # sys.stdout.flush()
            if self.domain_queue.empty():
                break
            for _ in range(self.domain_queue.qsize()):
                coroutine = [self.pool.spawn(self.query,self.domain_queue.get())]
            try:
                gevent.joinall(coroutine)
            except Exception as e:
                print(e)
                sys.exit(0)
        self.save_result()


# if __name__ == '__main__':
#     burter = DomainBruter("jieqi.com")
#     # burter.query("global.joyoung.com")
#     burter.run()
#     # print(this_rootpath)

