
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
