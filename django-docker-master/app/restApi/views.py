import requests, redfish, json
import copy, os
from django.db import connection

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from restApi.models import Servers
from restApi.serializers import ServersSerializer
from rest_framework.decorators import api_view

from django.http.response import JsonResponse
from rest_framework.decorators import api_view
from influxdb import InfluxDBClient


authorization = 'Bearer eyJrIjoiWEo3cjJkQVRyTjBVRzltWEh6OEtDVk5wYzdFVWx3VWgiLCJuIjoiZ3JhZmFuYSIsImlkIjoxfQ=='


@api_view(['GET', 'POST', 'DELETE'])
def server_list(request):
    if request.method == 'GET':
        servers = Servers.objects.all()

        ip = request.GET.get('ip', None)
        if ip is not None:
            servers = servers.filter(ip__icontains=ip)

        servers_serializer = ServersSerializer(servers, many=True)
        return JsonResponse(servers_serializer.data, safe=False)
        # 'safe=False' for objects serialization

    elif request.method == 'POST':
        server_data = JSONParser().parse(request)
        ip = server_data.get('ip')
        username = server_data.get('username')
        password = server_data.get('password')
        tempThreshold = 60
        powerThreshold = 200
        server_data["tempThreshold"] = tempThreshold
        server_data["powerThreshold"] = powerThreshold


        # ip validation check
        servers = Servers.objects.all()

        if ip is not None:
            filteredServer = servers.filter(ip__icontains=ip)
        if filteredServer.count() == 0:
            print(ip)
            try:
                server_data['grafanaId'] = add_Dashboard(ip, username, password, tempThreshold, powerThreshold).get('id')
                server_data['grafanaUid'] = add_Dashboard(ip, username, password, tempThreshold, powerThreshold).get('uid')

                with open('/etc/telegraf/telegraf.conf', 'r') as file:
                    data = file.readlines()
                LINE = 31
                COLUMN = -2
                with open('../../config/ip.txt', 'r') as file:
                    localIp = file.readline().rstrip()
                CHARACTER = '\"http://' + localIp + ':8000/api/telegraf?ip=' + ip + '\", ]'
                d = list(data[LINE])
                d[COLUMN] = CHARACTER
                data[LINE] = "".join(d)
                with open('/etc/telegraf/telegraf.conf', 'w') as file:
                    file.writelines(data)
                os.system("systemctl restart telegraf")

            except:
                return JsonResponse({'message': 'ip, password, username이 잘못되었습니다.'})
        else:
            return JsonResponse({'message': '이미 존재하는 ip입니다.'})

        server_serializer = ServersSerializer(data=server_data)
        if server_serializer.is_valid():
            server_serializer.save()
            # return JsonResponse(server_serializer.data, status=status.HTTP_201_CREATED)
            return JsonResponse({'message': '추가 완료'})
        return JsonResponse({'message': '잘못된 정보입니다.'})
        # return JsonResponse(server_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        count = Servers.objects.all().delete()
        return JsonResponse({'message': '{} Tutorials were deleted successfully!'.format(count[0])},
                            status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST', 'DELETE'])
def server_check(request):
    if request.method == 'POST':
        server_data = JSONParser().parse(request)
        ip = server_data.get('ip')
        username = server_data.get('username')
        password = server_data.get('password')

        # ip validation check
        servers = Servers.objects.all()

        if ip is not None:
            filteredServer = servers.filter(ip__icontains=ip)
        if filteredServer.count() == 0:
            print(ip)
            try:
                # validation check
                try:
                    REDFISH_OBJ = redfish.redfish_client(base_url='https://' + ip,
                                                         username=username, \
                                                         password=password, default_prefix='/redfish/v1')
                except:
                    return JsonResponse({'message': 'Redfish에 접속할 수 없습니다.'})
                REDFISH_OBJ.login(auth="session")

                res = getRedfishObjectData(REDFISH_OBJ, "/redfish/v1")
                if res.get('Id') == "RootService":
                    return JsonResponse({'message': 'Redfish와 연결 가능합니다.'})
            except:
                return JsonResponse({'message': 'ip 또는 password 또는 username이 잘못되었습니다.'})
        else:
            return JsonResponse({'message': '이미 존재하는 ip입니다.'})

        return JsonResponse({'message': '잘못된 정보입니다.'})

@api_view(['GET', 'POST', 'DELETE'])
def add_datasource(request):
    if request.method == 'GET':
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json;charset=UTF-8',
            'Authorization': authorization
        }

        data = {
            "name": "InfluxDB",
            "type": "influxdb",
            "url": "http://localhost:8086",
            "access": "proxy",
            "isDefault": True,
            "database": "telegraf",
            "user": "redfish",
            "password": "redfish21"
        }

        url = 'http://admin:admin@localhost:3000/api/datasources'
        r = requests.post(url=url, headers=headers, data=json.dumps(data), verify=False)

        # notification channel
        nData = {
          "uid": "redfish-notification",
          "name": "redfish-notification",
          "type":  "email",
          "isDefault": True,
          "sendReminder": False,
          "settings": {
            "addresses": "dev@grafana.com",
            "autoResolve": True,
            "singleEmail": True,
            "uploadImage": True
          }
        }

        nUrl = 'http://admin:admin@localhost:3000/api/alert-notifications'
        n = requests.post(url=nUrl, headers=headers, data=json.dumps(nData), verify=False)
        print(n)

        return JsonResponse({'message': 'datasource & notification channel 추가 완료!'})

@api_view(['POST', 'PUT'])
def edit_notification(request):
    try:
        server_data = JSONParser().parse(request)
        email = server_data.get('email')

        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json;charset=UTF-8',
            'Authorization': authorization
        }

        data = requests.get('http://localhost:3000/api/alert-notifications/uid/redfish-notification', auth=('admin', 'admin')).json()

        nData = copy.deepcopy(data)
        nData['settings']['addresses'] += ';' + email

        nUrl = 'http://admin:admin@localhost:3000/api/alert-notifications/uid/redfish-notification'
        n = requests.put(url=nUrl, headers=headers, data=json.dumps(nData), verify=False)

        return JsonResponse({'message': '{} 추가 완료!'.format(email)})

    except:
        return JsonResponse({'message': '에러 발생'})


@api_view(['GET', 'POST', 'DELETE'])
def delete_server(request):
    if request.method == 'POST':
        server_data = JSONParser().parse(request)
        ip = server_data.get('ip')

        # ip validation check
        server = Servers.objects.get(ip=ip)
        server.delete()
        return JsonResponse({'message': '{} 삭제 완료!'.format(ip)})



def getRedfishObjectData(REDFISH_OBJ, url):
    response = REDFISH_OBJ.get(url, None).text
    return json.loads(response)

