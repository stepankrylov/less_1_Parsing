import requests
import json

url_cat = "https://5ka.ru/api/v2/categories/"
url_2_spec_off = "https://5ka.ru/api/v2/special_offers/"


class Parser:
    def __init__(self, url_1, url_2):
        self.url_1 = url_1
        self.url_2 = url_2

    @staticmethod
    def generator(url):
        req_2 = requests.get(url)
        data_2 = json.loads(req_2.text)
        for item in data_2:
            yield item["parent_group_code"], item["parent_group_name"]

    @staticmethod
    def product(url, x):
        prod_data = []
        par = {
            "records_per_page": "12",
            "page": "1",
            "categories": x,
        }
        name_data = []
        while True:
            req = requests.get(url, params=par)
            data = json.loads(req.text)
            prod_data += data['results']
            par["page"] = str(int(par["page"]) + 1)
            if len(data['results']) != 0:
                for i in data['results']:
                    name_data.append(i['name'])
            if not data['next']:
                break
        return name_data

    def extractor(self):
        for q in Parser.generator(self.url_1):
            wr_data = {'name': q[1], 'code': q[0], 'product': Parser.product(self.url_2, q[0])}
            json_Data = json.dumps(wr_data, ensure_ascii=False, sort_keys=True, indent=4)
            with open(f"data_{q[0]}_{q[1]}.json", "w", encoding='utf-8') as file:
                file.write(json_Data)
            print(q)


c = Parser(url_cat, url_2_spec_off)
a = c.extractor()



