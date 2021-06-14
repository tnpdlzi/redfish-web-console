# 인턴십 프로젝트
# Redfish 웹 콘솔화 프로젝트

## 프로젝트 진행 이유
웹 콘솔 없이 Redfish API만 사용했을 경우 불편한 점
- web을 이용한 제어 콘솔의 부재
- 동시에 여러 대의 서버 상태 파악의 어려움
- 정보 파악을 위해 매 번 거쳐야하는 인증 과정(로그인)
- 데이터에 대한 시각화 기능 부재
- 저장되지 않는 데이터에 의한 Trend 파악의 어려움


django / vue.js를 이용한 web 관리 콘솔
- login, 권한, 접근제어등 부가적인 기능 불필요
- 온도, 파워 monitoring 기능
- trend graph, threshold alert
- log monitor
- BIOS, firmware 버전 확인
- 서버 추가, 삭제 기능
- Processor, Memory 등 서버에 대한 정보 확인
- configure 설정/변경

## 프로젝트 구성
웹 view를 위한 vue.js
Redfish API 사용을 위한 Django
Server Monitoring을 위한 Telegraf, InfluxDB, Grafana


실행 방법


OS : CentOS 7

사용 포트

django : :8000

vue.js : :8080

grafana : :3000

## django, vue 프로젝트 설치 및 mysql 설치

### mysql 5.6 설치
```
# wget http://repo.mysql.com/mysql-community-release-el7-5.noarch.rpm
# rpm -ivh mysql-community-release-el7-5.noarch.rpm
```
```
# yum install -y mysql-server
# systemctl start mysqld
# systemctl enable mysqld
```
비밀번호 설정 (password: redfish21)
```
# mysql_secure_installation

Enter current password for root (enter for none): 
Change the root password? [Y/n] y
New password: redfish21
Re-enter new password: redfish21
Remove anonymous users? [Y/n] y
Disallow root login remotely? [Y/n] y
Remove test database and access to it? [Y/n] y
Reload privilege tables now? [Y/n] y
```
database 생성
```
# mysql -u root -p
> CREATE DATABASE redfish;
> exit
```
### 프로젝트 설치

필요한 packages 설치
```
# yum install -y git mysql-devel gcc

# yum install -y epel-release.noarch
# yum install -y https://repo.ius.io/ius-release-el7.rpm
# yum install -y python36u python36u-devel
```
git clone project
```
# git clone https://git.toastoven.net/intern/redfish_project_dg.git
# cd redfish_project_dg/django-docker-master/
```
파이썬 가상환경 세팅
```
# python3 -m venv ./env
# source env/bin/activate
```
파이썬 패키지 설치
```
# pip install --upgrade pip
# pip install -r requirements.txt
```
django migration 및 실행
```
# cd app
# python manage.py migrate
# gunicorn app.wsgi:application --bind 0.0.0.0:8000

# ctrl + z
# bg
```
node 및 npm 설치
```
# cd ../../vue-cards

# yum -y install curl
# curl -sL https://rpm.nodesource.com/setup_14.x | bash -
# yum install -y nodejs
```
프로젝트 패키지 설치 및 실행
```
# npm install chokidar
# npm install @vue/cli-service --unsafe-perm
# npm install
# npm run serve

# ctrl + z
# bg
```
local ip 저장
```
# cd ~/redfish_project_dg

# vi config/ip.txt
(grafana 호스트 ip 입력)
ex) 127.0.0.1

# echo "(grafana 호스트 ip 입력) influxdb" >> /etc/hosts
ex) echo "127.0.0.1 influxdb" >> /etc/hosts
```

## influxdb, telegraf, grafana 설치
### influxdb 설치 및 실행
```
# cd ~/redfish_project_dg

# cat <<EOF | tee /etc/yum.repos.d/influxdb.repo
[influxdb]
name = InfluxDB Repository - RHEL \$releasever
baseurl = https://repos.influxdata.com/rhel/\$releasever/\$basearch/stable
enabled = 1
gpgcheck = 1
gpgkey = https://repos.influxdata.com/influxdb.key
EOF

# yum install -y influxdb
# systemctl start influxdb
# systemctl enable influxdb
```
influxdb 계정 생성 (username: redfish, password: redfish21)
```
# influx
> CREATE USER redfish WITH PASSWORD 'redfish21' WITH ALL PRIVILEGES
> show users
user    admin
----    -----
redfish true

> exit
```
### grafana 설치 및 실행
```
# cat <<EOF | tee /etc/yum.repos.d/grafana.repo
[grafana]
name=grafana
baseurl=https://packages.grafana.com/oss/rpm
repo_gpgcheck=1
enabled=1
gpgcheck=1
gpgkey=https://packages.grafana.com/gpg.key
sslverify=1
sslcacert=/etc/pki/tls/certs/ca-bundle.crt
EOF

# yum install -y grafana ssmtp
# cp ./config/grafana.ini /etc/grafana/grafana.ini
# cp ./config/ssmtp.conf /etc/ssmtp/ssmtp.conf
# systemctl start grafana-server
# systemctl enable grafana-server
```
grafana datasource 추가
```
# curl -X GET http://localhost:8000/api/datasources
```
### telegraf 설치 및 실행
```
# yum install -y telegraf

# cp ./config/telegraf.conf /etc/telegraf/telegraf.conf 

# systemctl start telegraf
# systemctl enable telegraf
```