@api_view(['GET'])
def dashboard_list(request):

    dashboardList = []
    servers = []

    try:
        cursor = connection.cursor()

        strSql = "SELECT ip, username, password FROM restApi_servers"
        result = cursor.execute(strSql)
        datas = cursor.fetchall()

        connection.commit()
        connection.close()

        for data in datas:
            row = {'ip': data[0],
                   'username': data[1],
                   'password': data[2]}
            servers.append(row)

    except:
        connection.rollback()
        print("Failed selecting")
        return JsonResponse(dashboardList, safe=False)

    for server in servers:

        try:
            REDFISH_OBJ = redfish.redfish_client(base_url='https://' + server.get("ip"), username=server.get("username"), \
                                                 password=server.get("password"), default_prefix='/redfish/v1')
            REDFISH_OBJ.login(auth="session")

            res = getRedfishObjectData(REDFISH_OBJ, "/redfish/v1/Systems/")
        except:
            continue
        idUrlList = res.get("Members")

        idUrls = []
        for idUrl in idUrlList:
            idUrls.append(idUrl.get('@odata.id'))

        columnList = ['ip', 'Id', 'Name', 'SystemType', 'AssetTag', 'Manufacturer', 'Model', 'SKU', 'SerialNumber', 'PartNumber', 'Description', 'UUID', 'HostName', 'Status', 'IndicatorLED', 'PowerState', 'BiosVersion', 'ProcessorSummary', 'MemorySummary']

        for idUrl in idUrls:
            systems = {}
            urls = getRedfishObjectData(REDFISH_OBJ, idUrl)
            systems['SystemId'] = idUrl.split('/')[4]

            for c in columnList:
                systems[c] = urls.get(c)
            systems['ip'] = server.get("ip")

            print(systems)

            dashboardList.append(systems)

        REDFISH_OBJ.logout()

    return JsonResponse(dashboardList, safe=False)

@api_view(['GET'])
def instance_list(request):
    ip = request.GET.get('ip')
    instance = Servers.objects.get(ip=ip)
    REDFISH_OBJ = redfish.redfish_client(base_url='https://' + ip, username=instance.username, \
                                         password=instance.password, default_prefix='/redfish/v1')

    REDFISH_OBJ.login(auth="session")

    res = getRedfishObjectData(REDFISH_OBJ, "/redfish/v1/Systems/")

    idUrlList = res.get("Members")

    idUrls = []
    for idUrl in idUrlList:
        idUrls.append(idUrl.get('@odata.id'))

    columnList = ['Name', 'SystemType', 'Manufacturer', 'Model', 'SKU', 'SerialNumber', 'UUID', 'HostName', 'IndicatorLED', 'PowerState', 'BiosVersion']

    instanceList = []
    for idUrl in idUrls:
        systems = {}
        urls = getRedfishObjectData(REDFISH_OBJ, idUrl)

        systems['SystemId'] = idUrl.split('/')[4]

        for c in columnList:
            systems[c] = urls.get(c)
        systems["Processors"] = urls.get('ProcessorSummary').get('Model')
        systems['Status'] = urls.get('Status').get('State')
        instanceList.append(systems)

    REDFISH_OBJ.logout()
    return JsonResponse(instanceList, safe=False)

@api_view(['GET'])
def processor_list(request):
    ip = request.GET.get('ip')
    print(ip)
    instance = Servers.objects.get(ip=ip)
    REDFISH_OBJ = redfish.redfish_client(base_url='https://' + ip, username=instance.username, \
                                         password=instance.password, default_prefix='/redfish/v1')
    REDFISH_OBJ.login(auth="session")
    res = getRedfishObjectData(REDFISH_OBJ, "/redfish/v1/Systems/")
    idUrlList = res.get("Members")

    #Systems 내의 Members를 통해 서버 이름 받기
    idUrls = []
    for idUrl in idUrlList:
        # 바로 Processors로 저장
        idUrls.append(idUrl.get('@odata.id') + '/Processors')

    #processors로부터 데이터 받기
    processorUrls = []
    for idUrl in idUrls:
        res = getRedfishObjectData(REDFISH_OBJ, idUrl)

        processorUrl = res.get("Members")

        #process Url로부터 각각의 cpu, processors 받기
        for url in processorUrl:
            processorUrls.append(url.get('@odata.id'))


    # 이제 여기서부터 end point로부터 데이터 받기

    columnList = ['Id', 'Socket', 'ProcessorType', 'ProcessorArchitecture', 'InstructionSet', 'Manufacturer', 'Model', 'MaxSpeedMHz', 'TotalCores', 'TotalThreads', 'Status']

    processorList = []
    for processor in processorUrls:
        datas = {}
        urls = getRedfishObjectData(REDFISH_OBJ, processor)

        for c in columnList:
            datas[c] = urls.get(c)

        datas['Status'] = urls.get('Status').get('State')

        processorList.append(datas)

    REDFISH_OBJ.logout()
    return JsonResponse(processorList, safe=False)

@api_view(['GET'])
def storage_list(request):
    ip = request.GET.get('ip')
    instance = Servers.objects.get(ip=ip)
    REDFISH_OBJ = redfish.redfish_client(base_url='https://' + ip, username=instance.username, \
                                         password=instance.password, default_prefix='/redfish/v1')
    REDFISH_OBJ.login(auth="session")

    res = getRedfishObjectData(REDFISH_OBJ, "/redfish/v1/Systems/")

    idUrlList = res.get("Members")

    #Systems 내의 Members를 통해 서버 이름 받기
    idUrls = []
    for idUrl in idUrlList:
        # 바로 SimpleStorag로 저장
        idUrls.append(idUrl.get('@odata.id') + '/SimpleStorage')
    print('idUrls' + str(idUrls))

    #storages로부터 데이터 받기
    storageUrls = []
    for idUrl in idUrls:
        res = getRedfishObjectData(REDFISH_OBJ, idUrl)

        storageUrl = res.get("Members")

        #storageUrl로부터 각각의 url 받기
        for url in storageUrl:
            storageUrls.append(url.get('@odata.id'))


    # 이제 여기서부터 end point로부터 데이터 받기

    columnList = ['Id', 'Name', 'Description', 'UEFIDevicePath', 'Status', 'Devices']

    storageList = []
    for storage in storageUrls:
        datas = {}

        urls = getRedfishObjectData(REDFISH_OBJ, storage)

        for c in columnList:
            datas[c] = urls.get(c)

        storageList.append(datas)

    REDFISH_OBJ.logout()

    return JsonResponse(storageList, safe=False)

