import pandas as pd
import numpy as np
import os
import re
from selenium import webdriver
import time


browser = webdriver.Chrome()
url = 'http://bond.sse.com.cn/bridge/information/'
# id=87
# url = base_url + str(id)
browser.get(url)
time.sleep(5)
begin=browser.find_elements_by_tag_name('td')#提取网页中这个部分的内容，为之后提取文本做准备
def GetData(info):
    a=[]
    for i in range(len(info)):#将提取的文本导入到一个list中
        a.append(info[i].text)
    step=8
    b=[a[i:i+step]for i in range(0,len(a),step)]#每8个元素一组进行安排
    result=pd.DataFrame(b,columns=['编号','债券名称','承销商/管理人','品种','拟发行金额（亿元）','项目状态','更新日期','受理日期'])#导出为表格
    return result
first=GetData(begin)
#以上实现了单页信息的抓取，如何进行下一页呢
for i in range(866):
    try:
        new=browser.find_element_by_link_text('下一页')
        new.click()
        info = browser.find_elements_by_tag_name('td')
        s=GetData(info)
    except:
        new=None
    first=first.append(s,ignore_index=True)
print(first)

first.to_excel('info.xls')