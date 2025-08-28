#!/usr/bin/env python3
"""
Truecaller-Sim: Advanced Phone Number Information Tool
"""

import random, json, asyncio, aiofiles, re, time
from datetime import datetime, timedelta
from pathlib import Path
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Colors
class Colors:
    RED = Fore.RED
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    BLUE = Fore.BLUE
    MAGENTA = Fore.MAGENTA
    CYAN = Fore.CYAN
    WHITE = Fore.WHITE
    BRIGHT = Style.BRIGHT
    RESET = Style.RESET_ALL
    BANNER = Fore.LIGHTMAGENTA_EX
    HEADER = Fore.LIGHTCYAN_EX
    SUCCESS = Fore.LIGHTGREEN_EX
    WARNING = Fore.LIGHTYELLOW_EX
    ERROR = Fore.LIGHTRED_EX
    INFO = Fore.LIGHTBLUE_EX

# Banner
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

# Sample Data
NAMES_DATA = {
    "nepal": {"male": ["Raj","Suresh","Amit","Bikash","Nabin","Krishna","Hari","Santosh","Prakash","Deepak"],
              "female":["Sita","Gita","Rita","Sabina","Anita","Sunita","Puja","Mina","Rina","Sarita"],
              "last":["Sharma","Poudel","Karki","Gurung","Rai","Tamang","Magar","Thapa","Acharya","Adhikari"]},
    "india": {"male": ["Rahul","Amit","Raj","Vijay","Sanjay","Arun","Kumar","Sandeep","Vikram","Ravi"],
              "female":["Priya","Anjali","Neha","Sunita","Kavita","Divya","Pooja","Anita","Sonia","Rani"],
              "last":["Sharma","Patel","Singh","Kumar","Gupta","Verma","Yadav","Jha","Reddy","Malik"]},
    "japan": {"male":["Hiroshi","Takashi","Yuki","Kenji","Taro","Satoshi","Makoto","Ryu","Kaito","Daichi"],
              "female":["Yuki","Hana","Sakura","Airi","Miyuki","Akari","Rin","Yui","Mei","Saki"],
              "last":["Sato","Suzuki","Tanaka","Watanabe","Yamamoto","Takahashi","Kobayashi","Nakamura","Yoshida","Yamada"]}
}

CARRIERS_DATA = {
    "nepal":["Ncell","Nepal Telecom","Smart Cell"],
    "india":["Airtel","Jio","Vodafone Idea","BSNL"],
    "japan":["NTT Docomo","KDDI au","SoftBank","Rakuten Mobile"]
}

CITIES = {
    "nepal":["Kathmandu","Pokhara","Lalitpur","Biratnagar","Bharatpur","Birgunj","Butwal","Dharan","Hetauda","Nepalgunj"],
    "india":["Mumbai","Delhi","Bangalore","Hyderabad","Ahmedabad","Chennai","Kolkata","Surat","Pune","Jaipur"],
    "japan":["Tokyo","Osaka","Kyoto","Yokohama","Nagoya","Sapporo","Kobe","Fukuoka","Kawasaki","Hiroshima"]
}

STATES = {
    "nepal":["Bagmati","Gandaki","Lumbini","Karnali","Province 1","Province 2","Sudurpashchim"],
    "india":["Maharashtra","Delhi","Karnataka","Tamil Nadu","Gujarat","West Bengal","Uttar Pradesh","Rajasthan","Bihar","Kerala"],
    "japan":["Tokyo","Osaka","Kyoto","Hokkaido","Kanagawa","Aichi","Fukuoka","Hyogo","Hiroshima","Saitama"]
}

BANKS = {
    "nepal":["Nabil Bank","Himalayan Bank","Nepal Bank","Everest Bank","Kumari Bank","Global IME Bank","NIC Asia Bank"],
    "india":["SBI","HDFC","ICICI","Axis Bank","Kotak Mahindra","Punjab National Bank","Bank of Baroda"],
    "japan":["Mitsubishi UFJ","Mizuho","Sumitomo Mitsui","Resona","SBI Shinsei","Rakuten Bank","PayPay Bank"]
}

OCCUPATIONS = {
    "nepal": ["Business Owner", "Farmer", "Teacher", "Government Employee", "Tour Guide", "Engineer", "Doctor", "Student", "Driver", "Shopkeeper"],
    "india": ["Software Engineer", "Business Executive", "Doctor", "Teacher", "Government Officer", "Farmer", "Student", "Driver", "Shop Owner", "Accountant"],
    "japan": ["Salaryman", "Engineer", "Teacher", "Doctor", "Shopkeeper", "Farmer", "Student", "Artist", "Chef", "Government Worker"]
}

