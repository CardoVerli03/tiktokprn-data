import requests
import re
import json
import os

# 1. Mpangilio wa Mafaili
ACCOUNTS_FILE = 'accounts.txt'
DATABASE_FILE = 'database.json'
SMARTLINK = "https://thoroughgear.com/k3FiUr"

def get_accounts():
    if not os.path.exists(ACCOUNTS_FILE):
        return []
    with open(ACCOUNTS_FILE, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def load_database():
    if not os.path.exists(DATABASE_FILE) or os.stat(DATABASE_FILE).st_size == 0:
        return []
    with open(DATABASE_FILE, 'r') as f:
        try:
            return json.load(f)
        except:
            return []

def save_database(data):
    with open(DATABASE_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def scrape_x_videos():
    accounts = get_accounts()
    database = load_database()
    
    # Tengeneza seti ya ID zilizopo ili kuzuia duplicates kwa haraka
    existing_ids = {item['id'] for item in database if 'id' in item}
    new_entries = 0

    print(f"Oya, naanza ujangili kwenye accounts {len(accounts)}...")

    for username in accounts:
        print(f"Niko kwa huyu ninja: @{username}")
        
        # Mbinu ya kunusa (Hapa tunatumia Search API ya X ya mchongo au NFX)
        # Kwa ajili ya usalama wa GitHub, tunatumia nfx-proxy au mbinu ya Guest
        search_url = f"https://api.nfx.com/v1/x/user/{username}/videos" # Mfano wa endpoint
        
        try:
            # Kumbuka: Kwenye ulimwengu wa kweli, X inahitaji headers kidogo
            # Hapa script itatumia requests kuvuta data ya JSON ya tweets
            # (Hii ni logic iliyorahisishwa, nimeiweka iwe ngumu kufeli)
            
            # GI-HACK: Tunapata video clips kupitia API ya wazi
            response = requests.get(f"https://x-scraper-api.vercel.app/api/user/{username}") 
            tweets = response.json().get('tweets', [])

            for tweet in tweets:
                v_id = tweet.get('id')
                v_url = tweet.get('video_url')
                v_thumb = tweet.get('thumbnail')

                # SHERIA: Link ikiwa tayari ipo,ipuuzie (No Duplicates)
                if v_id and v_id not in existing_ids and v_url:
                    new_item = {
                        "id": v_id,
                        "url": v_url,
                        "thumb": v_thumb,
                        "source": username,
                        "likes": f"{round(os.urandom(1)[0]/2, 1)}K", # Fake Likes Generator
                        "ad_link": SMARTLINK
                    }
                    database.append(new_item)
                    existing_ids.add(v_id)
                    new_entries += 1
        
        except Exception as e:
            print(f"Aisee, @{username} amezingua kidogo: {e}")
            continue

    if new_entries > 0:
        save_database(database)
        print(f"Ujangili Done! Tumevuta video mpya {new_entries}. Total sasa: {len(database)}")
    else:
        print("Hakuna kipya mwanangu, tunasubiri saa linalofuata.")

if __name__ == "__main__":
    scrape_x_videos()
