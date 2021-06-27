import csv
import mysql.connector
import pickle
f = open("bin2.dat","rb")
ngos = pickle.load(f)
f.close()
print(ngos.keys())
connector = mysql.connector.connect(host ="localhost",user ="root",passwd ="He@dshotkiller123")
cursor = connector.cursor()
for state in ngos:
    try :
        print("Processed :",state)
        f = open("{}.csv".format(state),"rt")
        reader = csv.reader(f,delimiter = ",")
        cursor.execute("Create database if not exists {}".format(state.replace(" ","")))
        cursor.execute("use {}".format(state.replace(" ","")))
        cursor.execute("drop table if exists NGO")
        cursor.execute("Create table NGO(Name TEXT,Address TEXT,City TEXT,Email TEXT, Phone TEXT,Mobile TEXT,Tel TEXT,Purpose TEXT)")
        for row in reader :
            query = "insert into NGO values(%s,%s,%s,%s,%s,%s,%s,%s)"
            values = tuple([i for i in row])
            cursor.execute(query,values)
        connector.commit()
        print()

    except Exception as e :
        print("Error processsing :",state ,"The error is  : ",e)
        print()
        pass

cursor.close()