@api_view(['GET'])
def log_list(request):
    ip = request.GET.get('ip')
    instance = Servers.objects.get(ip=ip)
    REDFISH_OBJ = redfish.redfish_client(base_url='https://' + ip, username=instance.username, \
                                         password=instance.password, default_prefix='/redfish/v1')
    REDFISH_OBJ.login(auth="session")

    res = getRedfishObjectData(REDFISH_OBJ, "/redfish/v1/")
    if res.get("Vendor") == "HPE":
        res = getRedfishObjectData(REDFISH_OBJ, "/redfish/v1/Systems/")

        idUrlList = res.get("Members")

        #Systems 내의 Members를 통해 서버 이름 받기
        idUrls = []
        for idUrl in idUrlList:
            idUrls.append(idUrl.get('@odata.id') + '/LogServices')

        #EthernetInterfaces로부터 데이터 받기
        logUrls = []
        for idUrl in idUrls:
            print(idUrl)
            res = getRedfishObjectData(REDFISH_OBJ, idUrl)
            print(res)
            logUrl = res.get("Members")
            print(logUrl)
            #ethernet Url로부터 각각의 url받기
            for url in logUrl:
                logUrls.append(url.get('@odata.id'))


        # 이제 여기서부터 end point로부터 데이터 받기

        columnList = ['Id', 'Name', 'MaxNumberOfRecords', 'OverWritePolicy', 'DateTime', 'DateTimeLocalOffset', 'Status']

        logList = []
        entryUrls = []
        for log in logUrls:
            datas = {}

            urls = getRedfishObjectData(REDFISH_OBJ, log)

            for c in columnList:
                datas[c] = urls.get(c)
            entryUrls.append(urls.get('Entries'))
            logList.append(datas)


        #Entries 데이터 받기
        entryIds = []
        logResults = []
        for entryUrl in entryUrls:
            res = getRedfishObjectData(REDFISH_OBJ, entryUrl.get('@odata.id'))

            entryIdUrls = res.get("Members")
            #entry Url로부터 각각의 url 받기
            for url in entryIdUrls:
                entryIds.append(url.get('@odata.id'))


            # 이제 여기서부터 end point로부터 데이터 받기
            logColumnList = ['Id', 'Name', 'EntryType', 'OemRecordFormat', 'RecordId', 'Severity', 'Created', 'EntryCode', 'SensorType', 'Number', 'Message', 'MessageID', 'MessageArgs', 'Links']

            try:
                for logs in range(len(entryIds) - 1, len(entryIds) - 11, -1):
                    datas = {}
                    urls = getRedfishObjectData(REDFISH_OBJ, entryIds[logs])

                    for c in logColumnList:
                        datas[c] = urls.get(c)

                    logResults.insert(0, datas)

                resultData = {'logStatus': logList, 'logList': logResults}
            except:
                resultData = {'logStatus': logList, 'logList': logResults}

            return JsonResponse(resultData, safe=False)

    elif res.get("Vendor") == "Dell":
        res = getRedfishObjectData(REDFISH_OBJ, "/redfish/v1/Managers/")

        idUrlList = res.get("Members")

        # Systems 내의 Members를 통해 서버 이름 받기
        idUrls = []
        for idUrl in idUrlList:
            idUrls.append(idUrl.get('@odata.id') + '/LogServices')

        # EthernetInterfaces로부터 데이터 받기
        logUrls = []
        for idUrl in idUrls:
            print(idUrl)
            res = getRedfishObjectData(REDFISH_OBJ, idUrl)
            print(res)
            logUrl = res.get("Members")
            print(logUrl)
            # ethernet Url로부터 각각의 url받기
            for url in logUrl:
                logUrls.append(url.get('@odata.id'))

        # 이제 여기서부터 end point로부터 데이터 받기

        columnList = ['Id', 'Name', 'OverWritePolicy', 'DateTime']

        logList = []
        entryUrls = []
        for log in logUrls:
            datas = {}

            urls = getRedfishObjectData(REDFISH_OBJ, log)

            for c in columnList:
                datas[c] = urls.get(c)
            entryUrls.append(urls.get('Entries'))
            logList.append(datas)

        # Entries 데이터 받기
        entryIds = []
        logResults = []
        for entryUrl in entryUrls:
            res = getRedfishObjectData(REDFISH_OBJ, entryUrl.get('@odata.id'))

            entryIdUrls = res.get("Members")
            # entry Url로부터 각각의 url 받기
            for url in entryIdUrls:
                entryIds.append(url.get('@odata.id'))

            # 이제 여기서부터 end point로부터 데이터 받기
            logColumnList = ['Id', 'Name', 'EntryType', 'OemRecordFormat', 'MessageId', 'Severity', 'Created', 'Message']
            try:
                for logs in range(len(entryIds) - 1, len(entryIds) - 11, -1):
                    datas = {}
                    urls = getRedfishObjectData(REDFISH_OBJ, entryIds[logs])

                    for c in logColumnList:
                        datas[c] = urls.get(c)

                    logResults.insert(0, datas)

                resultData = {'logStatus': logList, 'logList': logResults}
            except:
                resultData = {'logStatus': logList, 'logList': logResults}



            return JsonResponse(resultData, safe=False)

    REDFISH_OBJ.logout()

@api_view(['GET'])
def memory_list(request):
    ip = request.GET.get('ip')
    instance = Servers.objects.get(ip=ip)
    REDFISH_OBJ = redfish.redfish_client(base_url='https://' + ip, username=instance.username, \
                                         password=instance.password, default_prefix='/redfish/v1')

    REDFISH_OBJ.login(auth="session")

    res = getRedfishObjectData(REDFISH_OBJ, "/redfish/v1/Systems/")

    idUrlList = res.get("Members")

    #Systems 내의 Members를 통해 서버 이름 받기
    idUrls = []
    for idUrl in idUrlList:
        # 바로 Memory로 저장
        idUrls.append(idUrl.get('@odata.id') + '/Memory')

    #Memory로부터 데이터 받기
    memoryUrls = []
    for idUrl in idUrls:
        res = getRedfishObjectData(REDFISH_OBJ, idUrl)

        memoryUrl = res.get("Members")
        print('processUrl' + str(memoryUrl))

        #process Url로부터 각각의 cpu, processors 받기
        for url in memoryUrl:
            memoryUrls.append(url.get('@odata.id'))


    # 이제 여기서부터 end point로부터 데이터 받기

    columnList = ['Name', 'CapacityMiB', 'DataWidthBits', 'BusWidthBits', 'ErrorCorrection', 'MemoryType']

    memoryList = []
    for memory in memoryUrls:
        datas = {}

        urls = getRedfishObjectData(REDFISH_OBJ, memory)

        for c in columnList:
            datas[c] = urls.get(c)

        memoryList.append(datas)

    REDFISH_OBJ.logout()
    return JsonResponse(memoryList, safe=False)

@api_view(['GET'])
def ethernet_list(request):
    ip = request.GET.get('ip')
    instance = Servers.objects.get(ip=ip)
    REDFISH_OBJ = redfish.redfish_client(base_url='https://' + ip, username=instance.username, \
                                         password=instance.password, default_prefix='/redfish/v1')
    REDFISH_OBJ.login(auth="session")

    res = getRedfishObjectData(REDFISH_OBJ, "/redfish/v1/Systems/")

    idUrlList = res.get("Members")

    #Systems 내의 Members를 통해 서버 이름 받기
    idUrls = []
    for idUrl in idUrlList:
        # 바로 EthernetInterfaces로 저장
        idUrls.append(idUrl.get('@odata.id') + '/EthernetInterfaces')

    #EthernetInterfaces로부터 데이터 받기
    ethernetUrls = []
    for idUrl in idUrls:
        res = getRedfishObjectData(REDFISH_OBJ, idUrl)

        ethernetUrl = res.get("Members")

        #ethernet Url로부터 각각의 url받기
        for url in ethernetUrl:
            ethernetUrls.append(url.get('@odata.id'))


    # 이제 여기서부터 end point로부터 데이터 받기

    columnList = ['Id', 'Name', 'Description', 'Status', 'FactoryMacAddress', 'MacAddress', 'SpeedMbps', 'FullDuplex', 'HostName', 'FQDN', 'IPv6DefaultGateway', 'NameServers', 'IPv4Addresses', 'IPv6Addresses', 'VLANs']

    ethernetList = []
    vlanUrls = []
    for ethernet in ethernetUrls:
        datas = {}

        urls = getRedfishObjectData(REDFISH_OBJ, ethernet)

        for c in columnList:
            datas[c] = urls.get(c)
        vlanUrls.append(urls.get('VLANs'))
        ethernetList.append(datas)


    #VLANs 데이터 받기
    vlanIds = []
    vlanResults = []

    for vlanUrl in vlanUrls:
        res = getRedfishObjectData(REDFISH_OBJ, vlanUrl.get('@odata.id'))

        vlanIdUrls = res.get("Members")

        #vlan Url로부터 각각의 vlan/:id 받기
        for url in vlanIdUrls:
            vlanIds.append(url.get('@odata.id'))


        # 이제 여기서부터 end point로부터 데이터 받기
        vlanColumnList = ['Id', 'Name', 'Description', 'Status', 'VLANEnable', 'VLANId']

        for vlan in vlanIds:
            datas = {}

            urls = getRedfishObjectData(REDFISH_OBJ, vlan)

            for c in vlanColumnList:
                datas[c] = urls.get(c)
            vlanResults.append(datas)


        resultData = {'ethernetList': ethernetList, 'vlanList': vlanResults}

        return JsonResponse(resultData, safe=False)
    REDFISH_OBJ.logout()

