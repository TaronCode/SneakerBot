import requests
import json

class ReebokParse:
    def __init__(self):
        self.prodList = []
        self.headers = {
            "accept": "*/*",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36"
        }

    def get_data(self, url):
        s = requests.Session()
        res = s.get(url, headers=self.headers)
        self.data = res.json()
        self.collect_data()

    def collect_data(self):
        length = len(self.data["raw"]["itemList"]["items"])

        for self.prod in range(length):
            link = "https://www.reebok.com"
            price, salePrice = self.get_prices()
            title = self.data["raw"]["itemList"]["items"][self.prod]["displayName"]
            slug = self.data["raw"]["itemList"]["items"][self.prod]["link"]

            link = link + slug

            self.prodList.append({
                "title": title,
                "previous price": price,
                "total price": salePrice,
                "sale": str(round(((price - salePrice) / price) * 100)) + "%",
                "link": link
            })

        with open("reebok_results.json", "w", encoding="utf-8") as file:
            json.dump(self.prodList, file, indent=4, ensure_ascii=False)
        self.prodList.clear()

    def get_prices(self):
        id = self.data["raw"]["itemList"]["items"][self.prod]["productId"]
        sess = requests.Session()
        price_info = sess.get("https://www.reebok.com/api/search/product/" + id + "?sitePath=us", headers=self.headers)
        price_data = price_info.json()

        price = price_data["price"]
        salePrice = price_data["salePrice"]

        return price, salePrice

reebok_parser = ReebokParse()

