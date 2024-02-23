import pandas as pd 
import dataparser 
from  math import log
import numpy as np
import pickle
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import re
from geopy.geocoders import Nominatim

def parse_addr(cdata):
    addarr=cdata['adress']
    addrdic={}

    def get_metro_station_coordinates(station_name):
        geolocator = Nominatim(user_agent="metro_locator")  

        # Добавим "метро" к запросу для более точного результата
        location = geolocator.geocode(f"{station_name} , Москва")

        if location:
            coordinates = (location.latitude, location.longitude)
            return coordinates
        else:
            print(f"Координаты для станции метро {station_name} не найдены.")
            return None

    for i in addarr:
        try:
            if i in addrdic.keys():
                continue
            addrdic[i] = get_metro_station_coordinates(i)
        except:
            pass

    with open('coordinates', 'wb') as file:
        pickle.dump(addrdic, file)
    return addrdic

def splbac(s,f):
    return (s[:s.find(f)],s[s.find(f):])

def splfron(s,f):
    return (s[:s.find(f)+len(f)],s[s.find(f)+len(f):])

def splfb(f,s1,s2):
    return splbac(splfron(f,s1)[1],s2)[0]

def parse_rental(s):
    arr=s.split(',')+['']
    p1,_ = splbac (arr[0],' руб./ За месяц')
    ind=1

    if 'Залог' in arr[ind]:  
        p2 = splfb (arr[ind],'Залог - ',' руб.')
        ind+=1 
    else: 
        p2= -1
    
    if 'Коммунальные услуги включены'in arr[ind]:
        p3= 'Коммунальные услуги включены'
        ind+=1  
    else: 
        p3='Коммунальные услуги не включены'

    if 'Срок аренды'in arr[ind]:
        _,p4 = splfron(arr[ind],' Срок аренды - ')
        ind+=1  
    else: 
        p4=''
    
    if 'Предоплата'in arr[ind]:
        p5 = splfb(arr[ind],' Предоплата ',' мес')
        ind+=1  
    else: 
        p5=-1

    return float(p1),float(p2),p3,p4,float(p5) 

def parse_col_rooms(s):
    if len(s)==1:
        return (int(s),'')
    else:
        return (int(s[0]),s[:2])

""" 

for i ,n in enumerate( data['Цена']):
    try:
        parse_rental(data['Цена'][i])
    except:
        print(i,n)
        break 
    
"""





def get_col_room(data):
    # Функция для извлечения количества комнат
    return data['Количество комнат'].astype(str).apply(lambda x: int(x[0]))

def get_price(data):
    # Функция для извлечения цены
    return data['Цена'].astype(str).apply(lambda x: float(splbac(x,'руб./')[0]))

def get_area_lamb(s):
    # Вспомогательная функция для извлечения площади
    if '/'in s:
        return float(splbac(s,'/')[0])
    else:
        return float(s)

def get_area(data):
    # Функция для извлечения площади
    return data['Площадь, м2'].astype(str).apply(get_area_lamb)

def get_metro(data):
    # Функция для извлечения метро
    return data['Метро'].astype(str).apply(lambda x: splfb(x,))

def get_ceiling_height(data):
    # Функция для извлечения высоты потолков
    return data['Высота потолков, м'].astype(str).apply(lambda x: float(x.split()[0]))

def get_var_room_lamb(s):
    # Вспомогательная функция для извлечения варианта комнат
    if ',' in s:
        return s.split(',')[1][1:]

def get_var_room(data):
    # Функция для извлечения варианта комнат
    return data['Количество комнат'].astype(str).apply(get_var_room_lamb)

def get_metro_lamb(s):
    # Вспомогательная функция для извлечения метро
    return splfb(s,'м.','(').strip() if s is not None else None

def get_metro(data):
    # Функция для извлечения метро
    return data['Метро'].astype(str).apply(get_metro_lamb)