@api_view(['GET'])
def bios_list(request):
    ip = request.GET.get('ip')
    instance = Servers.objects.get(ip=ip)
    REDFISH_OBJ = redfish.redfish_client(base_url='https://' + ip, username=instance.username, \
                                         password=instance.password, default_prefix='/redfish/v1')
    REDFISH_OBJ.login(auth="session")

    res = getRedfishObjectData(REDFISH_OBJ, "/redfish/v1/Systems/")

    idUrlList = res.get("Members")

    #Systems 내의 Members를 통해 서버 이름 받기
    idUrls = []
    for idUrl in idUrlList:
        # 바로 BIOS로 저장
        idUrls.append(idUrl.get('@odata.id') + '/Bios')

    #BIOS로부터 데이터 받기
    columnList = ['Id', 'Name', 'AttributeRegistry', 'Attributes']

    biosList = []
    for idUrl in idUrls:
        systems = {}
        urls = getRedfishObjectData(REDFISH_OBJ, idUrl)

        for c in columnList:
            systems[c] = urls.get(c)

        biosList.append(systems)

    REDFISH_OBJ.logout()
    return JsonResponse(biosList, safe=False)

@api_view(['GET'])
def message_list(request):
    # ip = request.GET.get('ip')
    #
    # instance = Servers.objects.get(ip=ip)
    # REDFISH_OBJ = redfish.redfish_client(base_url='https://' + ip, username=instance.username, \
    #                                          password=instance.password, default_prefix='/redfish/v1')
    # REDFISH_OBJ.login(auth="session")
    #
    # response = getRedfishObjectData(REDFISH_OBJ, "/redfish/v1/Systems/")
    #
    # result = []
    #
    # memberRes = []
    # for member in response.get('Members'):
    #     res = member.get('@odata.id')
    #     res = baseUrl + res + "/LogServices"
    #     memberRes.append(res)
    #
    # systems = []
    #
    # for logUrls in memberRes:
    #     logUrl = requests.get(logUrls, auth=(username, password)).json()
    #     for logUrlMember in logUrl.get('Members'):
    #         logUrlResponse = baseUrl + logUrlMember.get('@odata.id') + "/Entries"
    #         systems.append(logUrlResponse)
    #
    #
    # for system in systems:
    #     systemResults = []
    #
    #     systemUrl = requests.get(system, auth=(username, password)).json()
    #
    #     for systemMember in systemUrl.get('Members'):
    #         systemData = {}
    #
    #         id = systemMember.get('@odata.id')
    #         Message = systemMember.get('Message')
    #         MessageArgs = systemMember.get('MessageArgs')
    #         MessageId = systemMember.get('MessageId')
    #         Name = systemMember.get('Name')
    #         SensorNumber = systemMember.get('SensorNumber')
    #         SensorType = systemMember.get('SensorType')
    #         Severity = systemMember.get('Severity')
    #
    #         systemData['id'] = id
    #         systemData['Message'] = Message
    #         systemData['MessageArgs'] = MessageArgs
    #         systemData['MessageId'] = MessageId
    #         systemData['Name'] = Name
    #         systemData['SensorNumber'] = SensorNumber
    #         systemData['SensorType'] = SensorType
    #         systemData['Severity'] = Severity
    #
    #         systemResults.append(systemData)
    #
    #     dataStr = systemUrl.get('@odata.id').split('/')[4] + '/' + systemUrl.get('@odata.id').split('/')[6]
    #     resultDict = {"systemId": dataStr, "systemData": systemResults}
    #     result.append(resultDict)
    result = []
    return JsonResponse(result, safe=False)

@api_view(['GET'])
def details(request):
    ip = request.GET.get('ip')

    instance = Servers.objects.get(ip=ip)
    REDFISH_OBJ = redfish.redfish_client(base_url='https://' + ip, username=instance.username, \
                                         password=instance.password, default_prefix='/redfish/v1')
    REDFISH_OBJ.login(auth="session")

    response = getRedfishObjectData(REDFISH_OBJ, "/redfish/v1/Systems/")

    result = []

    # 인스턴스 리스트
    idUrlList = response.get("Members")

    idUrls = []
    for idUrl in idUrlList:
        idUrls.append(idUrl.get('@odata.id'))

    columnList = ['Manufacturer', 'Model', 'PartNumber', 'PowerState', 'SKU', 'SystemType', 'UUID', 'State']

    for idUrl in idUrls:
        systems = {}

        urls = getRedfishObjectData(REDFISH_OBJ, idUrl)

        systems['SystemId'] = idUrl.split('/')[4]

        for c in columnList:
            systems[c] = urls.get(c)


        result.append(systems)



    # 온도 리스트
    res = getRedfishObjectData(REDFISH_OBJ, "/redfish/v1/Chassis/")

    idUrlList = res.get("Members")

    idUrls = []
    for idUrl in idUrlList:
        idUrls.append(idUrl.get('@odata.id'))


    for idUrl in idUrls:
        chassis = {}

        urls = getRedfishObjectData(REDFISH_OBJ, idUrl + "/Thermal")

        temperatureSensors = urls.get('Temperatures')

        chassis['idUrl'] = idUrl.split('/')[-1]
        chassis['tempSensors'] = temperatureSensors

        result.append(chassis)




    memberRes = []
    for member in response.get('Members'):
        res = member.get('@odata.id')
        res = res + "/LogServices"
        memberRes.append(res)

    systems = []

    for logUrls in memberRes:
        logUrl = getRedfishObjectData(REDFISH_OBJ, logUrls)

        for logUrlMember in logUrl.get('Members'):
            logUrlResponse = logUrlMember.get('@odata.id') + "/Entries"
            systems.append(logUrlResponse)


    for system in systems:
        systemResults = []

        systemUrl = getRedfishObjectData(REDFISH_OBJ, system)

        columnList = ['Message', 'MessageArgs', 'MessageId', 'Name', 'SensorNumber', 'SensorType', 'Severity']

        for systemMember in systemUrl.get('Members'):
            systemData = {}

            for c in columnList:
                systemData['id'] = systemMember.get('@odata.id')
                systemData[c] = systemMember.get(c)

            systemResults.append(systemData)

        dataStr = systemUrl.get('@odata.id').split('/')[4] + '/' + systemUrl.get('@odata.id').split('/')[6]
        resultDict = {"systemId": dataStr, "systemData": systemResults}
        result.append(resultDict)

    result = []
    REDFISH_OBJ.logout()
    return JsonResponse(result, safe=False)

@api_view(['GET'])
def chassis_list(request):
    ip = request.GET.get('ip')
    instance = Servers.objects.get(ip=ip)
    REDFISH_OBJ = redfish.redfish_client(base_url='https://' + ip, username=instance.username, \
                                         password=instance.password, default_prefix='/redfish/v1')
    REDFISH_OBJ.login(auth="session")

    res = getRedfishObjectData(REDFISH_OBJ, "/redfish/v1/Chassis/")

    idUrlList = res.get("Members")

    # Systems 내의 Members를 통해 서버 이름 받기
    idUrls = []
    for idUrl in idUrlList:
        idUrls.append(idUrl.get('@odata.id'))
    print('idUrls' + str(idUrls))


    # 이제 여기서부터 end point로부터 데이터 받기

    columnList = ['Id', 'Name', 'ChassisType', 'Manufacturer', 'Model', 'SKU',
                  'SerialNumber', 'PowerState', 'IndicatorLED']

    chassisList = []
    for chassis in idUrls:
        datas = {}

        urls = getRedfishObjectData(REDFISH_OBJ, chassis)

        for c in columnList:
            datas[c] = urls.get(c)
        datas['Status'] = urls.get('Status').get('State')

        chassisList.append(datas)
    REDFISH_OBJ.logout()
    return JsonResponse(chassisList, safe=False)

