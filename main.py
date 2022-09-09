import requests
from bs4 import BeautifulSoup
import json
import os
import matplotlib.pyplot as plt
from pyecharts.charts import Map
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0'
}
downloading_img = True

class Crawler:
    def __init__(self):
        self.url = ""
        self.results = {}
        self.num = {}

    def get_res(self):
        res = requests.get(self.url)
        with open('webdata.html', 'w', encoding='utf-8') as c:
            c.write(res.text)
        self.soup = BeautifulSoup(res.text, "lxml")

    def get_inf(self):
        jsonobj = json.loads(self.soup.find('script', id="__NEXT_DATA__").string)['props']['pageProps']['storeList'][0][
            'state']
        for item in jsonobj:
            self.num[item['name']] = len(item['store'])
            print('\n' + item['name']+' 门店数量:{}'.format(self.num[item['name']]))
            for itemt in item['store']:
                if itemt['address']['address2'] != '':
                    print('地区:{} , 地址1:{} , 地址2:{} , 电话:{} , 邮编:{}'.format(itemt['name'], itemt['address']['address1'],
                                                                           itemt['address']['address2'],
                                                                           itemt['telephone'],
                                                                           itemt['address']['postalCode']))
                else:
                    print('地区:{} , 地址1:{} , 电话:{} , 邮编:{}'.format(itemt['name'], itemt['address']['address1'],
                                                                  itemt['telephone'], itemt['address']['postalCode']))
                pass

                if downloading_img:
                    imgs = requests.get(
                        'https://rtlimages.apple.com/cmc/dieter/store/16_9/'
                        '{}.png?resize=1440:806&output-format=jpg&output-quality=85&interpolation=progressive-bicubic'
                        .format(itemt['id']),

                        headers=headers)
                    if not os.path.exists('./image/{}'.format(item['name'])):
                        os.makedirs('./image/{}'.format(item['name']))
                    with open('./image/{}/{}{}.png'.format(item['name'], itemt['address']['address1'],
                                                           itemt['address']['address2']), 'wb') as f:
                        f.write(imgs.content)

    def draw_plot(self):
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.figure(figsize=(15, 5),dpi=80)

        ax1 = plt.subplot(1,2,1)
        ax1.grid(color='r',
                 linestyle='--',
                 linewidth=1,
                 alpha=0.3)
        ax1.barh(list(self.num.keys()), self.num.values(), color='r', alpha=0.5)
        ax1.set_title('Apple Store ')
        ax2 = plt.subplot(1,2,2)

        ax2.pie(x=list(self.num.values()),labels = self.num.keys(),autopct='%1.f%%')
        map = Map()
        province_keys = list(self.num.keys())
        province_values = list(self.num.values())
        map.add("门店数量", [list(z) for z in zip(province_keys, province_values)], "china", zoom=1.2)
        map.render("门店数量.html")
        os.system("门店数量.html")
        plt.show()



if __name__ == "__main__":
    sta = Crawler()
    sta.url = "https://www.apple.com.cn/retail/storelist"
    sta.get_res()
    sta.get_inf()
    sta.draw_plot()
