from lxml import etree
import requests
import re
import os

headers = {
    'Referer': 'https://www.bilibili.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
}

class CIDNotFoundException(Exception):
    pass

def qualityid(quality_name):
    if quality_name == '1080P':
        return 80
    elif quality_name == '720P':
        return 64
    elif quality_name == '480P':
        return 32
    elif quality_name == '360P':
        return 16

# 正则提取bv号
def bvre(bv):
    bv += '?'
    rx = '(BV[\S]*?)\\?'
    r_bv = re.findall(rx, bv)[0]
    return r_bv.replace('/', '')

# 获取视频名称
def name(bv, headers):
    return etree.HTML(requests.get('https://www.bilibili.com/video/' + bv, headers=headers).text).xpath('//*[@id="viewbox_report"]/h1/span/text()')[0]


# 获取分页信息以及对应的cid
def get_cid(bv, page_num):
    url = 'https://api.bilibili.com/x/web-interface/view/detail'
    param = {
        'bvid': '%s' % bv,
    }
    text = requests.get(url, params=param, headers=headers).json()
    text_cid = text['data']['View']['pages']
    for page in text_cid:
        if page['page'] == page_num:
            return page['cid']
    raise CIDNotFoundException('目标视频似乎没有第 ' + page_num + ' 页。')


# 获取视频url
def play_url(cid, bv, headers, quality):
    url = 'https://api.bilibili.com/x/player/playurl'
    param = {
        'cid': '%s' % cid,
        'bvid': '%s' % bv,
        'qn': '%s' % quality,
    }
    return requests.get(url, params=param, headers=headers).json()


# 请求视频并保存
def get_flv(name, bv, flv_url, headers, page_num):
    response = requests.get(flv_url, headers=headers)
    code = response.status_code
    text = response.content
    if code == 200:
       # 删除标题中的 / 等字符，防止文件路径错误
        name = name.replace('/', '').replace('|', '')
        filename = "./Downloads/%s - PAGE %d.flv" % (name, page_num)
        with open(filename, 'wb') as fp1:
            fp1.write(text)
        with open("./DownloadHistory.txt", 'a') as fp2:
            fp2.write(name+"\nhttps://www.bilibili.com/video/" + bv + "?p=%d\n\n" % page_num)
        return os.path.abspath(filename)
    else:
        response.raise_for_status()
