# python3
import numpy as np
import tensorflow as tf
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # 关闭警告


#生成所有可能输入的数据集合，用于预测最大值
def createAllData(minGap):
    _x_ = []
    total = 0
    for r1 in np.arange(1.,20.,minGap):
        a1=max(-r1, -8)
        for delta1 in np.arange(a1+1,r1-1,minGap):
            for r2 in np.arange(1.,20.,minGap):
                a2=max(-r2, -8)
                for delta2 in np.arange(a2+1,r2-1,minGap):
                    pr1=0.
                    pr2=0.
                    if delta1>0:
                        pr1=np.sqrt(r1*r1-delta1*delta1)
                    else:
                        pr1=r1
                    if delta2>0:
                        pr2=np.sqrt(r2*r2-delta2*delta2)
                    else:
                        pr2=r2
                    for d1 in np.arange(2*pr1+1, 40, minGap):
                        for d2 in np.arange(2*pr2+1, 40, minGap):
                            for d3 in np.arange(pr1+pr2+1, 40, minGap):
                                for isCross in range(0,2,1):  #range()函数不包括end的那个数
                                    _x_.append([np.float32(r1), np.float32(r2), np.float32(delta1), np.float32(delta2), np.float32(d1), np.float32(d2), np.float32(d3), np.float32(isCross)])
                                    total = total+1
                                    if total % 10000 == 0:
                                        print("total data number is "+str(total))
    return total, _x_

def createSingleDataFromFile(file):
    _x_ = []
    with open(file, "r") as f:
        line=f.readline()
        if line.strip():
            datalist=line.strip().split(",")
            x_list = [x for x in datalist[0:8]]
            if x_list[0]:
                xnum = [np.float32(x) for x in x_list]
                _x_.append(xnum)  # 为数据个数行，8列的列表
    return 1,_x_

workingDirectory = os.path.split(os.path.realpath(__file__))[0]  # 该文件所在的目录，不是本文件的路径名，而是包含它的目录路径
import os
parent_path=os.path.dirname(workingDirectory)

total, _x_ = createSingleDataFromFile(os.path.join(parent_path, "para","givenByMATLAB.txt"))

# 将列表转化成矩阵
x_data = np.array(_x_)  # (shape:788,8)

# 归一化
data_shape = x_data.shape
rows = data_shape[0]
cols = data_shape[1]
m_normal = x_data
# xmax = x_data.max(axis=0)
# xmin = x_data.min(axis=0)
xmax = np.array([20.0, 20.0, 20.0, 20.0, 40.0, 40.0, 40.0, 1.0])
xmin = np.array([3.0, 3.0, -8.0, -8.0, 0., 0., 0., 0.0])
for i in range(rows):
    for j in range(cols - 1):  # 因为最后一列数据是bool值转化成的1和0，所以没有必要归一化，这里上限取cols-1
        # m_normal[i, j] = (xmax[j] - m_normal[i, j]) / (xmax[j] - xmin[j])
        m_normal[i, j] = (m_normal[i, j] - xmin[j]) / (xmax[j] - xmin[j])
xnormal = m_normal  # 归一化后的x_data


sess = tf.InteractiveSession()
X = tf.placeholder(tf.float32, [None, 8], name='x_input')
Y = tf.placeholder(tf.float32, [None, 1], name='y_input')
keep_prob = 1.0

W11 = tf.Variable(tf.truncated_normal([8, 1000], stddev = 0.1))
W12 = tf.Variable(tf.truncated_normal([8, 1000], stddev = 0.1))
W13 = tf.Variable(tf.truncated_normal([8, 1000], stddev = 0.1))
b1 = tf.Variable(tf.zeros([1000]) + 0.1)
#L1 = tf.matmul(X, W11) + b1
L1 = tf.matmul(tf.pow(X,3),W13)+tf.matmul(tf.square(X),W12)+tf.matmul(X,W11)+b1

# L1_drop = tf.nn.dropout(L1,keep_prob)

W21 = tf.Variable(tf.truncated_normal([1000, 2000], stddev=0.1))
W22 = tf.Variable(tf.truncated_normal([1000, 2000], stddev=0.1))
b2 = tf.Variable(tf.zeros([2000]) + 0.1)
L2 = tf.matmul(tf.square(L1), W22) + tf.matmul(L1, W21) + b2
# L2_drop = tf.nn.dropout(L2,keep_prob)

W3 = tf.Variable(tf.truncated_normal([2000, 1], stddev=0.1))
b3 = tf.Variable(tf.zeros([1]) + 0.1)
prediction = tf.matmul(L2, W3) + b3

# 代价函数及训练方法
# loss = tf.reduce_max(tf.square(tf.subtract(Y,prediction)))
loss = tf.reduce_mean(tf.abs(tf.subtract(np.float32(1), tf.div(prediction, Y))))
maxLoss = tf.reduce_max(tf.abs(tf.subtract(np.float32(1), tf.div(prediction, Y))))
train_step = tf.train.AdamOptimizer(0.001).minimize(loss)
init = tf.global_variables_initializer()
minAccuracy = tf.reduce_min(prediction / Y)


model_path =os.path.join(workingDirectory, "retrainmodel/tfmodel_chapter4_last")  # "model/tfmodel_chapter4"
saver = tf.train.Saver()
#with tf.Session() as sess2:
sess.run(init)
load_path=saver.restore(sess, model_path)
print("model restored from file: %s" % model_path)

#if total > 5000000:
#    pred=sess.run(prediction, feed_dict={X:xnormal[:5000000]})

pred = sess.run(prediction, feed_dict={X: xnormal})
print("debug python:prediction:"+str(pred[0][0]))
title=['radius1','radius2','delta1','delta2','d1','d2','d3','isCross','tp']
mergeData=np.hstack((xnormal,pred))
#输出xnormal和pred到文件“predictResult.txt”
import pandas as pd
out=pd.DataFrame(columns= title,data=mergeData)
out.to_csv(os.path.join(workingDirectory,"predictResult.csv"))

maxTP=max(pred)
print(maxTP)
location=np.where(pred==maxTP)
print(location)
#找出pred中对应的最大的10个极值




