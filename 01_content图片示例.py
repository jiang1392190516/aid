import requests

url = 'https://b-ssl.duitang.com/uploads/item/201604/25/20160425173224_4GHxj.png'
headers = {'User-Agent':'Mozilla/5.0'}

#发请求获响应
res = requests.get(url,headers=headers)
res.encoding = 'utf-8'

#获取bytes数据类型
html = res.content

#　写文件
with open('图片.png','wb') as f:
    f.write(html)



