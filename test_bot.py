import requests
import os

# 🛑 APNI DETAILS YAHAN DAALO (Bina kisi space ke)
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "REPLACE_ME")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "REPLACE_ME")

def test_telegram():
    print(f"Testing Bot Token: {TELEGRAM_BOT_TOKEN[:10]}...")
    print(f"Testing Chat ID: {TELEGRAM_CHAT_ID}")
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": "🚨 BHAUKAAL ALERT: System is working perfectly!"
    }
    
    try:
        response = requests.post(url, json=payload)
        print(f"\n--- RESULTS ---")
        print(f"Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")
        
        if response.status_code == 200:
            print("✅ SUCCESS! Message sent to your phone.")
        elif response.status_code == 401:
            print("❌ ERROR 401: Tumhara BOT_TOKEN galat hai. (BotFather se dobara copy karo)")
        elif response.status_code == 400:
            print("❌ ERROR 400: Tumhari CHAT_ID galat hai ya tumne bot ko '/start' nahi bheja hai.")
        else:
            print("❌ UNKNOWN ERROR. Check response text above.")
            
    except Exception as e:
        print(f"❌ NETWORK ERROR: {e}")

if __name__ == "__main__":
    test_telegram()