from urllib.request import urlopen
from urllib import request, error
from urllib.parse import quote, urlsplit, urlunsplit
import json, urllib, time, sys, csv

def get_id(d, k):
    if k[0] in d.keys():
        try:
            if d[k[0]] is None:
                # print('1')
                return ' '
            else:
                if len(k) > 1:
                    # print('2')
                    return get_id(d[k[0]],k[1:])
                else:
                    # print('3', str(d[k[0]]))
                    return str(d[k[0]])
        except:
            return ' '
    else:
        return ' '


qw2 = 0
get_cookie = urlopen('https://dom.gosuslugi.ru/ppa/api/rest/services/ppa/current/user')
cookie = get_cookie.headers.get('Set-Cookie')
print(cookie)
animation = ["[■□□□□□□□□□]","[■■□□□□□□□□]", "[■■■□□□□□□□]", "[■■■■□□□□□□]", "[■■■■■□□□□□]", "[■■■■■■□□□□]", "[■■■■■■■□□□]", "[■■■■■■■■□□]", "[■■■■■■■■■□]", "[■■■■■■■■■■]"]
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}
region_url = "https://dom.gosuslugi.ru/nsi/api/rest/services/nsi/fias/v4/regions"
response_region = urlopen(region_url)
data_json_region = json.loads(response_region.read())
kolvo_region = len(data_json_region)
for i in range(kolvo_region):
    print(i+1,data_json_region[i]["offName"],data_json_region[i]["shortName"])
    i += 1