@api_view(['GET'])
def Sensors_list(request):
    ip = request.GET.get('ip')
    instance = Servers.objects.get(ip=ip)
    REDFISH_OBJ = redfish.redfish_client(base_url='https://' + ip, username=instance.username, \
                                         password=instance.password, default_prefix='/redfish/v1')
    REDFISH_OBJ.login(auth="session")

    res = getRedfishObjectData(REDFISH_OBJ, "/redfish/v1/Chassis/")

    idUrlList = res.get("Members")

    #Chassis 내의 Members를 통해 서버 이름 받기
    idUrls = []
    for idUrl in idUrlList:
        # 바로 Sensors로 저장
        idUrls.append(idUrl.get('@odata.id') + '/Sensors')
    print('idUrls' + str(idUrls))

    #Sensors로부터 데이터 받기
    sensorsUrls = []
    for idUrl in idUrls:
        res = getRedfishObjectData(REDFISH_OBJ, idUrl)

        sensorsUrl = res.get("Members")

        #PowerSuppliesUrl로부터 각각의 url받기
        for url in sensorsUrl:
            sensorsUrls.append(url.get('@odata.id'))

    ## Sensors

    # 이제 여기서부터 end point로부터 데이터 받기

    columnList = ['Id', 'Name', 'PhysicalContext', 'Reading', 'ReadingRangeMax', 'ReadingRangeMin', 'ReadingType', 'ReadingUnits', 'Status', 'Thresholds']

    sensorsList = []
    for url in sensorsUrls:
        datas = {}

        urls = getRedfishObjectData(REDFISH_OBJ, url)

        for c in columnList:
            datas[c] = urls.get(c)
        sensorsList.append(datas)

    REDFISH_OBJ.logout()
    return JsonResponse(sensorsList, safe=False)

@api_view(['GET'])
def Thermal_list(request):
    ip = request.GET.get('ip')
    instance = Servers.objects.get(ip=ip)
    REDFISH_OBJ = redfish.redfish_client(base_url='https://' + ip, username=instance.username, \
                                         password=instance.password, default_prefix='/redfish/v1')
    REDFISH_OBJ.login(auth="session")

    res = getRedfishObjectData(REDFISH_OBJ, "/redfish/v1/Chassis/")
    result = []

    idUrlList = res.get("Members")

    #Systems 내의 Members를 통해 서버 이름 받기
    idUrls = []
    for idUrl in idUrlList:
        # 바로 Thermal로 저장
        idUrls.append(idUrl.get('@odata.id') + '/Thermal')
    print('idUrls' + str(idUrls))

    #Thermal로부터 데이터 받기
    for idUrl in idUrls:
        res = getRedfishObjectData(REDFISH_OBJ, idUrl)

        temperaturesData = res.get("Temperatures")
        result.append(temperaturesData)


    # Thermal로부터 데이터 받기
    for idUrl in idUrls:
        res = getRedfishObjectData(REDFISH_OBJ, idUrl)

        fanData = res.get("Fans")
        result.append(fanData)


    # Thermal로부터 데이터 받기
    for idUrl in idUrls:
        res = getRedfishObjectData(REDFISH_OBJ, idUrl)

        redundancyData = res.get("Redundancy")
        result.append(redundancyData)

    REDFISH_OBJ.logout()
    return JsonResponse(result, safe=False)

@api_view(['GET'])
def Power_list(request):
    ip = request.GET.get('ip')
    instance = Servers.objects.get(ip=ip)
    REDFISH_OBJ = redfish.redfish_client(base_url='https://' + ip, username=instance.username, \
                                         password=instance.password, default_prefix='/redfish/v1')
    REDFISH_OBJ.login(auth="session")

    res = getRedfishObjectData(REDFISH_OBJ, "/redfish/v1/Chassis/")
    result = []

    idUrlList = res.get("Members")

    #Systems 내의 Members를 통해 서버 이름 받기
    idUrls = []
    for idUrl in idUrlList:
        # 바로 Power로 저장
        idUrls.append(idUrl.get('@odata.id') + '/Power')

    print('idUrls' + str(idUrls))

    #Thermal로부터 데이터 받기
    for idUrl in idUrls:
        res = getRedfishObjectData(REDFISH_OBJ, idUrl)

        powerControlData = res.get("PowerControl")
        result.append(powerControlData)


    # Thermal로부터 데이터 받기
    for idUrl in idUrls:
        res = getRedfishObjectData(REDFISH_OBJ, idUrl)

        voltagesData = res.get("Voltages")
        result.append(voltagesData)


    # Thermal로부터 데이터 받기
    for idUrl in idUrls:
        res = getRedfishObjectData(REDFISH_OBJ, idUrl)

        powerSuppliesData = res.get("PowerSupplies")
        result.append(powerSuppliesData)

    REDFISH_OBJ.logout()
    return JsonResponse(result, safe=False)

@api_view(['GET'])
def ChartUid_list(request):
    servers = Servers.objects.all()

    ip = request.GET.get('ip', None)
    if ip is not None:
        servers = servers.filter(ip__icontains=ip)

    servers_serializer = ServersSerializer(servers, many=True)

    return JsonResponse(servers_serializer.data, safe=False)

@api_view(['GET'])
def getLocalIp(request):
    with open('../../config/ip.txt', 'r') as file:
        data = file.readline()

    return JsonResponse({'ip': data}, safe=False)

@api_view(['GET'])
def telegraf(request):
    ip = request.GET.get('ip')
    instance = Servers.objects.get(ip=ip)
    REDFISH_OBJ = redfish.redfish_client(base_url='https://' + ip, username=instance.username, \
                                         password=instance.password, default_prefix='/redfish/v1')
    REDFISH_OBJ.login(auth="session")

    res = getRedfishObjectData(REDFISH_OBJ, "/redfish/v1/Chassis/")

    idUrlList = res.get("Members")

    #Systems 내의 Members를 통해 서버 이름 받기
    tUrls = idUrlList[0].get('@odata.id') + '/Thermal'

    #Thermal로부터 데이터 받기
    tres = getRedfishObjectData(REDFISH_OBJ, tUrls)

    temperaturesData = tres.get("Temperatures")
    resultData = []
    for data in temperaturesData:
        resultData.append({"Name": data.get("Name"), "ReadingCelsius": data.get("ReadingCelsius")})


    ###### Power ######
    # Systems 내의 Members를 통해 서버 이름 받기
    pUrls = idUrlList[0].get('@odata.id') + '/Power'

    # Thermal로부터 데이터 받기
    pres = getRedfishObjectData(REDFISH_OBJ, pUrls)
    powerData = pres.get("PowerControl")

    for data in powerData:
        resultData.append({"Name": "PowerControl", "PowerConsumedWatts": data.get("PowerConsumedWatts")})
        # resultData.append({"Name": data.get("Name"), "PowerConsumedWatts": data.get("PowerConsumedWatts")})


    result = {"result": resultData}

    REDFISH_OBJ.logout()
    return JsonResponse(result, safe=False)