EDUCATION_LEVELS = ["High School", "Diploma", "Bachelor's Degree", "Master's Degree", "PhD", "No Formal Education"]
BLOOD_GROUPS = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]
MARITAL_STATUSES = ["Single", "Married", "Divorced", "Widowed", "Separated"]
DEVICE_MODELS = ["iPhone 13", "Samsung Galaxy S21", "Google Pixel 6", "Xiaomi Mi 11", "OnePlus 9", "Huawei P50", "Oppo Find X3", "Vivo X70"]
OS_VERSIONS = ["iOS 15", "Android 12", "Android 11", "iOS 14", "Android 10"]
NETWORK_TYPES = ["2G", "3G", "4G", "5G"]
SOCIAL_MEDIA_PLATFORMS = ["Facebook", "Twitter", "Instagram", "LinkedIn", "TikTok", "Snapchat", "YouTube", "Pinterest"]
FAVORITE_APPS = ["WhatsApp", "Instagram", "Facebook", "YouTube", "Twitter", "TikTok", "Snapchat", "Google Maps", "Gmail", "Amazon", "Netflix", "Spotify"]
SUBSCRIPTION_SERVICES = ["Netflix", "Amazon Prime", "Disney+", "Spotify", "YouTube Premium", "Apple Music", "HBO Max"]

