#!/usr/bin/env python3
"""
Truecaller-Sim: Advanced Phone Number Information Tool
Author: Renato
"""

import random, time, hashlib, sys
from datetime import datetime
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Banner (unchanged)
BANNER = r"""
▓█████▄ ▓█████  ██▓     ██▓ ███▄ ▄███▓ ▄▄▄       ███▄    █  ▄▄▄█████▓
▒██  ▀█▄▓█   ▀ ▓██▒    ▓██▒▓██▒▀█▀ ██▒▒████▄     ██ ▀█   █  ▓  ██▒ ▓▒
░██▄▄▄▄██▒███   ▒██░    ▒██▒▓██    ▓██░▒██  ▀█▄  ▓██  ▀█ ██▒▒ ▓██░ ▒░
 ▓█  █▀█░▓█  ▄ ▒██░    ░██░▒██    ▒██ ░██▄▄▄▄██ ▓██▒  ▐▌██▒░ ▓██▓ ░ 
 ▒▓█▒█▌ ░▒████▒░██████▒░██░▒██▒   ░██▒ ▓█   ▓██▒▒██░   ▓██░  ▒██▒ ░ 
 ░▒▓░▒░ ░░ ▒░ ░░ ▒░▓  ░░▓  ░ ▒░   ░  ░ ▒▒   ▓▒█░░ ▒░   ▒ ▒   ▒ ░░   
 ░▒ ░ ▒  ░ ░  ░░ ░ ▒  ░ ▒ ░░  ░      ░  ▒   ▒▒ ░░ ░░   ░ ▒░    ░    
 ░░   ░    ░     ░ ░    ▒ ░░      ░     ░   ▒      ░   ░ ░   ░      
  ░        ░  ░    ░  ░ ░         ░         ░  ░         ░          
"""

# Expanded data pools (Japan + India + Nepal)
NAMES = [
    # Japan
    "Hiroshi Sato", "Ayumi Takahashi", "Kenji Tanaka", "Yumi Nakamura", "Taro Suzuki",
    # India
    "Rahul Sharma", "Priya Verma", "Amit Patel", "Sneha Iyer", "Arjun Mehta", "Neha Gupta", "Ravi Kumar", "Pooja Singh",
    # Nepal
    "Sanjay Shrestha", "Anita Gurung", "Dipesh Rana", "Kritika Basnet", "Binod Adhikari", "Mina Tamang"
]
ALT_NAMES = [
    "H. Sato", "A. Takahashi", "K. Tanaka", "Y. Nakamura", "T. Suzuki",
    "R. Sharma", "P. Verma", "A. Patel", "S. Iyer", "A. Mehta", "N. Gupta", "R. Kumar", "P. Singh",
    "S. Shrestha", "A. Gurung", "D. Rana", "K. Basnet", "B. Adhikari", "M. Tamang"
]
CARRIERS = [
    # Japan
    "NTT Docomo", "SoftBank", "au KDDI", "Rakuten Mobile",
    # India
    "Jio", "Airtel", "Vodafone Idea", "BSNL",
    # Nepal
    "Ncell", "Nepal Telecom", "SmartCell"
]
CITIES = [
    # Japan
    "Tokyo", "Osaka", "Nagoya", "Sapporo", "Yokohama", "Fukuoka",
    # India
    "Delhi", "Mumbai", "Bengaluru", "Chennai", "Kolkata", "Hyderabad",
    # Nepal
    "Kathmandu", "Pokhara", "Biratnagar", "Lalitpur", "Bhaktapur"
]
GENDERS = ["Male", "Female"]
MODELS = ["iPhone 14 Pro", "iPhone 16 Plus", "Samsung Galaxy S23", "Google Pixel 8", "Xiaomi 13 Pro"]
OS_LIST = ["iOS 18.5", "iOS 17.6", "Android 14", "Android 13", "HarmonyOS 4.0"]

SOCIALS = [
    "facebook.com/", "instagram.com/", "twitter.com/", "t.me/"
]

# Function: seeded choice (consistent per number)
def seeded_choice(seed, options):
    random.seed(seed)
    return random.choice(options)

# Function: hash for consistency
def make_seed(phone):
    return int(hashlib.sha256(phone.encode()).hexdigest(), 16)

# Function: fake IP generator
def fake_ip(seed):
    random.seed(seed)
    return f"{random.randint(20, 223)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"

# Function: progress animation
def progress_bar(text="Searching", length=20):
    for i in range(length+1):
        bar = "█" * i + "-" * (length-i)
        sys.stdout.write(f"\r{text}: [{bar}] {int((i/length)*100)}%")
        sys.stdout.flush()
        time.sleep(0.05)
    print()

# Main
def main():
    print(Fore.CYAN + BANNER + Style.RESET_ALL)

    # Input
    phone = input(Fore.YELLOW + "Enter phone number: " + Style.RESET_ALL).strip()
    if not phone.startswith("+") or not phone[1:].isdigit():
        print(Fore.RED + "[!] Invalid number. Please use format like +919812345678" + Style.RESET_ALL)
        return

    # Simulate searching
    print("\n[+] Connecting to Global Caller ID Database...")
    time.sleep(0.7)
    print("[+] Querying carrier records...")
    time.sleep(0.7)
    print("[+] Checking spam reports...")
    time.sleep(0.7)
    progress_bar("Finalizing")

    # Generate fake but consistent info
    seed = make_seed(phone)
    name = seeded_choice(seed, NAMES)
    alt_name = seeded_choice(seed+1, ALT_NAMES)
    gender = seeded_choice(seed+2, GENDERS)
    carrier = seeded_choice(seed+3, CARRIERS)
    city = seeded_choice(seed+4, CITIES)
    model = seeded_choice(seed+5, MODELS)
    os_ver = seeded_choice(seed+6, OS_LIST)
    ip = fake_ip(seed+7)
    email = name.lower().replace(" ", ".") + "@example.com"
    spam_score = (seed % 100)

    # Display results
    print(Fore.GREEN + "\n=== Caller Info ===" + Style.RESET_ALL)
    print(f"Phone Number     : {phone}")
    print(f"Name             : {name}")
    print(f"Alternate Name   : {alt_name}")
    print(f"Gender           : {gender}")
    print(f"Carrier          : {carrier}")
    print(f"Line Type        : Mobile")
    print(f"City / State     : {city}")
    print(f"Email            : {email}")
    print(f"Last Seen        : {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    # Spam score with color
    if spam_score < 30:
        print(f"Spam Score       : {Fore.GREEN}{spam_score}% (Safe){Style.RESET_ALL}")
    elif spam_score < 70:
        print(f"Spam Score       : {Fore.YELLOW}{spam_score}% (Medium Risk){Style.RESET_ALL}")
    else:
        print(f"Spam Score       : {Fore.RED}{spam_score}% (High Risk 🚨){Style.RESET_ALL}")

    # Device info
    print(Fore.CYAN + "\n=== Device Info ===" + Style.RESET_ALL)
    print(f"Phone Model      : {model}")
    print(f"OS Version       : {os_ver}")
    print(f"Last Active IP   : {ip}")
    print("Network Type     : 4G LTE")

    # Social info
    print(Fore.MAGENTA + "\n=== Social Info ===" + Style.RESET_ALL)
    for s in SOCIALS:
        print(f"{s}{name.lower().replace(' ', '')}")

    print(Fore.CYAN + "\n=== End of Result ===" + Style.RESET_ALL)


if __name__ == "__main__":
    main()
