import requests 
import parsel
import csv


for page in range(1, 39):
    print(f'\n=======================正在抓取第{page}页数据========================')

    url = f'https://www.guahao.com/expert/all/%E5%85%A8%E5%9B%BD/all/%E4%B8%8D%E9%99%90/p{page}'
  
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'}

    response = requests.get(url=url, headers=headers)
    html_data = response.text  # .text 提取文本数据, 字符串 ---> 正则
    # print(html_data)

 
    selector = parsel.Selector(html_data)  # 数据类型的转换

    lis = selector.xpath('//div[@class="g-doctor-items to-margin"]/ul/li')  # 所有li

    for li in lis: # 二次提取  遍历  迭代
        doctor_name = li.xpath('.//dl/dt/a/text()').get().strip()
        doctor_level = li.xpath('.//dl/dt/text()').getall()[1].strip()  # 级别
        doctor_kind = li.xpath('.//dd/p[1]/text()').get().strip()  # 类别
        doctor_Belonging = li.xpath('//span[@class="g-txt-ell"]/text()').get().strip()  # 所属医院
        doctor_score = li.xpath('.//dd/p[3]/span[1]/em/text()').get()  # 评分
        doctor_inquiry = li.xpath('.//dd/p[3]/span[2]/i/text()').get()  # 问诊量
        doctor_goodFor = li.xpath('.//div[@class="skill"]/p/text()').get().strip() \
            .replace('\n', '').replace(' ', '')  # 擅长

        pic_see_price = li.xpath('.//span[@class="service-name"][1]/em[2]/text()').get().strip()  # 图文问诊价格

        video_see_price = li.xpath('.//a[@class="infos video"]/span/em[2]/text()').get()  # 视频问诊价格
        if video_see_price:
            video_see_price = video_see_price.strip()  # strip('*') 去除字符串前后两端的空格
        else:
            video_see_price = 'None'

        doctor_detail = li.xpath('.//a[@class="cover-bg seo-anchor-text"]/@href').get()  # 详情页

        print(doctor_name, doctor_level, doctor_kind, doctor_Belonging, doctor_score,
              doctor_inquiry, doctor_goodFor, pic_see_price, video_see_price, doctor_detail)

        with open('微医网数据.csv', mode='a', encoding='utf-8', newline='') as f:
            csv_write = csv.writer(f)
            csv_write.writerow([doctor_name, doctor_level, doctor_kind, doctor_Belonging, doctor_score,
              doctor_inquiry, doctor_goodFor, pic_see_price, video_see_price, doctor_detail])

 






























