import numpy as np
import tensorflow as tf
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # 关闭警告

# 储存输入数据
_x_ = []
# 储存标签数据
_y_ = []

with open('result1.txt', 'r', encoding='UTF-8') as r1:
    for line in r1.readlines():
        if not line.strip():  # 如果是空行，跳过
            continue
        wlist = line.strip().split(',')
        if (wlist[0] == 'modelName'):  # 判断标题行，如果是标题行，跳过
            continue

        x_list = [x for x in wlist[1:9]]
        if x_list[7] == 'True':
            x_list[7] = '1'
        else:
            x_list[7] = '0'

        if x_list[0]:
            xnum = [np.float32(x) for x in x_list]
            _x_.append(xnum)  # 为数据个数行，8列的列表
            _y_.append([np.float32(wlist[16])])  # 为数据个数行，1列的列表
# 将列表转化成矩阵
x_data = np.array(_x_)  # (shape:788,8)
y_data = np.array(_y_)  # (shape:788,1)

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

percentOfTest = 0.7
dataSplitRows=int(rows*percentOfTest)
print("共有"+str(rows)+"个数据，前"+str(dataSplitRows)+"个用于训练，后"+str(rows-dataSplitRows)+"个用于测试")
xTrain = xnormal[:dataSplitRows]
yTrain = y_data[:dataSplitRows]
xTest = xnormal[dataSplitRows:]
yTest = y_data[dataSplitRows:]

batch_size = 50
Nbatch = xTrain.shape[0] // batch_size

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
L3=tf.matmul(L2,W3)+b3

W4=tf.Variable(tf.truncated_normal([], stddev=0.1))
b4=tf.Variable(tf.zeros([1])+0.1)
#prediction=tf.matmul(L3,W4)+b4

# 代价函数及训练方法
# loss = tf.reduce_max(tf.square(tf.subtract(Y,prediction)))
loss = tf.reduce_mean(tf.abs(tf.subtract(np.float32(1), tf.div(prediction, Y))))
maxLoss = tf.reduce_max(tf.abs(tf.subtract(np.float32(1), tf.div(prediction, Y))))
train_step = tf.train.GradientDescentOptimizer(0.05).minimize(loss)
init = tf.global_variables_initializer()
minAccuracy = tf.reduce_min(prediction / Y)


sess.run(init)
for __epo in range(10000):
    for __batch in range(Nbatch):
        # 将样本和标签根据划分的batch导入程序中
        if __batch == Nbatch - 1:  # 把余数中的数据放在最后一个batch中
            batch_xs = xTrain[__batch * batch_size:]
            batch_ys = yTrain[__batch * batch_size:]
        else:
            batch_xs = xTrain[__batch * batch_size:(__batch + 1) * batch_size]
            batch_ys = yTrain[__batch * batch_size:(__batch + 1) * batch_size]
        sess.run(train_step, feed_dict={X: batch_xs, Y: batch_ys})
    train_acc = sess.run(minAccuracy, feed_dict={X: xTrain, Y: yTrain})
    train_loss = sess.run(loss, feed_dict={X: xTrain, Y: yTrain})
    print('循环第' + str(__epo) + '次：', '最小准确率,训练准确率：', train_acc, 1-train_loss)
saver=tf.train.Saver()
saver.save(sess, "model/tfmodel_chapter4.ckpt")

print('测试数据最小准确率：', sess.run(minAccuracy, feed_dict={X: xTest, Y: yTest}))
print('测试数据平均准确率：', 1-sess.run(loss, feed_dict={X: xTest, Y: yTest}))
TP_prime=sess.run(prediction, feed_dict={X:xnormal})
for i in range(rows):
    real_loss=np.square(1-TP_prime[i]/y_data[i])
    if (real_loss>0.01):
        print("第"+str(i)+"个数据，预测TP为："+str(TP_prime[i])+";实际TP为："+str(y_data[i])+";相对误差为："+str(1-TP_prime[i]/y_data[i]))
