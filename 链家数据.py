import re
import requests
import time
import pymysql
import csv
import pymongo

class LianJia:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)'}

        #mysql数据库的连接
        self.db = pymysql.connect(
            'localhost',
            'root',
            '123456',
            'maoyandb',
            charset='utf8')
        self.cursor = self.db.cursor()

        #mongo数据库的连接
        self.database = 'AID1811'
        self.table = 'stuinfo1'
        self.conn = pymongo.MongoClient('localhost', 27017)
        self.db1 = self.conn[self.database]
        self.myset = self.db1[self.table]

    #获取网页数据
    def get_page(self,url):
        res = requests.get(url,headers=self.headers)
        res.encoding = 'utf-8'
        html = res.text
        print('html成功')
        self.get_data(html)

    #对数据进行筛选(正则表达式)
    def get_data(self,html):
        print('进入抓取成功')
        p = re.compile('<span class="houseIcon">.*?data-el="region">(.*?)</a>(.*?)</div>.*?target="_blank">(.*?)</a>.*?<div class="totalPrice">.*?<span>(.*?)</div>')
        r_list = p.findall(html)
        print('抓取成功')
        print(r_list)
        time.sleep(1)
        self.db_cun(r_list)
        self.csv_cun(r_list)
        self.mongodb_cun(r_list)

    #对数据进行处理(存入数据库)
    def db_cun(self,r_list):
        for list in r_list:
            ins = "insert into house2(name,descp,address,price) values(%s,%s,%s,%s);"
            price = list[3].replace('</span>','')
            name = list[0]
            desc = list[1]
            address = list[2]
            l = [name,desc,address,price]
            print(l)
            self.cursor.execute(ins, l)
            print('调试代码1')
            self.db.commit()
            print('存入数据库成功')


    #对数据进行处理(存入csv)
    def csv_cun(self,r_list):
        for list in r_list:
            l = [list[0],list[1],list[2],list[3].replace('</span>','')]
            with open('链接二手房.csv','a') as f:
                writer = csv.writer(f)
                writer.writerow(l)
        print('存入csv成功')

    #对数据进行处理(存入mongodb)
    def mongodb_cun(self,r_list):
        for list in r_list:
            self.myset.insert_one({'name':list[0],'desc':list[1],'address':list[2],'price':list[3].replace('</span>','')})
        print('存入mongodb成功')

    #对数据进行分析,然后传入数据处理函数
    def data_analyze(self):
        pass

    #主函数
    def work_on(self):
        print('抓取开始')
        for x in range(1,20):
            url = 'https://cq.lianjia.com/ershoufang/pg%s'%x
            self.get_page(url)
            time.sleep(1)
        self.db.close()
        self.cursor.close()


if __name__ == "__main__":
    start = time.time()
    run01 = LianJia()
    run01.work_on()
    end = time.time()
    print('执行时间:%.2s'%(end-start))






