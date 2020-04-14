import requests
res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "p7Dxr8S6FUbkd5NEI0lmqQ", "isbns": "9781632168146"})
print(res.json())