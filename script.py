# coding=utf-8
from threading import Thread
import requests
import os
from random import randint
import random
from time import sleep
import json
import shutil
from shutil import make_archive
from token_and_version import token,version

def check_directory():
        if os.path.exists('/tmp/photos') == False:
            os.mkdir('/tmp/photos')
            os.mkdir('/tmp/photos/albums')
        else:
            shutil.rmtree(r'/tmp/photos')
            os.mkdir('/tmp/photos')
            os.mkdir('/tmp/photos/albums')
def get_user_photo(user_id):
    is_closed,deact = '',''
    offset = 0
    url_user_get = f"https://api.vk.com/method/users.get?user_id={user_id}&fields=&access_token={token}&v={version}"
    req = requests.get(url_user_get).json()['response']
    fir_las_name = req
    for info in fir_las_name:
        id = info['id']
        if 'deactivated' in info:
            deact = info['deactivated']
        if 'is_closed' in info:
            is_closed = info['is_closed']
    if (is_closed is True) or (deact == 'deleted') or (deact == 'banned'):
        page_not_accessble = 'Страница недоступна'
        return page_not_accessble
    #print(id)
    list_id_albums =[]
    album_id = 0
    check_directory()
    id_album = f"https://api.vk.com/method/photos.getAlbums?owner_id={id}&access_token={token}&v={version}"
    req = requests.get(id_album).json()
    for id_count in req['response']['items']:
        id_al = id_count['id']
        list_id_albums.append(id_al)
    for inputing in ['profile','wall']:
        if os.path.exists(f'/tmp/photos/{inputing}') == False:
            os.mkdir(f'/tmp/photos/{inputing}')
        count = 0
        album = f"https://api.vk.com/method/photos.get?owner_id={id}&album_id={inputing}&access_token={token}&v={version}"
        checking = requests.get(album).json()['response']['count']
        print(checking, inputing)
        #проблема со стенами где больше 1000 фоток, решение через offset
        count_offset = checking // 1000
        print(count_offset)
        if count_offset != 0:
            for i in range(0,count_offset+1):
                offset = 1000 * i
                checking = 1000
                print(inputing,offset,i)
                sleep(5)
                photo_in_something = f"https://api.vk.com/method/photos.get?owner_id={id}&album_id={inputing}&count={checking}&offset={offset}&access_token={token}&v={version}"
                req = requests.get(photo_in_something).json()
                print(req)
                if checking != 0:
                    sra = req['response']['items']
                    for counts in sra:
                        url_photo = counts['sizes'][-1]['url']
                        print(url_photo)
                        photo_get = requests.get(url_photo)
                        out_file_with_photo = open(f"/tmp/photos/{inputing}/photo{count}.jpg","wb")
                        count = count + 1
                        out_file_with_photo.write(photo_get.content)
                        out_file_with_photo.close()
                        print('Success')
        else:
                checking = 1000
                print(inputing)
                sleep(5)
                photo_in_something = f"https://api.vk.com/method/photos.get?owner_id={id}&album_id={inputing}&count={checking}&offset={offset}&access_token={token}&v={version}"
                req = requests.get(photo_in_something).json()
                print(req)
                if checking != 0:
                    sra = req['response']['items']
                    for counts in sra:
                        url_photo = counts['sizes'][-1]['url']
                        print(url_photo)
                        photo_get = requests.get(url_photo)
                        out_file_with_photo = open(f"/tmp/photos/{inputing}/photo{count}.jpg","wb")
                        count = count + 1
                        out_file_with_photo.write(photo_get.content)
                        out_file_with_photo.close()
                        print('Success')
    for iteration in list_id_albums:
        count = 0
        #print(iteration)
        url = f"https://api.vk.com/method/photos.getAlbums?owner_id={id}&album_id={iteration}&access_token={token}&v={version}"
        counter =list_id_albums.index(iteration)
        print(counter)
        title = requests.get(url).json()['response']['items'][counter]['title']
        print(title)
        photo_in_albums = f"https://api.vk.com/method/photos.get?owner_id={id}&album_id={iteration}&access_token={token}&v={version}"
        checking = requests.get(photo_in_albums).json()['response']['count']
        print(checking)
        sleep(10)
        #оформить offset каак выше
        photo_in_albums = f"https://api.vk.com/method/photos.get?owner_id={id}&album_id={iteration}&count={checking}&access_token={token}&v={version}"
        print(requests.get(photo_in_albums).json())
        ejecting_items = requests.get(photo_in_albums).json()['response']['items']

        for counts in ejecting_items:
            url_photo = counts['sizes'][-1]['url']
            #print(url_photo)
            count = count + 1
            photo_get = requests.get(url_photo)
            if os.path.exists(f'/tmp/photos/albums/"{title}"') == False:
                os.mkdir(f'/tmp/photos/albums/"{title}"')
            out_file_with_photo = open(f'/tmp/photos/albums/"{title}"/photo{count}.jpg',"wb")
            out_file_with_photo.write(photo_get.content)
            out_file_with_photo.close()

    shutil.make_archive("account_photos", 'zip', '/tmp/photos')

