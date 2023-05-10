import re
import itertools
import yaml
import os
from fuzzywuzzy import fuzz

# dictionary
dis = {'merk': [],
       'tipe': []
       }

# dict all merk types
laptop = {}
types = []

# regex
format = re.compile(r'\[.*?\]')
email_regex = re.compile(
    r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')

def yaml_to_list():
    from os.path import dirname, join
    current_dir = dirname(__file__)
    current_dir = current_dir.split('dialog_manager/form')
    file_path = join(current_dir[0], "data/produk.yaml")
    with open(file_path, 'r') as file:
        documents = yaml.full_load(file)

    # TIPE digabung dalam satu list
    for item in documents['ENTITAS']:
        list = []
        for i in range(len(item['TIPE'])):
            list.append(item['TIPE'][i])
        laptop[item['MERK']] = list


# get merk and tipe
yaml_to_list()

# seluruh kombinasi tipe laptop
type_list = []
for tipe in laptop:
    list1 = laptop.get(tipe)
    for value in list1:
        list1 = str(value)
        types.append(list1)
        lst = list1.split()
        per = set(itertools.permutations(lst))
        for p in per:
            type_list.append(' '.join(p))


def get_entitas(words, laptop=laptop, types=types, type_list=type_list):
    txt = words.lower()
    # compiling a pattern for all the combinations of the Models
    regex1one = re.compile(r'\b(?:%s)' % '|'.join(type_list))
    name4 = re.findall(regex1one, txt)
         
    # deteksi merk
    if dis['merk'] == []:
        for merk in laptop:
            find_merk = re.search(merk, txt)
            if find_merk:
                dis['merk'].append(merk)

    print(dis['merk'])
    
    if name4:
        # finding the original model
        type_list1 = []
        for name in name4:
            lst1 = name.split()
            pers = set(itertools.permutations(lst1))
            for per1 in pers:
                type_list1.append(' '.join(per1))
        dis['tipe'].append(list(set(type_list1) & set(types)))

    if dis['tipe'] == [] and dis['merk']:
        # deteksi entitas tipe
        numerator = 0
        most_similiar_tipe = []
        if dis['merk'] == []:
            spesifik_tipe = get_all_tipe()
        else:
            spesifik_tipe = get_spesifik_tipe()
        print(spesifik_tipe)
        for type in spesifik_tipe:
            intersection = list(set(type.split()) & set(words.split()))

            if intersection:
                print(type)
                if len(intersection) > numerator:
                    numerator = len(intersection)
                    most_similiar_tipe = [type]

                elif len(intersection) == numerator:
                    most_similiar_tipe.append(type)

            else:
                sim_ratio = fuzz.WRatio(type, words)

                if sim_ratio >= 75:
                    most_similiar_tipe.append(type)

        for tipe in most_similiar_tipe:
            dis['tipe'].append([tipe])
    
    return dis


def check_match():
    match = ''
    # deteksi kecocokan merk & tipe
    for key, value in laptop.items():
        for sub_value in value:
            if sub_value == dis['tipe'][0][0]:
                if key == dis['merk'][0]:
                    match = 'match'
                else:
                    match = 'not match'
    return match

def remove_merktipe():
    dis['tipe'] = []
    dis['merk'] = []

def remove_tipe():
    dis['tipe'] = []

def get_tipe(merk):
    return '<ul class="list-disc list-outside ml-5">' + ''.join(['<li>'.rjust(8) + str(name).title() + '</li>' for name in laptop[merk]]) + '</ul>'

# spesifik tipe per merk
def get_spesifik_tipe():
    return laptop[dis['merk'][0]]

# get seluruh tipe di db
def get_all_tipe():
    types = []
    for merk in laptop:
        for tipe in laptop[merk]:
            types.append(tipe)
    
    return types

# get seluruh merk
def get_all_merk():
    merks = '<ul class="list-disc list-outside ml-5">'
    for merk in laptop:
        merks += '<li>' + str(merk).title() + '</li>'
    merks+= '</ul>'
    return merks