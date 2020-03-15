import pandas as pd
from selenium import webdriver#需要安装selenium库,下载安装Chrome和匹配版本的chromedriver，将chromedriver.exe放到Python/Scripts下面
import time

#动态网页的抓取，核心是模拟人工打开网页点击刷新，先启动浏览器
browser = webdriver.Chrome()
#目标网址信息
url = 'http://bond.sse.com.cn/bridge/information/'
##打开网页
browser.get(url)
#初次启动，加载较慢，视网速不同，预留的加载时间不同，建议留5秒以上，网速慢，加载内容会空，和静态网页不同，异步加载
time.sleep(5)
#从首页提取信息对应标签内容
begin=browser.find_elements_by_tag_name('td')#提取网页中这个部分的内容，为之后提取文本做准备
#构建一个获取网址所需信息，返回一个二维表的函数
def GetData(info):
    a=[]
    for i in range(len(info)):#将提取的文本导入到一个list中
        a.append(info[i].text)
    step=8
    b=[a[i:i+step]for i in range(0,len(a),step)]#每8个元素一组进行安排
    result=pd.DataFrame(b,columns=['编号','债券名称','承销商/管理人','品种','拟发行金额（亿元）','项目状态','更新日期','受理日期'])#导出为表格
    return result
#首先获取首页内容
first=GetData(begin)
#以上实现了首页信息的抓取，下面进行下一页翻页，获取后续页面信息
for i in range(866):#866为总页数，可以在首页提取，也可以手动输入，这里我简化了，直接手动输入
    try:
        new=browser.find_element_by_link_text('下一页')#找到下一页的点击标签
        new.click()#点击下一页
        info = browser.find_elements_by_tag_name('td')#获取下一页中对应的关键信息
        s=GetData(info)#提取信息并返回
    except:
        new=None#到最后一页无‘下一页’，设置为None，结束循环
    first=first.append(s,ignore_index=True)#每个‘下一页’的内容合并到首页，形成完整的数据
print(first)

first.to_excel('info.xls')#将获取的数据写入EXCEL表格中