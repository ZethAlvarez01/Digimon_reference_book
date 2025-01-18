from bs4 import BeautifulSoup
import requests


url = 'https://digimon.net/reference_en/detail.php?directory_name='

digimon_name = 'beelstarmon_x'
digimon_name = 'gaioumon_itto'
#digimon_name = 'jougamon'
#digimon_name = 'erlangmon_blast'
#digimon_name = 'xiquemon'
#digimon_name = 'agumon'
#digimon_name = 'shoutmonx4k'
#digimon_name = 'fusamon'

image = 'https://digimon.net/cimages/digimon/'+digimon_name+'.jpg'


page = requests.get(url=url + digimon_name)

#print(url+digimon_name)

if page.status_code != 200:
    print("Error al cargar la pagina")
    
page = BeautifulSoup(page.text,"html.parser")

digimon_of_name = page.find('h3').contents[0]
tag = page.find('span','p-ico')
x_antibody = False
x_antibody_add = False
level = []
type_d = ''
attribute = ''
special_move = []

#print(digimon_of_name)

if tag:
    if tag.contents[0] == 'X Antibody':
        #print(tag.contents[0])
        x_antibody = True

data = page.find('div','p-ref__info').find_all('dl')

for i in data:
    title = i.find('dt').contents[0]

    if title == 'Special Move':
        #print(title+": ")
        for j in i.find('dd').contents:
            if 'bs4.element.Tag' not in str(type(j)):
                #print(j.replace('・',''))
                special_move.append(j.replace('・',''))
    else:
        try:
            desc = i.find('dd').contents[0]
        except:
            desc = ''
        if title == 'Level':
            for j in i.find('dd').contents:
                    #print(str(j).replace('・',''))
                    x = str(j).replace('・','')
                    x = x.replace('<br>','')
                    x = x.replace('</br>','')
                    level.append(x)
        if title == 'Type':
            type_d = desc
        if title == 'Attribute':
            attribute = desc


profile = page.find('section','p-ref__profile')

profile_text_1 = ''
profile_text_x = ''

for i in profile.contents[2:]:
    if 'Effects of the X Antibody on' in str(i):
        profile_text_x = str(i.find('br').contents[1]).replace('<br>','')
        profile_text_x = profile_text_x.replace("</br>",'')
        profile_text_x = profile_text_x.replace("\t",'')
        profile_text_x = profile_text_x.replace("\r",'')
        profile_text_x = profile_text_x.replace("\n",'')
        x_antibody_add = True
    else:
        x = str(i).replace('<br>','')
        x = x.replace("</br>",'')
        x = x.replace('　','')
        x = x.replace("\t",'')
        x = x.replace("\r",'')
        x = x.replace("\n",'')
        profile_text_1 = profile_text_1 + x + "\n"

############

digicore = {
    'name':digimon_of_name,
    'x_antibody':[x_antibody,x_antibody_add],
    'level':level,
    'type': type_d,
    'attribute': attribute,
    'special_move': special_move,
    'profile': profile_text_1,
    'profile_x': profile_text_x
}

print(digicore)