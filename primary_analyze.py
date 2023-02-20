import json
from collections import Counter

def determination_of_the_largest_city_among_friends():
    list_cities = []
    dict = {}
    with open('account_friends.json') as json_file:
        file = json.load(json_file)
        for item in file.items():
            if item[-1]['city_friend'] != '':
                list_cities.append(item[-1]['city_friend'])
    most_5_cities = Counter(list_cities).most_common(5)
    for elem in most_5_cities:
        dict[elem[0]] = elem[-1]
    print("Top 5 cities in friends",dict)
    for counter in range(0,4):
        print(list(dict.keys())[counter],":",round(((dict[f'{list(dict.keys())[counter]}'])/len(list_cities)*100),3),"%")
    json_file.close()
    return list(dict.keys())[0]

def determination_of_the_largest_city_among_subs(city):
    with open('account_subs.json') as json_file:
        file = json.load(json_file)
    for item in file.items():
        if 'page_name' in item[-1]:
            if item[-1]['page_name'].find(f'{city}') != -1:
                print('City in subs',item[-1]['page_name'])
    json_file.close()

def determination_of_the_largest_city_among_univer():
    list_univer = []
    dict = {}
    with open('account_friends.json') as json_file:
        file = json.load(json_file)
    for item in file.items():
        if item[-1]['university_name'] != '':
            list_univer.append(item[-1]['university_name'])
    most_5_univer = Counter(list_univer).most_common(5)
    for elem in most_5_univer:
        dict[elem[0]] = elem[-1]
    print("Top 5 univers in friends",dict)
    for counter in range(0,4):
        print(list(dict.keys())[counter],":",round(((dict[f'{list(dict.keys())[counter]}'])/len(list_univer)*100),3),"%")
    json_file.close()
    return list(dict.keys())[0]

def determination_of_the_largest_univer_among_subs(univer):
    with open('account_subs.json') as json_file:
        file = json.load(json_file)
    for item in file.items():
        if 'page_name' in item[-1]:
            if item[-1]['page_name'].find(f'{univer}') != -1:
                print('Univer in subs',item[-1]['page_name'])
    json_file.close()

def determination_correct_city(city):
    with open('account_info.json') as json_file:
        file = json.load(json_file)
    for item in file.items():
        if 'city' in item[0]:
            city_in_profile = item[-1]
    if city == city_in_profile:
        print('Cities match')
    else:
        print('Check city in profile and statistic from friends')

def main():
    city = determination_of_the_largest_city_among_friends()
    determination_of_the_largest_city_among_subs(city)
    univer = determination_of_the_largest_city_among_univer()
    determination_of_the_largest_univer_among_subs(univer)
    determination_correct_city(city)

if __name__ == "__main__":
    main()
