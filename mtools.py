import datetime
import pandas as pd
import numpy as np

class Ind:
    '''ставится в конец цикла и на вход принимает итерируемый объект для определения его длины'''
    i = 0
    def __init__(self, lst):
        if Ind.i == 0:
            Ind.start_time = datetime.datetime.now()
            Ind.length = len(lst)
        Ind.i += 1
        done = Ind.i
        total = Ind.length
        percent = (done / total * 100)
        time_diff = (datetime.datetime.now() - Ind.start_time).seconds
        time_dif = f"{time_diff // (60 * 60):03d} h {(time_diff - time_diff // (60 * 60) * 3600) // 60 :02d} min {time_diff % 60:02d} sec"

        total_bar = round((percent / 100) * 50) * '●' + (50 - round((percent / 100) * 50)) * '○'
        print(f'{total_bar} {percent:.2f}% {done}/{total} || {time_dif}', end='\r')
        if total == done:
            Ind.i = 0
            print('')

class MixinVis:
    def make_vis(self,col):
        self.col_name = col.name
        row_vis = ''
        
        #алгоритм для колонок со значениями <=20
        if col.unique_values <=20:
            temp_df = self.df.groupby(col.name,as_index=False,dropna=False)['tech_column_for_count'].count().sort_values(col.name)
            temp_df['diff'] = temp_df.apply(lambda x: temp_df['tech_column_for_count'].max(),axis=1)
            temp_df['height'] = temp_df.apply(lambda x: x['tech_column_for_count'] / x['diff'] * 15 //1,axis=1)
            
            for _ in range(1,15)[::-1]:
                for index,row in temp_df.iterrows():
                    if row['height'] >= _:
                        row_vis += '○  '
                    else:
                        row_vis += '   '
                row_vis += '\n'
            for index,row in temp_df.iterrows():
                row_vis += '¯  '
            
            row_vis+='\n'
            for index,row in temp_df.iterrows():
                row_vis += str(index) + ' '*(3-len(str(index)))
                
            row_vis += '\n______________________________________________________\n'
            
            for index,row in temp_df.iterrows():
                row_vis+=f"{index} - {row[col.name]} ~({round(row['tech_column_for_count'])})\n"
            return row_vis
        
        elif col.type in ('int','float'):
            self.temp_df = self.df[[col.name,'tech_column_for_count']]
            self.temp_df['diff'] = self.temp_df[col.name].apply(lambda x: self.temp_df[col.name].max() - self.temp_df[col.name].min())
            self.temp_df['min'] = self.temp_df[col.name].apply(lambda x: self.temp_df[col.name].min())
            min_temp = self.temp_df[col.name].min()
            max_temp = self.temp_df[col.name].max()
            self.temp_df['max'] = self.temp_df[col.name].apply(lambda x: (self.temp_df[col.name].max() - self.temp_df[col.name].min()))
            self.temp_df['normalized'] = self.temp_df.apply(lambda x: x[col.name] - x['min'],axis=1)
            self.temp_df['bar_intervals'] = self.temp_df.apply(lambda x: x['normalized']/x['max'] * 15//1,axis=1)
            self.temp_df = self.temp_df.groupby('bar_intervals',as_index=False,dropna=False)['tech_column_for_count'].count().sort_values('bar_intervals')
            
            temp_df = self.temp_df
            temp_df['diff'] = temp_df.apply(lambda x: temp_df['tech_column_for_count'].max(),axis=1)
            temp_df['height'] = temp_df.apply(lambda x: x['tech_column_for_count'] / x['diff'] * 15 //1,axis=1)
            
            for _ in range(1,15)[::-1]:

                for index,row in temp_df.iterrows():
                    if row['height'] >= _:
                        row_vis += '○  '
                    else:
                        row_vis += '   '
                row_vis += '\n'
            for index,row in temp_df.iterrows():
                row_vis += '¯  '
            row_vis+='\n'
            for index,row in temp_df.iterrows():
                row_vis += str(index) + ' '*(3-len(str(index)))
            
            nan = False
            if sum(self.temp_df['bar_intervals'].isna())>0:
                nan = len(self.temp_df['bar_intervals'])-1
                row_vis+='\n'+' '*(len(self.temp_df['bar_intervals'])*3-3) + '^ \n'
                row_vis+=' '*(len(self.temp_df['bar_intervals'])*3-3) + '^\n'
                row_vis+=' '*(len(self.temp_df['bar_intervals'])*3-3) + '^\n'
                row_vis+=' '*(len(self.temp_df['bar_intervals'])*3-3) + 'NA\n'
            row_vis += '______________________________________________________\n'
            
            for index,row in temp_df.iterrows():
                row_vis+=f"{index} - [{round(min_temp + (max_temp-min_temp)*index/len(temp_df),2) if nan != index else 'nan'}-{round(min_temp + (max_temp-min_temp)*(index+1)/len(temp_df),2) if nan != index else 'nan'}) ~{round(row['tech_column_for_count'])}\n"
            
        else:
            row_vis += f'no visualisation for {col.type}'
        return row_vis
    
        

class StatisticsColumn:
    def __init__(self,column):
        self.column = column
        try:
            self.type = str(type(max(column.dropna()))).replace("<class '",'').replace("'>",'')
        except:
            self.type = 'empty'
        self.name = column.name
        self.unique_values = len(column.unique())
        try:
            self.min = self.max_val()
        except:
            self.min = '-'
        try:
            self.max = self.min_val()
        except:
            self.max = '-'
        self.len = len(column)
        self.na = '-' if str(round(sum(column.isna()) / len(column)*100))+'%' =='0%' else str(round(sum(column.isna()) / len(column)*100))+'%'
        self.avg = '-' if self.type not in ('int','float') else round(self.column.mean(),2)
        self.std = '-' if self.type not in ('int','float') else round(self.column.std(),2)
        self.med = '-' if self.type not in ('int','float') else round(self.column.median(),2)

    def max_val(self):
        if self.type in ('int','float','datetime.date'):
            if self.type in ('int','float','datetime.date'):         
                return round(self.column.min(),2)
            else:
                return self.column.min()
        else:
            return '-'
    def min_val(self):
        if self.type in ('int','float','datetime.date'):
            if self.type in ('int','float','datetime.date'):         
                return round(self.column.max(),2)
            else:
                return self.column.max()
        else:
            return '-'
        
        
class StatisticsDF(MixinVis):
    def __init__(self,df):
        import warnings
        warnings.filterwarnings('ignore')
        self.check_type(df)
        self.df = df
        self.columns = self.get_columns()
        self.stat_col=[]
        self.column_statistics()
        self.stat_col= sorted(self.stat_col,key = lambda x: x.unique_values)
        self.mem_usage = f'{round(self.df.memory_usage().sum()/1024/1024,2)} Mb'
        
        
        self.repr_len_dict={}
        self.repr_dict()
        
    def repr_dict(self):
        self.repr_len_dict['name'] = 0
        for each in self.stat_col:
            if self.repr_len_dict['name'] < len(each.name):
                self.repr_len_dict['name'] = len(each.name)
                
        self.repr_len_dict['type'] = 0
        for each in self.stat_col:
            if self.repr_len_dict['type'] < len(each.type):
                self.repr_len_dict['type'] = len(each.type) 
                
        self.repr_len_dict['unique_values'] = 0
        for each in self.stat_col:
            if self.repr_len_dict['unique_values'] < len(str(each.unique_values)):
                self.repr_len_dict['unique_values'] = len(str(each.unique_values))
                
        self.repr_len_dict['max'] = 0
        for each in self.stat_col:
            if self.repr_len_dict['max'] < len(str(each.max)):
                self.repr_len_dict['max'] = len(str(each.max))
                
        self.repr_len_dict['min'] = 0
        for each in self.stat_col:
            if self.repr_len_dict['min'] < len(str(each.min)):
                self.repr_len_dict['min'] = len(str(each.min))
                
        self.repr_len_dict['len'] = 0
        for each in self.stat_col:
            if self.repr_len_dict['len'] < len(str(each.len)):
                self.repr_len_dict['len'] = len(str(each.len))
                
        self.repr_len_dict['avg'] = 0
        for each in self.stat_col:
            if self.repr_len_dict['avg'] < len(str(each.avg)):
                self.repr_len_dict['avg'] = len(str(each.avg))
                
        self.repr_len_dict['std'] = 0
        for each in self.stat_col:
            if self.repr_len_dict['std'] < len(str(each.std)):
                self.repr_len_dict['std'] = len(str(each.std))
            
        
    def check_type(self,df):
        if not isinstance(df,pd.core.frame.DataFrame):
            raise Exception('Only for pandas.core.frame.DataFrame')
    def get_columns(self) -> list:
        return list(self.df.columns)
    
    def column_statistics(self):
        i=1
        for each in self.columns:
            print(f'Processing {each}  {i}/{len(self.columns)}',end='\r')
            self.stat_col.append(StatisticsColumn(self.df[each]))
            i+=1
            print(' '*1000,end='\r')
    def __repr__(self):
        text = f'len = {len(self.df)}\n'
        text+= f'{self.mem_usage}\n'
        text+= f"name  {' '*(self.repr_len_dict['name']-len('name'))}"
        text+= f"type  {' '*(self.repr_len_dict['type']-len('type'))}"
        text+= f"unique  {' '*(max(self.repr_len_dict['unique_values'],len('unique'))-len('unique'))}"
        text+= f"na  {'   '}"
        text+= f"min  {' '*(self.repr_len_dict['min']-len('min'))}"
        text+= f"max  {' '*(self.repr_len_dict['max']-len('max'))}"
        text+= f"std  {' '*(self.repr_len_dict['std']-len('std'))}"
        text+= f"avg  {' '*(self.repr_len_dict['avg']-len('avg'))}"
        text+='\n\n'
        for each in self.stat_col:
            text+= f"{each.name}  {' '*(self.repr_len_dict['name']-len(each.name))}"
            text+= f"{each.type}  {' '*(self.repr_len_dict['type']-len(each.type))}"
            text+= f"{each.unique_values}  {' '*(max(self.repr_len_dict['unique_values'],len('unique'))-len(str(each.unique_values)))}"
            text+= f"{each.na}  {' ' * (5-len(each.na))}"
            text+= f"{each.min}  {' '*(self.repr_len_dict['min']-len(str(each.min)))}"
            text+= f"{each.max}  {' '*(self.repr_len_dict['max']-len(str(each.max)))}"
            text+= f"{each.std}  {' '*(self.repr_len_dict['std']-len(str(each.std)))}"
            text+= f"{each.avg}  {' '*(self.repr_len_dict['avg']-len(str(each.avg)))}"
            text+= f"\n"
        return text
    
    def __getitem__(self,value):
        if not value in self.df.columns:
            raise AttributeError('No such column')
            
        self.df['tech_column_for_count'] = self.df.iloc[:,0].apply(lambda x: 1)
        col = StatisticsColumn(self.df[value])

        text=''
        text+= f"Name   {col.name}\n"
        text+= f"Len    {col.len}\n"
        text+= f"Type   {col.type}\n"
        text+= f"Unique {col.unique_values}\n"
        text+= f"NA %   {col.na}\n"
        text+= f"Std    {col.std}\n"
        text+= f"Avg    {col.avg}\n\n"
        text+= f"Min {col.min} ->Med {col.med} -> Max {col.max}\n"
        text += '______________________________________________________\n'
        text+=self.make_vis(col)
        
        print(text)
        del self.df['tech_column_for_count']
        
    def print_stat(self):
        print(self)
# x = StatisticsDF(df)
# x['latitude']
