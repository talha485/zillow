# test_zillow_api.py
import requests, json
url = "https://www.zillow.com/async-create-search-page-state"
headers = {
  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) ... Chrome/132",
  "Accept": "*/*",
  "Content-Type": "application/json",
  "Referer": "https://www.zillow.com/homes/for_sale/"
}
payload = {
  "searchQueryState": {
    "pagination": {"currentPage": 1},
    "isMapVisible": False,
    "mapBounds": {"west": -119.1,"east": -117.6,"south": 33.6,"north": 34.5},
    "mapZoom": 10,
    "filterState": {},
    "isListVisible": True
  },
  "wants":{"cat1":["listResults"],"cat2":["total"]},
  "requestId": 1, "isDebugRequest": False
}
r = requests.put(url, headers=headers, json=payload, timeout=30)
print(r.status_code, len(r.json().get("cat1",{}).get("searchResults",{}).get("listResults",[])))
