import scrapy
import json


class ZillowSpider(scrapy.Spider):
    name = "zillow"
    allowed_domains = ["zillow.com"]

    # Your cookies
    cookies = {
        "zguid": "24|%241c7c7415-9068-4626-82d9-292c747e57ba",
        "zjs_anonymous_id": "1c7c7415-9068-4626-82d9-292c747e57ba",
        "zjs_user_id": "null",
        "_ga": "GA1.2.910916406.1759525592",
        "_gid": "GA1.2.1199002895.1759525592",
        "pxcts": "d68b4aee-a09c-11f0-b96e-452d411220fa",
        "_pxvid": "d68b4294-a09c-11f0-b96e-aac88f2b553e",
        "AWSALB": "jND3/o0FTVFX4ciT4kjRH++eCF6PVHEWdLLspGkuqf3PJ05zQbHdm+PKUvQW4JWlatfh0BM8briUiBnnGBdkZHXj2aEaEg/pJbvInqhAu9PXiieqUJT33F17Ne95",
        "AWSALBCORS": "jND3/o0FTVFX4ciT4kjRH++eCF6PVHEWdLLspGkuqf3PJ05zQbHdm+PKUvQW4JWlatfh0BM8briUiBnnGBdkZHXj2aEaEg/pJbvInqhAu9PXiieqUJT33F17Ne95",
        "_px3": "1ef9ea4cb2de42b20cff841fffac7141053f83263bf1a300d3fe00c366e128b1:3jhPsm+3L5+/eVZSqixT1J13gmeL6WR/Kgdr/DFgSeozuK25PnG7wVI2uFlFvASiDCsMqZRj+HWm0Gm/TBopDQ==:1000:lbS+cbcLlqe0aoXQE0TcMoc2qTe+RsGOfmOdndhddO4WXk1uuNSbjyHg91O1uojVTVzGAjDC/vMUOpBs8NL+NL1oXWDD98zny9XtBB6e7pgwd2K6eKmiDRp7TGbL3QsdLH6sKHA+wAizbISb3WZ7NXB/+musqPYhrCjdkoZjS7bN7LRhVCFcrcozrQAVFEoHa4VXsiQ/LPEeUe+NcX44Wy8md+opqz5AWR5DSJpCBsI="
    }

    def start_requests(self):
        url = "https://www.zillow.com/async-create-search-page-state"

        # PUT request payload for a city (Los Angeles)
        payload = {
            "searchQueryState": {
                "pagination": {"currentPage": 1},
                "usersSearchTerm": "Los Angeles, CA",
                "mapBounds": {
                    "west": -119.1,
                    "east": -117.6,
                    "south": 33.6,
                    "north": 34.5
                },
                "isMapVisible": True,
                "filterState": {},
                "isListVisible": True
            },
            "wants": {"cat1": ["listResults", "mapResults"]},
            "requestId": 1
        }

        yield scrapy.Request(
            url=url,
            method="PUT",
            cookies=self.cookies,
            headers={
                "User-Agent": self.settings.get('USER_AGENT'),
                "Content-Type": "application/json",
            },
            body=json.dumps(payload),
            callback=self.parse
        )

    def parse(self, response):
        try:
            data = json.loads(response.text)
            # Extract properties list
            properties = data.get("cat1", {}).get("searchResults", {}).get("listResults", [])

            for prop in properties:
                yield {
                    "address": prop.get("address"),
                    "price": prop.get("unformattedPrice"),
                    "beds": prop.get("beds"),
                    "baths": prop.get("baths"),
                    "area": prop.get("area"),
                    "zpid": prop.get("zpid"),
                    "statusType": prop.get("statusType"),
                    "statusText": prop.get("statusText")
                }
        except Exception as e:
            self.logger.error(f"Failed to parse JSON: {e}")
