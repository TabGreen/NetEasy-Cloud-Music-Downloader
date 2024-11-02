#倒入模块
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TRCK, TYER, TCON, COMM, TCOM, TEXT, TCOP, TSRC, TBPM, TIT1, APIC
import requests
import json
import os
import time
import re

#连接文件
from 分析歌单JSON import *
from 分析艺人歌曲列表JSON import *
from 分析歌曲 import *

#设置常量
音频比率 = 320000
#定义常量
用户代理 = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0'
网易云音乐歌单接口地址 = 'https://music.163.com/api/playlist/detail?id='
网易云音乐艺人接口地址 = 'https://music.163.com/api/artist/top/song?'
网易云音乐音乐接口地址 = 'https://music.163.com/api/song/enhance/player/url?'
请求数据 = {}


#用户数据
歌单ID = 12310528419
艺人ID = 1203033
cookie = open('cookie.txt','r',encoding = 'utf-8').read()
#把上面两个数据替换成你的数据(从浏览器获取)

请求标头 = {
    "authority": "music.163.com",
    "method": "GET",
    "path": "/api/playlist/detail?id=9344444379",
    "scheme": "https",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-encoding": "gzip, deflate, br, zstd",
    "Accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Cache-control": "max-age=0",
    "Priority": "u=0, i",
    "Sec-ch-ua": "\"Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"Microsoft Edge\";v=\"128\"",
    "Sec-ch-ua-mobile": "?0",
    "Sec-ch-ua-platform": "\"macOS\"",#操作系统
    "Sec-fetch-dest": "document",
    "Sec-fetch-mode": "navigate",
    "Sec-fetch-site": "none",
    "Sec-fetch-user": "?1",
    "Upgrade-insecure-requests": "1",
    'User-Agent': 用户代理,
    'cookie':cookie
}

#基础函数
##GET请求
def GET请求(URL):
    global 用户代理
    global 请求标头
    response = requests.get(URL, headers=请求标头)
    return response
def POST请求(URL):
    global 用户代理
    global 请求标头
    response = requests.post(URL,headers=请求标头)
    return response
def 爬取歌单信息(歌单ID):
    global 请求数据
    response = POST请求(网易云音乐歌单接口地址 + str(歌单ID))
    print(json.loads(response.text)['code'])
    if(response.status_code != 200):
        print(json.loads(response.text)['message'])
        return False
    response.encoding = 'utf-8'
    JSON = response.text
    歌单信息 = 处理歌单JSON(JSON)
    return 歌单信息
def 爬取艺人歌曲列表(艺人ID):
    global 请求数据
    response = GET请求(网易云音乐艺人接口地址 + 'id=' + str(艺人ID))
    if(response.status_code != 200):
        print(json.loads(response.text)['message'])
        return False
    response.encoding = 'utf-8'
    json = response.text
    艺人歌曲列表 = 分析艺人歌曲列表JSON(json)
    return 艺人歌曲列表
#获取音乐URL
def 组合音乐接口URL(ID,音频比率):
    global 网易云音乐音乐接口地址
    newURL = 网易云音乐音乐接口地址 + 'ids=['+str(ID)+']&br='+str(音频比率)
    return newURL
def 获取音乐URL(接口URL):
    response = GET请求(接口URL)
    数据 = json.loads(response.text)
    音乐URL = 数据['data'][0]['url']
    音频格式 = 数据['data'][0]['encodeType']
    return [音乐URL,音频格式]
def 清洗文件名(原始):
    #return re.sub(r'[\/\\\:\*\?\"\<\>\|]', '', 原始)
    return re.sub(r'[\\:\*\?\"\<\>\|]', '', 原始)

def 添加封面到音频(file_path, cover_data, 文件格式):
    # 根据文件格式选择合适的Mutagen库
    if 文件格式.lower() == 'mp3':
        from mutagen.id3 import ID3, APIC 
        from mutagen.mp3 import MP3
        audio = MP3(file_path, ID3=ID3)
        if audio.tags is None:
            audio.add_tags()
        audio.tags.add(
            APIC(
                encoding=3,  # UTF-8
                mime='image/jpeg',  # 图片类型
                type=3,  # 3表示封面正面
                desc='Cover',
                data=cover_data  # 图片的二进制数据
            )
        )
        audio.save(v2_version=3)  # 保存为v2.3版本的ID3标签
    elif 文件格式.lower() == 'flac':
        from mutagen.flac import FLAC, Picture
        audio = FLAC(file_path)
        picture = Picture()
        picture.type = 3  # 3表示封面正面
        picture.mime = 'image/jpeg'
        picture.desc = 'Cover'
        picture.data = cover_data
        audio.clear_pictures()
        audio.add_picture(picture)
        audio.save()
    elif 文件格式.lower() == 'm4a':
        from mutagen.mp4 import MP4, MP4Cover
        audio = MP4(file_path)
        audio['covr'] = [MP4Cover(cover_data, imageformat=MP4Cover.FORMAT_JPEG)]
        audio.save()
    else:
        print(f'不支持为{文件格式}添加图标')

