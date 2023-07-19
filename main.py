import os, random, string, time, json, sys, ctypes
from data.solver import Solver

try:
    import requests
    import httpx
    import bs4
    import pystyle
    import colorama
    import threading
    import datetime
    import tls_client
except ModuleNotFoundError:
    os.system("pip install requests")
    os.system("pip install httpx")
    os.system("pip install bs4")
    os.system("pip install pystyle")
    os.system("pip install colorama")
    os.system("pip install threading")
    os.system("pip install datetime")
    os.system("pip install tls_client")

from colorama import Fore
from pystyle import Write, System, Colors, Colorate, Anime
from bs4 import BeautifulSoup
from threading import Lock
from random import choice
from tls_client import Session
from json import dumps

red = Fore.RED
yellow = Fore.YELLOW
green = Fore.GREEN
blue = Fore.BLUE
orange = Fore.RED + Fore.YELLOW
pink = Fore.LIGHTMAGENTA_EX + Fore.LIGHTCYAN_EX
magenta = Fore.MAGENTA
lightblue = Fore.LIGHTBLUE_EX
cyan = Fore.CYAN
gray = Fore.LIGHTBLACK_EX + Fore.WHITE
reset = Fore.RESET

generated = 0
failed = 0
cap_solved = 0
proxy_error = 0
errors = 0
fingerprint = 0

def save_proxies(proxies):
    with open("proxies.txt", "w") as file:
        file.write("\n".join(proxies))

def get_proxies():
    with open('proxies.txt', 'r', encoding='utf-8') as f:
        proxies = f.read().splitlines()
    if not proxies:
        proxy_log = {}
    else:
        proxy = random.choice(proxies)
        proxy_log = {
            "http://": f"http://{proxy}", "https://": f"http://{proxy}"
        }
    try:
        url = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all"
        response = httpx.get(url, proxies=proxy_log, timeout=60)

        if response.status_code == 200:
            proxies = response.text.splitlines()
            save_proxies(proxies)
        else:
            time.sleep(1)
            get_proxies()
    except httpx.ProxyError:
        get_proxies()
    except httpx.ReadError:
        get_proxies()
    except httpx.ConnectTimeout:
        get_proxies()
    except httpx.ReadTimeout:
        get_proxies()
    except httpx.ConnectError:
        get_proxies()
    except httpx.ProtocolError:
        get_proxies()

def check_proxies_file():
    file_path = "proxies.txt"
    if os.path.exists(file_path) and os.path.getsize(file_path) == 0:
        get_proxies()

check_proxies_file()

def get_time_rn():
    date = datetime.datetime.now()
    hour = date.hour
    minute = date.minute
    second = date.second
    timee = "{:02d}:{:02d}:{:02d}".format(hour, minute, second)
    return timee

bad_proxies = []
locked_proxies = []
proxies = []
proxy_type = "http"
proxy_lock = Lock()

def balance():
    proxy = (random.choice
             (open
              ("proxies.txt", "r").readlines()
              ).strip()
    if len(open
           ("proxies.txt", "r")
           .readlines()
           ) != 0
    else None
    )
    session_proxy = Session(
        client_identifier="chrome_114",
        random_tls_extension_order=True
    )
    session_proxy.proxies = {
        "http": "http://" + proxy,
        "https": "http://" + proxy
    }
    with open("config.json") as imradu:
        data2 = json.load(imradu)
        key = data2.get("captcha_key")
    payload = {
        "clientKey": key
    }
    try:
        response = session_proxy.post("https://api.capmonster.cloud/getBalance", json=payload)
        if response.status_code == 200:
            data = response.json()
            balance = data["balance"]
            return balance
        elif "ERROR_KEY_DOES_NOT_EXIST" in response.text:
            return None
        else:
            return None
    except requests.exceptions.RequestException as e:
        pass
    except Exception as e:
        pass

