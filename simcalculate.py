
import math

from pymongo import MongoClient

# 输入
def wordsim(w1,w2):
    client = MongoClient('localhost',27017)
    db = client['NLP']
    collection = db['Cilin']

    # 同一个词可能有多个相似度编号，存入列表依次计算
    # 如果在词林中没有找到这个词则停止计算
    sim1 = ['']
    sim2 = ['']
    # if(collection.find({'word':w1})):
    #     sim1
    for item in collection.find({'word':w1}):
        sim1.append(item['index'])
    for item in collection.find({'word':w2}):
        sim2.append(item['index'])
    if sim1 == ['']:
        print('cannot find sim1')
        return
    else :
        sim1.remove('')
        print(w1+'的编号共'+str(len(sim1))+'个：')
        print(sim1)
    if sim2 == ['']:
        print('cannot find sim2')
        return
    else :
        sim2.remove('')
        print(w2+'的编号共'+str(len(sim2))+'个：')
        print(sim2)

    # 计算每两个Index的相似度，最大值存入simmax
    simmax = 0
    for s1 in sim1:
        for s2 in sim2:
            cals = calsim(s1,s2,collection)
            if cals > simmax:
                simmax = cals
    print(simmax)

# 调用collection只能传参吗？
def calsim(s1,s2,collection):
    #计算参数
    para = [0.65,0.8,0.9,0.96,0.5,0.1]
    # a=0.65
    # b=0.8
    # c=0.9
    # d=0.96
    # e=0.5
    # f=0.1
    lvlflag = 0

    # 考虑在每一级获取字符前进行字符范围检查
    # 第一级 大写字母
    x1=s1[0]
    x2=s2[0]
    if x1 == x2:
        # 第二级 小写字母
        x1=s1[1]
        x2=s2[1]
        if x1==x2:
            #第三级 两位十进制数
            x1=s1[2]+s1[3]
            x2=s2[2]+s2[3]
            if int(x1)==int(x2):
                # 第四级 大写字母
                x1 = s1[4]
                x2 = s2[4]
                if x1==x2:
                    # 第五级 两位十进制数
                    x1 = s1[5]+s1[6]
                    x2 = s2[5]+s2[6]
                    if x1==x2:
                        # 第六级 =：1，#：e，@：不存在
                        x1 = s1[7]
                        x2 = s2[7]
                        if x1=='=' and x2=='=':
                            return 1
                        elif x1=='#' and x2=='#':
                            return para[4]  # return e
                        elif x1=='@' and x2=='@': # 闭合，输入同一个词
                            return 1
                        else:
                            print('编号'+s1+','+s2+'计算有误')
                            return -1
                    else:
                        lvlflag =5
                else:
                    lvlflag = 4
            else:
                lvlflag = 3
        else:
            lvlflag = 2
    else:
        lvlflag = 1
    print('lvlflag:'+str(lvlflag))
    print(s1[0:2])
    # 根据在第几级不同进行相似度计算
    if lvlflag == 1 :
        return para[5] # return f
    else :
        if s1[0:lvlflag-1] == s2[0:lvlflag-1]:
            pattern = '^'+s1[0:lvlflag]+'.*'
            print('pattern '+pattern)
            n = collection.find({'index':{'$regex':pattern}}).count()
        else:
            print('ERROR：计算分支层节点数量有误，分支判断错误')
            return -1
        if lvlflag == 3 or lvlflag == 5 :
            k = abs(int(x1)-int(x2))
        else :
            k = abs(ord(x1)-ord(x2))
        return para[lvlflag-1] * math.cos(math.pi*n/180)*((n-k+1)/n)

wordsim('面包','饼干')