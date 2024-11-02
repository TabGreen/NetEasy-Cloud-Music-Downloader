import json
def 分析歌曲付费状态(JSONData):
    API数据 = json.loads(JSONData)
    用户付费状态 = API数据['data'][0]["payed"]
    是否需要付费 = API数据['data'][0]["fee"]
    if 是否需要付费 == 1:
        if 用户付费状态 == 1:
            return False#已付费,无需特殊处理
        else:
            return True#未付费,需要特殊处理
    else:
        return False
    
#测试代码
#print(分析歌曲付费状态(open('歌曲API数据样本(免费).json','r').read()))