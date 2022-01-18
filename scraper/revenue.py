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
                total_revenue = "0"
                href = record.parent['href']
                url = "https://elcinema.com"+href
                new_r = requests.get(url)
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
                    #release
                    release = movie_details.find('li', string="Release Date:")
                    if release is not None:
                        date = release.findNext('li').findChildren('a', recursive=False)
                        date_text = ""
                        arr = []
                        for child in date:
                            arr.append(child.text)
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
                    boxoffice_obj = BeautifulSoup(boxoffice.content, 'html5lib')
                    total_revenue_tag = boxoffice_obj.find('strong');
                    if total_revenue is not None:
                        mylist = total_revenue_tag.text.split();
                        total_rev = mylist[0];
                        total_revenue_list = total_rev.split(',');
                        if len(total_revenue_list) > 1:
                            for v in total_revenue_list:
                                total_revenue = total_revenue + v;
                        else:
                            total_revenue = total_rev;
                        
                    if(date_text == ""):
                        date_text = "2000-01-01"
                    if(media_type == "Movie"):
                        sql = "UPDATE `movie` SET `revenue` = %s WHERE `movie_name` = %s and release_date = %s"
                        cursor.execute(sql, (total_revenue, movie_name, date_text,))
            connection.commit()
    finally:
        connection.close()

