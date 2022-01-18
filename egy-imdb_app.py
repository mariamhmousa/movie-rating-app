#!/usr/bin/env python
# coding: utf-8

# In[3]:


get_ipython().system('pip install pymysql')
import pymysql.cursors
connection = pymysql.connect(host='sql3.freesqldatabase.com',
                             user='sql3408149',
                             password='TWkx5vakz4',
                             db='sql3408149',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

def main_function(email):
    flag = True
    sql = "SELECT `username` FROM `imdb_user` WHERE `email`=%s"
    cursor.execute(sql, (email,))
    result = cursor.fetchone();
    welcome = "Hi "+result["username"]+"!"
    print(welcome)
    while flag:
        val1 = input("Enter:\n1 for searching movies by genre\n2 for searching movies by cast member\n3 for viewing information on a movie\n4 for viewing information on a cast member\n5 for viewing top 10 movies by total revenue\n6 for writing a review\n7 for viewing reviews on a movie\n8 for exiting")
        if val1 == "1":
            movie_genre = input("Enter a genre")
            sql = "SELECT `movie_name`, `release_date` FROM `movie_genre` WHERE `genre`=%s"
            cursor.execute(sql, (movie_genre,))
            result = cursor.fetchall()
            if result is None:
                print("Sorry no movies were found in this genre!")
            else:
                for row in result:
                    details="movie name: "+row["movie_name"]+"\nrelease date: \n"+row["release_date"].strftime('%Y-%m-%d')
                    print(details)
        elif val1 == "2":#searching movies by cast member
            name = input("Enter cast member name")
            sql = "SELECT A.`movie_name`, M.`release_date` FROM `movie` AS M,`acted_in` AS A WHERE M.`movie_name`=A.`movie_name` and `member_name` LIKE CONCAT('%%', %s, '%%')"
            cursor.execute(sql, (name,))
            result = cursor.fetchall()
            if result is None:
                print("Sorry no movies were found for this cast member!")
            else:
                for row in result:
                    details="movie name: "+row["movie_name"]+"\nrelease date: \n"+row["release_date"].strftime('%Y-%m-%d')
                    print(details)
        elif val1 == "3":#viewing information on a movie
            movie_name = input("Enter movie name")
            release_date = input("Enter the release date")
            sql = "SELECT M.`movie_name`, M.`release_date`, G.`genre`, A.`member_name` FROM `movie` as M, `movie_genre` as G, `acted_in` as A WHERE M.`movie_name`=G.`movie_name` and M.`release_date`=G.`release_date` and M.`movie_name`=A.`movie_name` and M.`movie_name` LIKE CONCAT('%%', %s, '%%') and M.`release_date`=%s"
            cursor.execute(sql, (movie_name, release_date,))
            result=cursor.fetchone()
            if result is None:
                print("Sorry we couldn't find this movie!")
            else:
                details="movie name: \n"+result["movie_name"]+"\nrelease date: \n"+result["release_date"].strftime('%Y-%m-%d')
                print(details)
                genre = []
                cast_members = []
                while result is not None:
                    if genre.count(result["genre"]) == 0:
                        genre.append(result["genre"])
                    if genre.count(result["member_name"]) == 0:
                        cast_members.append(result["member_name"])
                    result=cursor.fetchone()
                print("genre: \n")
                for g in genre:
                    print(g)
                print("cast members: \n")
                for c in cast_members:
                    print(c)
        elif val1 == "4":#viewing information on cast_member
            name = input("Enter cast member name")
            birthdate = input("Enter their birthdate")
            sql = "SELECT `member_name`, `birthdate`, `nationality`, `biography` FROM cast_member WHERE `member_name` LIKE CONCAT('%%', %s, '%%') and `birthdate`=%s"
            cursor.execute(sql, (name, birthdate,))
            result=cursor.fetchone()
            if result is None:
                print("Sorry we couldn't find this cast member!")
            else:
                details="member name: "+result["member_name"]+"\nbirthdate: \n"+result["birthdate"].strftime('%Y-%m-%d')+"\nnationality:\n"+result["nationality"]+"\nbiography:\n"+result["biography"]
                print(details)
        elif val1 == "5":#viewing top 10 movies by revenue
            sql = "SELECT `movie_name`, `release_date` FROM `movie` ORDER BY `revenue` DESC LIMIT 10"
            cursor.execute(sql)
            result=cursor.fetchall()
            if result is None:
                print("Sorry there is an error!")
            else:
                for row in result:
                    details="movie name: "+row["movie_name"]+"release date: \n"+row["release_date"].strftime('%Y-%m-%d')
                    print(details)
        elif val1 == "6":#writing a review
            movie_name = input("Enter movie name")
            release_date = input("Enter release date")
            sql = "SELECT `movie_name`, `release_date` FROM `movie` WHERE `movie_name` LIKE CONCAT('%%', %s, '%%') and `release_date`=%s"
            cursor.execute(sql, (movie_name, release_date,))
            result=cursor.fetchone()
            if result is None:
                print("Sorry we couldn't find this movie!")
            else:
                rate = input("Rate the movie on a scale from 1-10")
                yn = input("Would you like to write a review? Y/N")
                if yn == "N":
                    sql = "INSERT IGNORE INTO `review` (`user_email`, `movie_name`, `release_date`, `review_text`, `rate`) VALUES (%s, %s, %s, %s, %s)"
                    cursor.execute(sql, (email, movie_name, release_date, "", rate))
                else:
                    review = input("Write your review\n")
                    sql = "INSERT IGNORE INTO `review` (`user_email`, `movie_name`, `release_date`, `review_text`, `rate`) VALUES (%s, %s, %s, %s, %s)"
                    cursor.execute(sql, (email, result["movie_name"], result["release_date"], review, rate))
        elif val1 == "7":#viewing reviews on a movie
            movie_name = input("Enter movie name")
            release_date = input("Enter release date")
            sql = "SELECT `movie_name`, `release_date`, `review_text`, `rate`, `user_email` FROM `review` WHERE `movie_name` LIKE CONCAT('%%', %s, '%%') and `release_date`=%s"
            cursor.execute(sql, (movie_name, release_date))
            result = cursor.fetchall()
            if result is None:
                print("Sorry there are no reviews for this movie!")
            else:
                details = "movie name:\t"+movie_name+"\trelease date:\t"+release_date
                print(details)
                for row in result:
                    details = "user: "+row["user_email"]+"\nrate: "+str(row["rate"])+"\nreview: "+row["review_text"]
                    print(details)
        else:#exit
            flag = False

try:
    with connection.cursor() as cursor:
        val = input("Hello! Enter:\n1 for creating a new account\n2 for logging in\n");
        if val == "1":
            email = input("Enter your email")
            user = input("Enter a username")
            gender = input("F or M")
            birthdate = input("Enter your birthdate")
            sql = "INSERT IGNORE INTO `imdb_user` (`email`, `username`, `gender`, `birthdate`) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (email, user, gender, birthdate,))
            connection.commit()
            main_function(email)
        else:
            email = input("Enter your email")
            main_function(email)

        connection.commit()
finally:
    connection.close()


# In[ ]:




