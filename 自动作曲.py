import random
import matplotlib.pyplot as plt
import mido
from mido import Message,MidiFile,MidiTrack
import sys
#输出midi文件
def transfer(statics,g,s):
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    track.append(Message('program_change', channel=0, program=2, time=0))
    for i in statics:
        for j in i:
            a=j[0]*240
            num=j[1]
            if num<=3:
                d=58+2*num
            elif 4<=num<=7:
                d=58+2*num-1
            elif 8<=num<=10:
                d=58+2*num-2
            elif 11<=num:
                d=58+2*num-3
            track.append(Message('note_on', note=d, velocity=81, time=0, channel=0))
            track.append(Message('note_off', note=d, velocity=81, time=a, channel=0))
    mid.save(f'第{g}代第{s}段.mid')
    return

#初始化种群
def ori(num):
    times=[[8,8],[8,4,2,2],[8,2,2,2,2],[4,4,4,4],[2,2,2,2,2,2,2,2],[4,4,2,2,2,1,1],
       [4,4,2,2,2,2],[4,2,2,2,2,2,2],[4,4,4,2,2],[8,4,2,1,1],[2,2,2,2,2,2,1,1,1,1]]
    present_time,temp_snatch,snatch=[],[],[]
    time,temp_scale,scale=[],[],[]
    grade1,grade2=[],[]
    temp_popular,popular=[],[]
    #生成num段音乐
    for x in range(num):
        #生成一段8节音乐
        a, b,c= 0, 0,0
        for i in range(8):
            #在times里任选一个数组并随机排列
            x=random.randint(0,len(times)-1)
            present_time=times[x]
            random.shuffle(present_time)
            time.append(present_time)#用以对时值评分,交换
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
            c=c+int(b/(len(i)))
        grade=6*a+4*c
        grade1.append(grade)
    grade2=grade1
    grade2.sort(reverse=False)
    popular.append(temp_popular[grade1.index(grade2[0])])
    for i in range(1,16):
        if grade2[i]!= grade2[i-1]:
            c=grade1.index(grade2[i])
            popular.append(temp_popular[c])
        else:
            c=grade1.index(grade2[i],grade1.index(grade2[i-1]))
            popular.append(temp_popular[c])
    return popular

def judge(popular,gen):
    #人工进行评分
    value,temp_value=[],[]
    for i in range(len(popular)):
        print(popular[i])
        transfer(popular[i],gen,i+1)
        print(f"请对第{i+1}段音乐进行评分：")
        for j in range(5):
            a=int(input())
            temp_value.append(a)
        value.append(sum(temp_value)/5)
        print(sum(temp_value)/5)
        temp_value=[]
    return value

def choose_ex(popular,value):
    #淘汰末两位
    for i in range(2):
        a=min(value)
        b=value.index(a)
        c=value.index(a)
        del popular[b]
        del value[c]
    #采用轮盘赌进行选择
    probability=[]
    for i in value:
        probability.append(i/sum(value))

    probability_sum=[]
    for i in range(len(probability)):
        if i ==0:
            probability_sum.append(probability[i])
        else:
            probability_sum.append(probability_sum[i - 1] + probability[i])

    popular_new = []
    for i in range(int(len(value)/2)):
        temp=[]
        for j in range(2):
            rand = random.uniform(0, 1)
            for k in range(len(value)):
                if k == 0:
                    if rand < probability_sum[k]:
                        temp.append(popular[k])
                else:
                    if (rand > probability_sum[k-1]) and (rand < probability_sum[k]):
                        temp.append(popular[k])

        change=random.randint(0,2)
        if change==1:
            temps=temp[0][2:6]
            temp[0]=temp[0][:2]+temp[1][2:6]+temp[0][6:]
            temp[1]=temp[1][:2]+temps+temp[1][6:]
        elif change==2:
            temps=temp[0][0:5]
            temp[0] = temp[1][0:5] + temp[0][5:]
            temp[1] = temps + temp[1][5:]
        popular_new.append(temp[0])
        popular_new.append(temp[1])
    return popular_new

def variation(popular_new):
    for i in range(len(popular_new)):
        is_variation=random.uniform(0,1)
        if is_variation<0.4:
            for x in popular_new[i]:
                z=x
                x=[]
                for y in z:
                    a=list(y)
                    a[1]=12-a[1]
                    y=tuple(a)
                    x.append(y)
    return popular_new

if __name__=="__main__":
    num=200
    popular=ori(num)
    i=0
    y=[]
    while True:
         i=i+1
         fitness=judge(popular,i)
         y.append(sum(fitness) / len(popular))
         popular=choose_ex(popular,fitness)
         popular=variation(popular)
         print(popular)
         a=input('请选择是否继续[Y/N]')
         if a=="N" or a=='n':
             break

    print(y)
    x=range(1,i+1,1)
    plt.figure(figsize=(10, 10), dpi=100)
    plt.plot(x,y)
    plt.xlim(0, 8)
    plt.ylim(0, 10)
    plt.scatter(x, y, c="grey")
    plt.xlabel("genetic algebra", fontdict={'size': 16})
    plt.ylabel("value", fontdict={'size': 16})
    plt.title('the relation between value and genetic algebra', fontdict={'size': 20})
    plt.show()