import requests
import os

# 🛑 यहाँ अपनी एकदम नई वाली API Key डालना (पुरानी वाली नहीं!)
API_KEY = os.environ.get("GOOGLE_API_KEY", "REPLACE_ME")

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
headers = {'Content-Type': 'application/json'}
data = {
    "contents": [{"parts": [{"text": "Hello, answer in 1 word."}]}]
}

print("Google के सर्वर पर डायरेक्ट रिक्वेस्ट जा रही है...")
response = requests.post(url, headers=headers, json=data)

print("Status Code:", response.status_code)
print("Response:", response.text)
