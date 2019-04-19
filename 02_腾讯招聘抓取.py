
import requests
import re
import time
import pymysql


class TenXun:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)'}
        self.page = 0
        self.db = pymysql.connect(
            'localhost',
            'root',
            '123456',
            'maoyandb',
            charset='utf8')
        self.cursor = self.db.cursor()

    def get_page(self,url,params):
        res = requests.get(url,params=params,headers=self.headers)
        res.encoding = 'utf-8'
        html = res.text
        return html
        # self.page_content(html)

    def page_content(self,html):
        p = re.compile('<td class="l square">.*?href="(.*?)">(.*?)</a>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>',re.S)
        r_list = p.findall(html)
        return r_list

    #数据处理
    def data_solute(self,list):
        for li in list:
            href = 'https://hr.tencent.com/'+li[0]
            list = self.data2_jiejue(href)
            job_res = list[0]
            job_spec = list[1]
            name = li[1]
            utype = li[2]
            number = li[3]
            address = li[4]
            time1 = li[5]
            dict = {
                'job_res':job_res,
                'job_spec':job_spec,
                'name':name,
                'utype':utype,
                'number':number,
                'address':address,
                'time1':time1,
            }

            print('项目名称:%s,项目类别:%s,需要人数:%s,工作地点:%s,发布时间:%s,项目职责:%s,项目要求:%s'
                  % (name, utype, number, address, time1,job_res,job_spec))
            print(type(number))
            self.db_cun(dict)
            time.sleep(1)



    def data2_jiejue(self,url):
        res = requests.get(url, headers=self.headers)
        res.encoding = 'utf-8'
        html = res.text
        p = re.compile('<td colspan="3" class="l2">.*?<ul class="squareli">(.*?)</ul>')
        list = p.findall(html)
        # print(list)
        job_res1 = list[0].replace('<li>','')
        # print(job_res1)
        job_spec1 = list[1].replace('<li>','')
        # print(job_spec1)
        job_res = job_res1.replace('</li>', '')
        job_spec = job_spec1.replace('</li>', '')
        # print('工作职责:%s'%job_res)
        # print('工作要求:%s'%job_spec)
        # print(list[0])
        time.sleep(1)
        list1 = [job_res,job_spec]
        # print('存入成功')
        return list1

#存入数据库
    def db_cun(self,dic):
        ins = 'insert into tenxun(name,type,people,address,time,responsibility,request) ' \
              'values(%s,%s,%s,%s,%s,%s,%s)'
        list = [dic['name'].strip(),dic['utype'],dic['number'].strip(),dic['address'].strip(),
                dic['time1'].strip(),dic['job_res'],dic['job_spec']]
        # print('调试代码')
        print(list)
        self.cursor.execute(ins,list)
        # print('调试代码2')
        self.db.commit()
        print('存入成功')



    def work_on(self):
        job = input('请输入你想了解的岗位:')
        dict = {
            'keywords':job,
            'starts':str(self.page)
        }
        print(dict)
        for x in range(0,3):
            url = 'https://hr.tencent.com/position.php?'
            self.page += 10
            html = self.get_page(url,dict)
            list = self.page_content(html)
            list = self.data_solute(list)
            time.sleep(1)
        self.db.close()
        self.cursor.close()

if __name__ == "__main__":
    start = time.time()
    tenxun = TenXun()
    tenxun.work_on()
    end = time.time()
    print('执行时间:%.2f'%(end-start))









