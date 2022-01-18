#!/usr/bin/env python
# coding: utf-8

# In[ ]:


###from 1 to 94
# Webpage connection
get_ipython().system('pip install pymysql')
import requests
from bs4 import BeautifulSoup
import pymysql.cursors

for x in range(94):
    URL = "https://elcinema.com/en/index/work/country/eg?page="+str(x+1);
    r = requests.get(URL) 

    bsObj = BeautifulSoup(r.content, 'html5lib') 

    recordList = bsObj.findAll('img', attrs = {'class':"lazy-loaded"})


    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='password',#change password
                                 db='db_name',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            for record in recordList:
                movie_name = ""
                date_text = ""
                time = ""
                href = record.parent['href']
                url = "https://elcinema.com"+href
                new_r = requests.get(url)
                print(url)
                movie_details = BeautifulSoup(new_r.content, 'html5lib')
                #media_type
                div = movie_details.find('div', attrs = {'class':'columns small-9 large-10'})
                if div is not None:
                    ul = div.findChild('ul', {'class':'list-separator'}).findChildren('li')
                    if(ul is not None):
                        media_type = ul[0].text;
                if(media_type == "Movie"):
                    #name
                    name = movie_details.find('span', {"class": "left"}, {"dir":"ltr"})
                    if name is None:
                        name = movie_details.find('span', {"class": "left"}, {"dir":"rtl"})
                    if name is None:
                        continue
                    movie_name = name.text
                    print(name.get_text().strip())
                    #release
                    release = movie_details.find('li', string="Release Date:")
                    if release is not None:
                        date = release.findNext('li').findChildren('a', recursive=False)
                        date_text = ""
                        arr = []
                        for child in date:
                            arr.append(child.text)
                            print(child.get_text().strip())
                        print('\n')
                        md = arr[0].split()
                        month = md[1]
                        day = md[0]
                        if(month == "January"):
                            monum = "01"
                        elif month == "February":
                            monum = "02"
                        elif(month == "March"):
                            monum = "03"
                        elif(month =="April"):
                            monum = "04"
                        elif(month == "May"):
                            monum = "05"
                        elif(month == "June"):
                            monum = "06"
                        elif(month == "July"):
                            monum = "07"
                        elif(month == "August"):
                            monum = "08"
                        elif(month == "September"):
                            monum = "09"
                        elif(month == "October"):
                            monum = "10"
                        elif(month == "November"):
                            monum = "11"
                        else:
                            monum = "12"

                        if(len(day) == 1):
                            day = '0'+day
                        date_text = arr[1] + '-' + monum + '-' + day
                    #cast
                    roles = [];
                    cast_url = url+"cast"
                    rr = requests.get(cast_url)
                    cast_details = BeautifulSoup(rr.content, 'html5lib')
                    cast_types = cast_details.findAll('h3', {'class':'section-title'})
                    for cast_type in cast_types:
                        mylist = cast_type.text.split("\n");
                        member_role = mylist[1];
                        roles.append(member_role)
                        print(member_role)
                    uls = cast_details.findAll('ul', attrs = {'class':'small-block-grid-2 medium-block-grid-3 large-block-grid-6'});
                    if ul is not None:
                        i = 0;
                        for ul in uls:
                            members = ul.findChildren('li');
                            for member in members:
                                member_details = member.findChild('div')
                                if member_details is not None:
                                    member_details_ul = member_details.findChild('ul', {'class':'description'}).findChild('li').findChild('a')
                                    print(member_details_ul)
                                    member_name = member_details_ul.text;
                                    sql = "INSERT IGNORE INTO `acted_in` (`movie_name`,`member_name`, `member_role`) VALUES (%s, %s, %s)"
                                    cursor.execute(sql, (movie_name, member_name, roles[i]))
                            i = i+1;
        connection.commit()
    finally:
        connection.close()

