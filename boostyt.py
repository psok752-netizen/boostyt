import time
import random
import threading
import requests  
import undetected_chromedriver as uc

driver_lock = threading.Lock()

def watch_video_thread(thread_id, video_url, agent, proxy):
    print(f"🚀 [Thread {thread_id}] ចាប់ផ្តើមដំណើរការជាមួយ IP: {proxy}")
    
    options = uc.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--mute-audio")
    options.add_argument(f"user-agent={agent}")
    options.add_argument(f"--proxy-server=http://{proxy}")
    options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    
    driver = None
    try:
        with driver_lock:
            print(f"🛠️ [Thread {thread_id}] កំពុងរៀបចំ និងបើក Browser...")
            driver = uc.Chrome(options=options, version_main=149)
            time.sleep(2)
            
        driver.set_page_load_timeout(35)
        driver.get(video_url)
        
        watch_time = random.randint(60, 120)
        print(f"📺 [Thread {thread_id}] កំពុងមើលវីដេអូ រង់ចាំ {watch_time} វិនាទី...")
        time.sleep(watch_time)
        
        print(f"✅ [Thread {thread_id}] បញ្ចប់ការងារដោយជោគជ័យ!")
        
    except Exception as e:
        print(f"⚠️ [Thread {thread_id}] មានបញ្ហា (Proxy ដើរយឺត/ងាប់)៖ {e}")
        
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass

def get_live_proxies_fast_api(limit=5):
    print("\n🌐 កំពុងទាក់ទងទៅ Proxyscrape API ដើម្បីទាញយក Proxy ថ្មីៗល្បឿនលឿន...")
    api_url = f"https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all"
    try:
        response = requests.get(api_url, timeout=30)
        all_proxies = response.text.strip().split("\r\n")
        # ប្រើ random.sample ដើម្បីចាប់យក IP ចម្រុះគ្នាដោយចៃដន្យរាល់ពេល Loop
        fetched_proxies = random.sample(all_proxies, limit) if len(all_proxies) >= limit else all_proxies[:limit]
        return fetched_proxies
    except Exception as e:
        print(f"❌ មិនអាចទាញយក Proxy បានទេ៖ {e}")
        return []

# ==================== ដំណើរការកម្មវិធីមេ (AUTO-RUN LOOP) ====================
if __name__ == "__main__":
    target_video = "https://youtu.be/5eW-Q0FkXXA?si=e9oEMuJhNuiD5RIl"
    total_threads = 5  
    round_count = 1  # បង្កើតកម្មវិធីរាប់ជុំ

    user_agents_pool = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-S901B) AppleWebKit/537.36",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124.0.6367.91 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/605.1.15 Version/17.5 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 Version/17.5 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_5 like Mac OS X) AppleWebKit/605.1.15 Version/17.5 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 Chrome/125.0.6422.113 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:126.0) Gecko/20100101 Firefox/126.0"
]

    # 🔥 ប្រើ while True ដើម្បីឱ្យវា Run Auto មិនចេះចប់
    while True:
        print(f"\n⚡🔄⚡ ================== ចាប់ផ្តើមរត់ AUTO ជុំទី {round_count} ================== ⚡🔄⚡")
        
        proxies_pool = get_live_proxies_fast_api(limit=total_threads)
        
        if proxies_pool and proxies_pool[0] != "":
            print(f"🎯 ទទួលបាន {len(proxies_pool)} Proxies សម្រាប់ជុំនេះ: {proxies_pool}")
            threads_list = []

            for i in range(len(proxies_pool)):
                t = threading.Thread(
                    target=watch_video_thread, 
                    args=(i+1, target_video, user_agents_pool[i % len(user_agents_pool)], proxies_pool[i])
                )
                threads_list.append(t)
                t.start()

            for t in threads_list:
                t.join()

            print(f"\n🎉 [មេកង] ជុំទី {round_count} ត្រូវបានបញ្ចប់សព្វគ្រប់!")
            round_count += 1  # ឡើងជុំបន្ទាប់
            
            # សម្រាក ១០ វិនាទី សន្សំកម្លាំងម៉ាស៊ីន RAM មុននឹងបុកជុំថ្មី
            print("⏳ សម្រាក ១០ វិនាទី មុននឹងចាប់ផ្តើមជុំបន្ទាប់...")
            time.sleep(10)
        else:
            print("❌ គ្មានទិន្នន័យ Proxy ទេ! រង់ចាំ ៣០ វិនាទី រួចសាកល្បងទៅបឺតយកម្តងទៀត...")
            time.sleep(30)