def get_metro_time_lamb(s):
    # Вспомогательная функция для извлечения времени до метро
    try:
        if 'пешком'in s:
            return float(splfb(s,'(',' мин').strip() if 'None' not in s else 0)*3 if s is not None or 'nan' else None
        else :
            return float(splfb(s,'(',' мин').strip() if 'None' not in s else 0) if s is not None or 'nan' else None
    except:
        pass

def get_metro_time(data):
    # Функция для извлечения времени до метро
    return data['Метро'].astype(str).apply(get_metro_time_lamb)

def get_adress_lamb(s):
    # Вспомогательная функция для извлечения адреса
    return s.split(',')[1]

def get_adress(data):
    # Функция для извлечения адреса
    return data['Адрес'].astype(str).apply(get_adress_lamb)

def get_kitchen_area_lamb(s):
    # Вспомогательная функция для извлечения площади кухни
    try:
        if len(s.split('/')) == 2:
            return float(s.split('/')[1])
        
        if len(s.split('/')) == 3:
            return float(s.split('/')[2])
    except:
        print(s.split('/'))

def get_kitchen_area(data):
    # Функция для извлечения площади кухни
    return data['Площадь, м2'].astype(str).apply(get_kitchen_area_lamb)

def get_living_area_lamb(s):
    # Вспомогательная функция для извлечения жилой площади
    if len(s.split('/')) == 3:
        return float(s.split('/')[1])

def get_living_area(data):
    # Функция для извлечения жилой площади
    return data['Площадь, м2'].astype(str).apply(get_living_area_lamb)

def get_floor_lamb(s):
    # Вспомогательная функция для извлечения этажа
    return float(s.split('/')[0])

def get_floor(data):
    # Функция для извлечения этажа
    return data['Дом'].astype(str).apply(get_floor_lamb)

def get_num_floors_lamb(s):
    # Вспомогательная функция для извлечения количества этажей
    if ',' in s:
        return float(s.split(',')[0].split('/')[1])
    else:
        return float(s.split('/')[1])

def get_num_floors(data):
    # Функция для извлечения количества этажей
    return data['Дом'].astype(str).apply(get_num_floors_lamb)

def get_phonenum(data):
    # Функция для извлечения телефона
    v = data['Телефоны'].value_counts()
    return data['Телефоны'].astype(str).apply(lambda x: log(v[x], 2))

def get_prolonged(data):
    # Функция для извлечения признака "Длительный"
    return data['Цена'].apply(lambda x: 'Длительный' if 'Длительный' in x  else '')

def get_coord_y(cdata):
    # Функция для  определения координат по адресу

    with open('coordinates', 'rb') as file:
        addrdic = pickle.load(file)

    return cdata['adress'].apply(lambda x: addrdic[x][0] if addrdic[x] is not None  else None )

def get_coord_x(cdata):
    # Функция для  определения координат по адресу

    with open('coordinates', 'rb') as file:
        addrdic = pickle.load(file)
    return cdata['adress'].apply(lambda x: addrdic[x][1] if addrdic[x] is not None  else None )

def check_phrases(element):
    if isinstance(element, float):
        return 0
    if 'Мебель в комнатах' in element and 'Мебель на кухне' in element and 'Ванна' or 'Душ' in element and 'Стиральная машина' in element:
        return 1
    return 0



# Функция для обработки информации о площади комнат
def get_area_room(s):
    if isinstance(s, str): 
        s = s.replace(' ', '-')  # Заменяем пробелы на тире
        s = s.replace('+', '-')  # Заменяем плюсы на тире


# Функция для обработки информации о ремонте
def process_repair_info(s):
    if s == 'Без ремонта':
        return 0
    if pd.isna(s):
        return 1
    elif isinstance(s, str):
        if 'Дизайнерский' in s:
            return 3
        elif 'Евроремонт' in s:
            return 2
        elif 'Косметический' in s:
            return 1

