import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "python",
    password = "9406817179!As",
    port=3306,
    database="discord_clone")

mycursor = mydb.cursor()

user_email="meghnasaraf1979@gmail.com"
user_password="197679"
user_name="meghna saraf"
user_dob="1979-11-13"

mycursor.execute(f"INSERT INTO user_login_data VALUES('{user_email}','{user_password}','{user_name}','{user_dob}')")

mydb.commit()