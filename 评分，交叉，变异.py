def judge(popular):
    #人工进行评分
    value=[]
    for i in range(len(popular)):
        print(popular[i])
        a=int(input(f"请对第{i+1}段音乐进行评分："))
        value.append(a)
    return value

def choose_ex(popular,value):
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
        temp = []
        for j in range(2):
            rand = random.uniform(0, 1)
            for k in range(len(value)):
                if k == 0:
                    if rand < probability_sum[k]:
                        temp.append(popular[k])
                else:
                    if (rand > probability_sum[k-1]) and (rand < probability_sum[k]):
                        temp.append(popular[k])

        change=random.randint(0,1)
        if change:
            temps=temp[0][2:5]
            temp[0]=temp[0][:2]+temp[1][2:5]+temp[0][5:]
            temp[1]=temp[1][:2]+temps+temp[1][5:]
        popular_new.append(temp[0])
        popular_new.append(temp[1])

    return popular_new

def variation(popular_new):
    for i in range(len(popular_new)):
        is_variation=random.uniform(0,1)
        if is_variation<0.05:
            for x in popular_new[i]:
                for y in x:
                    y[1]=12-y[1]
    return popular_new