def add_Dashboard(rawIp, username, password, tempThreshold, powerThreshold):

    ip = 'https://' + rawIp
    REDFISH_OBJ = redfish.redfish_client(base_url=ip, username=username, \
                                         password=password, default_prefix='/redfish/v1')
    REDFISH_OBJ.login(auth="session")

    res = getRedfishObjectData(REDFISH_OBJ, "/redfish/v1/Chassis/")

    idUrlList = res.get("Members")

    # Systems 내의 Members를 통해 서버 이름 받기
    idUrls = idUrlList[0].get('@odata.id') + '/Thermal'

    # Thermal로부터 데이터 받기
    res = getRedfishObjectData(REDFISH_OBJ, idUrls)

    temperaturesData = res.get("Temperatures")
    resultData = []
    for data in temperaturesData:
        resultData.append({"Name": data.get("Name")})

    REDFISH_OBJ.logout()

    target = []
    tempCondition = []
    powerCondition = []

    for result in resultData:
        target.append({
            "groupBy": [
                {
                    "params": [
                        "10s"
                    ],
                    "type": "time"
                },
                {
                    "params": [
                        "null"
                    ],
                    "type": "fill"
                }
            ],
            "hide": False,
            "measurement": "redfish",
            "orderByTime": "ASC",
            "policy": "default",
            "refId": result.get("Name"),
            "resultFormat": "time_series",
            "select": [
                [
                    {
                        "params": [
                            "ReadingCelsius"
                        ],
                        "type": "field"
                    },
                    {
                        "params": [],
                        "type": "mean"
                    },
                    {
                        "params": [
                            result.get("Name")
                        ],
                        "type": "alias"
                    }
                ]
            ],
            "tags": [
                {
                    "key": "Name",
                    "operator": "=",
                    "value": result.get("Name")
                }
            ]
        }, )
        if result.get("Name").find('CPU') != -1:
            tempCondition.append(
                {
                    "evaluator": {
                        "params": [
                            tempThreshold
                        ],
                        "type": "gt"
                    },
                    "operator": {
                        "type": "or"
                    },
                    "query": {
                        "params": [
                            result.get("Name"),
                            "5m",
                            "now"
                        ]
                    },
                    "reducer": {
                        "params": [],
                        "type": "last"
                    },
                    "type": "query"
                },
            )

        powerCondition.append(
            {
                "evaluator": {
                    "params": [
                        powerThreshold
                    ],
                    "type": "gt"
                },
                "operator": {
                    "type": "or"
                },
                "query": {
                    "params": [
                        "PowerConsumedWatts",
                        "5m",
                        "now"
                    ]
                },
                "reducer": {
                    "params": [],
                    "type": "last"
                },
                "type": "query"
            },
        )

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json;charset=UTF-8',
        'Authorization': authorization
    }

    data = {
        "dashboard": {
            "id": None,
            "uid": None,
            "title": '',
            "tags": ["templated"],
            "timezone": "browser",
            "schemaVersion": 16,
            "version": 0,
            "refresh": "25s",
            "panels": [
                {
                    "alert": {
                        "alertRuleTags": {},
                        "conditions": tempCondition,
                        "executionErrorState": "keep_state",
                        "for": "5m",
                        "frequency": "1m",
                        "handler": 1,
                        "message": "온도가 기준치를 초과하였습니다.",
                        "name": "Temperatures alert",
                        "noDataState": "no_data",
                        "notifications": [
                            {
                                "uid": "redfish-notification"
                            }
                        ]
                    },
                    "aliasColors": {},
                    "bars": False,
                    "dashLength": 10,
                    "dashes": False,
                    "datasource": "InfluxDB",
                    "fieldConfig": {
                        "defaults": {
                            "unit": "short"
                        },
                        "overrides": []
                    },
                    "fill": 1,
                    "fillGradient": 0,
                    "gridPos": {
                        "h": 9,
                        "w": 12,
                        "x": 0,
                        "y": 0
                    },
                    "hiddenSeries": False,
                    "id": 2,
                    "legend": {
                        "avg": True,
                        "current": True,
                        "max": True,
                        "min": True,
                        "show": True,
                        "total": False,
                        "values": True,
                        "hideZero": True,
                        "hideEmpty": True
                    },
                    "lines": True,
                    "linewidth": 1,
                    "NonePointMode": "None",
                    "options": {
                        "alertThreshold": True
                    },
                    "percentage": False,
                    "pluginVersion": "7.5.5",
                    "pointradius": 2,
                    "points": False,
                    "renderer": "flot",
                    "seriesOverrides": [],
                    "spaceLength": 10,
                    "stack": False,
                    "steppedLine": False,
                    "targets": target,
                    "thresholds": [],
                    "timeFrom": None,
                    "timeRegions": [],
                    "timeShift": None,
                    "title": "Temperatures",
                    "tooltip": {
                        "shared": True,
                        "sort": 0,
                        "value_type": "individual"
                    },
                    "type": "graph",
                    "xaxis": {
                        "buckets": None,
                        "mode": "time",
                        "name": None,
                        "show": True,
                        "values": []
                    },
                    "yaxes": [
                        {
                            "format": "short",
                            "label": None,
                            "logBase": 1,
                            "max": None,
                            "min": None,
                            "show": True
                        },
                        {
                            "format": "short",
                            "label": None,
                            "logBase": 1,
                            "max": None,
                            "min": None,
                            "show": True
                        }
                    ],
                    "yaxis": {
                        "align": False,
                        "alignLevel": None
                    }
                },
                #### power #####
                {
                    "alert": {
                        "alertRuleTags": {},
                        "conditions": powerCondition,
                        "executionErrorState": "keep_state",
                        "for": "5m",
                        "frequency": "1m",
                        "handler": 1,
                        "name": "Powers alert",
                        "noDataState": "no_data",
                        "notifications": [
                            {
                                "uid": "redfish-notification"
                            }
                        ],
                        "message": "파워가 기준치를 초과했습니다."
                    },
                    "type": "graph",
                    "title": "Powers",
                    "gridPos": {
                        "x": 0,
                        "y": 0,
                        "w": 12,
                        "h": 8
                    },
                    "id": 3,
                    "fieldConfig": {
                        "defaults": {},
                        "overrides": []
                    },
                    "pluginVersion": "7.5.5",
                    "datasource": "InfluxDB",
                    "targets": [
                        {
                            "refId": "PowerConsumedWatts",
                            "hide": False,
                            "policy": "default",
                            "resultFormat": "time_series",
                            "orderByTime": "ASC",
                            "tags": [
                                {
                                    "key": "Name",
                                    "operator": "=",
                                    "value": "PowerControl"
                                }
                            ],
                            "groupBy": [
                                {
                                    "type": "time",
                                    "params": [
                                        "10s"
                                    ]
                                },
                                {
                                    "type": "fill",
                                    "params": [
                                        "null"
                                    ]
                                }
                            ],
                            "select": [
                                [
                                    {
                                        "type": "field",
                                        "params": [
                                            "PowerConsumedWatts"
                                        ]
                                    },
                                    {
                                        "type": "mean",
                                        "params": []
                                    },
                                    {
                                        "type": "alias",
                                        "params": [
                                            "PowerConsumedWatts"
                                        ]
                                    }
                                ]
                            ],
                            "measurement": "redfish"
                        }
                    ],
                    "options": {
                        "alertThreshold": True
                    },
                    "renderer": "flot",
                    "yaxes": [
                        {
                            "label": None,
                            "show": True,
                            "logBase": 1,
                            "min": None,
                            "max": None,
                            "format": "short"
                        },
                        {
                            "label": None,
                            "show": True,
                            "logBase": 1,
                            "min": None,
                            "max": None,
                            "format": "short"
                        }
                    ],
                    "xaxis": {
                        "show": True,
                        "mode": "time",
                        "name": None,
                        "values": [],
                        "buckets": None
                    },
                    "yaxis": {
                        "align": False,
                        "alignLevel": None
                    },
                    "lines": True,
                    "fill": 1,
                    "fillGradient": 0,
                    "linewidth": 1,
                    "dashes": False,
                    "hiddenSeries": False,
                    "dashLength": 10,
                    "spaceLength": 10,
                    "points": False,
                    "pointradius": 2,
                    "bars": False,
                    "stack": False,
                    "percentage": False,
                    "legend": {
                        "show": True,
                        "values": True,
                        "min": True,
                        "max": True,
                        "current": True,
                        "total": False,
                        "avg": True,
                        "alignAsTable": True,
                        "hideZero": True,
                        "hideEmpty": True
                    },
                    "nullPointMode": "null",
                    "steppedLine": False,
                    "tooltip": {
                        "value_type": "individual",
                        "shared": True,
                        "sort": 0
                    },
                    "aliasColors": {},
                    "seriesOverrides": [],
                    "thresholds": [],
                    "timeRegions": []
                }

            ],
        },
        "folderId": 0,
        "message": "Made changes to xyz",
        "overwrite": False
    }

    dashboard_data = copy.deepcopy(data)
    dashboard_data['dashboard']['title'] = rawIp
    dashboard_data["overwrite"] = True
    url = 'http://admin:admin@localhost:3000/api/dashboards/db'
    r = requests.post(url=url, headers=headers, data=json.dumps(dashboard_data), verify=False)

    return r.json()

