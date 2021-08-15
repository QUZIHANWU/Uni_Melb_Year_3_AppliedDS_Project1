#!/usr/bin/env python
# coding: utf-8

# In[132]:


def data_yuchuli(data_path, month, month_days):
    import pandas as pd
    import numpy as np
    
    # 读入数据
    data = pd.read_csv(data_path)

    # 数据清洗
    temp_data = data.drop(data[data.trip_distance<3].index)
    temp_data = temp_data.drop(temp_data[temp_data.trip_distance>200].index)
    temp_data = temp_data.drop(temp_data[temp_data.passenger_count<7].index)
    temp_data = temp_data.drop(temp_data[temp_data.passenger_count>0].index)
    temp_data = temp_data.drop(temp_data[temp_data.payment_type == 1].index)
    temp_data = temp_data.drop(temp_data[temp_data.fare_amount < 2.5].index)
    temp_data = temp_data.drop(temp_data[temp_data.total_amount < 2.5].index)

    time = temp_data['lpep_pickup_datetime']
    trip_distance = temp_data['trip_distance']
    fare_amount = temp_data['fare_amount']
    extra = temp_data['extra']
    total_amount = temp_data['total_amount']
    tip_amount = temp_data['tip_amount']
    x_list = [time, trip_distance,fare_amount,extra,tip_amount]
    x_label = ['time','trip_distance','fare_amount','extra','tip_amount']


    time = np.array(time).reshape(-1,1)
    trip_distance = np.array(trip_distance).reshape(-1,1)
    fare_amount = np.array(fare_amount).reshape(-1,1)
    extra = np.array(extra).reshape(-1,1)
    total_amount = np.array(total_amount).reshape(-1,1)
    data_final = np.concatenate((time, total_amount, trip_distance,
                                fare_amount, extra),axis=1)

    data_final = pd.DataFrame(data_final, columns=['time','total_amount', 'trip_distance',
                                'fare_amount', 'extra'])
    data_final = data_final.dropna(axis=0, how='any') 


    # 获取原数据中时间序列
    # time_list = data_final.time
    time_list = data_final['time'].values.tolist()
    import datetime
    time_list_drop = []
    if month == 1:
        for i in range(len(time_list)):
            time_list_drop.append(str(time_list[i])[:9])
    else:
        for i in range(len(time_list)):
            time_list_drop.append(str(time_list[i])[:10])
    time_list_drop = pd.DataFrame(time_list_drop).drop_duplicates()


    # 读入天气数据
    tianqi = pd.read_csv("2020_01_12.csv")
    tianqi_temp = tianqi.loc[:,['DATE','TEMP']]
    tianqi_new = []
    tianqi_temp = np.array(tianqi_temp)
    if month == 1:
        for i in range(len(tianqi_temp)):
            str_date = str(tianqi_temp[i][0])
            if str_date[:7] == '2020-01':
                tianqi_new.append(tianqi_temp[i][1])
                
    if month == 2:
        for i in range(len(tianqi_temp)):
            str_date = str(tianqi_temp[i][0])
            if str_date[:7] == '2020-02':
                tianqi_new.append(tianqi_temp[i][1])
                
    if month == 3:
        for i in range(len(tianqi_temp)):
            str_date = str(tianqi_temp[i][0])
            if str_date[:7] == '2020-03':
                tianqi_new.append(tianqi_temp[i][1])
                
    if month == 4:
        for i in range(len(tianqi_temp)):
            str_date = str(tianqi_temp[i][0])
            if str_date[:7] == '2020-04':
                tianqi_new.append(tianqi_temp[i][1])
        
#     tianqi_new = tianqi.TEMP[:month_days]
    tianqi_new = np.array(tianqi_new).reshape(-1, 1)

    # 将天气和时间信息整合到一起
    time_list_new = np.array(time_list_drop).reshape(-1, 1)
    time_tianqi = np.concatenate((time_list_new, tianqi_new),axis=1)


    # 将天气整合到原数据的最后一列
    tianqi_list = []
    for j in range(len(time_tianqi)):
        for i in range(len(data_final)):
            time = data_final.time[i]
            if month == 1:
                if time[:9] == time_tianqi[j][0]:
                    tianqi_list.append(time_tianqi[j][1])
            else:
                if time[:10] == time_tianqi[j][0]:
                    tianqi_list.append(time_tianqi[j][1])

    tianqi_list = np.array(tianqi_list).reshape(-1, 1)
    data_final_new = np.array(data_final).reshape(-1,5)
    data_final_new = np.concatenate((data_final_new, tianqi_list),axis=1)
    data_final_new = pd.DataFrame(data_final_new, columns=['time','total_amount', 'trip_distance',
                                'fare_amount', 'extra', 'temp'])

    return data_final_new