# Data Generator
class DataGenerator:
    def __init__(self):
        self.search_history = []
        self.history_file = Path("search_history.json")

    async def load_history(self):
        if self.history_file.exists():
            async with aiofiles.open(self.history_file, "r") as f:
                content = await f.read()
                self.search_history = json.loads(content) if content else []

    async def save_history(self, data):
        self.search_history.append(data)
        async with aiofiles.open(self.history_file,"w") as f:
            await f.write(json.dumps(self.search_history,indent=2))

    def validate_phone_number(self, number):
        patterns = {
            'nepal': r'^\+977(?:-)?(?:98|97|96)\d{8}$',
            'india': r'^\+91(?:-)?[6-9]\d{9}$',
            'japan': r'^\+81(?:-)?[7890]\d{8,9}$'
        }
        for country, pat in patterns.items():
            if re.match(pat, number):
                return True,country
        return False,None

    def format_phone_number(self,number):
        return re.sub(r"[^\d+]","",number)

    async def generate_random_number(self,country=None):
        prefixes = {"nepal":["+97798","+97797","+97796"],"india":["+919","+918","+917"],"japan":["+8180","+8190","+8170"]}
        if not country: country=random.choice(list(prefixes.keys()))
        prefix=random.choice(prefixes[country])
        number=prefix+"".join([str(random.randint(0,9)) for _ in range(12-len(prefix))])
        return number,country

    async def generate_person_data(self,phone_number,country):
        gender=random.choice(["Male","Female"])
        age=random.randint(18,75)
        data={}
        
        # Basic Info
        first=random.choice(NAMES_DATA[country]['male'] if gender=="Male" else NAMES_DATA[country]['female'])
        last=random.choice(NAMES_DATA[country]['last'])
        dob=datetime.now()-timedelta(days=age*365+random.randint(0,364))
        
        data['basic_info']={
            "phone_number":phone_number,
            "full_name":f"{first} {last}",
            "first_name":first,
            "last_name":last,
            "gender":gender,
            "age":age,
            "date_of_birth":dob.strftime("%Y-%m-%d"),
            "country":country.capitalize(),
            "nationality":country.capitalize(),
            "marital_status":random.choice(MARITAL_STATUSES),
            "occupation":random.choice(OCCUPATIONS[country]),
            "education":random.choice(EDUCATION_LEVELS),
            "blood_group":random.choice(BLOOD_GROUPS)
        }
        
        # Contact Info
        data['contact_info']={
            "email":f"{first.lower()}.{last.lower()}{random.randint(10,99)}@example.com",
            "alt_email":f"{first.lower()}{random.randint(100,999)}@altmail.com",
            "address":f"{random.randint(1,999)} {random.choice(['Main', 'Oak', 'Maple', 'Pine'])} St",
            "city":random.choice(CITIES[country]),
            "state":random.choice(STATES[country]),
            "zip_code":"".join([str(random.randint(0,9)) for _ in range(6)]),
            "landline":f"+{random.randint(1,99)}{random.randint(1000000,9999999)}",
            "emergency_contact":f"+{random.randint(1,99)}{random.randint(1000000,9999999)}"
        }
        
        # Device Info
        device_model = random.choice(DEVICE_MODELS)
        os_version = random.choice(OS_VERSIONS)
        purchase_date = datetime.now() - timedelta(days=random.randint(30, 1000))
        
        data['device_info']={
            "imei":"".join([str(random.randint(0,9)) for _ in range(15)]),
            "imsi":"".join([str(random.randint(0,9)) for _ in range(15)]),
            "sim_serial":"".join([str(random.randint(0,9)) for _ in range(19)]),
            "device_model":device_model,
            "os_version":os_version,
            "mac_address":":".join(['%02x'%random.randint(0,255) for _ in range(6)]),
            "ip_address":f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}",
            "public_ip":f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}",
            "browser":random.choice(["Chrome", "Safari", "Firefox", "Edge"]),
            "user_agent":f"Mozilla/5.0 ({random.choice(['Windows NT 10.0', 'Macintosh; Intel Mac OS X 10_15_7', 'Linux x86_64'])})",
            "device_age":f"{(datetime.now() - purchase_date).days} days",
            "battery_health":f"{random.randint(70,100)}%",
            "storage_usage":f"{random.randint(20,95)}%",
            "ram":f"{random.choice(['4GB', '6GB', '8GB', '12GB'])}",
            "screen_time":f"{random.randint(2,12)} hours/day",
            "last_backup":(datetime.now() - timedelta(days=random.randint(1,30))).strftime("%Y-%m-%d"),
            "security_patch":(datetime.now() - timedelta(days=random.randint(1,90))).strftime("%Y-%m-%d")
        }
        
        # Network Info
        data['network_info']={
            "carrier":random.choice(CARRIERS_DATA[country]),
            "sim_type":random.choice(["Prepaid","Postpaid"]),
            "network_type":random.choice(NETWORK_TYPES),
            "signal_strength":f"{random.randint(-120,-60)} dBm",
            "data_speed":f"{random.randint(10,100)} Mbps",
            "network_quality":f"{random.randint(70,100)}%",
            "roaming":random.choice(["Enabled","Disabled"]),
            "recharge_date":(datetime.now() - timedelta(days=random.randint(1,30))).strftime("%Y-%m-%d"),
            "validity":f"{random.randint(1,90)} days"
        }
        
        # Financial Info
        data['financial_info']={
            "bank":random.choice(BANKS[country]),
            "account_number":"".join([str(random.randint(0,9)) for _ in range(12)]),
            "ifsc":"".join([chr(random.randint(65,90)) for _ in range(4)])+"0"+"".join([str(random.randint(0,9)) for _ in range(6)]),
            "credit_card":"".join([str(random.randint(0,9)) for _ in range(16)]),
            "card_expiry":f"{random.randint(1,12)}/{random.randint(23,30)}",
            "cvv":str(random.randint(100,999)),
            "upi":f"{first.lower()}.{last.lower()}@upi",
            "last_transaction":(datetime.now() - timedelta(days=random.randint(0,7))).strftime("%Y-%m-%d"),
            "wallet_balance":f"{random.choice(['$', '₹', '¥'])}{random.randint(10,5000)}",
            "credit_score":random.randint(600,850)
        }
        
        # Communication Info
        calls = []
        frequent_contacts = []
        
        for _ in range(random.randint(5,15)):
            contact_number = f"+{random.randint(1,99)}{random.randint(100000000,999999999)}"
            call_type = random.choice(["Incoming","Outgoing","Missed"])
            calls.append({
                "number": contact_number,
                "type": call_type,
                "duration": f"{random.randint(0,59)}m {random.randint(0,59)}s",
                "date": (datetime.now() - timedelta(days=random.randint(0,30))).strftime("%Y-%m-%d")
            })
            
            if random.random() > 0.7:  # 30% chance to be a frequent contact
                frequent_contacts.append(contact_number)
        
        blocked_numbers = [f"+{random.randint(1,99)}{random.randint(100000000,999999999)}" for _ in range(random.randint(0,3))]
        
        data['communication_info']={
            "call_history":calls,
            "total_calls":len(calls),
            "sms_count":random.randint(10,100),
            "data_usage":f"{random.randint(1,10)}GB",
            "spam_score":f"{random.randint(0,100)}%",
            "blocked_numbers": blocked_numbers,
            "frequent_contacts": list(set(frequent_contacts))[:5]  # Limit to 5 unique contacts
        }
        
        # Social Info
        username = f"{first.lower()}{last.lower()}{random.randint(1,99)}"
        
        data['social_info']={
            "facebook":f"facebook.com/{username}",
            "twitter":f"twitter.com/{username}",
            "instagram":f"instagram.com/{username}",
            "linkedin":f"linkedin.com/in/{username}",
            "tiktok":f"tiktok.com/@{username}",
            "whatsapp":random.choice(["Active","Inactive"]),
            "telegram":random.choice(["Online","Offline"]),
            "social_influence_score": random.randint(100,10000),
            "last_online": (datetime.now() - timedelta(minutes=random.randint(0,1440))).strftime("%H:%M"),
            "online_status": random.choice(["Active", "Idle", "Offline"])
        }
        
        # Misc Info
        data['misc_info']={
            "favorite_apps":random.sample(FAVORITE_APPS, random.randint(3,6)),
            "app_usage_hours": f"{random.randint(1,8)} hours/day",
            "location_services":random.choice(["Enabled","Disabled"]),
            "bluetooth_devices": [f"Device_{random.randint(1,5)}" for _ in range(random.randint(0,3))],
            "wifi_networks":[f"WiFi_{random.randint(100,999)}" for _ in range(random.randint(1,5))],
            "recent_searches": random.sample(["weather", "news", "restaurants near me", "how to cook", "movie tickets"], 3),
            "digital_footprint":random.randint(100,10000),
            "privacy_score": f"{random.randint(30,100)}%",
            "risk_level":random.choice(["Low","Medium","High"]),
            "verification_status":random.choice(["Verified","Unverified"]),
            "panic_button": random.choice(["Enabled", "Disabled"]),
            "nearby_contacts": [f"Contact_{random.randint(1,5)}" for _ in range(random.randint(0,5))],
            "gps_coordinates": f"{round(random.uniform(26.0, 28.0), 6)}, {round(random.uniform(84.0, 88.0), 6)}",
            "subscription_services": random.sample(SUBSCRIPTION_SERVICES, random.randint(0,3)),
            "browser_history_summary": random.sample(["news sites", "social media", "shopping", "entertainment", "educational"], 3),
            "installed_apps_count": random.randint(20,100),
            "deep_risk_score": f"{random.randint(0,100)}%"
        }
        
        return data

    async def display_results(self,data):
        print(Colors.BANNER+BANNER+Colors.RESET)
        print(f"{Colors.HEADER}=== TRUECALLER SIM RESULTS ==={Colors.RESET}\n")
        
        # Basic Info
        bi=data['basic_info']
        print(f"{Colors.CYAN}Full Name: {bi['full_name']} | Phone: {bi['phone_number']} | Age: {bi['age']} | Gender: {bi['gender']}{Colors.RESET}")
        print(f"{Colors.CYAN}Nationality: {bi['nationality']} | Marital Status: {bi['marital_status']} | Occupation: {bi['occupation']}{Colors.RESET}")
        print(f"{Colors.CYAN}Education: {bi['education']} | Blood Group: {bi['blood_group']}{Colors.RESET}")
        
        # Contact Info
        ci=data['contact_info']
        print(f"\n{Colors.GREEN}Email: {ci['email']} | Alt Email: {ci['alt_email']}{Colors.RESET}")
        print(f"{Colors.GREEN}Address: {ci['address']}, {ci['city']}, {ci['state']} {ci['zip_code']}{Colors.RESET}")
        print(f"{Colors.GREEN}Landline: {ci['landline']} | Emergency: {ci['emergency_contact']}{Colors.RESET}")
        
        # Device Info
        di=data['device_info']
        print(f"\n{Colors.MAGENTA}Device: {di['device_model']} | OS: {di['os_version']} | IMEI: {di['imei']}{Colors.RESET}")
        print(f"{Colors.MAGENTA}IP: {di['ip_address']} | Public IP: {di['public_ip']} | MAC: {di['mac_address']}{Colors.RESET}")
        print(f"{Colors.MAGENTA}Browser: {di['browser']} | User Agent: {di['user_agent']}{Colors.RESET}")
        print(f"{Colors.MAGENTA}Device Age: {di['device_age']} | Battery: {di['battery_health']} | Storage: {di['storage_usage']}{Colors.RESET}")
        print(f"{Colors.MAGENTA}RAM: {di['ram']} | Screen Time: {di['screen_time']} | Last Backup: {di['last_backup']}{Colors.RESET}")
        print(f"{Colors.MAGENTA}Security Patch: {di['security_patch']}{Colors.RESET}")
        
        # Network Info
        ni=data['network_info']
        print(f"\n{Colors.BLUE}Carrier: {ni['carrier']} | SIM Type: {ni['sim_type']} | Network: {ni['network_type']}{Colors.RESET}")
        print(f"{Colors.BLUE}Signal: {ni['signal_strength']} | Data Speed: {ni['data_speed']} | Quality: {ni['network_quality']}{Colors.RESET}")
        print(f"{Colors.BLUE}Roaming: {ni['roaming']} | Recharge Date: {ni['recharge_date']} | Validity: {ni['validity']}{Colors.RESET}")
        
        # Financial Info
        fi=data['financial_info']
        print(f"\n{Colors.YELLOW}Bank: {fi['bank']} | Account: {fi['account_number']} | IFSC: {fi['ifsc']}{Colors.RESET}")
        print(f"{Colors.YELLOW}Credit Card: {fi['credit_card']} | Expiry: {fi['card_expiry']} | CVV: {fi['cvv']}{Colors.RESET}")
        print(f"{Colors.YELLOW}UPI: {fi['upi']} | Last Transaction: {fi['last_transaction']}{Colors.RESET}")
        print(f"{Colors.YELLOW}Wallet Balance: {fi['wallet_balance']} | Credit Score: {fi['credit_score']}{Colors.RESET}")
        
        # Communication Info
        ci=data['communication_info']
        print(f"\n{Colors.WHITE}Total Calls: {ci['total_calls']} | SMS Count: {ci['sms_count']} | Data Usage: {ci['data_usage']}{Colors.RESET}")
        print(f"{Colors.WHITE}Spam Score: {ci['spam_score']} | Blocked Numbers: {len(ci['blocked_numbers'])} | Frequent Contacts: {len(ci['frequent_contacts'])}{Colors.RESET}")
        
        # Social Info
        si=data['social_info']
        print(f"\n{Colors.RED}FB: {si['facebook']} | Insta: {si['instagram']} | Twitter: {si['twitter']}{Colors.RESET}")
        print(f"{Colors.RED}LinkedIn: {si['linkedin']} | TikTok: {si['tiktok']}{Colors.RESET}")
        print(f"{Colors.RED}WhatsApp: {si['whatsapp']} | Telegram: {si['telegram']}{Colors.RESET}")
        print(f"{Colors.RED}Social Influence: {si['social_influence_score']} | Last Online: {si['last_online']} | Status: {si['online_status']}{Colors.RESET}")
        
        # Misc Info
        mi=data['misc_info']
        print(f"\n{Colors.CYAN}Favorite Apps: {', '.join(mi['favorite_apps'])} | App Usage: {mi['app_usage_hours']}{Colors.RESET}")
        print(f"{Colors.CYAN}Location Services: {mi['location_services']} | Bluetooth Devices: {len(mi['bluetooth_devices'])}{Colors.RESET}")
        print(f"{Colors.CYAN}WiFi Networks: {len(mi['wifi_networks'])} | Recent Searches: {', '.join(mi['recent_searches'])}{Colors.RESET}")
        print(f"{Colors.CYAN}Digital Footprint: {mi['digital_footprint']} | Privacy Score: {mi['privacy_score']}{Colors.RESET}")
        print(f"{Colors.CYAN}Risk Level: {mi['risk_level']} | Verification: {mi['verification_status']}{Colors.RESET}")
        print(f"{Colors.CYAN}Panic Button: {mi['panic_button']} | Nearby Contacts: {len(mi['nearby_contacts'])}{Colors.RESET}")
        print(f"{Colors.CYAN}GPS: {mi['gps_coordinates']} | Subscriptions: {', '.join(mi['subscription_services'])}{Colors.RESET}")
        print(f"{Colors.CYAN}Browser History: {', '.join(mi['browser_history_summary'])} | Installed Apps: {mi['installed_apps_count']}{Colors.RESET}")
        print(f"{Colors.CYAN}Deep Risk Score: {mi['deep_risk_score']}{Colors.RESET}")
        
        print("\n"+Colors.HEADER+"=== END OF SIMULATION ==="+Colors.RESET)

# Main
async def main():
    dg=DataGenerator()
    await dg.load_history()
    print(Colors.BANNER+BANNER+Colors.RESET)
    choice=input(f"{Colors.INFO}Enter phone number (or leave empty to generate random): {Colors.RESET}")
    if not choice:
        phone,country=await dg.generate_random_number()
    else:
        phone=dg.format_phone_number(choice)
        valid,country=dg.validate_phone_number(phone)
        if not valid:
            print(Colors.ERROR+"Invalid phone number format! Generating random number instead."+Colors.RESET)
            phone,country=await dg.generate_random_number()
    data=await dg.generate_person_data(phone,country)
    await dg.display_results(data)
    await dg.save_history(data)

if __name__=="__main__":
    asyncio.run(main())