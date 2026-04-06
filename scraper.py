import requests
import json
import os
import re
import random

ACCOUNTS_FILE = 'accounts.txt'
DATABASE_FILE = 'database.json'
SMARTLINK = "https://thoroughgear.com/k3FiUr"

# List ya Nitter Instances (Tuna-rotate ili tusinaswe)
NITTER_INSTANCES = [
    "https://nitter.net",
    "https://nitter.cz",
    "https://nitter.privacydev.net",
    "https://nitter.it"
]

def get_accounts():
    if not os.path.exists(ACCOUNTS_FILE): return []
    with open(ACCOUNTS_FILE, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def load_db():
    if not os.path.exists(DATABASE_FILE) or os.stat(DATABASE_FILE).st_size < 5: return []
    with open(DATABASE_FILE, 'r') as f:
        try: return json.load(f)
        except: return []

def save_db(data):
    with open(DATABASE_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def scrape():
    accounts = get_accounts()
    db = load_db()
    existing_ids = {str(item['id']) for item in db if 'id' in item}
    new_added = 0
    
    instance = random.choice(NITTER_INSTANCES)

    for user in accounts:
        print(f"Ninja anavizia: @{user} kupitia {instance}")
        try:
            # RSS Feed ya Nitter ni rahisi kuisoma na haina ulinzi
            api_url = f"{instance}/{user}/rss"
            res = requests.get(api_url, timeout=15)
            
            # Tunatafuta Tweet IDs kwenye RSS feed
            # Link huwa inafanana na: instance/user/status/123456789#m
            tweet_ids = re.findall(r'status/(\實+)', res.text)
            
            if not tweet_ids:
                # Jaribu mbinu nyingine ya ID search
                tweet_ids = re.findall(r'status/(\d+)', res.text)

            for t_id in list(set(tweet_ids)):
                if t_id not in existing_ids:
                    # Tunatengeneza Video Embed (Hii itafanya kazi kwenye site yako)
                    # Tunatumia 'video-player.twimg.com' logic au Embed
                    db.append({
                        "id": t_id,
                        "url": f"https://platform.twitter.com/embed/Tweet.html?id={t_id}",
                        "thumb": f"https://nitter.net/pic/media%2Fplaceholder.jpg",
                        "source": user,
                        "likes": f"{random.randint(10, 99)}.{random.randint(1, 9)}K",
                        "ad_link": SMARTLINK
                    })
                    existing_ids.add(t_id)
                    new_added += 1
        except Exception as e:
            print(f"Instance {instance} imegoma kwa {user}: {e}")
            continue

    if new_added > 0:
        save_db(db)
        print(f"Oyaa! Tumeongeza video {new_added} mpya.")
    else:
        print("Bado kiza kinene! Nitter instances zinaweza kuwa zimelemewa.")

if __name__ == "__main__":
    scrape()