# 사용자 이용 가이드

## 서버 리스트
좌상단의 Server List 클릭 / 첫 페이지

![image](/uploads/2bbafa80cce6e41b23be8b469bf96fe6/image.png)

테이블 기본 기능
- 총 x 행씩 보기
- Copy, Excel, PDF Export
- Column visibility
- 검색 기능
- pagenation
- Column sorting

ip column에 적힌 ip 클릭시
- https 연결이 되며 해당 벤더사의 하드웨어 컨트롤 페이지로 이동

상세보기 클릭시
- 해당 서버에 대한 상세한 내용 확인 가능

### Add Server
좌상단의 'Add Server' 클릭시

![image](/uploads/ce7f1910102d1309dc919a15b0937c96/image.png)

다음과 같은 모달 창이 생기며 IP, User Name, Password 입력시 서버 추가 가능
서버 연결 확인 버튼을 통해 추가 전 서버 연결 여부 확인 가능

### Delete Server
좌상단의 'Delete Server' 클릭시

![image](/uploads/841f020d7303a43d8bb2a706a1262019/image.png)

다음과 같은 모달 창이 생기며 IP 입력시 서버 삭제 가능

## 대시보드
좌상단의 Dashboard 클릭시

![image](/uploads/797d1b6b98679da03856ce8743c14904/image.png)

- 빨강 - 주황 - 파랑 순으로 임계치와 가까워진 서버를 표시
- 빨강은 현재 상태가 임계치 이상인 경우. 주황은 온도가 임계치 - 5℃ 이내 or Power가 - 10 Watts 이내인 경우.
- 빨강의 경우 임계치가 넘은 값을 붉은색의 텍스트로 나타내며 온도만 넘은 경우 온도를, 파워만 넘은 경우 파워만 나타내며 둘 다 넘은 경우 두 개 다 표시된다.
- 최초의 임계치 값은 60 / 200 으로 고정. 변경은 상세보기 페이지에서 가능

### 하나의 카드
![image](/uploads/98a096e0b43a7dedcfdc2357b1a86453/image.png)

- 카드의 상단 색상 부분 클릭시 상세보기 페이지로 이동
- 센서 이름와 값으로 매핑되어 나타내어진다.
- 온도의 경우 CPU를 기준으로 나타낸다.
- 파워의 경우 현재 소비중인 Watts로 나타낸다.

## 상세정보

### Details
![image](/uploads/46cdd6a79a643b51a4b6ea73030f5d6e/image.png)

- Systems, Chassis, Processors, Memory로 구성
- 해당 하는 사항을 텍스트로 확인 가능

### Charts
![image](/uploads/d259b777869c257dec38bfff3fbdce6a/image.png)

- Grafana embedded Charts
- Grafana Chart. 상단에 온도, 하단에 파워 그래프 표시.
- 우상단에서 시간 조정, Save Dashboard, Dashboard Setting 등 변경 가능

![image](/uploads/a0dc0430a3bb62242eea90134cdccca5/image.png)

- 임계치 설정. 온도, 파워 임계치 설정 가능.
- Dashboard에서 나타나는 위험도에 따른 임계치도 이 값을 따른다.
- Alert 받을 이메일 추가 가능.
- 임계치를 넘긴 시간이 5분 이상이 되면 이메일 발송.

### BIOS
![image](/uploads/d0fafdd9b93784bf2813030efe350f9f/image.png)

- bios 정보를 텍스트로 확인 가능

### logs
![image](/uploads/91ca7ad2189a9035ad4c18a1a482433e/image.png)

- log status는 어떤 로그인지에 대한 정보를 나타낸다.

![image](/uploads/0059be83aad0009db221014cff2279f3/image.png)

- log list는 해당하는 로그 이름과 날짜, 메시지를 나타낸다.
- 최근 10개의 로그만  출력된다.