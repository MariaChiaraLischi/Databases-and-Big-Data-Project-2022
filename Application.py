import mysql.connector as mysql
from mysql.connector import Error

psw = input('Insert password for: localhost --> root: ')
db_name = 'dogs_database'
try:
    mydb = mysql.connect(host='localhost', user='root', password=psw)
    if mydb.is_connected():
        mycursor = mydb.cursor()
        mycursor.execute('USE ' + db_name)
        mydb.commit()

        mycursor.execute(
            '''
                CREATE TABLE D_description_finder (
                LINE int PRIMARY KEY NOT NULL,
                ID varchar(8),
                URL varchar(1000),
                BREED_PRIMARY varchar(1000),
                BREED_SECONDARY varchar(1000),
                BREED_MIXED Boolean,
                COLOR varchar(200),
                AGE varchar(10) check(AGE = 'Baby' or AGE = 'Young' or AGE = 'Adult' or AGE = 'Senior'),
                SEX varchar (10) check (SEX = 'Male' or SEX ='Female' or SEX='Unknown'), 
                DIMENSION varchar(20) check (DIMENSION = 'Small' or DIMENSION='Medium' or DIMENSION ='Large' or DIMENSION ='Extra Large'), 
                COAT varchar (20) check (COAT='Short' or COAT ='Medium' or COAT ='Wire' or COAT='Long' or COAT ='Curly'), 
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
        mydb.commit()

except Error as e:
     print("Error while connecting to MySQL", e)

fd = open('queries.sql', 'r')
sqlfile = fd.read()
fd.close()
sqlCommands = sqlfile.split(';')

queries_type = ['1) Search a dog with particular characteristics', '2) Count the young dogs found in Albuquerque', '3) Count dogs per city', '4) Search the dogs with a name similar to Felix', '5) Count the number of exported and imported dogs of the whole USA', '6) Return the ID of all the dogs named Snoopy in Fort Valley']

mycursor.execute("SELECT COLUMN_NAME FROM information_schema.columns WHERE table_name = 'D_description_finder' ORDER BY ORDINAL_POSITION")
filters = mycursor.fetchall()
filters.remove(('LINE',))
mycursor.execute("TRUNCATE TABLE dogs_database.D_description_finder")
mycursor.execute("INSERT INTO dogs_database.D_description_finder VALUES (1" + (", NULL" * len(filters)) + ")")
mydb.commit()

still_there = None
cont = True
while cont:

    cont2 = True
    while cont2:
        print('\nWhich type of query you would like to run?')
        print('0) No one: quit application')
        for query in queries_type:
            print(query)
        query_n = input('Select a number: ')
        try:
            query_n = int(query_n)
            cont2 = False
            if query_n > 1:
                query_n += 1
        except:
            print('Not recognized answer!')
        if query_n > 7:
            print('Not recognized answer!')

    # Search a dog with particular characteristics
    while query_n == 1:

        cont3 = True
        while cont3:
            print('\nWhat would you like to do?')
            print('1) Launch research\n2) View applied filters\n3) Change a filter status\n4) Remove a filter\n5) Remove all filters\n6) Change query type\n7) Quit application')
            inp = input('Select a number: ')
            try:
                inp = int(inp)
                cont3 = False
            except:
                print('Not recognized answer!')

        # Launch research
        if inp == 1:
            if still_there:
                mycursor.execute(sqlCommands[1])
            elif still_there == False:
                mycursor.execute(sqlCommands[2])
            else:
                mycursor.execute(sqlCommands[0])
            rows = mycursor.fetchall()
            if not rows:
                print('No results for this research!')
            else:
                print('Here are the result of your research:')
                i = 0
                while i < 10 and i < len(rows):
                    print(rows[i])
                    i += 1
                if len(rows) > 10:
                    print('There are also other ' + str(len(rows)-10) + ' dogs with these characteristics...')

        # View applied filters
        elif inp == 2:
            mycursor.execute("SELECT * FROM dogs_database.D_description_finder")
            rows = mycursor.fetchall()
            check = True
            for i in range(len(filters)):
                if rows[0][i+1] is not None:
                    check = False
                    break
            if still_there or still_there == False:
                check = False
            if check:
                print('No filter applied!')
            else:
                print('Here are the the applied filters:')
                for i in range(len(filters)):
                    if rows[0][i+1] is not None:
                        try:
                            print(filters[i][0] + ': ' + rows[0][i+1])
                        except:
                            if rows[0][i+1] == 0:
                                print(filters[i][0] + ': False')
                            elif rows[0][i+1] == 1:
                                print(filters[i][0] + ': True')
                            else:
                                print('Error')
                if still_there:
                    print('STILL_THERE: True')
                elif still_there == False:
                    print('STILL_THERE: False')

        # Change a filter status
        elif inp == 3:
            cont4 = True
            while cont4:
                print('\nWhich filter would you like to change?')
                for i in range(len(filters)):
                    print(str(i+1) + ') ' + filters[i][0])
                print(str(len(filters)+1) + ') STILL_THERE')
                inp = input('Select a number: ')
                try:
                    inp = int(inp)
                    cont4 = False
                except:
                    print('Not recognized answer!')
            if inp <= len(filters):
                mycursor.execute("SELECT DISTINCT " + filters[inp-1][0] + " FROM dogs_database.D_description")
                values = mycursor.fetchall()
                updated = False
                while not updated:
                    j = 0
                    for i in range(len(values)):
                        if values[i-j][0] == None:
                            del values[i-j]
                            j+=1
                    if values == [(0,),(1,)]:
                        print()
                        print('False')
                        print('True')
                        value = input('Select a new value from above for the filter ' + filters[inp - 1][0] + ': ')
                    elif len(values) < 10:
                        print()
                        for i in range(len(values)):
                            print(values[i][0])
                        value = input('Select a new value from above for the filter ' + filters[inp - 1][0] + ': ')
                    else:
                        value = input('\nSelect a new value for the filter ' + filters[inp-1][0] + ': ')
                    try:
                        mycursor.execute("UPDATE dogs_database.D_description_finder SET " + filters[inp-1][0] + " = '" + str(value) + "' WHERE LINE = 1")
                        updated = True
                    except:
                        try:
                            if value == 'F' or value == 'f' or value == 'false' or value == 'False':
                                mycursor.execute("UPDATE dogs_database.D_description_finder SET " + filters[inp-1][0] + " = FALSE WHERE LINE = 1")
                                updated = True
                            elif value == 'T' or value == 't' or value == 'true' or value == 'True':
                                mycursor.execute("UPDATE dogs_database.D_description_finder SET " + filters[inp-1][0] + " = TRUE WHERE LINE = 1")
                                updated = True
                        except:
                            pass
                    if not updated:
                        print('Not recognized answer!')
                mydb.commit()
            else:
                updated = False
                while not updated:
                    value = input('\nSelect T or F for the STILL_THERE filter: ')
                    try:
                        if value == 'F' or value == 'f':
                            still_there = False
                            updated = True
                        elif value == 'T' or value == 't':
                            still_there = True
                            updated = True
                    except:
                        pass
                    if not updated:
                        print('Not recognized answer!')

        # Remove a filter
        elif inp == 4:
            cont4 = True
            while cont4:
                print('\nWhich filter would you like to change?')
                for i in range(len(filters)):
                    print(str(i+1) + ') ' + filters[i][0])
                print(str(len(filters)+1) + ') STILL_THERE')
                inp = input('Select a number: ')
                try:
                    inp = int(inp)
                    cont4 = False
                except:
                    print('Not recognized answer!')
            if inp <= len(filters):
                mycursor.execute("UPDATE dogs_database.D_description_finder SET " + filters[inp-1][0] + " = NULL WHERE LINE = 1")
                mydb.commit()
            elif inp == len(filters)+1:
                still_there = None
            print('Filter reset')

        # Remove all filters
        elif inp == 5:
            mycursor.execute("TRUNCATE TABLE dogs_database.D_description_finder")
            mycursor.execute("INSERT INTO dogs_database.D_description_finder VALUES (1" + (", NULL" * len(filters)) + ")")
            mydb.commit()
            still_there = None
            print('Filters reset')

        # Change query type
        elif inp == 6:
            query_n = -1

        # Quit application
        elif inp == 7:
            query_n = 0

        else:
            print('Not recognized answer!')

    # Count the young dogs found in Albuquerque
    if query_n == 3:
        mycursor.execute(sqlCommands[3])
        rows = mycursor.fetchall()
        if not rows:
            print('No results for this research!')
        else:
            print('Here are the result of your research:')
            print('There are ' + str(rows[0][0]) + ' young dogs in Albuquerque')

    # Count dogs per city
    if query_n == 4:
        mycursor.execute(sqlCommands[4])
        rows = mycursor.fetchall()
        if not rows:
            print('No results for this research!')
        else:
            print('Here are the result of your research:')
            i = 0
            while i < 10 and i < len(rows):
                print(str(rows[i][0]) + ': ' + str(rows[i][1]))
                i += 1
            if len(rows) > 10:
                print('There are also other ' + str(len(rows) - 10) + ' cities')

    # Search the dogs with a name similar to Felix
    if query_n == 5:
        mycursor.execute(sqlCommands[5])
        rows = mycursor.fetchall()
        print(rows)
        if not rows:
            print('No results for this research!')
        else:
            print('Here are the result of your research:')
            i = 0
            while i < 10 and i < len(rows):
                print(rows[i])
                i += 1
            if len(rows) > 10:
                print('There are also other ' + str(len(rows) - 10) + ' dogs with these characteristics...')

    # Count the number of exported and imported dogs of the whole USA
    if query_n == 6:
        mycursor.execute(sqlCommands[6])
        rows = mycursor.fetchall()
        if not rows:
            print('No results for this research!')
        else:
            print('Here are the result of your research:')
            print('There are ' + str(int(rows[0][0])) + ' exported dogs and ' + str(int(rows[0][1])) + ' imported dogs for USA')

    # Return the ID of all the dogs named Snoopy in Fort Valley
    if query_n == 7:
        mycursor.execute(sqlCommands[7])
        rows = mycursor.fetchall()
        if not rows:
            print('No results for this research!')
        else:
            print('Here are the result of your research:')
            print(str(rows[0][0]))

    # Quit application
    if query_n == 0:
        cont = False

mycursor.execute("DROP TABLE dogs_database.D_description_finder")
mydb.commit()