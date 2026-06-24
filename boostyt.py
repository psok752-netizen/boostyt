import time
import random
import threading
import requests  
import undetected_chromedriver as uc
import os

driver_lock = threading.Lock()

def watch_video_thread(thread_id, video_url, agent, proxy):
    print(f"🚀 [Thread {thread_id}] ចាប់ផ្តើមដំណើរការជាមួយ IP: {proxy}")
    
    options = uc.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--mute-audio")
    options.add_argument(f"user-agent={agent}")
    options.add_argument(f"--proxy-server=http://{proxy}")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    if os.name == 'nt': 
        options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    
    driver = None
    try:
        with driver_lock:
            print(f"🛠️ [Thread {thread_id}] កំពុងរៀបចំ និងបើក Browser...")
            
            # 💡 ដំណោះស្រាយ៖ បង្ខំឱ្យវាប្រើជំនាន់ ១៤៩ ទាំងនៅលើ Linux និង Windows
            if os.name != 'nt':
                driver = uc.Chrome(options=options, version_main=149)
            else:
                driver = uc.Chrome(options=options)
                
            time.sleep(2)
            
        driver.set_page_load_timeout(35)
        driver.get(video_url)
        
        watch_time = random.randint(15, 25)
        print(f"📺 [Thread {thread_id}] កំពុងមើលវីដេអូ រង់ចាំ {watch_time} វិនាទី...")
        time.sleep(watch_time)
        
        print(f"✅ [Thread {thread_id}] បញ្ចប់ការងារដោយជោគជ័យ!")
        
    except Exception as e:
        print(f"⚠️ [Thread {thread_id}] មានបញ្ហា៖ {e}")
        
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass

def get_live_proxies_fast_api(limit=3):
    print("\n🌐 កំពុងទាក់ទងទៅ Proxyscrape API ដើម្បីទាញយក Proxy ថ្មីៗល្បឿនលឿន...")
    api_url = f"https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all"
    try:
        response = requests.get(api_url, timeout=30)
        all_proxies = response.text.strip().split("\r\n")
        fetched_proxies = random.sample(all_proxies, limit) if len(all_proxies) >= limit else all_proxies[:limit]
        return fetched_proxies
    except Exception as e:
        print(f"❌ មិនអាចទាញយក Proxy បានទេ៖ {e}")
        return []

# ==================== ដំណើរការកម្មវិធីមេ ====================
if __name__ == "__main__":
    target_video = "https://youtu.be/YuWlVPwXnsc?si=GSbYei3r7sda1yKF"
    total_threads = 3  
    round_count = 1  

    user_agents_pool = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Mozilla/5.0 (Linux; Android 13; SM-S901B) AppleWebKit/537.36"
    ]

    max_rounds = 10 
    while round_count <= max_rounds:
        print(f"\n⚡🔄⚡ ================== ចាប់ផ្តើមរត់ AUTO ជុំទី {round_count}/{max_rounds} ================== ⚡🔄⚡")
        
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

            print(f"\n🎉 ជុំទី {round_count} ត្រូវបានបញ្ចប់សព្វគ្រប់!")
            round_count += 1  
            
            time.sleep(10)
        else:
            print("❌ គ្មានទិន្នន័យ Proxy ទេ! រង់ចាំ ៣០ វិនាទី...")
            time.sleep(30)
