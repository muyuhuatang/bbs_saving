#coding=utf-8
# reference: https://bbs.huaweicloud.com/blogs/230515 / https://www.pythontutorial.net/python-basics/python-write-text-file/


import requests
from bs4 import Tag
from bs4 import BeautifulSoup
import re

paper_url = 'http://bbs.tianya.cn/post-no05-515153-1.shtml'
# paper_url = str(input('Please input the first page web link of the Tianya BBS Post:'))

def get_page_count(paper_url):  # obtain the total page count
    response = requests.get(paper_url)
    response.encoding = 'utf-8'
    result = response.text
    reg = r'pageCount : (.*?),'
    page_count = re.findall(reg, result)
    print(page_count)
    return int((page_count[0]))

def get_page_name(paper_url):  # obtian the post name 
    response = requests.get(paper_url)
    response.encoding = 'utf-8'
    result = response.text
    reg = r'<title>(.*?)_论坛_天涯社区</title>'
    paper_name = re.findall(reg, result)[0]
    paper_name = paper_name.replace(' ', '_') #  replace the blankets with _
    return paper_name

def getHtml(url):
    page = requests.get(url)
    html =page.text
    return html

def getText(html, name):
    get_text = Tag.get_text
    soup = BeautifulSoup(html, 'html.parser')
    author_info = soup.find_all('div', class_='atl-info')
    listauthor  = [x.get_text() for x in author_info]
    list_info = soup.find_all('div', class_='bbs-content')
    listtext  = [x.get_text() for x in list_info]
    global i
    if i > 1:
        listtext = [""] + listtext
    for x in range(len(listauthor)):
        if "楼主" in listauthor[x]:
            # print (listtext[x].strip())
            Data = listtext[x].strip() # remove the blanks before and after the text within the text
            # Data = listtext[x].strip('　　')
            Data = Data.replace('　　', '\n')
            with open('\\'+name+".txt", 'a') as f:  
                # f.write('Data')
                f.write(Data)
                f.write('\n')
  
            f.close()         


if __name__=='__main__':
    url  = paper_url
    page_count = get_page_count(url)
    page_name = get_page_name(url)
    print(page_name)
    # os.system(r'mkdir' + r' ' + paper_name)

    url = url[0:-7]  # http://bbs.tianya.cn/post-no05-471093- cut to here (the left is before the page number in the link)
        

    for i in range(1,page_count + 1):
        page_num = str(i)
        page_url_i = url + page_num + '.shtml'  # get the full link of i_th page

        html = getHtml(page_url_i)
        getText(html, page_name)
        print(str(i)+'th page has been processed')