def generate_members():
    global generated, failed, cap_solved, proxy_error, errors
    url = "https://discord.com/api/v9/experiments"
    output_lock = threading.Lock()
    try:
        money = balance()
        ctypes.windll.kernel32.SetConsoleTitleW(f'Discord Member Booster | Generated ~ {generated} | Solved ~ {cap_solved} | Errors ~ {errors} | Proxy Error ~ {proxy_error} | Balance ~ ${money} | https://github.com/H4cK3dR4Du')
        proxy = (choice
                 (open
                  ("proxies.txt", "r").readlines()
                  ).strip()
        if len(open
               ("proxies.txt", "r")
               .readlines()) != 0
        else None
        )
        session = Session(
                client_identifier="chrome_114",
                random_tls_extension_order=True
        )
        session.proxies = {
            "http": "http://" + proxy,
            "https": "http://" + proxy
        }

        headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Referer': 'https://discord.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-GPC': '1',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36 Edg/114.0.1823.51',
            'X-Track': 'eyJvcyI6IklPUyIsImJyb3dzZXIiOiJTYWZlIiwic3lzdGVtX2xvY2FsZSI6ImVuLUdCIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKElQaG9uZTsgQ1BVIEludGVybmFsIFByb2R1Y3RzIFN0b3JlLCBhcHBsaWNhdGlvbi8yMDUuMS4xNSAoS0hUTUwpIFZlcnNpb24vMTUuMCBNb2JpbGUvMTVFMjQ4IFNhZmFyaS82MDQuMSIsImJyb3dzZXJfdmVyc2lvbiI6IjE1LjAiLCJvc192IjoiIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfZG9tYWluX2Nvb2tpZSI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjk5OTksImNsaWVudF9ldmVudF9zb3VyY2UiOiJzdGFibGUiLCJjbGllbnRfZXZlbnRfc291cmNlIjoic3RhYmxlIn0',
        }

        response = session.get('https://discord.com/api/v9/experiments', headers=headers)
        if response.status_code == 200:
            data = response.json()
            fingerprint = data["fingerprint"]
            with output_lock:
                time_rn = get_time_rn()
                print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({lightblue}~{gray}) {pink}Got Fingerprint {gray}| {green}{fingerprint}")
        else:
            with output_lock:
                time_rn = get_time_rn()
                print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({red}-{gray}) {pink}Failed Getting Fingerprint {gray}| {red}Bad Gateaway")
            errors += 1
            generate_members()
        captcha_code = 'P1_eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.hKdwYXNza2V5xQbV'
        with open('config.json') as config_file:
            config_data = json.load(config_file)
        invite = config_data.get('invite')
        cap = Solver.solve_capmonster(site_key='4c672d35-0701-42b2-88c3-78380b0db560', page_url='https://discord.com/')
        cap_solved += 1
        with output_lock:
            time_rn = get_time_rn()
            print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({yellow}*{gray}) {pink}Solved Captcha {gray}| {magenta}{captcha_code}")
        url = "https://raw.githubusercontent.com/TahaGorme/100k-usernames/main/usernames.txt"
        response = requests.get(url)
        lines = response.text.splitlines()
        random_user = random.choice(lines)
        payload = {
            "consent": True,
            "fingerprint": fingerprint,
            "username": random_user,
            "gift_code_sku_id": None,
            "invite": invite,
            "captcha_key": cap,
        }
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-GB',
            'Connection': 'keep-alive',
            'content-length': str(len(dumps(payload))),
            'Content-Type': 'application/json',
            'Origin': 'https://discord.com',
            'Referer': 'https://discord.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-GPC': '1',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/609.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/609.1.15',
            'X-Fingerprint': fingerprint,
            'X-Track': 'eyJvcyI6IklPUyIsImJyb3dzZXIiOiJTYWZlIiwic3lzdGVtX2xvY2FsZSI6ImVuLUdCIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKElQaG9uZTsgQ1BVIEludGVybmFsIFByb2R1Y3RzIFN0b3JlLCBhcHBsaWNhdGlvbi8yMDUuMS4xNSAoS0hUTUwpIFZlcnNpb24vMTUuMCBNb2JpbGUvMTVFMjQ4IFNhZmFyaS82MDQuMSIsImJyb3dzZXJfdmVyc2lvbiI6IjE1LjAiLCJvc192IjoiIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfZG9tYWluX2Nvb2tpZSI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjk5OTksImNsaWVudF9ldmVudF9zb3VyY2UiOiJzdGFibGUiLCJjbGllbnRfZXZlbnRfc291cmNlIjoic3RhYmxlIn0',
        }
        response = session.post('https://discord.com/api/v9/auth/register', headers=headers, json=payload)
        if "token" not in response.text:
            if "retry_after" in response.text:
                with output_lock:
                    time_rn = get_time_rn()
                    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({red}-{gray}) {pink}Ratelimit {gray}| {red}{response.json().get('retry_after')}s")
                errors += 1
                proxy_error += 1
                failed += 1
        token = response.json().get('token')
        if token == None:
            errors += 1
            generate_members()
        else:
            with output_lock:
                time_rn = get_time_rn()
                print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pink}Generated {gray}| ", end='')
                sys.stdout.flush()
                Write.Print(token + "\n", Colors.cyan_to_blue, interval=0.000)
                generated += 1
                generate_members()
    except:
        proxy_error += 1
        failed += 1
        generate_members()

Write.Print(f"""
\t\t    __  ___               __                 ____                   __           
\t\t   /  |/  /__  ____ ___  / /_  ___  _____   / __ )____  ____  _____/ /____  _____
\t\t  / /|_/ / _ \/ __ `__ \/ __ \/ _ \/ ___/  / __  / __ \/ __ \/ ___/ __/ _ \/ ___/
\t\t / /  / /  __/ / / / / / /_/ /  __/ /     / /_/ / /_/ / /_/ (__  ) /_/  __/ /    
\t\t/_/  /_/\___/_/ /_/ /_/_.___/\___/_/     /_____/\____/\____/____/\__/\___/_/     
                                                                                 
\t\t\t\t\t[ https://github.com/H4cK3dR4Du ]
\t\t\t\t\t [   Leave A Star Please! :)   ]
""", Colors.cyan_to_blue, interval=0.000)
print(f"\n\n")
time.sleep(1)
def run():
    while True:
        generate_members()

with open("config.json") as f:
    data = json.load(f)

num_threads = data.get('threads', 100)
threads = []
for i in range(int(num_threads)):
    thread = threading.Thread(target=run, name=f"BOOSTER-{i+1}")
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()