def get_user_subs(user_id):
    is_closed,deact = '',''
    url_user_get = f"https://api.vk.com/method/users.get?user_id={user_id}&fields=deactivated,is_closed&access_token={token}&v={version}"
    req = requests.get(url_user_get)
    src = req.json()
    print(src)
    fir_las_name = src['response']

    for info in fir_las_name:
        id = info['id']
        if 'deactivated' in info:
            deact = info['deactivated']
        if 'is_closed' in info:
            is_closed = info['is_closed']
    if (is_closed is True) or (deact == 'deleted') or (deact == 'banned'):
        page_not_accessble = 'Страница недоступна'
        return page_not_accessble
    count_public_pages = 0
    count_groups = 0
    count_persons = 0
    info_about_all_subs = {}
    url_subs = f"https://api.vk.com/method/users.getSubscriptions?user_id={id}&extended=1&access_token={token}&v={version}"
    req = requests.get(url_subs)
    sra = req.json()
    subs = sra['response']
    count_subs = sra['response']['count']
    offset = 0
    url_subs = f"https://api.vk.com/method/users.getSubscriptions?user_id={id}&extended=1&offset={offset}&access_token={token}&v={version}"
    req = requests.get(url_subs)
    subes = req.json()
    items_for_ejecting_subs = sra['response']['items']
    while items_for_ejecting_subs != []:
        url_subs = f"https://api.vk.com/method/users.getSubscriptions?user_id={id}&extended=1&offset={offset}&access_token={token}&v={version}"
        req = requests.get(url_subs)
        sra = req.json()
        print(sra)
        name_subs = sra['response']['items']
        for u in name_subs:
            if u['type'] == 'page':
                name = u['name']
                count_public_pages +=1
                page = {}
                page[f"page_name"] = name
                page[f"page_id"] = f"vk.com/public{u['id']}"
                info_about_all_subs[f"page_{count_public_pages}"] = page
            elif u['type'] == 'group':
                name = u['name']
                count_groups +=1
                group = {}
                group[f"groups"] = name
                group[f"groups_id"] = f"vk.com/group{u['id']}"
                info_about_all_subs[f"group_{count_groups}"] = group
            else:
                f_name = u['first_name']
                l_name = u['last_name']
                count_persons +=1
                person = {}
                person[f"person_name"] = f_name + ' ' + l_name
                person[f"person_id"] = f"vk.com/id{u['id']}"
                info_about_all_subs[f"person_{count_persons}"] = person
        items_for_ejecting_subs = sra['response']['items']
        offset = offset + 20
        sleep(randint(0,3))
    json_info = json.dumps(info_about_all_subs,ensure_ascii=False, indent=4)
    jsonfile = open("account_subs.json","w",encoding='utf8')
    jsonfile.write(json_info)
    jsonfile.close()

