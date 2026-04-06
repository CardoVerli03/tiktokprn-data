import requests
import re
import json
import os
import time
import random

ACCOUNTS_FILE = 'accounts.txt'
DATABASE_FILE = 'database.json'
SMARTLINK = "https://thoroughgear.com/k3FiUr"

# Mazingira ya Nitter (Tunaongeza mengi zaidi)
INSTANCES = [
    "https://nitter.net", 
    "https://nitter.unixfox.eu",
    "https://nitter.privacydev.net",
    "https://nitter.it",
    "https://nitter.projectsegfau.lt"
]

def scrape():
    if not os.path.exists(ACCOUNTS_FILE): return
    with open(ACCOUNTS_FILE, 'r') as f:
        accounts = [l.strip() for l in f if l.strip()]

    db = []
    if os.path.exists(DATABASE_FILE) and os.stat(DATABASE_FILE).st_size > 5:
        with open(DATABASE_FILE, 'r') as f:
            try: db = json.load(f)
            except: db = []

    existing_ids = {str(item['id']) for item in db}
    new_added = 0

    for user in accounts:
        # Chagua instance tofauti kila mara
        base_url = random.choice(INSTANCES)
        print(f"Vizia @{user} kupitia {base_url}...")
        
        try:
            # Tunatumia /rss kwa sababu haina ulinzi wa JavaScript
            url = f"{base_url}/{user}/rss"
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Edge/91.0.864.59'}
            
            response = requests.get(url, headers=headers, timeout=20)
            if response.status_code != 200:
                print(f"Zingua! {base_url} imekataa (Status: {response.status_code})")
                continue

            # Tafuta IDs za tweets (Zipo kwenye <link> tags za RSS)
            ids = re.findall(r'status/(\d+)', response.text)
            
            for t_id in list(set(ids)):
                if t_id not in existing_ids:
                    db.append({
                        "id": t_id,
                        "url": f"https://platform.twitter.com/embed/Tweet.html?id={t_id}",
                        "thumb": f"https://pbs.twimg.com/media/placeholder.jpg",
                        "source": user,
                        "likes": f"{random.randint(10, 95)}K",
                        "ad_link": SMARTLINK
                    })
                    existing_ids.add(t_id)
                    new_added += 1
            
            # PUMZIKA KIDOGO (Siri ya kutopigwa block)
            time.sleep(random.randint(2, 5))

        except Exception as e:
            print(f"Error kwa @{user}: {e}")

    if new_added > 0:
        with open(DATABASE_FILE, 'w') as f:
            json.dump(db, f, indent=4)
        print(f"DONE! Tumeiba video {new_added} mpya.")
    else:
        print("Bado kiza! Jaribu kuongeza akaunti zaidi kwenye accounts.txt")

if __name__ == "__main__":
    scrape()
