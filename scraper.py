import requests
import json
import os
import re

ACCOUNTS_FILE = 'accounts.txt'
DATABASE_FILE = 'database.json'
SMARTLINK = "https://thoroughgear.com/k3FiUr"

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

    # Ninja Headers - Kujifanya iPhone
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1',
        'Accept': 'application/json',
        'Referer': 'https://twitter.com/'
    }

    for user in accounts:
        print(f"Checking: @{user}")
        try:
            # Tunatumia Public API ya Syndication (Hii haihitaji Login)
            api_url = f"https://syndication.twitter.com/srv/timeline-profile/screen-name/{user}"
            res = requests.get(api_url, headers=headers)
            
            # Tafuta IDs za Tweets kwenye HTML (Mbinu ya kienyeji lakini inafanya kazi)
            html_content = res.text
            tweet_ids = re.findall(r'tweet-(\d+)', html_content)
            
            for t_id in list(set(tweet_ids)):
                if t_id not in existing_ids:
                    # Tunatengeneza Embed URL ambayo ndio video yenyewe
                    # X inaruhusu embed links bila ulinzi mkali
                    video_embed = f"https://platform.twitter.com/embed/Tweet.html?id={t_id}"
                    
                    db.append({
                        "id": t_id,
                        "url": video_embed,
                        "thumb": f"https://pbs.twimg.com/media/dummy_{t_id}.jpg", # Thumbnail itajijaza yenyewe ikicheza
                        "source": user,
                        "likes": f"{os.urandom(1)[0] % 50 + 1}.{os.urandom(1)[0] % 9}K",
                        "ad_link": SMARTLINK
                    })
                    existing_ids.add(t_id)
                    new_added += 1
        except Exception as e:
            print(f"Error on {user}: {e}")

    if new_added > 0:
        save_db(db)
        print(f"Safi! Tumeiba video {new_added} mpya.")
    else:
        print("Bado mkavu! X wamefunga mlango. Tutajaribu njia nyingine.")

if __name__ == "__main__":
    scrape()
