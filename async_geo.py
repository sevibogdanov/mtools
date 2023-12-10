import pandas as pd
from multiprocessing import Pool
import random
from math import sin, cos, sqrt, atan2, radians
import warnings
import datetime

#кол-во потоков для обработки
num_proc = 6

start_time = datetime.datetime.now()
warnings.filterwarnings("ignore")

def distance(lat1,lon1,lat2,lon2):
    '''функция определеяет расстояние от одной точки до другой'''
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = 6373.0 * c
    return distance

#создаем два датафрейма длиной в 1000 строк со случайными координатами
dl = 1000 #длина датафреймов
name1 = ['left ' + str(i) for i in range(dl)]
x1 = [random.randint(40,90) for i in range(dl)]
y1 = [random.randint(40,90) for i in range(dl)]
name2 = ['right ' + str(i) for i in range(dl)]
x2 = [random.randint(40,90) for i in range(dl)]
y2 = [random.randint(40,90) for i in range(dl)]

df_left = pd.DataFrame({'name_left':name1,
                    'lat':x1,
                    'lon':y1})

df_right = pd.DataFrame({'name_right':name2,
                    'latitude':x2,
                    'longitude':y2})

# добавляем поля в первый датафрейм
df_left['latitude'] = df_left['lat'].apply(lambda x: None)
df_left['longitude'] = df_left['lat'].apply(lambda x: None)
df_left['name_right'] = df_left['lat'].apply(lambda x: None)
df_left['dist'] = df_left['lat'].apply(lambda x: None)

# функция для обработки части датафрейма
def parts(arg):
    df_left = arg[0] #основной датафрейм
    df_right = arg[1] #датафрейм для сравнения
    start = arg[2] #начало конкретной части датафрейма
    finish = arg[3] #конец части датафрейма
    '''функция принимает два исходных датафрейма, выбирает часть первого от start до finish'''
    df1 = df_left.iloc[start:finish]
    df2 = df_right

    for ind, row in df1.iterrows():
        df2['temp_dist'] = df2.apply(lambda x: distance(x['latitude'],
                                                        x['longitude'],
                                                        row['lat'],
                                                        row['lon']), axis=1)
        df1['latitude'].iloc[ind - start] = df2[df2['temp_dist'] == df2['temp_dist'].min()]['latitude'].iloc[0]
        df1['longitude'].iloc[ind - start] = df2[df2['temp_dist'] == df2['temp_dist'].min()]['longitude'].iloc[0]
        df1['name_right'].iloc[ind - start] = df2[df2['temp_dist'] == df2['temp_dist'].min()]['name_right'].iloc[0]
        df1['dist'].iloc[ind - start] = df2['temp_dist'].min()

    return df1

def ranges_list(df_len, parts):
    '''функция готовит список [start,end] согласно желаемому числу процессов по обработке'''
    range_list = []
    start = 0
    iter = df_len // parts
    last_part = df_len % parts

    for each in range(parts):
        if each == parts - 1:
            range_list.append([start, start + iter + last_part])
        else:
            range_list.append([start, start + iter])
            start += iter
    return range_list

df_list = []
processes = num_proc

#создаем список аргументов для обработки и подстановки в функцию
for each in ranges_list(len(df_left), processes):
    df_list.append([df_left, df_right, each[0], each[1]])

#параллельная обработка
if __name__ == '__main__':
    with Pool(processes) as p:
        x = p.map(parts, df_list)
        print(f'Finish {num_proc} {datetime.datetime.now() - start_time}')


