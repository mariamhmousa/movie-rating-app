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
                                 password='El3abd@skoon7alawany',#change password
                                 db='test_imdb2',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            for record in recordList:
                movie_name = ""
                date_text = ""
                time = ""
                descr = ""
                rating = ""
                total_revenue = "0"
                href = record.parent['href']
                url = "https://elcinema.com"+href
                new_r = requests.get(url)
                print(url)
                movie_details = BeautifulSoup(new_r.content, 'html5lib')
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
                #revenue
                boxoffice_url = url+"boxoffice/";
                boxoffice = requests.get(boxoffice_url);
                total_revenue_tag = boxoffice.find('strong');
                if total_revenue is not None:
                    total_revenue = total_revenue_tag.text;
                #duration
                div = movie_details.find('div', attrs = {'class':'columns small-9 large-10'})
                if div is not None:
                    ul = div.findChild('ul', {'class':'list-separator'}).findChildren('li')
                    if(ul is not None):
                        media_type = ul[0].text;
                        for child in ul:
                            string = child.text;
                            if string[0:2].isdigit():
                                duration = child.text
                                print(duration)
                                lst = duration.split();
                                hours = int(lst[0])//60;
                                mins = int(lst[0])%60;
                                shours = str(hours);
                                smins = str(mins);
                                if(shours == "0"):
                                    shours = "00"
                                if(smins == "0"):
                                    smins = "00"
                                time = shours+":"+smins+":"+"00"
                                print(time)

                #description
                description = movie_details.find('p')
                if description is not None:
                    child = description.findChild('a')
                    if child is None:
                        descr = description.text
                        print(descr)
                #rating
                rating_class = movie_details.find('ul', attrs = {'class':'censorship'})
                if(rating_class is not None):
                    rating = rating_class.findChild('li').findNext('li').text
                    print(rating)

                if(date_text == ""):
                    date_text = "2000-01-01"
                if(time == ""):
                    time = "00:00:00"
                if(media_type == "Movie"):
                    sql = "INSERT IGNORE INTO `movie` (`movie_name`, `release_date`, `duration`, `movie_description`, `rating`, `revenue`) VALUES (%s, %s, %s, %s, %s, %s)"
                    cursor.execute(sql, (movie_name, date_text, time, descr, rating, total_revenue))
        connection.commit()
    finally:
        connection.close()