a = int(input('Введите номер региона, который вам интересен '))
if a>=1 and a<=i:
    print('Вы выбрали', data_json_region[a-1]["offName"],data_json_region[a-1]["shortName"])
    cities_url = "https://dom.gosuslugi.ru/nsi/api/rest/services/nsi/fias/v4/cities?actual=true&itemsPerPage=10000&page=1&regionCode="+data_json_region[a-1]["aoGuid"]
    response_cities = urlopen(cities_url)
    data_json_cities = json.loads(response_cities.read())
    kolvo_cities = len(data_json_cities)
    for j in range(kolvo_cities):
        print(j+1,data_json_cities[j]["shortName"],data_json_cities[j]["offName"])
        j += 1
    b = int(input('Введите номер населенного пункта, который вам интересен '))
    if b>=1 and b<=j:
        print('Вы выбрали', data_json_cities[b-1]["shortName"],data_json_cities[b-1]["offName"])
        print("Загрузка:")
        address_url = "https://dom.gosuslugi.ru/homemanagement/api/rest/services/houses/public/searchByAddress?pageIndex=1&elementsPerPage=10"
        post_data = {"regionCode":data_json_region[a-1]["aoGuid"],"cityCode":data_json_cities[b-1]["aoGuid"],"fiasHouseCodeList":None,"estStatus":None,"strStatus":None,"calcCount":True,"houseConditionRefList":None,"houseTypeRefList":None,"houseManagementTypeRefList":None,"cadastreNumber":None,"oktmo":None,"statuses":["APPROVED"],"regionProperty":None,"municipalProperty":None,"hostelTypeCodes":None}
        jsondata = json.dumps(post_data)
        Qdata = jsondata.encode('utf-8')
        clen = len(Qdata)
        headers2 = {
            "Content-Type": "application/json;charset=utf-8",
            "Content-Length": clen,
            "Accept": "application/json; charset=utf-8",
            "Session-GUID": "bcfd7e47-5cce-42bb-ab77-6f99be097fb5",
            "Request-GUID": "fbaa5893-e292-483f-a3b2-75f03ccdabd6",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Cookie": cookie
        }
        
        req = request.Request(address_url, Qdata, headers2)
        response_address  = request.urlopen(req)
        data_json_address = json.loads(response_address.read())
        total_address = data_json_address["total"]
        celoe = total_address // 100
        ostatok = total_address % 100
        if ostatok == 0:
            prov = celoe
        else:
            prov = celoe + 1
        for qw in range(1, prov+1):
            address_url = "https://dom.gosuslugi.ru/homemanagement/api/rest/services/houses/public/searchByAddress?pageIndex=" + str(qw) + "&elementsPerPage=100"
            post_data = {"regionCode":data_json_region[a-1]["aoGuid"],"cityCode":data_json_cities[b-1]["aoGuid"],"fiasHouseCodeList":None,"estStatus":None,"strStatus":None,"calcCount":True,"houseConditionRefList":None,"houseTypeRefList":None,"houseManagementTypeRefList":None,"cadastreNumber":None,"oktmo":None,"statuses":["APPROVED"],"regionProperty":None,"municipalProperty":None,"hostelTypeCodes":None}
            jsondata = json.dumps(post_data)
            Qdata = jsondata.encode('utf-8')
            clen = len(Qdata)
            headers2 = {
                "Content-Type": "application/json;charset=utf-8",
                "Content-Length": clen,
                "Accept": "application/json; charset=utf-8",
                "Session-GUID": "bcfd7e47-5cce-42bb-ab77-6f99be097fb5",
                "Request-GUID": "fbaa5893-e292-483f-a3b2-75f03ccdabd6",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Cookie": cookie
            }
            req = request.Request(address_url, Qdata, headers2)
            delayaddr = 10
            max_retries_addr = 10
            for _ in range(max_retries_addr):
                try:
                    response_address  = request.urlopen(req)
                    data_json_address = json.loads(response_address.read())
                    break
                except Exception:
                    time.sleep(delayaddr)
                    delayaddr *= 2
            kolvo_address = len(data_json_address["items"])
            for po in range(kolvo_address):
                pass_url = "https://dom.gosuslugi.ru/homemanagement/api/rest/services/passports/search"
                post_data_pass = {"houseGuid":data_json_address["items"][po]["guid"],"passportParameterCode":None,"page":1,"itemsPerPage":5000}
                jsondatapass = json.dumps(post_data_pass)
                Qdatapass = jsondatapass.encode('utf-8')
                clenpass = len(Qdatapass)
                passheaders2 = {
                    "Content-Type": "application/json;charset=utf-8",
                    "Content-Length": clenpass,
                    "Accept": "application/json; charset=utf-8",
                    "Session-GUID": "bcfd7e47-5cce-42bb-ab77-6f99be097fb5",
                    "Request-GUID": "fbaa5893-e292-483f-a3b2-75f03ccdabd6",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Connection": "keep-alive",
                    "Cookie": cookie
                }
                pasreq = request.Request(pass_url, Qdatapass, passheaders2)
                delaypass = 10
                max_retries_pass = 10
                for _ in range(max_retries_pass):
                    try:
                        response_pass  = request.urlopen(pasreq)
                        data_json_pass = json.loads(response_pass.read())
                        break
                    except Exception:
                        time.sleep(delaypass)
                        delaypass *= 2
                passjsonina = data_json_pass["parameters"]
                data_file_pass = open('passporthousebase.csv', 'a', newline='')
                csv_writer_pass = csv.writer(data_file_pass)
                if(qw2 == 0):
                    count = 0
                else:
                    count = 1
                aas = len(passjsonina)
                if count == 0:
                    zagolpass = ['ID дома']
                    for req in range(aas):
                        zagolpass.append(passjsonina[req]["name"])
                        req += 1
                    csv_writer_pass.writerow(zagolpass)
                    count += 1
                    qw2 = 1
                strokapass = [str(data_json_address["items"][po]["guid"])]
                for preq in range(aas):
                    strokapass.append(passjsonina[preq]["value"])
                    preq += 1
                csv_writer_pass.writerow(strokapass)
                data_file_pass.close()
                po += 1

            jsonina = data_json_address["items"]
            data_file = open('fullhousebase.csv', 'a', newline='')
            csv_writer = csv.writer(data_file)
            if(qw == 1):
                count = 0
            else:
                count = 1
            adas = len(jsonina)
            if count == 0:
                zagoladdr = ['ID дома', 'Адрес', 'Серия дома', 'Тип дома', 'Дата постройки', 'Дата ввода в эксплуатацию', 'Количество жилых помещений', 'Количество нежилых помещений', 'Название управляющей компании', 'Адрес управляющей компании', 'Телефон управляющей компании', 'ОГРН управляющей компании', 'ОМС', 'Количество этажей в доме', 'Общий износ здания в %', 'Тип дома', 'Состояние дома', 'Кадастровый номер']
                csv_writer.writerow(zagoladdr)
                count += 1
            for preq1 in range(adas):
                strokaddass = [str(get_id(jsonina[preq1], ['guid'])), str(get_id(jsonina[preq1], ['address','formattedAddress'])), str(get_id(jsonina[preq1], ['planSeries'])), str(get_id(jsonina[preq1], ['planType'])), str(get_id(jsonina[preq1], ['buildingYear'])), str(get_id(jsonina[preq1], ['operationYear'])), str(get_id(jsonina[preq1], ['residentialPremiseCount'])), str(get_id(jsonina[preq1], ['nonResidentialPremiseCount'])), str(get_id(jsonina[preq1], ['managementOrganization','fullName'])), str(get_id(jsonina[preq1], ['managementOrganization','orgAddress'])), str(get_id(jsonina[preq1], ['managementOrganization','phone'])), str(get_id(jsonina[preq1], ['managementOrganization','ogrn'])), str(get_id(jsonina[preq1], ['municipalityOrganization','fullName'])), str(get_id(jsonina[preq1], ['maxFloorCount'])), str(get_id(jsonina[preq1], ['deterioration'])), str(get_id(jsonina[preq1], ['houseType','houseTypeName'])), str(get_id(jsonina[preq1], ['houseCondition','houseCondition'])), str(get_id(jsonina[preq1], ['cadastreNumber']))]
                csv_writer.writerow(strokaddass)
                preq1 += 1
            data_file.close()
            
            pers = int((qw*100 / total_address) * 100)
            ani = pers // 10
            sys.stdout.write("\r Обработано " + str(qw*100) + " адресов из " + str(total_address) + "\n\r" + str(pers) + "% " + animation[ani  % len(animation)])
            sys.stdout.flush()
            qw +=1
        print('База всех домов с адресами в', data_json_cities[b-1]["shortName"],data_json_cities[b-1]["offName"], ' сохранена в файле fullhousebase.csv в папке проекта, а все паспорта домов сохранены в файле passporthousebase.csv')
    else:
        print('Населенного пункта с таким номером нет ')
else:
    print('Региона с таким номером нет')