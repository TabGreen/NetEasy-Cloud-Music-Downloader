import json
def 处理歌单JSON(JSONData):
    包含文件格式的子词典名称 = ['hMusic','mMusic','lMusic','bMusic']
    原始词典 = json.loads(JSONData)
    歌单数据词典 = {}
    歌单数据词典['歌曲'] = []
    if(原始词典['code'] != 200):
        print(原始词典)
        return False
    print(原始词典['result']['name'])
    歌单数据词典['歌单名称'] = 原始词典['result']['name']
    for i in range(len(原始词典['result']['tracks'])):
        歌单数据词典['歌曲'].append({})
        歌单数据词典['歌曲'][i]['歌名'] = 原始词典['result']['tracks'][i]['name']
        歌单数据词典['歌曲'][i]['图标'] = 原始词典['result']['tracks'][i]['album']['picUrl']
        歌单数据词典['歌曲'][i]['歌手'] = []
        for j in range(len(原始词典['result']['tracks'][i]['artists'])):
            歌手 = 原始词典['result']['tracks'][i]['artists'][j]['name']
            歌单数据词典['歌曲'][i]['歌手'].append(歌手)
        歌单数据词典['歌曲'][i]['歌曲ID'] = 原始词典['result']['tracks'][i]['id']
        for j in range(len(包含文件格式的子词典名称)):
            try:
                歌单数据词典['歌曲'][i]['文件格式'] = 原始词典['result']['tracks'][i][包含文件格式的子词典名称[j]]['extension']
                歌单数据词典['歌曲'][i]['音频比率'] = 原始词典['result']['tracks'][i][包含文件格式的子词典名称[j]]['bitrate']
            except:
                pass
    return 歌单数据词典

if __name__ == '__main__':
    歌单JSON = open('歌单数据JSON样本.json','r',encoding='utf-8').read()
    歌单数据 = 处理歌单JSON(歌单JSON)
    print(歌单数据)

