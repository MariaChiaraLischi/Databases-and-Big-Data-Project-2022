import pandas as pd
import mysql.connector as mysql
from mysql.connector import Error

all_dog_descriptions = pd.read_csv('archive/allDogDescriptions.csv')
dog_travel = pd.read_csv('archive/dogTravel.csv')
moves_by_locations = pd.read_csv('archive/movesByLocation.csv')

psw = input('Insert password for: localhost --> root: ')
db_name = 'dogs_database'
try:
    mydb = mysql.connect(host='localhost', user='root', password=psw)
    if mydb.is_connected():
        mycursor = mydb.cursor()
        mycursor.execute('SHOW DATABASES')
        result = mycursor.fetchall()
        for x in result:
            if db_name == x[0]:
                mycursor.execute('DROP DATABASE ' + db_name)
                mydb.commit()
                print("The database already exists! The old database has been deleted!)")

        mycursor.execute("CREATE DATABASE " + db_name)
        print("Database is created!")
except Error as e:
    print("Error while connecting to MySQL", e)

print("Filling database...")
mycursor= mydb.cursor()
mycursor.execute("USE " + db_name)

mycursor.execute(
      '''
        CREATE TABLE D_description (
          ID varchar(8) PRIMARY KEY not null,
          URL varchar(1000),
          BREED_PRIMARY varchar(1000),
          BREED_SECONDARY varchar(1000),
          BREED_MIXED Boolean,
          COLOR varchar(200),
          AGE varchar(10) check(AGE = 'Baby' or AGE = 'Young' or AGE = 'Adult' or AGE = 'Senior' or AGE = null),
          SEX varchar (10) check (SEX = 'Male' or SEX ='Female' or SEX='Unknown' or SEX = null), 
          DIMENSION varchar(20) check (DIMENSION = 'Small' or DIMENSION='Medium' or DIMENSION ='Large' or DIMENSION ='Extra Large' or DIMENSION = null ), 
          COAT varchar (20) check (COAT='Short' or COAT ='Medium' or COAT ='Wire' or COAT='Long' or COAT ='Curly' or COAT = null ), 
          HOUSE_TRAINED Boolean,
          FIXED Boolean,
          SPECIAL_NEEDS Boolean,
          SHOTS_CURRENT Boolean,
          ENV_CHILDREN Boolean,
          ENV_DOGS Boolean, 
          ENV_CATS Boolean, 
          NAME varchar(1000),
          CITY varchar(30),
          STATE varchar(10),
          ZIP varchar(10),
          COUNTRY varchar(10)
        );
      '''
      )

#for column in ['id','url','breed_primary','breed_secondary','color_primary','age','sex','size','coat','name','posted','contact_city','contact_state', 'contact_zip','contact_country']:
    #all_dog_descriptions[column] = all_dog_descriptions[column].fillna('---')
#for column in ['breed_mixed','house_trained','fixed', 'special_needs','shots_current','env_children','env_dogs','env_cats']:
    #all_dog_descriptions[column] = all_dog_descriptions[column].fillna(False)
for i, row in all_dog_descriptions.iterrows():
    sql = "INSERT INTO dogs_database.D_description VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    mycursor.execute(sql, tuple([row['id'], row['url'], row['breed_primary'], row['breed_secondary'], row['breed_mixed'], row['color_primary'], row['age'], row['sex'], row['size'], row['coat'],row['house_trained'],row['fixed'], row['special_needs'], row['shots_current'], row['env_children'], row['env_dogs'], row['env_cats'], row['name'], row['contact_city'], row['contact_state'], row['contact_zip'], row['contact_country']]))
    mydb.commit()

mycursor.execute(
      '''
        CREATE TABLE D_travel (
          TRAVEL_ID integer PRIMARY KEY NOT NULL,
          ID varchar(8) not null,
          CONTACT_CITY varchar(100),
          CONTACT_STATE varchar (100),
          FOUND varchar (200),
          MANUAL varchar(200),
          REMOVE Boolean,
          STILL_THERE Boolean,
          foreign key (ID) references D_description(ID)
        );
      '''
      )
#for column in ['id','contact_city', 'contact_state','found','manual']:
    #dog_travel[column] = dog_travel[column].fillna('---')
#for column in ['remove', 'still_there']:
    #dog_travel[column] = dog_travel[column].fillna(False)
for i, row in dog_travel.iterrows():
    sql = 'INSERT INTO dogs_database.D_travel VALUES (%s,%s,%s,%s,%s,%s,%s,%s);'
    mycursor.execute(sql, tuple([row['index'],row['id'], row['contact_city'],row['contact_state'], row['found'], row['manual'], row['remove'],row['still_there']]))
    mydb.commit()

mycursor.execute(
      '''
        CREATE TABLE D_moves_by_location (
        LOCATION varchar(50) primary key not null,
        EXPORTED integer,
        IMPORTED integer,
        TOTAL integer,
        INSIDE_US Boolean
        );
      '''
      )
#for column in ['exported','imported','total']:
    #moves_by_locations[column] = moves_by_locations[column].fillna(1.0)
#for column in ['inUS']:
    #moves_by_locations[column] = moves_by_locations[column].fillna(False)
for i, row in moves_by_locations.iterrows():
    sql = 'INSERT INTO dogs_database.D_moves_by_location  VALUES (%s,%s,%s,%s,%s);'
    mycursor.execute(sql, tuple([row['location'],row['exported'],row['imported'],row['total'],row['inUS']]))
    mydb.commit()

print('Database correctly filled!')
