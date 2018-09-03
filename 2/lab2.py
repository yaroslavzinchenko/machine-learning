from functools import reduce
import requests
import matplotlib.pyplot as plt
from pylab import *
from matplotlib import rcParams
%matplotlib inline 

#считывание 1000 вакансий с hh.ru

str_ = []
req = []

for i in range(10):
    i = 'https://api.hh.ru/vacancies?per_page=100&page=' + str(i) + '&text=machine+learning+OR+big data'
    str_.append(i)
for j in str_:
    req.append(requests.get(j))
    
#обработка данных в список 

js = []

for i in req:
    js.append(i.json())

vac = []

for i in js:
    for vacancy in i['items']:
        vac.append(vacancy)

#получение значения зарплат

sal_dict = {}

print('\n')
for sal in vac:
    if(sal['salary'] != None):
        if ((sal['salary']['to'] != None) and (sal['salary']['from'] != None)):
            salary = (sal['salary']['to'] + sal['salary']['from'])/2
            sal_dict[sal['name']] = salary
        elif ((sal['salary']['to'] == None) and (sal['salary']['from'] != None)):
            salary = sal['salary']['from']
            sal_dict[sal['name']] = salary
        elif ((sal['salary']['to'] != None) and (sal['salary']['from'] == None)):
            salary = sal['salary']['to']/2
            sal_dict[sal['name']] = salary
            
#print(sal_dict)

#получение медианного значения зарплат

sal_data = []
sal_prog = []
sal_deve = []
sal_othe = []

for val in sal_dict.keys():
    if('ata' in val):
        sal_data.append(sal_dict[val])
    elif('рограммист' in val):
        sal_prog.append(sal_dict[val])
    elif('азработчик' in val):
        sal_deve.append(sal_dict[val])
    elif('дминистратор' in val or 'енеджер' in val):
        sal_othe.append(sal_dict[val])

sal_data = sorted(sal_data)
sal_prog = sorted(sal_prog)
sal_deve = sorted(sal_deve)
sal_othe = sorted(sal_othe)

med_sdat = sal_data[int(len(sal_data)/2)]
med_spro = sal_prog[int(len(sal_prog)/2)]
med_sdev = sal_deve[int(len(sal_deve)/2)]
med_soth = sal_othe[int(len(sal_othe)/2)]

print(med_sdat, '   ', med_spro, '   ', med_sdev, '   ', med_soth)

#получение распределения всех зарплат по диапазонам

val = sal_dict.values()
        
s1 = reduce((lambda x, y: x + y), map((lambda x: 1 if x < 30000 else 0), sal_dict.values()))
s2 = reduce((lambda x, y: x + y), map((lambda x: 1 if 30000 < x < 50000 else 0), sal_dict.values()))
s3 = reduce((lambda x, y: x + y), map((lambda x: 1 if 50000 < x < 80000 else 0), sal_dict.values()))
s4 = reduce((lambda x, y: x + y), map((lambda x: 1 if 80000 < x < 100000 else 0), sal_dict.values()))
s5 = reduce((lambda x, y: x + y), map((lambda x: 1 if 100000 < x < 150000 else 0), sal_dict.values()))
s6 = reduce((lambda x, y: x + y), map((lambda x: 1 if 1500000 < x else 0), sal_dict.values()))

#график №1

bins = range(15000, 300000, 10000)

salary = []
for i in sal_dict.values():
    salary.append(int(i))

plt.title('all salary schedule')
plt.ylabel("value")
plt.xlabel("salary")

hist, bins = np.histogram(salary, bins = bins)
print(hist, bins)

plt.hist(salary, bins)
plt.show()

#график медиан

#bins = range(50000, 350000, 25000)

med = [med_sdat, med_spro, med_sdev, med_soth]
print(med)

plt.title('med salary schedule')
plt.ylabel("value")
plt.xlabel("salary")

hist, bins = np.histogram(med)
print(hist, bins)

plt.hist(med, bins)
plt.show()

#график диапазона

#bins = range(0, 50, 5)

ran = [s1, s2, s3, s4, s5, s6]
print(ran)

plt.title('salary schedule')
plt.ylabel("value")
plt.xlabel("people")

hist, bins = np.histogram(ran)
print(hist, bins)

plt.hist(ran, bins)
plt.show()

