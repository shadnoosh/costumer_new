import requests
# working with mongo DB
import sqlite3
from sqlite3 import Error
from flask import Flask, request, render_template
import webbrowser


con = sqlite3.connect('costumersdatabase.db', check_same_thread=False)

cursorObj = con.cursor()
cursorObj.execute(
    "create table if not exists costumers(name text, niruyeforush int, niruyefani int, moredi int, date text, special_score float, ups_score float, battery_score float)")
cursorObj.execute(
    "create table if not exists scors(name text, year text, mounth text, Lastniruyeforush int, Lastniruyefani int)")
cursorObj.execute("create table if not exists contract(name text, year text, mounth text)")

con.commit()

app = Flask(__name__)
app.secret_key = "development key"


def InsertToCostumerTable(con, name, s1, s2, s3, key_value, p, s, a):
    sql = 'INSERT INTO costumers(name, niruyeforush, niruyefani, moredi, date, special_score, ups_score, battery_score) VALUES(?,?,?,?,?,?,?,?)'
    temp_tuple = (name, s1, s2, s3, key_value, p, s, a)
    cursorObj.execute(sql, temp_tuple)

    con.commit()


def InsertToScoreTable(con, name, year, mounth, s11, s22):
    sql = 'INSERT INTO scors(name, year, mounth, Lastniruyeforush, Lastniruyefani ) VALUES(?,?,?,?,?)'
    temp_tuple = (name, year, mounth, s11, s22)
    cursorObj.execute(sql, temp_tuple)
    con.commit()


def InsertToContractTable(con, name, year, mounth):
    sql = 'INSERT INTO contract(name, year, mounth) VALUES(?,?,?)'
    temp_tuple = (name, year, mounth)
    cursorObj.execute(sql, temp_tuple)
    con.commit()


def UpdateCostumerTable(con, name, first_score, second_score, key_score, thired_score):
    sql = 'UPDATE costumers SET niruyeforush=?, niruyefani=?, moredi=? WHERE name=? AND date=?'
    temp_tuple = (first_score, second_score, thired_score, name, key_score)
    cursorObj.execute(sql, temp_tuple)
    con.commit()


def UpdateScoreTable(con, name, year, mounth, s11, s22):
    sql = 'UPDATE scors SET year=?,mounth=?, Lastniruyeforush=?, Lastniruyefani=? WHERE name=?'
    temp_tuple = (year, mounth, s11, s22, name)
    cursorObj.execute(sql, temp_tuple)
    con.commit()


def UpdateContractTable(con, name, year, mounth):
    sql = 'UPDATE contract SET year=?,mounth=? WHERE name=?'
    temp_tuple = (year, mounth, name)
    cursorObj.execute(sql, temp_tuple)
    con.commit()


def FindContent(con, name):
    sql = 'SELECT * FROM costumers WHERE name=?'
    cursorObj.execute(sql, (name,))
    rows = cursorObj.fetchall()

    return rows


def FindScore(con, name):
    sql = 'SELECT * FROM scors WHERE name=?'
    cursorObj.execute(sql, (name,))
    rows1 = cursorObj.fetchall()

    return rows1


def FindContract(con, name):
    sql = 'SELECT * FROM contract WHERE name=?'
    cursorObj.execute(sql, (name,))
    rows1 = cursorObj.fetchall()

    return rows1


def conect_Api_Gather_info():
    contact = {
        "Criteria": {

            "PipelineId": "00000000-0000-0000-0000-000000000000",

        },
        "From": 0,
        "Limit": 8000
    }
    req = requests.post("https://app.didar.me/api/deal/search?apikey=g170pxn6spxqrb4pac65ouiawf7ifyxv", json=contact)
    json_response = req.json()
    # print("req is : ############:" , req)
    repository = json_response["Response"]["List"]
      # total list for keeping a list of dictionary of items
    total_info_list = []
    for i in range(len(json_response["Response"]["List"])):

        if json_response["Response"]["List"][i]["Status"] == 'Won':
            temp_arr = []
            repository = json_response["Response"]["List"][i]
            # total_info_list = []  # total list for keeping a list of dictionary of items
            # print(repository["Contact"]["DisplayName"])
            info_dict = {}
            info_dict["Date"] = repository['ChangeToWonTime']
            if repository["Contact"] != None:
                info_dict["DisplayName"] = repository['Contact']["DisplayName"]
            else:
                info_dict["DisplayName"] = "No Name"
            # print(info_dict)
            temp_arr = []
            for items in repository["Items"]:
                # print(items)
                temp_dict = {}
                info_dict["Code"]=items["ProductCode"]
                temp_dict["OriginalTitle"] = items["TitleForInvoice"]
                temp_dict["UnitPrice"] = items["UnitPrice"]
                temp_dict["Quantity"] = items["Quantity"]
                temp_dict["ProductCode"] = items["ProductCode"]
                temp_arr.append(temp_dict)
            info_dict["Products"] = temp_arr
            total_info_list.append(info_dict)
    return (total_info_list)

