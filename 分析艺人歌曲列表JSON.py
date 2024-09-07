import json
def 分析艺人歌曲列表JSON(JSONData):
    原始JSON = json.loads(JSONData)
    if(原始JSON['code']!=200):
        return False
    音质列表 = ['h','m','l','sq']
    歌单数据词典 = {}
    歌单数据词典['歌曲'] = []
    for i in range(len(原始JSON['songs'])):
        歌单数据词典['歌曲'].append({})
        歌单数据词典['歌曲'][i]['歌名'] = 原始JSON['songs'][i]['name']
        歌单数据词典['歌曲'][i]['图标'] = 原始JSON['songs'][i]['al']['picUrl']
        歌单数据词典['歌曲'][i]['歌手'] = []
        for j in range(len(原始JSON['songs'][i]['ar'])):
            歌手 =  原始JSON['songs'][i]['ar'][j]['name']
            歌单数据词典['歌曲'][i]['歌手'].append(歌手)
        歌单数据词典['歌曲'][i]['歌曲ID'] = 原始JSON['songs'][i]['id']
        for j in range(len(音质列表)):
            try:
                歌单数据词典['歌曲'][i]['音频比率'] = 原始JSON['songs'][i][音质列表[j]]['br']
            except:
                pass
    #查找每一首歌曲都有的歌手,作为歌单名字
    歌手名字出现的次数 = {}
    #初始化字典
    for i in range(len(歌单数据词典['歌曲'])):
        for j in range(len(歌单数据词典['歌曲'][i]['歌手'])):
            歌手名字 = 歌单数据词典['歌曲'][i]['歌手'][j]
            歌手名字出现的次数[歌手名字] = 0
    for i in range(len(歌单数据词典['歌曲'])):
        for j in range(len(歌单数据词典['歌曲'][i]['歌手'])):
            歌手名字 = 歌单数据词典['歌曲'][i]['歌手'][j]
            歌手名字出现的次数[歌手名字] += 1
            if(歌手名字出现的次数[歌手名字]==len(歌单数据词典['歌曲'])):
                歌单数据词典['歌单名称'] = 歌手名字+'的热门歌曲'
                break
    return 歌单数据词典