import requests
import json
import os
import openpyxl

url = "https://biz.giftishow.com/fo_api/main/searchGGoods"

headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
    "Origin": "https://biz.giftishow.com",
    "Referer": "https://biz.giftishow.com/search?searchWord=%EC%BB%A4%ED%94%BC",
    "cookie": os.environ.get("GIFTISHOW_COOKIE", "")
}

with open("keywords.txt", "r", encoding="utf-8") as f:
    keywords = [line.strip() for line in f if line.strip()]

# 첫 번째 키워드 응답 구조 확인용 출력
test_payload = {"start": "1", "size": "20", "searchWord": keywords[0], "lineUp": "popular"}
test_resp = requests.post(url, json=test_payload, headers=headers, timeout=10)
print("=== 응답 구조 확인 (첫 번째 키워드) ===")
print(json.dumps(test_resp.json(), ensure_ascii=False, indent=2)[:2000])

# 전체 키워드 처리
wb = openpyxl.Workbook()
ws = wb.active
ws.append(["키워드", "쿠폰 결과 여부", "결과 수"])

for kw in keywords:
    try:
        payload = {"start": "1", "size": "20", "searchWord": kw, "lineUp": "popular"}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        data = resp.json()

        # 응답 구조에 따라 아래 키 조정 필요
        result_list = data.get("list") or data.get("data", {}).get("list") or []
        count = len(result_list)
        has_result = "있음" if count > 0 else "없음"
        ws.append([kw, has_result, count])
        print(f"{kw}: {has_result} ({count}개)")

    except Exception as e:
        ws.append([kw, "오류", str(e)])
        print(f"{kw}: 오류 - {e}")

wb.save("result.xlsx")
print("완료: result.xlsx 저장됨")