# Функция для обработки информации о типе окон
def process_window_info(s):
    if isinstance(s, str):
        if 'На улицу и двор' in s:
            return 2
        elif 'Во двор' in s:
            return 1
        elif 'На улицу' in s:
            return 0
        return 0


# Функция для обработки информации о санузле
def process_bathroom_info(s):
    if pd.isna(s):  # Если значение NaN, возвращаем 0
        return 0
    else:
        digits = ''.join(filter(str.isdigit, s))  # Извлекаем все цифры из строки
        return digits

# Функция для обработки информации о детях и животных
def process_children_pets_info(s):
    if pd.isna(s):
        return 0
    elif 'Можно с детьми, Можно с животными' in s:
        return 2
    elif 'Можно с детьми' in s:
        return 1
    elif 'Можно с животными' in s:
        return 1
    else:
        return 0

# Функция для обработки информации о балконах
def process_balcony_info(s):
    if pd.isna(s) or 'Лоджия' in s:
        return 0
    digits = ''.join(filter(str.isdigit, s))  # Извлекаем цифры из строки
    return int(digits) if digits else 0


def get_data(data):
    cdata = pd.DataFrame()
    cdata['ID']=data['ID  объявления']
    cdata['price'] = get_price(data)
    cdata['col_rooms'] = get_col_room(data)
    cdata['ceiling_height'] = get_ceiling_height(data)
    #cdata['var_room'] = get_var_room(data)
    #cdata['metro'] = get_metro(data)
    cdata['metro_time'] = get_metro_time(data)
    cdata['adress'] = get_adress(data)
    cdata['full_area'] = get_area(data)
    #cdata['kitchen_area'] = get_kitchen_area(data)
    #cdata['living_area'] = get_living_area(data)
    cdata['floor'] = get_floor(data)
    cdata['num_floors'] = get_num_floors(data)
    #cdata['parking'] = data['Парковка']
    cdata['prolonged'] = get_prolonged(data)
    cdata['phone_number'] = get_phonenum(data)
    cdata['coord_y'] = get_coord_x(cdata).clip(lower=36.74401, upper=38.140841)
    cdata['coord_x'] = get_coord_y(cdata).clip(lower=55.386254, upper=56.119649)
    cdata['Furnished'] = data['Дополнительно'].apply(check_phrases)

    #Выводим в отдельную колонку общее число лифтов, вместо Nan у нас будет 0, потом мы это значение заполним средним по столбцу
    cdata['elevator'] = data['Лифт'].astype(str).apply(lambda x: sum([int(num) for num in re.findall(r'\d+', x)]))
    cdata['elevator'] = cdata['elevator'].apply(lambda x: sum([int (i) for i in  list(str(x))]))

    #Обработка колонки "Мусоропровод"
    cdata['garbage_chute'] = data['Мусоропровод'].replace({'Да': 1, 'Нет': 0, np.nan: 0}).astype(int)

    # Применение функций к соответствующим столбцам данных
    cdata['repair'] = data['Ремонт'].apply(process_repair_info)
    #cdata['rooms_area'] = data['Площадь комнат, м2'].apply(get_area_room)
    cdata['balcony_count'] = data['Балкон'].apply(process_balcony_info)
    cdata['windows'] = data['Окна'].apply(process_window_info)
    cdata['bathroom'] = data['Санузел'].apply(process_bathroom_info)
    cdata['bathroom'] = cdata['bathroom'].apply(lambda x: sum([int (i) for i in  list(str(x))]))
    cdata['child_pet'] = data['Можно с детьми/животными'].apply(process_children_pets_info)
    return cdata

from math import radians, sin, cos, sqrt, atan2

def haversine_distance(lat1, lon1, lat2, lon2):
    # Преобразование координат из градусов в радианы
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Разница между широтами и долготами
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Формула Haversine
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Радиус Земли в километрах (приблизительно)
    radius = 6371.0

    # Вычисление расстояния
    distance = radius * c

    return distance