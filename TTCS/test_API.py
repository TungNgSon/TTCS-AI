import requests

# Nhập API key của bạn
API_KEY = ""  # Thay bằng API key của bạn

url = "https://api.together.xyz/v1/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

data = {
    "model": "mistralai/Mistral-7B-Instruct-v0.1",  # Model miễn phí của Together AI
    "prompt": "tell me where is wrong in this sentence: ' '? Answer in one sentence.",
    "max_tokens": 200
}

response = requests.post(url, headers=headers, json=data)

if response.status_code == 200:
    print(response.json()["choices"][0]["text"])
else:
    print("Lỗi:", response.text)
