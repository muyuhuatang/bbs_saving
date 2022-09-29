# -*- coding: UTF-8 -*-
# reference: https://www.amobbs.com/thread-5711869-1-1.html
import requests
import re
import os


# http://bbs.tianya.cn/post-no05-471093-1.shtml
# paper_url = str(input('请输入天涯社区主贴网址：'))
paper_url = 'http://bbs.tianya.cn/post-1197-241-1.shtml'

def get_page_count(paper_url):  # 获取页面数量
    response = requests.get(paper_url)
    response.encoding = 'utf-8'
    result = response.text
    reg = r'pageCount : (.*?),'
    page_count = re.findall(reg, result)
    print(page_count)
    return int((page_count[0]))


def get_paper_name(paper_url):  # 获取文章名称+版块名称，建立文件夹用
    response = requests.get(paper_url)
    response.encoding = 'utf-8'
    result = response.text
    reg = r'<title>(.*?)_论坛_天涯社区</title>'
    paper_name = re.findall(reg, result)[0]
    paper_name = paper_name.replace(' ', '_') #  文件夹名有空格情况下mkdir会不正常，用下划线替代
    # print(paper_name)
    return paper_name


def get_author_id(paper_url):  # 获取作者ID，提取作者回复的内容用
    response = requests.get(paper_url)
    response.encoding = 'utf-8'
    result = response.text
    reg = r'authorId : (.*?),'
    author_id = re.findall(reg, result)
    return author_id[0]


def get_author_content(paper_url):
    page_count = get_page_count(paper_url)
    author_id = get_author_id(paper_url)
    paper_name = get_paper_name(paper_url)
    os.system(r'mkdir' + r' ' + paper_name)
    page_url = paper_url[0:-7]  # http://bbs.tianya.cn/post-no05-471093- 截到这里
    for i in range(1, page_count + 1):  # 遍历所有页面
        page_num = str(i)
        page_url_i = page_url + page_num + '.shtml'  # 拼凑为第i个页面
        response = requests.get(page_url_i)
        response.encoding = 'utf-8'
        result = response.text
        reg = r'hostid=' + author_id + r'.*?<div class="bbs-conte.*?">(.*?)<div class="atl-reply"'
        author_bbs_content = re.findall(reg, result, re.S)
        if author_bbs_content != []:  # 本页作者有回复则保存
            print('正在保存第%s页数据' % page_num)
            # 保存第i个页面为html
            fn = open('%s\\%s.html' % (paper_name, page_num), 'w', encoding='utf-8')
            for j in author_bbs_content:
                fn.write(j)
            fn.close


get_author_content(paper_url)