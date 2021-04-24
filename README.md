### Hi there 👋

<!--
**xycm-ks/xycm-ks** is a ✨ _special_ ✨ repository because its `README.md` (this file) appears on your GitHub profile.

Here are some ideas to get you started:

- 🔭 I’m currently working on ...
- 🌱 I’m currently learning ...
- 👯 I’m looking to collaborate on ...
- 🤔 I’m looking for help with ...
- 💬 Ask me about ...
- 📫 How to reach me: ...
- 😄 Pronouns: ...
- ⚡ Fun fact: ...
-->
import random
import numpy as np

#初始化种群
def ori(num):
    times=[[16],[8,8],[8,4,2,2],[8,2,2,2,2],[4,4,4,4],[2,2,2,2,2,2,2,2],
       [4,4,2,2,2,2],[4,2,2,2,2,2,2],[8,2,2,1,1,1,1],[4,4,2,2,2,2,1,1],
        [4,4,4,2,1,1],[8,4,2,1,1]]
    present_time,temp_snatch,snatch=[],[],[]
    time,temp_scale,scale=[],[],[]
    grade1,grade2=[],[]
    temp_popular,popular=[],[]
    #生成num段音乐
    for x in range(num):
        #生成一段8节音乐
        a, b = 0, 0
        for i in range(8):
            #在times里任选一个数组并随机排列
            x=random.randint(0,len(times)-1)
            present_time=times[x]
            random.shuffle(present_time)
            # time.append(present_time)#用以对时值评分
            #添加上音符
            for j in present_time:
                y=random.randint(0,12)
                temp_scale.append(y)#用以对音级评分
                z=(j,y)
                temp_snatch.append(z)
            scale.append(temp_scale)
            snatch.append(temp_snatch)
            temp_snatch,temp_scale=[],[]
        temp_popular.append(snatch)
        snatch=[]
        #最大音高差计算评分
        for i in range(len(scale)-1):
            dif=abs(scale[i][0]-scale[i+1][0])
            if dif<=3:
               a=a+1
        #小节内音差评分
        for i in scale:
            for j in range(len(i)-1):
                dif=abs(i[j]-i[j+1])
                if dif<=6:
                    b=b+1
        grade=6*a+4*b
        grade1.append(grade)
    grade2=grade1
    grade2.sort(reverse=False)
    popular.append(temp_popular[grade1.index(grade2[0])])
    for i in range(1,20):
        if grade2[i]!= grade2[i-1]:
            c=grade1.index(grade2[i])
            popular.append(temp_popular[c])
        else:
            c=grade1.index(grade2[i],grade1.index(grade2[i-1]))
            popular.append(temp_popular[c])
    return popular

#编码
#def decode(popular):

if __name__ == '__main__':
       popular=ori(200)
       print(popular)
