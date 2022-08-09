import requests
import time
import random
import os
import argparse

from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from anole import UserAgent

ua = UserAgent()

# 使用git接口搜索cve编号
def search(cve, *args):
    url = f"https://api.github.com/search/repositories?q={cve}&sort=updated"
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        'Connection': 'close',
        'User-Agent': ua.random}

    try:
        if len(args) == 1:
            res = requests.get(url, headers=headers, verify=False, proxies={"http": args[0], "https": args[0]},
                               timeout=10)
        else:
            res = requests.get(url, headers=headers, verify=False, timeout=10)
        if res.status_code == 200:
            data = res.json()
            for i in range(0, len(data['items'])):
                cve_url = data['items'][i]['html_url']
                print(cve_url)
                yield cve_url
    except Exception as e:
        print(e)

# 读取文件（cve编号）
def fromFile(filePath, *args):
    with open(filePath, "r") as f:
        for i in f.readlines():
            save(f"----------------------------{i.strip()}-----------------------------------")
            if len(args) == 1:
                for url in search(i.strip(), *args):
                    save(url)
            else:
                for url in search(i.strip()):
                    save(url)
            s = random.randint(5, 10)
            time.sleep(s)


def save(data):
    if data:
        with open("result.txt", "a") as f:
            f.write(data + "\n")


if __name__ == "__main__":
    print("-----------CVE_Github_Spider---------------")
    print("-----------Author：Panacea-----------------")
    parser = argparse.ArgumentParser(description='CVE Search.')
    parser.add_argument("-n", "--NAME", type=str, help="CVE NAME")
    parser.add_argument("-f", "--FILE", type=str, help="FILE PATH")
    parser.add_argument("-p", "--PROXY", type=str, help="PROXY, eg: http://127.0.0.1:8080")
    args = parser.parse_args()
    if args.PROXY:
        if args.NAME:
            save(f"----------------------------{args.NAME}-----------------------------------")
            for url in search(args.NAME, args.PROXY):
                save(url)
        elif args.FILE:
            fromFile(args.FILE, args.PROXY)

    else:
        if args.NAME:
            save(f"----------------------------{args.NAME}-----------------------------------")
            for url in search(args.NAME):
                save(url)
        elif args.FILE:
            fromFile(args.FILE)
