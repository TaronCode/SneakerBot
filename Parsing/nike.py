import requests
import json

class NikeParse:
    def __init__(self):
        self.prodList = []
    def get_data(self, url="https://api.nike.com/product_feed/rollup_threads/v2?filter=marketplace%28US%29&filter=language%28en%29&filter=employeePrice%28true%29&filter=attributeIds%280f64ecc7-d624-4e91-b171-b83a03dd8550%2C16633190-45e5-4830-a068-232ac7aea82c%2C5b21a62a-0503-400c-8336-3ccfbff2a684%2C193af413-39b0-4d7e-ae34-558821381d3f%29&anchor=0&consumerChannelId=d9a5bc42-4b9c-4976-858a-f159cf99c647&count=24"):
        s = requests.Session()
        res = s.get(url)
        self.data = res.json()
        self.collect_data()
    def collect_data(self):

        next_pg = self.data["pages"]["next"]
        length = len(self.data["objects"])

        for prod in range(length):
            link = "https://www.nike.com/t/"
            price = self.data["objects"][prod]["productInfo"][0]["merchPrice"]["fullPrice"]
            salePrice  = self.data["objects"][prod]["productInfo"][0]["merchPrice"]["currentPrice"]
            title = self.data["objects"][prod]["productInfo"][0]["productContent"]["title"]
            slug = self.data["objects"][prod]["productInfo"][0]["productContent"]["slug"]
            styleColor = self.data["objects"][prod]["productInfo"][0]["merchProduct"]["styleColor"]

            link = link + slug + "/" + styleColor

            self.prodList.append({
                "title" : title,
                "previous price" : price,
                "total price" : salePrice,
                "sale" : str(round(((price - salePrice)/price) * 100)) + "%",
                "link" : link
            })
        if len(next_pg) != 0:
            self.get_data(url="https://api.nike.com" + next_pg)


        with open("nike_result.json", "w", encoding="utf-8") as file:
            json.dump(self.prodList, file, indent=4, ensure_ascii=False)


parserNike = NikeParse()
parserNike.get_data()
