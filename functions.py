from lxml import etree
import requests
import re

headers = {
    'Referer': 'https://www.bilibili.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
}

# 正则提取bv号
def bvre(bv):
    bv += '?'
    rx = '(BV[\S]*?)\\?'
    r_bv = re.findall(rx, bv)[0]
    r_bv = r_bv.replace('/', '')
    return r_bv

# 获取视频名称
def name(bv, headers):
    url = 'https://www.bilibili.com/video/'+bv
    text = requests.get(url, headers=headers).text
    tree = etree.HTML(text)
    name = tree.xpath('//*[@id="viewbox_report"]/h1/span/text()')[0]
    return name


# 获取分页信息以及对应的cid
# https://api.bilibili.com/x/web-interface/view/detail?bvid=BV1CX4y1P7M8&aid=713833694&need_operation_card=1&web_rm_repeat=&need_elec=1&out_referer=https%3A%2F%2Fspace.bilibili.com%2F

def page(bv):
    url = 'https://api.bilibili.com/x/web-interface/view/detail'
    param = {
        'bvid': '%s' % bv,
    }
    text = requests.get(url, params=param, headers=headers).json()
    text_cid = text['data']['View']['pages']
    for page in text_cid:
        if page['page'] == 1:
            f_cid = page['cid']
    cid = ""
    for page in text_cid:
        if cid == "":
            cid = f_cid
            num = 1
            break
        else:
            cid = int(cid)
        if page['page'] == cid or page['cid'] == cid:
            cid = page['cid']
            num = page['page']
            break
    ret = [cid, num]
    return ret

# 获取视频url
def flv(cid, bv, headers, quality):
    url = 'https://api.bilibili.com/x/player/playurl'
    param = {
        'cid': '%s' % cid,
        'bvid': '%s' % bv,
        'qn': '%s' % quality,
    }
    return requests.get(url, params=param, headers=headers).json()

# 请求视频并保存
async def get_flv(name, bv, flv_url, headers, page_num):
    response = requests.get(flv_url, headers=headers)
    code = response.status_code
    text = response.content
    if code == 200:
       # 删除标题中的 / 等字符，防止文件路径错误
        name = name.replace('/', '').replace('|', '')
        filename = "./%s-%d.flv" % (name, page_num)
        with open(filename, 'wb') as fp1:
            fp1.write(text)
        with open("./list.txt", 'a') as fp2:
            fp2.write(name+"\nhttps://www.bilibili.com/video/" +
                      bv+"?p=%d\n\n" % page_num)
        return filename
    else:
        try:
            response.raise_for_status()
        except Exception as e:
            return e.__str__()


# main
if __name__ == '__main__':
    bv = input("输入BV号(网页链接)：")
    bv = bvre(bv)

    cid_get = page(bv)
    cid = cid_get[0]
    page_num = cid_get[1]

    # cid = cid(bv,headers)
    print('\ncid:', cid)
    print('page:', page_num)
    name = name(bv, headers)
    print('\n标题：', name)

    quality = ''
    text = flv(cid, bv, headers, quality)
    qn = text['data']['support_formats']

    print("\n可选择的清晰度(部分清晰度可能获取失败)：")
    for qu in qn:
        print(('清晰度：%s' % qu['new_description']).ljust(
            15)+('视频质量参数:%d' % qu['quality']).ljust(15)+('格式参数:%s' % qu['format']).ljust(15))
    quality = input("输入清晰度对应的视频质量参数（默认1080p）：")

    if quality == '':
        quality = '80'

    text = flv(cid, bv, headers, quality)
    flv_url = text['data']['durl'][0]['url']

    print('\nflv_url:', flv_url)
    get_flv(name, flv_url, headers, page_num)
