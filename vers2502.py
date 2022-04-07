import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import dateutil.relativedelta
import os

def date_year_month(): #определение предыдущего месяца и года
    date_now = datetime.now() - dateutil.relativedelta.relativedelta(months=1)
    d = date_now.strftime("%Y%m")
    return d

def table_find(table): #нахождение .csv по сформированному пути и отбор колонок
    if  os.path.isfile(table) is True:
        data = pd.read_csv(table, encoding= 'utf-8', delimiter=';')
        if 'Дата акта'in data.columns and 'ИНН' in data.columns and 'КПП' in data.columns  and 'Имя файла документа'in data.columns: 
            df = data[['Дата акта', 'ИНН', 'КПП', 'Имя файла документа']]
            attention = 'Файл по пути: '+ table + ' найден' 
            with open(the_end_txt, "a") as file:
                        file.write(attention)
                        file.write('\n')
            return df
        
        else:   # поиск колонки, которая была не найдена в .csv и занесение информации в .txt   
            a = ['Дата акта', 'ИНН', 'КПП', 'Имя файла документа']
            for i in a:
                if i in data.columns:
                    continue
                else:
                    error = 'Файл по пути: '+ table + ' не был использован, т.к. не найдена колонка: ' + str(i) 
                    with open(the_end_txt, "a") as file:
                        file.write(error)
                        file.write('\n')
                        
    else: #если .csv не найден по указанному пути, прописывать информацию в .txt
        error = 'файл по пути: '+ table + ' не найден'
        with open(the_end_txt, "a") as file:
            file.write(error)
            file.write('\n')
            
def path_formation(df, new_link): #формирование пути с указанием названия документа
    try:
        df['путь до документа'] = new_link
        df['путь до документа'] = df['путь до документа'].astype(str) + df['Имя файла документа'].astype(str)
        return df
    except:
        pass

def normalize_kpp(df):#нормализация кпп из float в int
    try:
        df['КПП'] =  df['КПП'].fillna(0)
        df['КПП'] =  df['КПП'].astype(str) 
        for i in range(len(df['КПП'])):
            if df['КПП'][i]== '0.0' or df['КПП'][i]== '0':
                df['КПП'][i] = None
            elif df['КПП'][i][-2:]== '.0':
                df['КПП'][i] = df['КПП'][i][:-2]
            else:
                 df['КПП'][i] = df['КПП'][i]
        df['КПП'] = df['КПП'].str.zfill(9)
        return df
    except:
        pass

def unication(*args):#объединение всех имеющихся .csv
    try:
        unified_table = pd.concat([*args], ignore_index=True)
        return unified_table
    except:
        pass
    
def table_creation():# создание и сохранение новой .csv
    try:    
        the_end_dop = str(the_end)+str(date_year_month())+str(csv_dop)
        new.to_csv(the_end_dop, encoding= 'utf-8', header=True, index=False, sep=';')
        way = 'Файл для отправки сформирован'
        with open(the_end_txt, "a") as file:
            file.write(way)
        return new
    except:
        error = 'Файл для отправки актов не был сформирован. По возникшим вопросам обращайтесь в техподдержку ООО "Тензор"'
        with open(the_end_txt, "a") as file:
            file.write(error)
        
def normalization_date():#преобразование даты акта в "гг-мм-дд"
    try:  
        new['Дата акта'] = pd.to_datetime(new['Дата акта']).dt.normalize()
        return new
    except:
        pass
    
link = 'C:\\Users\\pered\\OneDrive\\Рабочий стол\\EDO\\'
link1, link2, link3 ='-AR\\АКТ_РАБОТ', '-ARC\\АКТ_КОР', '-AS\\АКТ_СВЕРКИ'
link1_dop, link2_dop, link3_dop = '-AR\\', '-ARC\\', '-AS\\'
csv_dop = '.csv'
txt_dop = '.txt'


new_link1 = str(link)+str(date_year_month())+str(link1)+str(csv_dop) #формирование пути
new_link2 = str(link)+str(date_year_month())+str(link2)+str(csv_dop)  #формирование пути
new_link3 = str(link)+'quarter\\'+str(date_year_month())+str(link3)+str(csv_dop) #формирование пути
the_end = 'C:\\СБИС Коннект\\Отправляемые\\' #путь конечного csv 
the_end_txt = str(the_end)+str(date_year_month())+str(txt_dop) #путь итогового txt

result = open(the_end_txt, "w+")  #создание .txt для передачи информации

df1 = table_find(new_link1)
df2 = table_find(new_link2)
df3 = table_find(new_link3)

df1 = normalize_kpp(df1)
df2 = normalize_kpp(df2)
df3 = normalize_kpp(df3) 

new_link_dop1 = str(link) + str(date_year_month()) + str(link1_dop) #путь до документа
new_link_dop2 = str(link) + str(date_year_month()) + str(link2_dop) #путь до документа
new_link_dop3 = str(link) + str(date_year_month()) + str(link3_dop) #путь до документа

df_1 = path_formation(df1, new_link_dop1)
df_2 = path_formation(df2, new_link_dop2)
df_3 = path_formation(df3, new_link_dop3) 

new = unication(df_1, df_2, df_3)

new = normalization_date() 

new = table_creation() #сохранение таблицы

display(new)