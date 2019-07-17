#encoding=utf-8
import urllib
import re
from pyquery import PyQuery as pq

def replace(x):
    replacebr=re.compile('<br/>|<br />|<br>')
    x=re.sub(replacebr,"\n",x)
    return x.strip()

def geturl(mainpage):
    links = []
    pagenum = 999
    now = 0
    try:
        while now < pagenum:
            print('Now:' + str(int(now/50+1)))
            html = pq(url=mainpage+'&ie=utf-8&pn=' + str(now))
            if now == 0:
                pagenum = int(re.search('pn=(\d+)', html('.last.pagination-item').attr('href')).group(1))
            for i in html('#thread_list .j_th_tit a').items():
                url = i.attr('href')
                pre = 'https://tieba.baidu.com'
                if url[0] != '/':
                    pre += '/'
                links.append(pre+url)
            now += 50
    finally:
        return links

def getposts(url,seelz):
    print('Now: ' + url)
    pagenum = 999
    now = 1
    content = ''
    title = url
    while now <= pagenum:
        url += '?see_lz=' + str(seelz) + '&pn=' + str(now)
        html = pq(url)
        if now == 1:
            pagenum = int(html('.l_reply_num .red')[1].text)
            title = html('.core_title_txt').text()
        for i in html('.p_postlist .d_post_content').items():
            #print(replace(i.html()))
            content = content + replace(i.html()) + '\n'
        now += 1
    title = re.sub(r"[\/\\\:\*\?\"\<\>\|]", "_", title)
    with open(title+'.txt', 'w', encoding='utf-8') as f:
        f.write(content)

seelz = 1
#主页链接格式：https://tieba.baidu.com/f?kw=***
mainpage = input()
urls = geturl(mainpage)
for i in urls:
    getposts(i, seelz)