def get_user_info(user_id):
    url_user_get = f"https://api.vk.com/method/users.get?user_id={user_id}&fields=deactivated,is_closed,activities,about,books,bdate,career,country,domain,education,exports,home_town,sex,site,schools,status,maiden_name,occupation,personal,relation,relatives,tv,universities,interests,contacts,city,interests,photo_max_orig&access_token={token}&v={version}"
    req = requests.get(url_user_get)
    src = req.json()
    print(src)
    fir_las_name = src['response']
    for info in fir_las_name:
        id = info['id']
        is_closed = ''
        deact = ''
        city = ''
        mobile_phone = ''
        home_phone = ''
        interests = ''
        books = ''
        tv = ''
        about = ''
        activities = ''
        university = ''
        faculty_name = ''
        education_form = ''
        education_status = ''
        home_town = ''
        bdate = ''
        if 'deactivated' in info:
            deact = info['deactivated']
        if 'is_closed' in info:
            is_closed = info['is_closed']
        first_name = info['first_name']
        last_name = info['last_name']
        sex = info['sex']
        if sex == 1:
            sex = 'Женский'
        elif sex == 0:
            sex = 'Не указан'
        else:
            sex = 'Мужской'
        if 'bdate' in info:
            bdate = info['bdate']
        if 'interests' in info:
            interests = info['interests']
        if 'books' in info:
            books = info['books']
        if 'tv' in info:
            tv = info['tv']
        if 'about' in info:
            about = info['about']
        if 'activities' in info:
            activities = info['activities']
        if 'university_name' in info:
            university = info['university_name']
        if 'faculty_name' in info:
            faculty_name = info['faculty_name']
        if 'education_form' in info:
            education_form = info['education_form']
        if 'education_status' in info:
            education_status = info['education_status']
        if 'home_town' in info:
            home_town = info['home_town']
        if 'city' in info:
            city = info['city']['title']
        if 'mobile_phone' in info:
            mobile_phone = info['mobile_phone']
        if 'home_phone' in info:
            home_phone = info['home_phone']
        if 'interests' in info:
            interests = info['interests']
    account_review = {'id':id,'first_name':first_name,'second_name':last_name,'is_closed':is_closed,'page_deactiv':deact,'birth_date':bdate,'sex':sex,'city':city,'mobile_phone':mobile_phone,'home_phone':home_phone,'interests':interests,'books':books,'tv':tv,'about':about,'activities':activities,'university':university,'faculty_name':faculty_name,'education_form':education_form,'education_status':education_status,'home_town':home_town}
    json_info = json.dumps(account_review,ensure_ascii=False, indent = 4)
    jsonfile = open("account_info.json","w",encoding='utf8')
    jsonfile.write(json_info)
    jsonfile.close()

def get_friends_user(user_id):
    is_closed,deact,is_banned = '','',''
    url_user_get = f"https://api.vk.com/method/users.get?user_id={user_id}&fields=deactivated,is_closed&access_token={token}&v={version}"
    req = requests.get(url_user_get)
    src = req.json()
    fir_las_name = src['response']
    print(fir_las_name)
    for info in fir_las_name:
        id = info['id']
        if 'deactivated' in info:
            deact = info['deactivated']
        if 'is_closed' in info:
            is_closed = info['is_closed']
    if (is_closed is True) or (deact == 'deleted') or (deact == 'banned'):
        page_not_accessble = 'Страница недоступна'
        return page_not_accessble
    univer_name = ''
    url_friends = f"https://api.vk.com/method/friends.get?user_id={id}&fields=schools,city,education,contacts,country,sex,status,universities,nickname&access_token={token}&v={version}"
    req = requests.get(url_friends)
    src = req.json()
    friends_review = {}
    count_friend = 0
    print(src)
    info_friends_user = src['response']['items']
    for info in info_friends_user:
        #print(info)
        school_name = ''
        school_city = ''
        count_friend +=1
        id = info.get('id')
        first_name = info.get('first_name')
        last_name = info.get('last_name')
        sex = info.get('sex')
        if sex == 1:
            sex = 'Женский'
        elif sex == 0:
            sex = 'Не указан'
        else:
            sex = 'Мужской'
        is_close = info.get('is_closed')
        if is_close == False:
            is_close = 'Open'
        elif is_close == True:
            is_close = 'Close'
        status = info.get('status')
        city_friends = info.get('city')
        mobile_phone = info.get('mobile_phone')
        home_phone = info.get('home_phone')
        univer_name = ''
        if 'university' in info:
            univer_name = info.get('university_name')
        schools = info.get('schools')
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
            school_name = ''

        if school_city == '':
            school_city = ''

        if school_name == '':
            school_name = ''

        if (mobile_phone == '') or (mobile_phone == None):
            mobile_phone = ''

        if (home_phone == '') or (home_phone == None):
            home_phone = ''

        if (city_friends != None):
            city_friends = city_friends['title']
        else:
            city_friends = ''
        friend = {}
        friend['person_name'] = first_name + ' ' + last_name
        friend['person_id'] = "vk.com/id{id}"
        friend = {'friend_name':first_name + ' ' + last_name,'person_link':f"vk.com/id{id}",'is_closed':is_close,'sex':sex,'city_friend':city_friends,'school_city':school_city,'school_name':school_name,'university_name':univer_name,'mobile_phone':mobile_phone,'home_phone':home_phone}
        friends_review[f"friend_{count_friend}"] = friend
    json_info = json.dumps(friends_review,ensure_ascii=False, indent=4)
    jsonfile = open("account_friends.json","w",encoding='utf8')
    jsonfile.write(json_info)
    jsonfile.close()

user_id = input("Введи айди страницы: ")
get_user_info(user_id)
get_user_photo(user_id)
get_user_subs(user_id)
get_friends_user(user_id)
print("Success")
    