def 添加元数据到音频(file_path,metadata):
    audio = ID3(file_path)
    # 添加标题
    if '标题' in metadata:
        audio.add(TIT2(encoding=3, text=metadata['标题']))
    # 添加艺术家
    if '艺术家' in metadata:
        audio.add(TPE1(encoding=3, text=metadata['艺术家']))
    # 添加专辑
    if '专辑' in metadata:
        audio.add(TALB(encoding=3, text=metadata['专辑']))
    # 添加曲目编号
    if '曲目编号' in metadata:
        audio.add(TRCK(encoding=3, text=str(metadata['曲目编号'])))
    # 添加发行年份
    if '发行年份' in metadata:
        audio.add(TYER(encoding=3, text=str(metadata['发行年份'])))
    # 添加流派
    if '流派' in metadata:
        audio.add(TCON(encoding=3, text=metadata['流派']))
    # 添加评论
    if '评论' in metadata:
        audio.add(COMM(encoding=3, lang='eng', desc='', text=metadata['评论']))
    # 添加编曲者
    if '编曲者' in metadata:
        audio.add(TCOM(encoding=3, text=metadata['编曲者']))
    # 添加词作者
    if '词作者' in metadata:
        audio.add(TEXT(encoding=3, text=metadata['词作者']))
    # 添加版权信息
    if '版权信息' in metadata:
        audio.add(TCOP(encoding=3, text=metadata['版权信息']))
    # 添加ISRC
    if 'ISRC' in metadata:
        audio.add(TSRC(encoding=3, text=metadata['ISRC']))
    # 添加BPM
    if 'BPM' in metadata:
        audio.add(TBPM(encoding=3, text=str(metadata['BPM'])))
    # 添加编组
    if '编组' in metadata:
        audio.add(TIT1(encoding=3, text=metadata['编组']))
#下载音乐文件
def 依次下载音乐(歌单信息):
    try:
        os.mkdir(歌单信息['歌单名称'])
    except FileExistsError:
        if(input('歌单已存在，是否覆盖？(y/n)') == 'y'):
            pass
        else:
            return False
    os.chdir(歌单信息['歌单名称'])
    for i in range(len(歌单信息['歌曲'])):
        歌名 = 歌单信息['歌曲'][i]['歌名']
        #print(歌单信息['歌曲'][i])
        #合并歌手名字
        歌手名s = 歌单信息['歌曲'][i]['歌手']
        歌手名s = list(set(歌手名s))
        歌手 = ''
        for j in range(len(歌手名s)):
            歌手 += 歌手名s[j]
            if(j != len(歌手名s)-1):
                歌手 += ','
        歌曲ID = 歌单信息['歌曲'][i]['歌曲ID']
        歌曲图标 = 歌单信息['歌曲'][i]['图标']
        专辑名 = 歌单信息['歌曲'][i]['专辑']['专辑名']
        发行年份 = 歌单信息['歌曲'][i]['专辑']['发行年份']
        #文件格式 = 歌单信息['歌曲'][i]['文件格式']
        音频比率 = 歌单信息['歌曲'][i]['音频比率']
        [音乐URL,文件格式] = 获取音乐URL(组合音乐接口URL(歌曲ID,音频比率))
        if(音乐URL == None):
            print('歌曲 《'+歌名+'》 下载失败')
            continue
        print('下载 《'+歌名+'》')
        音乐文件数据 = GET请求(音乐URL)
        图标文件数据 = GET请求(歌曲图标)
        if(音乐文件数据.status_code != 200):
            print('歌曲 《'+歌名+'》 下载失败')
            continue
        if(音乐文件数据.content == b'check sign failed'):
            print('歌曲 《'+歌名+'》 下载失败')
            continue
        文件名 = 清洗文件名(歌名+'-'+歌手+'.'+文件格式)
        open(文件名,'wb').write(音乐文件数据.content)
        添加封面到音频(文件名, 图标文件数据.content, 文件格式)
        添加元数据到音频(文件名,{
            '标题': 歌名,
            '艺术家': 歌手,
            '专辑': 专辑名,
            '发行年份': 发行年份,
        })
        time.sleep(0.2)

def main():
    用户想要爬取 = input('需要爬取\n1.网易云歌单\n2.艺人歌曲列表\n请输入序号:')
    用户输入的ID = input('请输入ID:')
    if(用户想要爬取 == '1'):
        while input('是否继续爬取歌单？(y/n)') == 'y':
            歌单ID = 用户输入的ID
            歌单信息 = 爬取歌单信息(歌单ID)
            if(歌单信息 == False):
                print('歌单信息获取失败')
                continue
                #exit()
            依次下载音乐(歌单信息)
            break
    elif(用户想要爬取 == '2'):
        while input('是否继续爬取艺人歌曲列表？(y/n)') == 'y':
            艺人ID = 用户输入的ID
            艺人歌曲列表 = 爬取艺人歌曲列表(艺人ID)
            if(艺人歌曲列表 == False):
                print('艺人歌曲列表获取失败')
                #exit()
                continue
            依次下载音乐(艺人歌曲列表)
            break
    else:
        print('序号不存在')
        exit()
    print('完成')

def main2():
    歌单信息 = 爬取歌单信息(歌单ID)
    依次下载音乐(歌单信息)
if __name__ == '__main__':
    main()