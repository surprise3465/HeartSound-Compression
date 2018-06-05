
import numpy as np

train_data = np.array([[1, "S", -1], [1, "M", -1], [1, "M", 1], [1, "S", 1], [1, "S", -1],
                       [2, "S", -1], [2, "M", -1], [2, "M", 1], [2, "L", 1], [2, "L",  1],
                       [3, "L",  1], [3, "M",  1], [3, "M", 1], [3, "L", 1], [3, "L", -1]])

test_data = np.array([2, "S"])

fea = [{"1": 0, "2": 0, "3": 0}, {"S": 0, "M": 0, "L": 0}]
Y = {"-1": 0, "1": 0}

fea_concat_y = {}

train_set_num = len(train_data)

for i in range(train_set_num):
    data = train_data[i]
    size = len(data)
    '''
    key = x0,y or x1,y
    '''
    for j in range(size-1):
        fea[j][str(data[j])] = fea[j][str(data[j])] + 1
        key = data[j] + ',' + data[size-1]
        if key not in fea_concat_y:
            fea_concat_y[key] = 1
        else:
            fea_concat_y[key] = fea_concat_y[key] + 1
    Y[data[size-1]] = Y[data[size-1]] + 1

'''
特征个数 len(test_data)
'''

p_result = .0
predict_label = ''
for y in Y:
    p_y = Y[y]*1.0 / train_set_num
    p_mul = p_y
    for j in range(len(test_data)):
        key = test_data[j]+',' + y
        p_x_1_y = fea_concat_y[key]*1.0 / train_set_num / p_y
        p_mul = p_mul * p_x_1_y
    if p_mul > p_result:
        p_result = p_mul
        predict_label = y
print("test case is:", test_data)
print("predict label is:", predict_label)
print("prob is", p_result)