@api_view(['GET', 'POST'])
def edit_Dashboard(request):
    # rawIp = request.GET.get('ip', None)
    # print(rawIp)
    server_data = JSONParser().parse(request)
    rawIp = server_data.get('ip')
    tempThreshold = int(server_data.get('tempThreshold'))
    powerThreshold = int(server_data.get('powerThreshold'))

    post_instance = Servers.objects.get(ip=rawIp)
    post_instance.tempThreshold = tempThreshold
    post_instance.powerThreshold = powerThreshold
    post_instance.save()

    ip = 'https://' + rawIp
    REDFISH_OBJ = redfish.redfish_client(base_url=ip, username=post_instance.username, \
                                         password=post_instance.password, default_prefix='/redfish/v1')
    REDFISH_OBJ.login(auth="session")

    res = getRedfishObjectData(REDFISH_OBJ, "/redfish/v1/Chassis/")

    idUrlList = res.get("Members")

    # Systems 내의 Members를 통해 서버 이름 받기
    idUrls = idUrlList[0].get('@odata.id') + '/Thermal'

    # Thermal로부터 데이터 받기
    res = getRedfishObjectData(REDFISH_OBJ, idUrls)

    temperaturesData = res.get("Temperatures")
    resultData = []
    for data in temperaturesData:
        resultData.append({"Name": data.get("Name")})

    REDFISH_OBJ.logout()

    target = []
    tempCondition = []
    powerCondition = []

    for result in resultData:
        target.append({
                            "groupBy": [
                                {
                                    "params": [
                                        "10s"
                                    ],
                                    "type": "time"
                                },
                                {
                                    "params": [
                                        "null"
                                    ],
                                    "type": "fill"
                                }
                            ],
                            "hide": False,
                            "measurement": "redfish",
                            "orderByTime": "ASC",
                            "policy": "default",
                            "refId": result.get("Name"),
                            "resultFormat": "time_series",
                            "select": [
                                [
                                    {
                                        "params": [
                                            "ReadingCelsius"
                                        ],
                                        "type": "field"
                                    },
                                    {
                                        "params": [],
                                        "type": "mean"
                                    },
                                    {
                                        "params": [
                                            result.get("Name")
                                        ],
                                        "type": "alias"
                                    }
                                ]
                            ],
                            "tags": [
                                {
                                    "key": "Name",
                                    "operator": "=",
                                    "value": result.get("Name")
                                }
                            ]
                        },)
        if result.get("Name").find('CPU') != -1:
            tempCondition.append(
                {
                    "evaluator": {
                        "params": [
                            tempThreshold
                        ],
                        "type": "gt"
                    },
                    "operator": {
                        "type": "or"
                    },
                    "query": {
                        "params": [
                            result.get("Name"),
                            "5m",
                            "now"
                        ]
                    },
                    "reducer": {
                        "params": [],
                        "type": "last"
                    },
                    "type": "query"
                },
            )

        powerCondition.append(
            {
                "evaluator": {
                    "params": [
                        powerThreshold
                    ],
                    "type": "gt"
                },
                "operator": {
                    "type": "or"
                },
                "query": {
                    "params": [
                        "PowerConsumedWatts",
                        "5m",
                        "now"
                    ]
                },
                "reducer": {
                    "params": [],
                    "type": "last"
                },
                "type": "query"
            },
        )




    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json;charset=UTF-8',
        'Authorization': authorization
    }

    data = {
        "dashboard": {
            "id": None,
            "uid": None,
            "title": '',
            "tags": ["templated"],
            "timezone": "browser",
            "schemaVersion": 16,
            "version": 0,
            "refresh": "25s",
            "panels": [
                {
                    "alert": {
                        "alertRuleTags": {},
                        "conditions": tempCondition,
                        "executionErrorState": "keep_state",
                        "for": "5m",
                        "frequency": "1m",
                        "handler": 1,
                        "message": "온도가 기준치를 초과하였습니다.",
                        "name": "Temperatures alert",
                        "noDataState": "no_data",
                        "notifications": [
                            {
                                "uid": "redfish-notification"
                            }
                        ]
                    },
                    "aliasColors": {},
                    "bars": False,
                    "dashLength": 10,
                    "dashes": False,
                    "datasource": "InfluxDB",
                    "fieldConfig": {
                        "defaults": {
                            "unit": "short"
                        },
                        "overrides": []
                    },
                    "fill": 1,
                    "fillGradient": 0,
                    "gridPos": {
                        "h": 9,
                        "w": 12,
                        "x": 0,
                        "y": 0
                    },
                    "hiddenSeries": False,
                    "id": 2,
                    "legend": {
                        "avg": True,
                        "current": True,
                        "max": True,
                        "min": True,
                        "show": True,
                        "total": False,
                        "values": True,
                        "hideZero": True,
                        "hideEmpty": True
                    },
                    "lines": True,
                    "linewidth": 1,
                    "NonePointMode": "None",
                    "options": {
                        "alertThreshold": True
                    },
                    "percentage": False,
                    "pluginVersion": "7.5.5",
                    "pointradius": 2,
                    "points": False,
                    "renderer": "flot",
                    "seriesOverrides": [],
                    "spaceLength": 10,
                    "stack": False,
                    "steppedLine": False,
                    "targets": target,
                    "thresholds": [],
                    "timeFrom": None,
                    "timeRegions": [],
                    "timeShift": None,
                    "title": "Temperatures",
                    "tooltip": {
                        "shared": True,
                        "sort": 0,
                        "value_type": "individual"
                    },
                    "type": "graph",
                    "xaxis": {
                        "buckets": None,
                        "mode": "time",
                        "name": None,
                        "show": True,
                        "values": []
                    },
                    "yaxes": [
                        {
                            "format": "short",
                            "label": None,
                            "logBase": 1,
                            "max": None,
                            "min": None,
                            "show": True
                        },
                        {
                            "format": "short",
                            "label": None,
                            "logBase": 1,
                            "max": None,
                            "min": None,
                            "show": True
                        }
                    ],
                    "yaxis": {
                        "align": False,
                        "alignLevel": None
                    }
                },
#### power #####
                {
                    "alert": {
                        "alertRuleTags": {},
                        "conditions": powerCondition,
                        "executionErrorState": "keep_state",
                        "for": "5m",
                        "frequency": "1m",
                        "handler": 1,
                        "name": "Powers alert",
                        "noDataState": "no_data",
                        "notifications": [
                            {
                                "uid": "redfish-notification"
                            }
                        ],
                        "message": "파워가 기준치를 초과했습니다."
                    },
                    "type": "graph",
                    "title": "Powers",
                    "gridPos": {
                        "x": 0,
                        "y": 0,
                        "w": 12,
                        "h": 8
                    },
                    "id": 3,
                    "fieldConfig": {
                        "defaults": {},
                        "overrides": []
                    },
                    "pluginVersion": "7.5.5",
                    "datasource": "InfluxDB",
                    "targets": [
                        {
                            "refId": "PowerConsumedWatts",
                            "hide": False,
                            "policy": "default",
                            "resultFormat": "time_series",
                            "orderByTime": "ASC",
                            "tags": [
                                {
                                    "key": "Name",
                                    "operator": "=",
                                    "value": "PowerControl"
                                }
                            ],
                            "groupBy": [
                                {
                                    "type": "time",
                                    "params": [
                                        "10s"
                                    ]
                                },
                                {
                                    "type": "fill",
                                    "params": [
                                        "null"
                                    ]
                                }
                            ],
                            "select": [
                                [
                                    {
                                        "type": "field",
                                        "params": [
                                            "PowerConsumedWatts"
                                        ]
                                    },
                                    {
                                        "type": "mean",
                                        "params": []
                                    },
                                    {
                                        "type": "alias",
                                        "params": [
                                            "PowerConsumedWatts"
                                        ]
                                    }
                                ]
                            ],
                            "measurement": "redfish"
                        }
                    ],
                    "options": {
                        "alertThreshold": True
                    },
                    "renderer": "flot",
                    "yaxes": [
                        {
                            "label": None,
                            "show": True,
                            "logBase": 1,
                            "min": None,
                            "max": None,
                            "format": "short"
                        },
                        {
                            "label": None,
                            "show": True,
                            "logBase": 1,
                            "min": None,
                            "max": None,
                            "format": "short"
                        }
                    ],
                    "xaxis": {
                        "show": True,
                        "mode": "time",
                        "name": None,
                        "values": [],
                        "buckets": None
                    },
                    "yaxis": {
                        "align": False,
                        "alignLevel": None
                    },
                    "lines": True,
                    "fill": 1,
                    "fillGradient": 0,
                    "linewidth": 1,
                    "dashes": False,
                    "hiddenSeries": False,
                    "dashLength": 10,
                    "spaceLength": 10,
                    "points": False,
                    "pointradius": 2,
                    "bars": False,
                    "stack": False,
                    "percentage": False,
                    "legend": {
                        "show": True,
                        "values": True,
                        "min": True,
                        "max": True,
                        "current": True,
                        "total": False,
                        "avg": True,
                        "alignAsTable": True,
                        "hideZero": True,
                        "hideEmpty": True
                    },
                    "nullPointMode": "null",
                    "steppedLine": False,
                    "tooltip": {
                        "value_type": "individual",
                        "shared": True,
                        "sort": 0
                    },
                    "aliasColors": {},
                    "seriesOverrides": [],
                    "thresholds": [],
                    "timeRegions": []
                }

            ],
        },
        "folderId": 0,
        "message": "Made changes to xyz",
        "overwrite": False
    }

    dashboard_data = copy.deepcopy(data)
    dashboard_data['dashboard']['title'] = rawIp
    dashboard_data["overwrite"] = True
    url = 'http://admin:admin@localhost:3000/api/dashboards/db'
    r = requests.post(url=url, headers=headers, data=json.dumps(dashboard_data), verify=False)

    return JsonResponse(r.json())

