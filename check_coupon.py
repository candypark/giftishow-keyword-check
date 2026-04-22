import requests
import json

url = "https://biz.giftishow.com/fo_api/main/searchGGoods"
headers = {"Content-Type": "application/json"}

payload = {
    "start": "1",
    "size": "20",
    "searchWord": "커피",
    "lineUp": "popular"
}

resp = requests.post(url, json=payload, headers=headers, timeout=10)
print("상태코드:", resp.status_code)
print(json.dumps(resp.json(), ensure_ascii=False, indent=2))
