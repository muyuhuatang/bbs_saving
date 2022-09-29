#coding=utf-8
# reference: https://bbs.huaweicloud.com/blogs/230515 / https://www.pythontutorial.net/python-basics/python-write-text-file/


import requests
from bs4 import Tag
from bs4 import BeautifulSoup

def getHtml(url):
    page = requests.get(url)
    html =page.text
    return html

def getText(html):
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
            with open("output.txt", 'a') as f:  
                # f.write('Data')
                f.write(Data)
                f.write('\n')
  
            f.close()         


if __name__=='__main__':
    page_num = 622
    url  = "http://bbs.tianya.cn/post-1197-241-1.shtml"
    url = url[0:-7]  # http://bbs.tianya.cn/post-no05-471093- cut to here (the left is before the page number in the link)
    for i in range(1,page_num+1):
        page_num = str(i)
        page_url_i = url + page_num + '.shtml'  # get the full link of i_th page

        html = getHtml(page_url_i)
        getText(html)
        print(str(i)+'th page has been processed')
