import requests
from random import randint
from time import sleep
# 1. доделать парсинг целевой страницы, дополнив проверками
# 2. парсинг фотографий на компьютер
# 3. анализ собранной информации
# 4. интеграция с яндекс.картинки, гугл картинки и прочими подобными сервисами


token = 'your token'
version = '5.131'

def get_user_subs(id):
    url_subs = f"https://api.vk.com/method/users.getSubscriptions?user_id={id}&extended=1&access_token={token}&v={version}"
    req = requests.get(url_subs)
    sra = req.json()
    subs = sra['response']
    count_subs = sra['response']['count']
    print('Всего подписок: ', count_subs)
    offset = 0
    url_subs = f"https://api.vk.com/method/users.getSubscriptions?user_id={id}&extended=1&offset={offset}&access_token={token}&v={version}"
    req = requests.get(url_subs)
    subes = req.json()
    items_for_ejecting_subs = sra['response']['items']
    offset = offset + 20
    while items_for_ejecting_subs != []:
        url_subs = f"https://api.vk.com/method/users.getSubscriptions?user_id={id}&extended=1&offset={offset}&access_token={token}&v={version}"
        req = requests.get(url_subs)
        sra = req.json()
        name_subs = sra['response']['items']
        for u in name_subs:
            if u['type'] == 'page':
                name = u['name']
                print('Это публичная страница: ',name)
            elif u['type'] == 'group':
                name = u['name']
                print('Это группа: ',name)
            else:
                f_name = u['first_name']
                l_name = u['last_name']
                print('Это страница: ',f_name,l_name)
        items_for_ejecting_subs = sra['response']['items']
        offset = offset + 20
        sleep(randint(0,3))

def get_user_info(user_id):
    url_user_get = f"https://api.vk.com/method/users.get?user_id={user_id}&fields=activities,about,books,bdate,career,country,domain,education,exports,home_town,sex,site,schools,status,maiden_name,occupation,personal,relation,relatives,tv,universities,interests,contacts,city,interests&access_token={token}&v={version}"
    req = requests.get(url_user_get)
    src = req.json()
    fir_las_name = src['response']
    for info in fir_las_name:
        id = info['id']
        sex = info['sex']
        if sex == 1:
            sex = 'Женский'
        elif sex == 0:
            sex = 'Не указан'
        else:
            sex = 'Мужской'
        interests = info['interests']
        books = info['books']
        tv = info['tv']
        about = info['about']
        activities = info['activities']
        university = info['university_name']
        faculty_name = info['faculty_name']
        education_form = info['education_form']
        education_status = info['education_status']
        home_town = info['home_town']
        print(interests,books,tv,about,activities,university,faculty_name,education_form,education_status,home_town)
        #print(info)
        first_name = info['first_name']
        last_name = info['last_name']
        #удален парсинг аргументов ниже, т.к. нужна проверка на наличие данных аргументов
        if info == 'city':
            city = info['city']['title']
            print('Город: ',city,'\n')
        if info == 'mobile_phone':
            mobile_phone = info['mobile_phone']
            print('Мобильный телефон: ',mobile_phone,'\n')
        if info =='home_phone':
            home_phone = info['home_phone']
            print('Домашний телефон: ',home_phone,'\n')
        if info =='interests':
            interests = info['interests']
            print('Интересы: ',interests,'\n')
    print('\nФамилия Имя: ',first_name,last_name)
    print('Айди человека: ',id,'\n')
    sleep(5)
    return id

def get_friends_user(id):
    url_friends = f"https://api.vk.com/method/friends.get?user_id={id}&fields=schools,city,education,contacts,country,sex,status,universities,nickname&access_token={token}&v={version}"
    req = requests.get(url_friends)
    src = req.json()
    info_friends_user = src['response']['items']
    for info in info_friends_user:
        #print(info)
        first_name = info.get('first_name')
        last_name = info.get('last_name')
        sex = info.get('sex')
        if sex == 1:
            sex = 'Женский'
        elif sex == 0:
            sex = 'Не указан'
        else:
            sex = 'Мужской'
        mobile_phone = info.get('mobile_phone')
        home_phone = info.get('home_phone')
        status = info.get('status')
        print(status)
        city = info.get('city')
        university = info.get('university')
        if university != 0:
            print(info.get('university_name'))
        schools = info.get('schools')
        school_name = ''
        school_city = ''
        if schools != None:
            if (len(schools) != 0) or (schools != []):
                school_name = schools[0]['name']
                school_id = schools[0]['city']
                url_for_id_school = f"https://api.vk.com/method/database.getCitiesById?city_ids={school_id}&access_token={token}&v={version}"
                sleep(1)
                requ = requests.get(url_for_id_school)
                src1 = requ.json()
                id_school = src1['response']
                for iteration in id_school:
                    school_city = iteration['title']
        else:
            school_name = 'Не найдено'

        if school_city == '':
            school_city = 'Не найдено'

        if school_name == '':
            school_name = 'Не найдено'

        if (mobile_phone == '') or (mobile_phone == None):
            mobile_phone = 'Не найдено'

        if (home_phone == '') or (home_phone == None):
            home_phone = 'Не найдено'

        if (city == ''):
            city = 'Не найдено'

        if city != None:
            print('Имя Фамилия: ', first_name, last_name,'\n','Пол: ', sex,'\n','Город: ', city['title'],'\n','Город школы: ',school_city,'\n','Школа: ', school_name,'\n','Мобильный телефон: ', mobile_phone,'\n','Домашний телефон: ', home_phone,'\n')
        else:
            print('Имя Фамилия: ', first_name, last_name,'\n','Пол: ', sex,'\n','Город школы: ',school_city,'\n','Школа: ', school_name,'\n','Мобильный телефон: ', mobile_phone,'\n','Домашний телефон: ', home_phone,'\n')

#user_id = ''
user_id = input("Введи айди страницы: ")
id = get_user_info(user_id)
#get_user_subs(id)
get_friends_user(id)