def jalali_to_gregorian(gy, gm, gd):
    g_d_m = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    if (gm > 2):
        gy2 = gy + 1
    else:
        gy2 = gy
    days = 355666 + (365 * gy) + ((gy2 + 3) // 4) - ((gy2 + 99) // 100) + ((gy2 + 399) // 400) + gd + g_d_m[gm - 1]
    jy = -1595 + (33 * (days // 12053))
    days %= 12053
    jy += 4 * (days // 1461)
    days %= 1461
    if (days > 365):
        jy += (days - 1) // 365
        days = (days - 1) % 365
    if (days < 186):
        jm = 1 + (days // 31)
        jd = 1 + (days % 31)
    else:
        jm = 7 + ((days - 186) // 30)
        jd = 1 + ((days - 186) % 30)
    return [jy, jm, jd]


def gregorian_to_jalali(gy, gm, gd):
    g_d_m = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    if (gm > 2):
        gy2 = gy + 1
    else:
        gy2 = gy
    days = 355666 + (365 * gy) + ((gy2 + 3) // 4) - ((gy2 + 99) // 100) + ((gy2 + 399) // 400) + gd + g_d_m[gm - 1]
    jy = -1595 + (33 * (days // 12053))
    days %= 12053
    jy += 4 * (days // 1461)
    days %= 1461
    if (days > 365):
        jy += (days - 1) // 365
        days = (days - 1) % 365
    if (days < 186):
        jm = 1 + (days // 31)
        jd = 1 + (days % 31)
    else:
        jm = 7 + ((days - 186) // 30)
        jd = 1 + ((days - 186) % 30)
    return [jy, jm, jd]



def extract_info(UserName):
    Special_Contact_Array = []
    created_list = conect_Api_Gather_info()
    for items in created_list:
        if UserName in items["DisplayName"]:
            Special_Contact_Array.append(items)

    return (Special_Contact_Array)


def systemdate():
    import datetime
    x = datetime.datetime.now()
    gd = x.day
    gm = x.month
    gy = x.year
    y, m, d = gregorian_to_jalali(gy, gm, gd)
    return (y, m, d)


def split_date(d):
    splited_date = (d.split("T"))[0]
    year_mounth_day = splited_date.split("-")
    return year_mounth_day


def extracting_info_date(extracted_list, start_date, end_date):
    temp_array = []
    for i in extracted_list:
        temp_date_list = split_date(i["Date"])
        #print(f" temp_date_list===={temp_date_list}")
        # print(f"start date==== {start_date} and end date==={end_date}")
        if int(temp_date_list[0]) > int(start_date[0]):

            if int(temp_date_list[0]) <= int(end_date[0]):
                # if int(start_date[1])<=int(temp_date_list[1]):
                if int(end_date[1]) > int(temp_date_list[1]):
                    temp_array.append(i)
                elif int(end_date[1]) == int(temp_date_list[1]):
                    # if int(end_date)>=int(temp_date_list[1]):
                    if int(end_date[2]) >= int(temp_date_list[2]):
                        temp_array.append(i)

                else:
                    print("not")
        if int(temp_date_list[0]) == int(start_date[0]):
            if int(temp_date_list[0]) < int(end_date[0]):
                if int(start_date[1]) < int(temp_date_list[1]):
                    # if int(end_date[1])>=int(temp_date_list[1]):
                    temp_array.append(i)

                elif int(start_date[1]) == int(temp_date_list[1]):

                    if int(start_date[2]) < int(temp_date_list[2]):
                        temp_array.append(i)

                elif int(end_date[1]) == int(temp_date_list[1]):
                    # if int(start_date[1])<=int(temp_date_list[1]):
                    if int(end_date[2]) >= int(temp_date_list[2]):
                        temp_array.append(i)

                else:
                    print("not")
        if (int(temp_date_list[0]) == int(end_date[0])) & (int(temp_date_list[0]) >= int(end_date[0])):
            if int(start_date[1]) < int(temp_date_list[1]):
                if int(end_date[1]) > int(temp_date_list[1]):
                    temp_array.append(i)
                elif int(start_date[1]) == int(temp_date_list[1]):
                    if int(start_date[2]) <= int(temp_date_list[2]):
                        temp_array.append(i)
                elif int(end_date[1]) == int(temp_date_list[1]):
                    # if int(start_date[1])<=int(temp_date_list[1]):
                    if int(end_date[2]) >= int(temp_date_list[2]):
                        temp_array.append(i)

                else:
                    print("not")
            if int(start_date[1]) == int(temp_date_list[1]):
                if int(start_date[2]) <= int(temp_date_list[2]):
                    temp_array.append(i)


    #print(f"temp_array===={temp_array}")
    return (temp_array)


def calculating_scores(info_special_date):
    code = []
    a = 0
    s = 0
    nups3000 = 0
    nups2000 = 0
    nups1000 = 0
    nups600 = 0
    nups10000 = 0
    nups6000 = 0
    nbs10000l = 0
    nbs10000s = 0
    nbs1000s = 0
    nbs1000l = 0
    nbv1000s = 0
    nbv1000l = 0
    nbs2000s = 0
    nbs2000l = 0
    nbv2000s = 0
    nbv2000l = 0
    nbs3000s = 0
    nbs3000l = 0
    nbv3000s = 0
    nbv3000l = 0
    nbs6000s = 0
    nbs6000l = 0
    nbv6000s = 0
    nbv6000l = 0
    nA0 = 0
    nA1 = 0
    nA2 = 0
    nA4 = 0
    nA6 = 0
    nA8 = 0
    nspecial = 0
    ncabin = 0
    bat4_5 = 0
    bat7 = 0
    bat8 = 0
    bat9 = 0
    bat12 = 0
    bat18 = 0
    bat26 = 0
    bat28 = 0
    bat35 = 0
    bat40 = 0
    bat42 = 0
    bat45 = 0
    bat50 = 0
    bat55 = 0
    bat60 = 0
    bat65 = 0
    bat66 = 0
    bat70 = 0
    bat74 = 0
    bat75 = 0
    bat80 = 0
    bat88 = 0
    bat100 = 0
    bat120 = 0
    bat150 = 0
    bat170 = 0
    bat190 = 0
    bat200 = 0
    latest_info = {}
    for items in info_special_date:
        if items["Code"] not in code:
            code.append(items["Code"])
        for i in items["Products"]:
            if i['ProductCode'] == "4.5 Ah":
                bat4_5 += int(i['Quantity'])
                latest_info[i['OriginalTitle']] = str(bat4_5)
            elif i['ProductCode'] == "7 Ah":
                bat7 += int(i['Quantity'])
                latest_info[i['OriginalTitle']] = str(bat7)
            elif i['ProductCode'] == "8 Ah":
                bat8 += int(i['Quantity'])
                latest_info[i['OriginalTitle']] = str(bat8)
            elif i['ProductCode'] == "9 Ah":
                bat9 += int(i['Quantity'])
                latest_info[i['OriginalTitle']] = str(bat9)
            elif i['ProductCode'] == "12 Ah":
                bat12 += int(i['Quantity'])
                latest_info[i['OriginalTitle']] = str(bat12)
            elif i['ProductCode'] == "18 Ah":
                bat18 += int(i['Quantity'])
                latest_info[i['OriginalTitle']] = str(bat18)
            elif i['ProductCode'] == "26 Ah":
                bat26 += int(i['Quantity'])
                latest_info[i['OriginalTitle']] = str(bat26)
            elif i['ProductCode'] == "28 Ah":
                bat28 += int(i['Quantity'])
                latest_info[i['OriginalTitle']] = str(bat28)
            elif i['ProductCode'] == "35 Ah":
                bat35 += int(i['Quantity'])
                latest_info[i['OriginalTitle']] = str(bat35)
            elif i['ProductCode'] == "40 Ah":
                bat40 += int(i['Quantity'])
                latest_info[i['OriginalTitle']] = str(bat40)
            elif i['ProductCode'] == "42 Ah":
                bat42 += int(i['Quantity'])
                latest_info[i['OriginalTitle']] = str(bat42)
            elif i['ProductCode'] == "45 Ah":
                bat45 += int(i['Quantity'])
                latest_info[i['OriginalTitle']] = str(bat45)
            elif i['ProductCode'] == "50 Ah":
                bat50 += int(i['Quantity'])
                latest_info[i['OriginalTitle']] = str(bat50)
            elif i['ProductCode'] == "55 Ah":
                bat55 += int(i['Quantity'])
                latest_info[i['OriginalTitle']] = str(bat55)
            elif i['ProductCode'] == "60 Ah":
                bat60 += int(i['Quantity'])
                latest_info[i['OriginalTitle']] = str(bat60)
            elif i['ProductCode'] == "65 Ah":
                bat65 += int(i['Quantity'])
                latest_info[i['OriginalTitle']] = str(bat65)
            elif i['ProductCode'] == "66 Ah":
                bat66 += int(i['Quantity'])
                latest_info[i['OriginalTitle']] = str(bat66)
            elif i['ProductCode'] == "70 Ah":
                bat70 += int(i['Quantity'])
                latest_info[i['OriginalTitle']] = str(bat70)
            elif i['ProductCode'] == "74 Ah":
                bat74 += int(i['Quantity'])
                latest_info[i['OriginalTitle']] = str(bat74)
            elif i['ProductCode'] == "75 Ah":
                bat75 += int(i['Quantity'])
                latest_info[i['OriginalTitle']] = str(bat75)
            elif i['ProductCode'] == "80 Ah":
                bat80 += int(i['Quantity'])
                latest_info[i['OriginalTitle']] = str(bat80)
            elif i['ProductCode'] == "88 Ah":
                bat88 += int(i['Quantity'])
                latest_info[i['OriginalTitle']] = str(bat88)
            elif i['ProductCode'] == "100 Ah":
                bat100 += int(i['Quantity'])
                latest_info[i['OriginalTitle']] = str(bat100)
            elif i['ProductCode'] == "120 Ah":
                bat120 += int(i['Quantity'])
                latest_info[i['OriginalTitle']] = str(bat120)
            elif i['ProductCode'] == "150 Ah":
                bat150 += int(i['Quantity'])
                latest_info[i['OriginalTitle']] = str(bat150)
            elif i['ProductCode'] == "170 Ah":
                bat170 += int(i['Quantity'])
                latest_info[i['OriginalTitle']] = str(bat170)
            elif i['ProductCode'] == "190 Ah":
                bat190 += int(i['Quantity'])
                latest_info[i['OriginalTitle']] = str(bat190)
            elif i['ProductCode'] == "200 Ah":
                bat200 += int(i['Quantity'])
                latest_info[i['OriginalTitle']] = str(bat200)
            elif i['OriginalTitle'] == "یو پی اس BS10000S":

                nups10000 += int(i['Quantity'])
                nbs10000s += int(i['Quantity'])
            elif i['OriginalTitle'] == "یو پی اس BS10000L":
                nups10000 += int(i['Quantity'])
                nbs10000l += int(i['Quantity'])

            elif i['OriginalTitle'] == "یو پی اس BS1000S":
                nups1000 += int(i['Quantity'])
                nbs1000s += int(i['Quantity'])
            elif i['OriginalTitle'] == "یو پی اس BV1000L":

                nups1000 += int(i['Quantity'])
                nbv1000l += int(i['Quantity'])
            elif i['OriginalTitle'] == "یو پی اس BS1000L":
                nups1000 += int(i['Quantity'])
                nbs1000l += int(i['Quantity'])
            elif i['OriginalTitle'] == "یو پی اس BV1000S":

                nups1000 += int(i['Quantity'])
                nbv1000s += int(i['Quantity'])
            # elif i['OriginalTitle'] == "یو پی اس BV1000L":
            #     nups1000 += int(i['Quantity'])
            elif i['OriginalTitle'] == "یو پی اس BS2000S":
                nups2000 += int(i['Quantity'])
                nbs2000s += int(i['Quantity'])
            elif i['OriginalTitle'] == "یو پی اس BS2000L":
                nups2000 += int(i['Quantity'])
                nbs2000l += int(i['Quantity'])
            elif i['OriginalTitle'] == "یو پی اس BV2000S":
                nups2000 += int(i['Quantity'])
                nbv2000s += int(i['Quantity'])
            elif i['OriginalTitle'] == "یو پی اس BV2000L":
                nups2000 += int(i['Quantity'])
                nbv2000l += int(i['Quantity'])
            elif i['OriginalTitle'] == "یو پی اس BS3000S":
                nups3000 += int(i['Quantity'])
                nbs3000s += int(i['Quantity'])
            elif i['OriginalTitle'] == "یو پی اس BS3000L":
                nups3000 += int(i['Quantity'])
                nbs3000l += int(i['Quantity'])
            elif i['OriginalTitle'] == "یو پی اس BV3000S":
                nups3000 += int(i['Quantity'])
                nbv3000s += int(i['Quantity'])
            elif i['OriginalTitle'] == "یو پی اس BV3000L":
                nups3000 += int(i['Quantity'])
                nbv3000l += int(i['Quantity'])

            elif i['OriginalTitle'] == "یو پی اس BS6000S":
                nups6000 += int(i['Quantity'])
                nbs6000s += int(i['Quantity'])
            elif i['OriginalTitle'] == "یو پی اس BS6000L":
                nups6000 += int(i['Quantity'])
                nbs6000l += int(i['Quantity'])
            elif i['OriginalTitle'] == "یو پی اس BV6000S":
                nups6000 += int(i['Quantity'])
                nbv6000s += int(i['Quantity'])
            elif i['OriginalTitle'] == "یو پی اس BV6000L":
                nups6000 += int(i['Quantity'])
                nbv6000l += int(i['Quantity'])
            elif i['OriginalTitle'] == "یو پی اس BS600S":
                nups600 += int(i['Quantity'])
            elif i['OriginalTitle'] == "کابینت اختصاصی":
                nspecial += int(i['Quantity'])
                ncabin += 1
            elif i['OriginalTitle'] == "کابینت 4 طبقه A8":
                ncabin += 1
                nA8 += int(i['Quantity'])
            elif i['OriginalTitle'] == "کابینت 1 طبقه A1":
                nA1 += int(i['Quantity'])
                ncabin += 1
            elif i['OriginalTitle'] == "کابینت 1 طبقه A0":
                nA1 += int(i['Quantity'])
                ncabin += 1
            elif i['OriginalTitle'] == "کابینت 4 طبقه A1":
                nA1 += int(i['Quantity'])
                ncabin += 1
            elif i['OriginalTitle'] == "کابینت 1 طبقه A2":
                nA2 += int(i['Quantity'])
                ncabin += 1
            elif i['OriginalTitle'] == "کابینت 2 طبقه A4":
                nA4 += int(i['Quantity'])
                ncabin += 1
            elif i['OriginalTitle'] == "کابینت 3 طبقه A6":
                nA6 += int(i['Quantity'])
                ncabin += 1

    latest_info["یو پی اس BS10000S"] = str(nbs10000s)
    latest_info["یو پی اس BS10000l"] = str(nbs10000l)
    latest_info["یو پی اس BS1000S"] = str(nbs1000s)
    latest_info["یو پی اس BS1000l"] = str(nbs1000l)
    latest_info["یو پی اس BV1000S"] = str(nbv1000s)
    latest_info["یو پی اس BV1000l"] = str(nbv1000l)
    latest_info["یو پی اس BS2000S"] = str(nbs2000s)
    latest_info["یو پی اس BS2000l"] = str(nbs2000l)
    latest_info["یو پی اس BV2000S"] = str(nbs2000s)
    latest_info["یو پی اس BV2000l"] = str(nbv2000l)
    latest_info["یو پی اس SBS3000S"] = str(nbs3000s)
    latest_info["یو پی اس SBS3000l"] = str(nbs3000l)
    latest_info["یو پی اس SBV3000S"] = str(nbv3000s)
    latest_info["یو پی اس SBV3000l"] = str(nbv3000l)
    latest_info["یو پی اس SBS6000S"] = str(nbs6000s)
    latest_info["یو پی اس SBS6000l"] = str(nbs6000l)
    latest_info["یو پی اس SBv6000S"] = str(nbv6000s)
    latest_info["یو پی اس SBv6000l"] = str(nbv6000l)
    latest_info["یو پی اس SBS600S"] = str(nups600)
    latest_info["کابینت 4 طبقه A8"] = str(nA8)
    latest_info["کابینت 3 طبقه A6"] = str(nA6)
    latest_info["کابینت 2 طبقه A4"] = str(nA4)
    latest_info['کابینت 1 طبقه A2'] = str(nA2)
    latest_info["کابینت 1 طبقه A1"] = str(nA1)
    latest_info["کابینت 1 طبقه A0"] = str(nA0)
    latest_info["کابینت اختصاصی"] = str(nspecial)
    s += (nups10000 * 10) + (nups1000 * 1) + (nups6000 * 6) + (nups2000 * 2) + (nups600 * 0.6) + (nups3000 * 3)

    a += ((4.5 * bat4_5) + (7 * bat7) + (8 * bat8) + (9 * bat9) + (12 * bat12) + (18 * bat18) + (26 * bat26) + (
            28 * bat28) + (35 * bat35) + (40 * bat40) + (42 * bat42) + (45 * bat45) + +(50 * bat50) + (
                  55 * bat55) + (60 * bat60) + (65 * bat65) + (66 * bat66) + (70 * bat70) + (74 * bat74) + (
                  75 * bat75) + (80 * bat80) + (88 * bat88) + (100 * bat100) + (120 * bat120) + (150 * bat150) + (
                  170 * bat170) + (190 * bat190) + (200 * bat200)) / 1000

    p = (1.5 * len(code) + s + (5 * a)) * 100
    # print("p=: ", p)

    n = len(code)
    BatString = ""
    if bat4_5 > 0:
        BatString += "battery 4.5 Ah: " + str(bat4_5) + '\n'
    if bat7 > 0:
        BatString += "battery 7 Ah: " + str(bat7) + '\n'
    if bat8 > 0:
        BatString += "battery 8 Ah: " + str(bat8) + '\n'
    if bat9 > 0:
        BatString += "battery 9 Ah: " + str(bat9) + '\n'
    if bat9 > 0:
        BatString += "battery 9 Ah: " + str(bat9) + '\n'
    if bat12 > 0:
        BatString += "battery 12 Ah: " + str(bat12) + '\n'
    if bat18 > 0:
        BatString += "battery 18 Ah" + str(bat18) + '\n'
    if bat26 > 0:
        BatString += "battery 26 Ah: " + str(bat26) + '\n'
    if bat28 > 0:
        BatString += "battery 28 Ah: " + str(bat28) + '\n'
    if bat35 > 0:
        BatString += "battery 35 Ah: " + str(bat35) + '\n'
    if bat40 > 0:
        BatString += "battery 40 Ah: " + str(bat40) + '\n'
    if bat42 > 0:
        BatString += "battery 42 Ah: " + str(bat42) + '\n'
    if bat50 > 0:
        BatString += "battery 50 Ah: " + str(bat50) + '\n'
    if bat55 > 0:
        BatString += "battery 55 Ah: " + str(bat55) + '\n'
    if bat60 > 0:
        BatString += "battery 60 Ah: " + str(bat60) + '\n'
    if bat65 > 0:
        BatString += "battery 65 Ah: " + str(bat65) + '\n'
    if bat66 > 0:
        BatString += "battery 66 Ah: " + str(bat66) + '\n'
    if bat70 > 0:
        BatString += "battery 70 Ah: " + str(bat70) + '\n'
    if bat74 > 0:
        BatString += "battery 74 Ah: " + str(bat74) + '\n'
    if bat75 > 0:
        BatString += "battery 75 Ah: " + str(bat75) + '\n'
    if bat80 > 0:
        BatString += "battery 80 Ah: " + str(bat80) + '\n'
    if bat88 > 0:
        BatString += "battery 88 Ah: " + str(bat88) + '\n'
    if bat100 > 0:
        BatString += "battery 100 Ah: " + str(bat100) + '\n'
    if bat120 > 0:
        BatString += "battery 120 Ah: " + str(bat120) + '\n'
    if bat150 > 0:
        BatString += "battery 150 Ah: " + str(bat150) + '\n'
    if bat170 > 0:
        BatString += "battery 170 Ah: " + str(bat170) + '\n'
    if bat190 > 0:
        BatString += "battery 190 Ah: " + str(bat190) + '\n'
    if bat200 > 0:
        BatString += "battery 200 Ah: " + str(bat200) + '\n'
    UpsString = ""
    if nups600 > 0:
        UpsString += "UPS600: " + str(nups600) + "\n"
    if nbs1000s > 0:
        UpsString += "UPS BS1000S: " + str(nbs1000s) + "\n"
    if nbs1000l > 0:
        UpsString += "UPS BS1000L: " + str(nbs1000l) + "\n"
    if nbv1000s > 0:
        UpsString += "UPS BV1000S: " + str(nbv1000s) + "\n"
    if nbv1000l > 0:
        UpsString += "UPS BV1000L: " + str(nbv1000l) + "\n"
    if nbs2000s > 0:
        UpsString += "UPS BS2000S: " + str(nbs2000s) + "\n"
    if nbs2000l > 0:
        UpsString += "UPS BS2000L: " + str(nbs2000l) + "\n"
    if nbv2000s > 0:
        UpsString += "UPS BV2000S: " + str(nbv2000s) + "\n"
    if nbv2000l > 0:
        UpsString += "UPS BV2000L: " + str(nbv2000l) + "\n"
    if nbs3000s > 0:
        UpsString += "UPS BS3000S: " + str(nbs3000s) + "\n"
    if nbs3000l > 0:
        UpsString += "UPS BS3000L: " + str(nbs3000l) + "\n"
    if nbv3000s > 0:
        UpsString += "UPS BV3000S: " + str(nbv3000s) + "\n"
    if nbv3000l > 0:
        UpsString += "UPS BV3000L: " + str(nbv3000l) + "\n"
    if nbs6000s > 0:
        UpsString += "UPS BS6000S: " + str(nbs6000s) + "\n"
    if nbs6000l > 0:
        UpsString += "UPS BS6000L: " + str(nbs6000l) + "\n"
    if nbv6000s > 0:
        UpsString += "UPS BV6000S: " + str(nbv6000s) + "\n"
    if nbv6000l > 0:
        UpsString += "UPS BV6000L: " + str(nbv6000l) + "\n"
    if nbs10000s > 0:
        UpsString += "UPS BS10000s: " + str(nbs10000s) + "\n"
    if nbs10000l > 0:
        UpsString += "UPS BS10000l: " + str(nbs10000l) + "\n"
    cabinetStr = ""
    if nA8 > 0:
        cabinetStr += str(nA8) + ": کابینت باتری A8" + "\n"
    if nA6 > 0:
        cabinetStr += str(nA6) + ": کابینت باتری A6" + "\n"
    if nA4 > 0:
        cabinetStr += str(nA4) + ": کابینت باتری A4" + "\n"
    if nA2 > 0:
        cabinetStr += str(nA2) + ": کابینت باتری A2" + "\n"
    if nA1 > 0:
        cabinetStr += str(nA1) + ": کابینت باتری A1" + "\n"
    if nA0 > 0:
        cabinetStr += str(nA0) + ": کابینت باتری A0" + "\n"
    if nA0 > 0:
        cabinetStr += str(nspecial) + ": کابینت باتری اختصاصی" + "\n"

    if (p > 0 and p <= 1000.0):
        rate = "G1"
        # UpsDiscount = 12 + (p / 500)
        UpsDiscount =15
        # CabinBatteryDiscount = 5 + (p / 1000)
        CabinBatteryDiscount =10
        # ServiceDiscount = 8 + (p / 500)
        ServiceDiscount =10
    elif (p > 0 and p > 1000.0) & (p <= 2500.0):
        rate = "G2"
        # UpsDiscount = 11 + ((p * 1.5) / 500)
        UpsDiscount =19
        # CabinBatteryDiscount = 5 + ((p * 1.5) / 1000)
        CabinBatteryDiscount =14
        # ServiceDiscount = 10 + ((p * 1.3) / 500)
        ServiceDiscount =15

    elif (p > 0 and p > 2500.0):
        rate = "G3"
        # UpsDiscount = 9 + ((p * 2) / 500)
        UpsDiscount =23
        # CabinBatteryDiscount = 5 + ((p * 2) / 1000)
        CabinBatteryDiscount =18
        # ServiceDiscount = 10 + ((p * 1.8) / 500)
        ServiceDiscount =20
    elif (p == 0):
        rate = "No rate"
        UpsDiscount = 0
        CabinBatteryDiscount = 0
        ServiceDiscount = 0

    return (
        BatString, UpsString, cabinetStr, round(UpsDiscount, 2), round(CabinBatteryDiscount, 2),
        round(ServiceDiscount, 2),
        n, round(s, 2), round(a, 2), round(p, 2), rate, latest_info)


def creat_start_end_date(mounth):
    if int(mounth) <= 6:
        day_start = 1
        day_end = 31
    elif int(mounth) < 12 and int(mounth) > 6:
        day_start = 1
        day_end = 30
    else:
        day_start = 1
        day_end = 29
    return (day_start, day_end)


def CalculatePm(name, mounth,year):  # we need to calculate pm in an individual function for mounth befor the netered mounth
    ContractDate = FindContract(con, name)  # to find the date of contract
    pm = []
    for items2 in ContractDate:
        if items2[0] == name:
            ContractYear = int(items2[1])
            Contractmounth = int(items2[2])
    if (int(ContractYear) > int(year)) and (int(Contractmounth) < 12):
        counter = int(mounth) + (12 - int(Contractmounth))
    elif (int(ContractYear) > int(year)) and (int(Contractmounth) == 12):
        counter = int(mounth) + 1
    elif (int(ContractYear) < int(year)) and (int(Contractmounth) < 12) and ((int(year)-int(ContractYear))<2):
        counter = int(mounth) + (12 - int(Contractmounth))
    elif (int(ContractYear) < int(year)) and (int(Contractmounth) < 12) and ((int(year)-int(ContractYear))>=2):
        counter = int(mounth) + (12 - int(Contractmounth))+(12*((int(year)-int(ContractYear))-1))
    else:
        counter = int(mounth) - int(Contractmounth)
    # print(counter)
    if int(ContractYear)>=int(year):
        for i in range(counter):
            mounth = int(mounth) - 1  # we want to calculate pm for mounths befor the entered date
            if int(mounth) == 0:
                mounth = 12
            day_start, day_end = creat_start_end_date(mounth)
            # print(f"the mounth is: {mounth} and year is: {year}")
            start_date = convert_date(int(year), int(mounth), int(day_start))
            end_date = convert_date(int(ContractYear), int(mounth), int(day_end))
            extracted_list = extract_info(name)

            info_special_date = extracting_info_date(extracted_list, start_date, end_date)
            BatString, UpsString, cabinetStr, UpsDiscount, CabinBatteryDiscount, ServiceDiscount, n, s, a, p, rate, info_list = calculating_scores(
                info_special_date)
            pm.append(p)
    if int(ContractYear) < int(year):
        print(f"farvardin")
        if (int(mounth)-1)==0:
            mounth1=12
            year1=int(year)-1
            for l in range((12-int(Contractmounth)+1)):
                day_start, day_end = creat_start_end_date(mounth)
                # print(f"the mounth is: {mounth1} and year is: {year1}")
                start_date = convert_date(int(year1), int(mounth1), int(day_start))
                end_date = convert_date(int(ContractYear), int(mounth1), int(day_end))
                extracted_list = extract_info(name)
                info_special_date = extracting_info_date(extracted_list, start_date, end_date)
                BatString, UpsString, cabinetStr, UpsDiscount, CabinBatteryDiscount, ServiceDiscount, n, s, a, p, rate, info_list = calculating_scores(
                    info_special_date)
                pm.append(p)
                mounth1-=1
                if mounth1<Contractmounth:
                    break
        count=0
        if (int(mounth)-1)!=0:
            count+=1
            mounthn=mounth
            for k in range (int(mounthn) -1):
                mounth2=int(mounthn)-1
                day_start, day_end = creat_start_end_date(mounth)
                # print(f"the mounth is: {mounth2} and year is: {year}")
                start_date = convert_date(int(year), int(mounth2), int(day_start))
                end_date = convert_date(int(year), int(mounth2), int(day_end))
                # print(f"end mounth for farvardin is: {end_date}")
                extracted_list = extract_info(name)
                info_special_date = extracting_info_date(extracted_list, start_date, end_date)
                BatString, UpsString, cabinetStr, UpsDiscount, CabinBatteryDiscount, ServiceDiscount, n, s, a, p, rate, info_list = calculating_scores(
                    info_special_date)
                pm.append(p)
                mounthn=mounth2

            # print(count)
            mounth1 = int(Contractmounth)
            year1=int(ContractYear)
            for l in range((12-int(Contractmounth)+1)):
                day_start, day_end = creat_start_end_date(mounth)
                # print(f"the mounth is: {mounth1} and year is: {year1}")
                start_date = convert_date(int(year1), int(mounth1), int(day_start))
                end_date = convert_date(int(ContractYear), int(mounth1), int(day_end))
                extracted_list = extract_info(name)
                info_special_date = extracting_info_date(extracted_list, start_date, end_date)
                BatString, UpsString, cabinetStr, UpsDiscount, CabinBatteryDiscount, ServiceDiscount, n, s, a, p, rate, info_list = calculating_scores(
                    info_special_date)
                pm.append(p)
                mounth1+=1
                if mounth1==13:
                    break

    p = 0
    for p1 in pm:
        p += p1
    if counter==0:
        counter=1
    pmean = p / counter

    if p == 0:
        pmean = 0

    return pmean


def special_score(s1, s2):
    FixScore = int(s1) * 400 + int(s2) * 500
    return (FixScore)

def convert_date(jy, jm, jd):
    jy += 1595
    days = -355668 + (365 * jy) + ((jy // 33) * 8) + (((jy % 33) + 3) // 4) + jd
    if (jm < 7):
        days += (jm - 1) * 31
    else:
        days += ((jm - 7) * 30) + 186
    gy = 400 * (days // 146097)
    days %= 146097
    if (days > 36524):
        days -= 1
        gy += 100 * (days // 36524)
        days %= 36524
        if (days >= 365):
            days += 1
    gy += 4 * (days // 1461)
    days %= 1461
    if (days > 365):
        gy += ((days - 1) // 365)
        days = (days - 1) % 365
    gd = days + 1
    if ((gy % 4 == 0 and gy % 100 != 0) or (gy % 400 == 0)):
        kab = 29
    else:
        kab = 28
    sal_a = [0, 31, kab, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    gm = 0
    while (gm < 13 and gd > sal_a[gm]):
        gd -= sal_a[gm]
        gm += 1

    return [gy, gm, gd]

def create_factor(info_special_date):
    stri = ""
    j = 0
    tempList = []
    dateList = []
    for item in info_special_date:
        stri = ""
        # temparray=[]
        j += 1
        year, mounth, day = split_date(item['Date'])
        dateday = gregorian_to_jalali(int(year), int(mounth), int(day))
        # datestr=""
        datestr = str(dateday[0]) + "/" + str(dateday[1]) + "/" + str(dateday[2])
        # for i in dateday:
        #     datestr= datestr + str(i)+"/"
        for i in item['Products']:
            stri = stri + "       " + i['OriginalTitle'] + "  تعداد  " + " : " + str(
                int(i['Quantity'])) + "  قیمت واحد  " + " : " + str(i['UnitPrice']) + "____" + "\n"
            # print("stri is: ", stri)
        # temparray=[i, stri]
        tempList.append([j, datestr, stri])
        dateList.append(datestr)

    return (tempList, dateList)


@app.route("/")
def index():
    return render_template("form1.html")


@app.route("/info", methods=["POST"])
def show_info():
    if request.method == "POST":
        user_name = request.form["q35_input35[first]"]
        password = request.form["q35_input35[last]"]
        if user_name == "admin" and password == "admin":
            return render_template("admin_1_2.html", result=user_name)
        elif user_name == "chavoshpardaz" and password == "mjs123!@#":
            return render_template("form2.html", username="شرکت فناوران ارتباطات چاوش پرداز")
        else:
            return render_template("form6_1.html")


@app.route("/select_score", methods=["Post"])
def register_score():
    s11 = 0
    s22 = 0
    y, m, d = systemdate()

    name = request.form["element_1"]
    ListScore = FindScore(con, name)
    if ListScore == []:
        InsertToScoreTable(con, name, y, m, s11, s22)
    else:
        for items1 in ListScore:
            if items1[0] == name:
                s11 = items1[3]

                s22 = items1[4]

    return render_template("admin_1_3.html", name=name, s11=s11, s22=s22)


@app.route("/enter_contract_date", methods=["POST"])
def select_date():
    name = request.form["element_1"]
    mounth = request.form["element_3_5"]
    year = request.form["element_2_2"]
    s11 = 0
    s22 = 0
    y, m, d = systemdate()

    findcontarct = FindContract(con, name)
    ListScore = FindScore(con, name)
    if ListScore == []:
        InsertToScoreTable(con, name, y, m, s11, s22)
    else:
        for items1 in ListScore:
            if items1[0] == name:
                s11 = items1[3]

                s22 = items1[4]

    if findcontarct != []:
        UpdateContractTable(con, name, year, mounth)
    else:
        InsertToContractTable(con, name, year, mounth)

    return render_template("admin_1_3.html", name=name, s11=s11, s22=s22)


@app.route("/show-user-info", methods=["POST"])
def admin_show_info():
    if request.method == "POST":
        name = request.form["element_1"]

        if request.form.get('submit') == "وروداطلاعات قرارداد":

            return render_template("contract_entery.html", name=name)
        elif request.form.get('submit') == "ادامه":
            s1 = 0
            s2 = 0
            s3 = 0

            if request.method == "POST":
                name = request.form["element_1"]

                if request.form.get("element_3_1"):
                    s11 = 1
                    # print("s11 is: ", s11)
                else:
                    s11 = 0
                if request.form.get("element_4_1"):
                    s22 = 1
                else:
                    s22 = 0
                    # print("s22 is: ", s22)

                # print("s22 is: ",s22)
                y, m, d = systemdate()
                ListScore = FindScore(con, name)

                for items1 in ListScore:
                    if items1[0] == name:
                        s111 = items1[3]

                        s222 = items1[4]
                if s11 != s111 or s22 != s222:
                    UpdateScoreTable(con, name, y, m, s11, s22)

                name = (request.form["element_1"])

                mounth = request.form["element_3_5"]
                if mounth == "1":
                    equlamounth = "فروردین"
                elif mounth == "2":
                    equlamounth = "اردیبهشت"
                elif mounth == "3":
                    equlamounth = "خرداد"
                elif mounth == "4":
                    equlamounth = "تیر"
                elif mounth == "5":
                    equlamounth = "مرداد"
                elif mounth == "6":
                    equlamounth = "شهریور"
                elif mounth == "7":
                    equlamounth = "مهر"
                elif mounth == "8":
                    equlamounth = "آبان"
                elif mounth == "9":
                    equlamounth = "آذر"
                elif mounth == "10":
                    equlamounth = "دی"
                elif mounth == "11":
                    equlamounth = "بهمن"
                elif mounth == "12":
                    equlamounth = "اسفند"
                year = request.form["element_2_2"]
                pm = CalculatePm(name, mounth, year)  # to calculate pm for mounth befor the selected mounth and add to pm for selected date
                if int(mounth) <= 6:
                    day_start = 1
                    day_end = 31
                elif int(mounth) < 12 and int(mounth) > 6:
                    day_start = 1
                    day_end = 30
                else:
                    day_start = 1
                    day_end = 29
                day_start, day_end = creat_start_end_date(mounth)
                start_date = convert_date(int(year), int(mounth), int(day_start))
                end_date = convert_date(int(year), int(mounth), int(day_end))
                extracted_list = extract_info(name)

                info_special_date = extracting_info_date(extracted_list, start_date, end_date)
                # print(f" info_special_data===={info_special_date}")

                ListContent = FindContent(con, name)
                ListScore = FindScore(con, name)

                key_value = mounth + "-" + year

                BatString, UpsString, cabinetStr, UpsDiscount, CabinBatteryDiscount, ServiceDiscount, n, s, a, p, rate, info_list = calculating_scores(
                    info_special_date)

                flag = True
                for items in ListScore:
                    if items:
                        if items[0] == name:
                            if (items[1] == year and items[2] >= mounth) or items[1] < year:
                                s1 = items[3]
                                s2 = items[4]
                                if ListContent != []:
                                    UpdateCostumerTable(con, name, s1, s2, key_value, s3)
                                else:
                                    InsertToCostumerTable(con, name, s1, s2, s3, key_value, p, s, a)
                            elif items[1] == year and items[2] < mounth:
                                s1 = 0
                                s2 = 0
                                if ListContent != []:
                                    UpdateCostumerTable(con, name, s1, s2, key_value, s3)
                                else:
                                    InsertToCostumerTable(con, name, s1, s2, s3, key_value, p, s, a)
                # changing time for calculating costumer rate
                if mounth == "1":
                    mounth_rate = 12
                    year_rate = int(year) - 1
                else:
                    mounth_rate = int(mounth) - 1
                    year_rate = year

                start_date_rate = convert_date(int(year_rate), int(mounth_rate), int(day_start))
                end_date_rate = convert_date(int(year_rate), int(mounth_rate), int(day_end))

                info_special_date_rate = extracting_info_date(extracted_list, start_date_rate, end_date_rate)
                BatString1, UpsString1, cabinetStr1, UpsDiscount1, CabinBatteryDiscount1, ServiceDiscount1, n1, s333, a1, p1, rate1, info_list1 = calculating_scores(
                    info_special_date_rate)

                if rate1 == "G1":
                    conditions = "نقد"
                elif rate1 == "G2":
                    conditions = "50 درصد نقد- 50 درصد چک یک ماهه"
                elif rate1 == "G3":
                    conditions = "چک یک ماهه"
                else:
                    conditions = "هیچ فاکتوری در ماه قبلی برای مشتری ثبت نشده است"
                smoredi = s3
                pnew = p + (0.3 * (pm))
                pnew1=pnew
                if (pnew1 > 0 and pnew1 <= 1000.0):
                    rate = "G1"
                    UpsDiscount = 12 + (pnew1 / 500)
                    CabinBatteryDiscount = 5 + (pnew1 / 1000)
                    ServiceDiscount = 8 + (pnew1 / 500)
                elif (pnew1 > 0 and pnew1 > 1000.0) & (pnew1 <= 2500.0):
                    rate = "G2"
                    UpsDiscount = 11 + ((pnew1 * 1.5) / 500)
                    CabinBatteryDiscount = 5 + ((pnew1 * 1.5) / 1000)
                    ServiceDiscount = 10 + ((pnew1 * 1.3) / 500)

                elif (pnew1 > 0 and pnew1 > 2500.0):
                    rate = "G3"
                    UpsDiscount = 9 + ((pnew1 * 2) / 500)
                    CabinBatteryDiscount = 5 + ((pnew1 * 2) / 1000)
                    ServiceDiscount = 10 + ((pnew1 * 1.8) / 500)
                elif (pnew1 == 0):
                    rate = "No rate"
                    UpsDiscount = 0
                    CabinBatteryDiscount = 0
                    ServiceDiscount = 0

            return render_template("form6.html", NumberOfBat=BatString, NumberOfUps=UpsString, Cabinet=cabinetStr,
                                   mounth=equlamounth, year=year, name=name, s=s, a=a, p=pnew, rate=rate,
                                   info_list=info_list, n=n, smoredi=smoredi, conditions=conditions,
                                   UpsDiscount=UpsDiscount, CabinBatteryDiscount=CabinBatteryDiscount,
                                   ServiceDiscount=ServiceDiscount)
        else:
            s1 = 0
            s2 = 0
            s3 = 0

            if request.method == "POST":
                name = request.form["element_1"]

                if request.form.get("element_3_1"):
                    s11 = 1
                    # print("s11 is: ", s11)
                else:
                    s11 = 0
                if request.form.get("element_4_1"):
                    s22 = 1
                else:
                    s22 = 0
                    # print("s22 is: ", s22)

                # print("s22 is: ",s22)
                y, m, d = systemdate()
                ListScore = FindScore(con, name)

                for items1 in ListScore:
                    if items1[0] == name:
                        s111 = items1[3]

                        s222 = items1[4]
                if s11 != s111 or s22 != s222:
                    UpdateScoreTable(con, name, y, m, s11, s22)

                name = (request.form["element_1"])

                mounth = request.form["element_3_5"]
                if mounth == "1":
                    equlamounth = "فروردین"
                elif mounth == "2":
                    equlamounth = "اردیبهشت"
                elif mounth == "3":
                    equlamounth = "خرداد"
                elif mounth == "4":
                    equlamounth = "تیر"
                elif mounth == "5":
                    equlamounth = "مرداد"
                elif mounth == "6":
                    equlamounth = "شهریور"
                elif mounth == "7":
                    equlamounth = "مهر"
                elif mounth == "8":
                    equlamounth = "آبان"
                elif mounth == "9":
                    equlamounth = "آذر"
                elif mounth == "10":
                    equlamounth = "دی"
                elif mounth == "11":
                    equlamounth = "بهمن"
                elif mounth == "12":
                    equlamounth = "اسفند"
                year = request.form["element_2_2"]
                pm = CalculatePm(name, mounth,
                                 year)  # to calculate pm for mounth befor the selected mounth and add to pm for selected date
                if int(mounth) <= 6:
                    day_start = 1
                    day_end = 31
                elif int(mounth) < 12 and int(mounth) > 6:
                    day_start = 1
                    day_end = 30
                else:
                    day_start = 1
                    day_end = 29
                day_start, day_end = creat_start_end_date(mounth)
                start_date = convert_date(int(year), int(mounth), int(day_start))
                end_date = convert_date(int(year), int(mounth), int(day_end))
                extracted_list = extract_info(name)

                info_special_date = extracting_info_date(extracted_list, start_date, end_date)

                ListContent = FindContent(con, name)
                ListScore = FindScore(con, name)

                key_value = mounth + "-" + year

                BatString, UpsString, cabinetStr, UpsDiscount, CabinBatteryDiscount, ServiceDiscount, n, s, a, p, rate, info_list = calculating_scores(
                    info_special_date)

                flag = True
                for items in ListScore:
                    if items:
                        if items[0] == name:
                            if (items[1] == year and items[2] >= mounth) or items[1] < year:
                                s1 = items[3]
                                s2 = items[4]
                                if ListContent != []:
                                    UpdateCostumerTable(con, name, s1, s2, key_value, s3)
                                else:
                                    InsertToCostumerTable(con, name, s1, s2, s3, key_value, p, s, a)
                            elif items[1] == year and items[2] < mounth:
                                s1 = 0
                                s2 = 0
                                if ListContent != []:
                                    UpdateCostumerTable(con, name, s1, s2, key_value, s3)
                                else:
                                    InsertToCostumerTable(con, name, s1, s2, s3, key_value, p, s, a)
                # changing time for calculating costumer rate
                if mounth == "1":
                    mounth_rate = 12
                    year_rate = int(year) - 1
                else:
                    mounth_rate = int(mounth) - 1
                    year_rate = year

                start_date_rate = convert_date(int(year_rate), int(mounth_rate), int(day_start))
                end_date_rate = convert_date(int(year_rate), int(mounth_rate), int(day_end))

                info_special_date_rate = extracting_info_date(extracted_list, start_date_rate, end_date_rate)
                BatString1, UpsString1, cabinetStr1, UpsDiscount1, CabinBatteryDiscount1, ServiceDiscount1, n1, s333, a1, p1, rate1, info_list1 = calculating_scores(
                    info_special_date_rate)

                if rate1 == "G1":
                    conditions = "نقد"
                elif rate1 == "G2":
                    conditions = "50 درصد نقد- 50 درصد چک یک ماهه"
                elif rate1 == "G3":
                    conditions = "چک یک ماهه"
                else:
                    conditions = "هیچ فاکتوری در ماه قبلی برای مشتری ثبت نشده است"
                smoredi = s3
                pnew = p + (0.3 * (pm))
                # print(f'Pm {pm}')
                # print("pnew=====", pnew)
                # print(f"n {n} , s={s},a={a},p={p} ")
            pnew1 = pnew
            if (pnew1 > 0 and pnew1 <= 1000.0):
                rate = "G1"
                # UpsDiscount = 12 + (pnew1 / 500)
                UpsDiscount = 15/100
                # CabinBatteryDiscount = 5 + (pnew1 / 1000)
                CabinBatteryDiscount =10/100
                # ServiceDiscount = 8 + (pnew1 / 500)
                ServiceDiscount =10/100
            elif (pnew1 > 0 and pnew1 > 1000.0) & (pnew1 <= 2500.0):
                rate = "G2"
                # UpsDiscount = 11 + ((pnew1 * 1.5) / 500)
                UpsDiscount =19/100
                # CabinBatteryDiscount = 5 + ((pnew1 * 1.5) / 1000)
                CabinBatteryDiscount =14/100
                # countServiceDis = 10 + ((pnew1 * 1.3) / 500)
                countServiceDis =15/100
            elif (pnew1 > 0 and pnew1 > 2500.0):
                rate = "G3"
                # UpsDiscount = 9 + ((pnew1 * 2) / 500)
                UpsDiscount =23/100
                # CabinBatteryDiscount = 5 + ((pnew1 * 2) / 1000)
                CabinBatteryDiscount =18/100
                # ServiceDiscount = 10 + ((pnew1 * 1.8) / 500)
                ServiceDiscount =20/100
            elif (pnew1 == 0):
                rate = "No rate"
                UpsDiscount = 0
                CabinBatteryDiscount = 0
                ServiceDiscount = 0

        return render_template("form6.html", NumberOfBat=BatString, NumberOfUps=UpsString, Cabinet=cabinetStr,
                                   mounth=equlamounth, year=year, name=name, s=s, a=a, p=pnew, rate=rate,
                                   info_list=info_list,
                                   n=n, smoredi=smoredi, conditions=conditions, UpsDiscount=UpsDiscount,
                                   CabinBatteryDiscount=CabinBatteryDiscount, ServiceDiscount=ServiceDiscount)


@app.route("/final-score-by-admin", methods=["POST"])
def show_final_info():
    if request.method == "POST":
        first_score = 0
        second_score = 0
        name = request.form["element_1"]
        ListContent = FindContent(con, name)
        ups_score = request.form["element_6"]
        # print("ups_score is: ",ups_score)
        battery_score = request.form["element_7"]
        final_score_CRM = request.form.get("element_8")
        costumer_rate = request.form["element_9"]
        thired_score = request.form["element_2_5"]

        mounth = request.form["element_2"]
        if mounth == "فروردین":
            mounth = "1"
        elif mounth == "اردیبهشت":
            mounth = "2"
        elif mounth == "خرداد":
            mounth = "3"
        elif mounth == "تیر":
            mounth = "4"
        elif mounth == "مرداد":
            mounth = "5"
        elif mounth == "شهریور":
            mounth = "6"
        elif mounth == "مهر":
            mounth = "7"
        elif mounth == "آبان":
            mounth = "8"
        elif mounth == "آذر":
            mounth = "9"
        elif mounth == "دی":
            mounth = "10"
        elif mounth == "بهمن":
            mounth = "11"
        elif mounth == "اسفند":
            mounth = "12"

        year = request.form["element_2_2"]
        rate = request.form["element_9"]
        UpsDiscount = request.form["element_10"]
        CabinBatteryDiscount = request.form["element_11"]
        ServiceDiscount = request.form["element_12"]
        key_value = mounth + "-" + year

        # ListScore=FindScore(con, name)

        if int(mounth) <= 6:
            day_start = 1
            day_end = 31
        elif int(mounth) < 12 and int(mounth) > 6:
            day_start = 1
            day_end = 30
        else:
            day_start = 1
            day_end = 29

        start_date = convert_date(int(year), int(mounth), int(day_start))
        # print(f"start data===={start_date}")
        end_date = convert_date(int(year), int(mounth), int(day_end))
        # print(f"end data===={end_date}")
        for items in ListContent:
            if items[0] == name and items[4] == key_value:
                first_score = items[1]
                second_score = items[2]
                UpdateCostumerTable(con, name, items[1], items[2], key_value, thired_score)

        # flag = True
        # for items in ListScore:
        #     if items:
        #         if items[0] == name:
        #             if items[1] == year:
        #                 if items[2] >= mounth:
        #                     if ListContent != []:
        #                         for items1 in ListContent:
        #                             if items1:
        #                                 if items1[0] == name:
        #                                     k = items1[4].split("-")
        #                                     print("k is; ", k)
        #                                     if int(k[0]) >= int(mounth) and int(k[1]) == int(year):
        #                                         first_score = items[3]
        #                                         print("s1 is; ", first_score)
        #                                         second_score = items[4]
        #                                         print("s2 is : ", second_score)
        #                                         s3 = 0
        # UpdateCostumerTable(con, name, first_score, second_score, key_value, thired_score)
        # print("update is done...")
        # flag = False
        # if flag == False:
        #     break
        #
        #
        # else:
        #     first_score = 0
        #     second_score = 0
        #     s3 = 0
        # print("else 1")

        # else:
        #     first_score = 0
        #     second_score = 0
        #     s3 = 0
        #     print("else 2")
        # else:
        #     first_score = items[3]
        #     second_score  = items[4]
        #     print("else 3")
        # elif items[1] < year:
        #     first_score = items[3]
        #     second_score = items[4]
        #     print("elif")

        if ListContent == []:
            InsertToCostumerTable(con, name, first_score, second_score, thired_score, key_value, final_score_CRM,
                                  ups_score, battery_score)
        # for items1 in ListScore:
        #     if items1[0] == name:
        #
        #         s11 = items1[3]
        #
        #         if s11 == 0:
        #
        #             snforush = "خیر"
        #         else:
        #             snforush = "بله"
        #
        #         s22 = items1[4]
        #
        #         if s22 == 0:
        #             snfani = "خیر"
        #         else:
        #             snfani = "بله"
        #
        #         s33 = items1[3]

        # if flag == True:
        # InsertToCostumerTable(con, name, first_score, second_score, thired_score, key_value, final_score_CRM, ups_score, battery_score)

        extracted_list = extract_info(name)

        special_score1 = special_score(first_score, second_score)
        extracted_list = extract_info(name)
        info_special_date = extracting_info_date(extracted_list, start_date, end_date)
        # print(f" info_special_data===={info_special_date}")
        factor, date = create_factor(info_special_date)
        len1 = len(factor)

        total_score = float(final_score_CRM) + special_score1

        key_score = mounth + "-" + year

        # InsertToCostumerTable(con, name, int(first_score), int(second_score),int(thired_score), key_score,  special_score1, ups_score, battery_score)
        if request.form.get('submit') == 'مشاهده گزارش فروش به تفکیک هر فاکتور':
            return render_template("form8.html", len=len1, factor=factor, date=date)
        if request.form.get('submit') == 'ورود اطلاعات و ثبت آن در دیتابیس':
            return render_template("form7.html", UpsDiscount=UpsDiscount, CabinBatteryDiscount=CabinBatteryDiscount,
                                   ServiceDiscount=ServiceDiscount, final_score_CRM=final_score_CRM,
                                   ups_score=ups_score, battery_score=battery_score, rate=rate, name=name,
                                   first_score=first_score, second_score=second_score, total_score=total_score,
                                   costumerrate=costumer_rate, mounth=mounth, year=year)

        return render_template("form7.html", UpsDiscount=UpsDiscount, CabinBatteryDiscount=CabinBatteryDiscount,
                               ServiceDiscount=ServiceDiscount, final_score_CRM=final_score_CRM, ups_score=ups_score,
                               battery_score=battery_score, rate=rate, name=name, first_score=first_score,
                               second_score=second_score, total_score=total_score, costumerrate=costumer_rate,
                               mounth=mounth, year=year)


@app.route("/result", methods=["POST"])
def show_score_info():
    conditions = "به صورت نقدی"
    if request.method == "POST":
        s111 = 0
        s222 = 0
        s333 = 0
        s2 = 0
        s1 = 0
        s3 = 0

        name = (request.form["element_3_1"])
        if name == "شرکت فناوران ارتباطات چاوش پرداز":
            name = "معمارنژاد"
        mounth = request.form["element_1_2"]
        if mounth == "1":
            equlamounth = "فروردین"
        elif mounth == "2":
            equlamounth = "اردیبهشت"
        elif mounth == "3":
            equlamounth = "خرداد"
        elif mounth == "4":
            equlamounth = "تیر"
        elif mounth == "5":
            equlamounth = "مرداد"
        elif mounth == "6":
            equlamounth = "شهریور"
        elif mounth == "7":
            equlamounth = "مهر"
        elif mounth == "8":
            equlamounth = "آبان"
        elif mounth == "9":
            equlamounth = "آذر"
        elif mounth == "10":
            equlamounth = "دی"
        elif mounth == "11":
            equlamounth = "بهمن"
        elif mounth == "12":
            equlamounth = "اسفند"
        year = request.form["element_1_3"]

        key_score = mounth + "-" + year
        pm = CalculatePm(name, mounth,
                         year)  # to calculate pm for mounth befor the selected mounth and add to pm for selected date
        if int(mounth) <= 6:
            day_start = 1
            day_end = 31
        elif int(mounth) < 12 and int(mounth) > 6:
            day_start = 1
            day_end = 30
        else:
            day_start = 1
            day_end = 29

        start_date = convert_date(int(year), int(mounth), int(day_start))
        end_date = convert_date(int(year), int(mounth), int(day_end))
        extracted_list = extract_info(name)
        info_special_date = extracting_info_date(extracted_list, start_date, end_date)
        mydoc = FindContent(con, name)
        flag = False
        for x in mydoc:
            if x[0] == name:
                print("name is found....")
                if x[4] == key_score:
                    print("key score is found")
                    if x[1] == 1:
                        s111 = x[1]
                        s1 = "دارد"
                        print("done 1")
                    else:
                        s1 = "ندارد"
                    if x[2] == 1:
                        s222 = x[2]
                        s2 = "دارد"
                        print("done 2")
                    else:
                        s2 = "ندارد"
                    s3 = x[3]
                    s333 = x[3]
                    flag = True
                    break
                else:
                    flag = False
                    s1 = "ندارد"
                    s2 = "ندارد"
                    s3 = "ندارد"

        if flag == False:
            s1 = "ندارد"
            s2 = "ندارد"
            s3 = "ندارد"
        # print("scores are", s1, s2, s3)
        BatString, UpsString, cabinetStr, UpsDiscount, CabinBatteryDiscount, ServiceDiscount, n, s, a, p, r, info_list = calculating_scores(
            info_special_date)
        # changing time for calculating costumer rate
        pnew = p + (0.3 * (pm))
        if mounth == "1":
            mounth_rate = 12
            year_rate = int(year) - 1
        else:
            mounth_rate = (int(mounth) - 1)
            year_rate = year

        start_date_rate = convert_date(int(year_rate), int(mounth_rate), int(day_start))
        end_date_rate = convert_date(int(year_rate), int(mounth_rate), int(day_end))

        info_special_date_rate = extracting_info_date(extracted_list, start_date_rate, end_date_rate)
        BatString1, UpsString1, cabinetStr1, UpsDiscount1, CabinBatteryDiscount1, ServiceDiscount1, n1, s3333, a1, p1, r1, info_list1 = calculating_scores(
            info_special_date_rate)

        if r1 == "G1":
            conditions = "نقد"
        elif r1 == "G2":
            conditions = "50 درصد نقد- 50 درصد چک یک ماهه"
        if r1 == "G3":
            conditions = "چک یک ماهه"
        totalscore = s111 * 600 + s222 * 800 + s333 + p
        if name == "معمارنژاد":
            name = "شرکت فناوران ارتباطات چاوش پرداز"

        return render_template("form4.html", NumberOfBat=BatString, NumberOfUps=UpsString, cabinetStr=cabinetStr,
                               conditions=conditions, name=name, year=year, mounth=equlamounth, UpsDiscount=UpsDiscount,
                               CabinBatteryDiscount=CabinBatteryDiscount, ServiceDiscount=ServiceDiscount, n=n, s=s,
                               a=a, p=pnew, rate=r, info_list=info_list, niruyeforush=s1, niruyefani=s2, smoredi=s3,
                               totalscore=totalscore)


@app.route("/show_factor_user", methods=["POST"])
def show_factor():
    if request.method == "POST":

        name = (request.form["element_11"])
        if name == "شرکت فناوران ارتباطات چاوش پرداز":
            name = "معمارنژاد"
        mounth = request.form["element_22"]
        if mounth == "فروردین":
            mounth = "1"
        elif mounth == "اردیبهشت":
            mounth = "2"
        elif mounth == "خرداد":
            mounth = "3"
        elif mounth == "تیر":
            mounth = "4"
        elif mounth == "مرداد":
            mounth = "5"
        elif mounth == "شهریور":
            mounth = "6"
        elif mounth == "مهر":
            mounth = "7"
        elif mounth == "آبان":
            mounth = "8"
        elif mounth == "آذر":
            mounth = "9"
        elif mounth == "دی":
            mounth = "10"
        elif mounth == "بهمن":
            mounth = "11"
        elif mounth == "اسفند":
            mounth = "12"
        year = request.form["element_33"]

        key_score = mounth + "-" + year
        if int(mounth) <= 6:
            day_start = 1
            day_end = 31
        elif int(mounth) < 12 and int(mounth) > 6:
            day_start = 1
            day_end = 30
        else:
            day_start = 1
            day_end = 29

        start_date = convert_date(int(year), int(mounth), int(day_start))
        end_date = convert_date(int(year), int(mounth), int(day_end))

        extracted_list = extract_info(name)
        info_special_date = extracting_info_date(extracted_list, start_date, end_date)
        factor, date = create_factor(info_special_date)
        len1 = len(factor)

        return render_template("form8.html", len=len1, factor=factor, date=date)


if __name__ == "__main__":
    app.debug = True
    app.run()
