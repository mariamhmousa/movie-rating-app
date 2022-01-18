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
                                 db='db_name',#change db name
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
                    #cast
                    cast_url = url+"cast"
                    rr = requests.get(cast_url)
                    cast_details = BeautifulSoup(rr.content, 'html5lib')
                    uls = cast_details.findAll('ul', attrs = {'class':"description"});
                    if uls is not None:
                        for ul in uls:
                            member_nat = "";
                            date_text = "1800-01-01"
                            bio = ""
                            li = ul.find('li');
                            print(li)
                            if li is not None:
                                href = li.find('a');
                                member_url = "https://elcinema.com"+href['href']
                                req = requests.get(member_url)
                                member_details = BeautifulSoup(req.content, 'html5lib');
                                #name
                                member_name_tag = member_details.find('h1');
                                if member_name_tag is None:
                                    continue
                                member_name_span = member_name_tag.find('span', attrs = {'class':"left"});
                                if member_name_span is None:
                                    member_name_span = member_name_tag.find('span', attrs = {'class':"right"});
                                member_name = member_name_span.text;
                                print(member_name)
                                #nationality
                                member_nat_li = member_details.find('li', string="Nationality:");
                                if member_nat_li is not None:
                                    member_nat_tag = member_nat_li.findNext('li').findChild('a');
                                    if member_nat_tag is not None:
                                        member_nat = member_nat_tag.text;
                                        print(member_nat);
                                #biography
                                bio_tag = member_details.find('p', attrs = {'class':"no-margin"})
                                if bio_tag is not None:
                                    bio = bio_tag.text;
                                print(bio);
                                #birthdate
                                bod_tag = member_details.find('li', string="Date of Birth:")
                                if bod_tag is not None:
                                    date = bod_tag.findNext('li').findChildren('a', recursive=False)
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
                                    print(date_text);
                                
                                    sql = "INSERT IGNORE INTO `cast_member` (`member_name`,`nationality`, `birthdate`, `biography`) VALUES (%s, %s, %s, %s)"
                                    cursor.execute(sql, (member_name, member_nat, date_text, bio))

        connection.commit()
    finally:
        connection.close()

