
'''
Задание Pro


Выполнить Light со следующим изменением: вместо страницы с парсером

реализовать страницу определения основных навыков по определенным

вакансиям (взаимодействие с hh api). Например, на странице представлена форма:

город, название вакансии, кнопка. По нажатию пользователю будет показана

средняя ЗП по данной вакансии в этом городе и список релевантных навыков

(бекэнд взять из 12-го вебинара).

'''

from flask import Flask, render_template , request
import requests

def avg_sal_parser(vacancy, area): #Расчёт средней зарплаты по региону
  '''
  :param vacancy: название вакансии
  :param area: регион Москва=1, Санкт-Петербург=2, Екатеринбург=3, Новосибирск=4 ...
  :return: средняя зарплата
  '''
  x=[]
  all_zp = 0
  all_n = 0
  #цикл, который скачивает вакансии
  for i in range(200):
      # запрос
      url = 'https://api.hh.ru/vacancies'
      #параметры, которые будут добавлены к запросу
      # par = {'text': 'интернет маркетолог', 'area':'113','per_page':'10', 'page':i}
      par = {'text': str(vacancy), 'area': str(area), 'per_page': '10', 'page': i}
      r = requests.get(url, params=par)
      e=r.json()
      x.append(e)
  for j in x:
      y = j['items']
      #объявляем переменную n для подсчета, количества итераций цикла перебирающего зарплаты в вакансиях
      n=0
      #объявляем переменную sum_zp для подсчета, суммы зарплат в вакансиях
      sum_zp=0
      #цикл, переберает объекты, т.е перебирает вакансии
      for i in y:
          # проверяем есть ли значения в словаре по ключу salary. Т.е проверяем есть ли в вакансии данные по зарплате
          if i['salary'] !=None:
              #записываем значение в переменную s
              s=i['salary']
              # проверяем есть ли значения по ключу from. Т.е проверяем есть ли в вакансии данные по минимальной зп
              if s['from'] !=None:
                  # считаем количество обработанных вакансий в которых указана минимальная ЗП
                  n+=1
                  #получаем минимальную ЗП по ключу from
                  s['from']
                  #считаем сумму ЗП по вакансиям
                  sum_zp +=s['from']
      #добавляем сумму зп по итерации цикла
      all_zp +=sum_zp
      #добавляем сумму n по итерации цикла
      all_n +=n
      #считаем среднюю ЗП
  av_zp = all_zp / all_n
  return av_zp


app = Flask(__name__)

@app.route('/')
@app.route('/main')
def home():
  return render_template('main.html')

@app.route('/form_2')
def form_2():
  return render_template('form_2.html')
  
@app.route('/form_3',  methods = ['POST'])
def form_3():
    v = request.form['vacancy']
    a = request.form['area']
    avg_salary = avg_sal_parser(vacancy=v, area=a)
    # avg_salary=109333.29653679654
    av_s = "{:.2f}".format(avg_salary)
    return render_template('form_3.html', vacancy=v, area=a, avg_salary=av_s)

if __name__ == "__main__":
  app.run()