@api_view(['GET'])
def getCardData(request):
    cardList = []
    serverIPs = []

    try:
        cursor = connection.cursor()

        strSql = "SELECT ip FROM restApi_servers"
        result = cursor.execute(strSql)
        datas = cursor.fetchall()
        print(datas)

        connection.commit()
        connection.close()

        for data in datas:
            row = data[0]
            serverIPs.append(row)

    except:
        connection.rollback()
        print("Failed selecting")

    for ip in serverIPs:
        try:
            instance = Servers.objects.get(ip=ip)
            REDFISH_OBJ = redfish.redfish_client(base_url="https://" + ip, username=instance.username, \
                                                 password=instance.password, default_prefix='/redfish/v1')
            REDFISH_OBJ.login(auth="session")
            res = getRedfishObjectData(REDFISH_OBJ, "/redfish/v1/Chassis/")
        except:
            continue

        idUrlList = res.get("Members")
        # Systems 내의 Members를 통해 서버 이름 받기
        tUrls = idUrlList[0].get('@odata.id') + '/Thermal'

        # Thermal로부터 데이터 받기
        tres = getRedfishObjectData(REDFISH_OBJ, tUrls)

        temperaturesData = tres.get("Temperatures")
        resultData = []
        color = "Blue"
        part = None

        try:
            resultData.append({"ip": ip, "tempThreshold": instance.tempThreshold, "powerThreshold": instance.powerThreshold})
        except:
            resultData.append({"ip": ip, "tempThreshold": None, "powerThreshold": None})

        for data in temperaturesData:
            if data.get("PhysicalContext") == "CPU":
                resultData.append({"Name": data.get("Name"), "ReadingCelsius": data.get("ReadingCelsius")})
                if data.get("ReadingCelsius") == None or instance.tempThreshold == None:
                    continue
                elif color != "Red" and data.get("ReadingCelsius") >= instance.tempThreshold:
                    color = "Red"
                    part = "Temp"
                elif color == "Blue" and instance.tempThreshold > data.get("ReadingCelsius") >= instance.tempThreshold - 5:
                    color = "Orange"

        ###### Power ######
        # Systems 내의 Members를 통해 서버 이름 받기
        pUrls = idUrlList[0].get('@odata.id') + '/Power'

        # Thermal로부터 데이터 받기
        pres = getRedfishObjectData(REDFISH_OBJ, pUrls)
        powerData = pres.get("PowerControl")

        for data in powerData:
            resultData.append({"Name": "PowerControl", "PowerConsumedWatts": data.get("PowerConsumedWatts")})
            if data.get("PowerConsumedWatts") != None or instance.powerThreshold == None:
                continue
            elif color != "Red" and data.get("PowerConsumedWatts") >= instance.powerThreshold:
                color = "Red"
                part = "Power"
            elif color == "Red" and data.get("PowerConsumedWatts") >= instance.powerThreshold:
                part = "Both"
            elif color == "Blue" and instance.powerThreshold > data.get("PowerConsumedWatts") >= instance.powerThreshold - 10 and instance.powerThreshold != None:
                color = "Orange"


            # resultData.append({"Name": data.get("Name"), "PowerConsumedWatts": data.get("PowerConsumedWatts")})

        result = {"result": resultData, "color": color, "part": part}
        cardList.append(result)
        REDFISH_OBJ.logout()

    return JsonResponse(cardList, safe=False)

#
# @api_view(['GET', 'POST', 'DELETE'])
# def getThreshold(request):
#     if request.method == 'GET':
#
#         ip = request.GET.get('ip', None)
#         instance = Servers.objects.get(ip=ip)
#         result = {"tempThreshold": instance.tempThreshold, "powerThreshold": instance.powerThreshold}
#
#         return JsonResponse(result, safe=False)
#         # 'safe=False' for objects serialization




