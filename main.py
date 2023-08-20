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
    import websocket
except ModuleNotFoundError:
    os.system("pip install requests")
    os.system("pip install httpx")
    os.system("pip install bs4")
    os.system("pip install pystyle")
    os.system("pip install colorama")
    os.system("pip install threading")
    os.system("pip install datetime")
    os.system("pip install tls_client")
    os.system("pip install websocket")

from colorama import Fore
from pystyle import Write, System, Colors, Colorate, Anime
from bs4 import BeautifulSoup
from threading import Lock
from random import choice
from tls_client import Session
from json import dumps
from websocket import WebSocket

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

with open("proxies.txt", "w", encoding='utf-8') as f:
    f.write("")

time.sleep(1)

with open(f"config.json", "r") as j:
    dassss = json.load(j)
    if dassss['proxy_scraper'] == "y" or dassss['proxy_scraper'] == "yes":
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
    else:
        pass

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
            return "0"
        else:
            return "0"
    except requests.exceptions.RequestException as e:
        return "0"
    except Exception as e:
        return "0"

def generate_members():
    global generated, failed, cap_solved, proxy_error, errors
    url = "https://discord.com/api/v9/experiments"
    output_lock = threading.Lock()
    try:
        money = balance()
        ctypes.windll.kernel32.SetConsoleTitleW(f'Discord Member Booster | Generated ~ {generated} | Solved ~ {cap_solved} | Errors ~ {errors} | Proxy Error ~ {proxy_error} | https://github.com/H4cK3dR4Du')
        session = tls_client.Session(
            client_identifier="safari_ios_16_0"
        )
        
        proxies = (random.choice(open("proxies.txt", "r").readlines()).strip()
            if len(open("proxies.txt", "r").readlines()) != 0
            else None)

        if ":" in proxies and len(proxies.split(":")) == 4:
            ip, port, user, pw = proxies.split(":")
            proxy = f"http://{user}:{pw}@{ip}:{port}"
        else:
            ip, port = proxies.split(":")
            proxy = f"http://{ip}:{port}"

        session.proxies = {
            "http": proxy,
            "https": proxy
        }

        headers = {
            'Accept': '*/*',
            'Accept-Language': 'es-ES,es;q=0.9',
            'Connection': 'keep-alive',
            'Referer': 'https://discord.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-GPC': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
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
        cap = Solver.solve_capmonster(site_key='4c672d35-0701-42b2-88c3-78380b0db560', page_url='https://discord.com/')
        cap_solved += 1
        with output_lock:
            time_rn = get_time_rn()
            print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({yellow}*{gray}) {pink}Solved Captcha {gray}| {magenta}{captcha_code}")
        url = "https://raw.githubusercontent.com/TahaGorme/100k-usernames/main/usernames.txt"
        response = requests.get(url)
        lines = response.text.splitlines()
        random_user = random.choice(lines)
        with open("config.json") as f:
            data = json.load(f)
            invite_code = data['invite']

        payload = {
            'consent': True,
            'global_name': random_user,
            'unique_username_registration': True,
            'fingerprint': fingerprint,
            'captcha_key': cap,
            'invite': invite_code,
        }

        headers = {
            'authority': 'discord.com',
            'accept': '*/*',
            'accept-language': 'es-ES,es;q=0.9',
            'referer': 'https://discord.com/',
            'origin': 'https://discord.com',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Brave";v="114"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sec-gpc': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'x-track': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImZyLUZSIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzExNC4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTE0LjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjk5OTksImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9',
            'x-fingerprint': fingerprint
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
                with open("tokens.txt", "w", encoding='utf-8') as f:
                        f.write(token + "\n")
                with open("config.json") as f:
                        a = json.load(f)
                        if a['online_tokens'] == "y":
                            ws_online = websocket.WebSocket()
                            ws_online.connect("wss://gateway.discord.gg/?encoding=json&v=9")
                            response = ws_online.recv()
                            event = json.loads(response)
                            platform = sys.platform
                            details = "https://radutool.org"
                            state = "discord.gg/radutool"
                            name = "H4cK3dR4Du#1337"
                            status_list = ["online", "idle", "dnd"]
                            status = random.choice(status_list)
                            ws_online.send(json.dumps({
                                "op": 2,
                                "d": {
                                    "token": token,
                                    "properties": {
                                        "$os": platform,
                                        "$browser": "RTB",
                                        "$device": f"{platform} Device",
                                    },
                                    "presence": {
                                    "game": {
                                        "name": name,
                                        "type": 0,
                                        "details": details,
                                        "state": state,
                                    },
                                    "status": status,
                                    "since": 0,
                                    "activities": [],
                                    "afk": False,
                                    },
                                },
                                "s": None,
                                "t": None
                            }))
                            with output_lock:
                                time_rn = get_time_rn()
                                print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({orange}${gray}) {orange}Onlined {gray}| ", end='')
                                sys.stdout.flush()
                                Write.Print(token + "\n", Colors.red_to_blue, interval=0.000)
                        if a['join_voice'] == "y":
                            channel_id = a["channel_id"]
                            server_id = a["server_id"]
                            ws_voice = WebSocket()
                            ws_voice.connect("wss://gateway.discord.gg/?v=8&encoding=json")
                            ws_voice.send(dumps(
                                {
                                    "op": 2,
                                    "d": {
                                        "token": token,
                                        "properties": {
                                            "$os": "windows",
                                            "$browser": "Discord",
                                            "$device": "desktop"
                                        }
                                    }
                                }))
                            ws_voice.send(dumps({
                                "op": 4,
                                "d": {
                                    "guild_id": server_id,
                                    "channel_id": channel_id,
                                    "self_mute": True,
                                    "self_deaf": True, 
                                    "self_stream?": True, 
                                    "self_video": True
                                }
                            }))
                            ws_voice.send(dumps({
                                "op": 18,
                                "d": {
                                    "type": "guild",
                                    "guild_id": server_id,
                                    "channel_id": channel_id,
                                    "preferred_region": "spain"
                                }
                            }))
                            ws_voice.send(dumps({
                                "op": 1,
                                "d": None
                            }))
                            with output_lock:
                                time_rn = get_time_rn()
                                print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({cyan}#{gray}) {magenta}Joined Voice {gray}| ", end='')
                                sys.stdout.flush()
                                Write.Print(token + "\n", Colors.purple_to_red, interval=0.000)
                                pass
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
