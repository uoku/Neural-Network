import random
import tkinter as tk
from tkinter import filedialog
import math
import matplotlib.pyplot as plt
import numpy as np


def dataProcess(file):
    list = []
    file = open(file, mode='r')
    clas = []
    for line in file.readlines():
        line = line.split(' ')
        line[-1] = line[-1].replace('\n', '')
        # take answer
        clas.append(line[-1])
        line.insert(0, '-1')
        list.append(line)
    file.close()
    set1 = set(clas)
    class_num = len(set1)
    dic = {}
    gap = 1/class_num
    c = 0
    for obj in set1:
        dic[obj] = c
        c +=1
    for obj in range(len(list)):
        list[obj][-1] = dic[list[obj][-1]]
    return list, len(list[0]) - 2, dic, class_num


def dot(x, w):
    t = len(x)
    tol = 0.
    for i in range(t):
        x[i], w[i] = float(x[i]), float(w[i])
        tol += x[i] * w[i]
    return tol


def pred_acc(test_data, W, class_num):
    tol = len(test_data)
    correct = 0
    gap = 1/class_num
    for data in test_data:
        ans = int(data[-1])
        data = data[:-1]
        v = dot(data, W)
        predict = int((1 / (1 + math.exp(-v)))/gap)
        # print(data,' ',ans,' ',predict,' ',(1 / (1 + math.exp(-v))))
        if predict == ans:
            correct += 1
    acc = (correct / tol) * 100
    return acc


path = None
window = tk.Tk()
window.title('感知機訓練')
window.geometry('500x500')
window.configure(background='gray')
var = tk.StringVar()
label = tk.Label(window, textvariable=var, bg='white', width=15, height=3)
label.pack()


def openfile():
    global path
    path = filedialog.askopenfilename()
    show = path.split('/')
    var.set(show[-1])


button = tk.Button(window, text='choose data', width=10, height=2, command=openfile)
button.pack()

tk.Label(window, text="學習率", width=10, height=2, bg='red').pack()
rate = tk.Entry(window, show=None)
rate.pack()

tk.Label(window, text="收斂條件", width=10, height=2, bg='red').pack()
frame = tk.Frame(window)
frame.pack()

frame_left = tk.Frame(frame)
frame_r = tk.Frame(frame)
frame_left.pack(side='left')
frame_r.pack(side='right')
tk.Label(frame_left, text="epoch", width=10, height=1, bg='green').pack()
epoch = tk.Entry(frame_r, show=None)
epoch.pack()
tk.Label(frame_left, text="訓練準確度", width=10, height=1, bg='green').pack()
req_acc = tk.Entry(frame_r, show=None)
req_acc.pack()
tk.Label(window, text="(若無法達到就不會停止)", width=20, height=1, bg='green').pack()


def start_train():
    '''
    print(epoch.get())
    print(req_acc.get())
    print(path)
    print(rate)
    '''
    t = int(epoch.get())
    learn_rate = float(rate.get())
    re_acc = int(req_acc.get())
    w_range = [-1, 1]
    D, dim, dic, class_num = dataProcess(path)
    #print(list)
    #raise Exception


    # data split
    random.shuffle(D)
    l = len(D)
    test_data = D[0:int(l / 3)]
    train_data = D[int(l / 3):]
    # data split

    # init w(0) , a,b is init range a<b
    a, b = w_range[0], w_range[1]
    W1 = []
    for i in range(dim + 1):
        Wi = random.uniform(-1,1)
        W1.append(Wi)

    predict = None
    if t == 0:
        t = 9999999999
    for i in range(t):
        for data in train_data:
            ans = int(data[-1])
            data = data[:-1]
            v = dot(data, W1)
            predict = 1 / (1 + math.exp(-v))
            gap = 1 / class_num
            # Correction
            if predict < (ans*gap) or predict > ((ans+1)*gap):
                if ans == 0:
                    for num in range(len(W1)):
                        W1[num] = W1[num] + learn_rate*((0-predict)*predict*(1-predict))*int(data[num])
                elif ans == class_num-1:
                    for num in range(len(W1)):
                        W1[num] = W1[num] + learn_rate * ((1 - predict) * predict * (1 - predict)) * int(data[num])
                else:
                    for num in range(len(W1)):
                        aim = ans*gap + gap / 2
                        W1[num] = W1[num] + learn_rate * ((aim - predict) * predict * (1 - predict)) * int(data[num])
        print(W1)
        temp = pred_acc(train_data, W1, class_num)
        print(temp,"%")
        random.shuffle(train_data)
        if temp >= re_acc:
            break


    # now have all result
    print(pred_acc(train_data, W1, class_num),'%')
    print(pred_acc(test_data, W1, class_num),'%')

    # need to print picture
    org_list = list(dic.keys())
    # plt.plot([1,2],[2,1],'ro') print example
    zero_x = []
    zero_y = []
    one_x = []
    one_y = []
    two_x = []
    two_y = []
    gap = 1 / class_num
    for test in D:
        ans = test[-1]
        input = test[:-1]
        v = dot(input, W1)
        predict = int((1 / (1 + math.exp(-v))) / gap)
        if predict == 0:
            zero_x.append(input[1])
            zero_y.append(input[2])
        elif predict == 1:
            one_x.append(input[1])
            one_y.append(input[2])
        else:
            two_x.append(input[1])
            two_y.append(input[2])

    plt.plot(zero_x,zero_y,'ro')
    plt.plot(one_x,one_y,'bo')
    plt.plot(two_x,two_y, 'go')

    plt.xlabel("x-axis")
    plt.ylabel("y-axis")

    plt.show()







tk.Button(window, text="開始訓練", width=10, height=2, command=start_train).pack()

window.mainloop()

'''
# init parameter
learn_rate = 1
Threshold = -1
w_range = [-3, 3]

# list is data, dim

list, dim = dataProcess('2Ccircle1.txt')

# data split
random.shuffle(list)
l = len(list)
test_data = list[0:int(l / 3)]
train_data = list[int(l / 3):]
# data split

# init w(0) , a,b is init range a<b
a, b = w_range[0], w_range[1]
W = []
for i in range(dim + 1):
    Wi = int(random.randint(a, b))
    W.append(Wi)

predict = None
# train process
for data in train_data:
    data = data[:-1]
    v = dot(data, W)
    if v >= 0:
        predict = 2
    else:
        predict = 1
    # Correction
    if predict != data[dim]:
        if v < 0:
            for i in range(dim + 1):
                W[i] = W[i] + data[i] * learn_rate
        else:
            for i in range(dim + 1):
                W[i] = W[i] - data[i] * learn_rate
    print(W)

print(pred_acc(test_data, W))
'''
