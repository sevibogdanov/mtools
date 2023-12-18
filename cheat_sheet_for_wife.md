# Шпаргалка
В начале каждого файла нужно импортировать библиотеку pandas  
```import pandas as pd```

### Забираем данные

---
<details> 
<summary> Забираем excel </summary>

```df = pd.read_excel(r"test.xlsx", sheet_name='list1')```  
__sheet_name__ - необязательный параметр, если лист один, то выберет его самостоятельно
</details>

<details>
<summary> Забираем csv </summary>

```df = pd.read_csv(r"test.csv", sep=',',encoding='utf8')```  
__sep__ - какой разделитель в csv (запятая, двоеточие, точка с запятой и проч.)  
__encoding__ - нужен для корректного отобрааения кириллицы
</details>

<details> 
<summary> Забираем из БД </summary>

```df = pd.read_sql("select * from test_table", con=connection)```   
__con__ - подключение к БД (прописано в отдельном файле)
</details>

---
### Фильтация

Все записи, где column1 __РАВНА__ 1 (int)  
```df[(df['column1'] == 1)]```

Все записи, где column2 __РАВНА__ 'abcd' (str)  
```df[(df['column2'] == 'abcd')]```

Все записи, где column2 равна 'abcd' (str) __И__ column1 равна 1 (int)
```
df[
    (df['column2'] == 'abcd') & 
    (df['column1'] == 1)
    ]
```
Все записи, где column2 равна 'abcd' (str) __ИЛИ__ column1 равна 1 (int)
```
df[
    (df['column2'] == 'abcd') | 
    (df['column1'] == 1)
    ]
```

Все записи, где column2 __СОДЕРЖИТ__ 'cd' (str)  
```
df[
    (df['column2'].str.contains('cd'))
    ]
```

__ОБРАТНЫЙ ФИЛЬТР__ ~ Все записи, где column2 __НЕ СОДЕРЖИТ__ 'cd' (str)  
```
df[
    ~(df['column2'].str.contains('cd'))
    ]
 ```

Все записи, где column2 __ПРИНАДЛЕЖИТ СПИСКУ__  
```
df[
    (df['column2'].isin(['ab','bc','abcd']))
    ]
```
* в качестве списка можно передать колонку 
```
df[
    (df['column2'].isin(df2['other_df_column']))
    ]
```
---
### Сортировка
```df.sort_values('column',ascending=False)```  
__ascending__ - False это по убыванию, True это по возрастанию

### Группировка
```df.groupby(['column1','column2'],as_index=False).count()```  
__count()__ - считает кол-во
__sum()__ - считает сумму

### Запись в excel
```df.to_excel(r'result.xlsx',as_index=False)```  
Вместо reuslt.xlsx можно добавить путь с именем файла, как он будет сохранен

## Джойн (проще чем в SQL)

```
df_1.merge(
            df_2, # какую таблицу прикрепляем
            how='left', # вид джойна (например, left)
            left_on = ['col1','col2'], #список или одна колонка из df_1
            right_on = ['col_1','col_2'] #список или одна колонка из df_2
            )
```
