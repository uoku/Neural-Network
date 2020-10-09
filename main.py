import random
import tkinter as tk
from tkinter import filedialog


def dataProcess(file):
    list = []
    file = open(file, mode='r')
    for line in file.readlines():
        line = line.split(' ')
        line[-1] = line[-1].replace('\n', '')
        line.insert(0, -1)
        list.append(line)
    file.close()
    return list, len(list[0]) - 2


def dot(x, w):
    t = len(x)
    tol = 0.
    for i in range(t):
        x[i], w[i] = float(x[i]), float(w[i])
        tol += x[i] * w[i]
    return tol


def pred_acc(test_data, W):
    acc = None
    tol = len(test_data)
    correct = 0
    for data in test_data:
        ans = int(data[-1])
        data = data[:-1]
        v = dot(data, W)
        if (v < 0) & (ans == 1.):
            correct = correct + 1
        if (v >= 0) & (ans == 2.):
            correct = correct + 1
    print(correct)
    acc = (correct / tol) * 100
    return acc


window = tk.Tk()
window.title('感知機訓練')
window.geometry('500x500')
window.configure(background='gray')


def openfile():
    path = filedialog.askopenfilename()
    print(path)


button = tk.Button(window, text='print', width=10, height=1, command=openfile)
button.pack()
window.mainloop()

# init parameter
learn_rate = 1
Threshold = -1
w_range = [-3, 3]

# list is data, dim
list, dim = dataProcess('2CloseS.txt')

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
