# django-docker
docker를 이용한 django 환경 세팅 및 nginx 배포

우선 도커를 설치하고 실행해 준다.
```
[root@dg-django ~]# yum install -y docker
[root@dg-django django-docker-tdd]# systemctl start docker
[root@dg-django django-docker-tdd]# systemctl status docker
● docker.service - Docker Application Container Engine
   Loaded: loaded (/usr/lib/systemd/system/docker.service; disabled; vendor preset: disabled)
   Active: active (running) since Tue 2021-04-06 16:23:18 KST; 3s ago
     Docs: http://docs.docker.com
 Main PID: 14966 (dockerd-current)
   CGroup: /system.slice/docker.service
           ├─14966 /usr/bin/dockerd-current --add-runtime docker-runc=/usr/li...
           └─14974 /usr/bin/docker-containerd-current -l unix:///var/run/dock...

```
원하는 세팅을 requirement.txt로 만들기 위해 프로젝트를 진행했던 프로젝트의 env 세팅을 가져온다. 나의 경우 https://velog.io/@ddengkun/django 에서 사용했던 프로젝트의 설정을 가져왔다.

```
[root@dg-django ~]# cd django
[root@dg-django django]# ls
DjangoRestApiMongoDB  env
[root@dg-django django]# source env/bin/activate
(env) [root@dg-django django]# pip freeze
asgiref==3.3.1
dataclasses==0.8
Django==3.0.5
django-cors-headers==3.7.0
djangorestframework==3.12.4
djongo==1.3.4
pymongo==3.11.3
pytz==2021.1
sqlparse==0.2.4

(env) [root@dg-django django-docker-tdd]# cd /root/django-docker-tdd

(env) [root@dg-django django-docker-tdd]# pip freeze > requirements.txt

(env) [root@dg-django django-docker-tdd]# cat requirements.txt
asgiref==3.3.1
dataclasses==0.8
Django==3.0.5
django-cors-headers==3.7.0
djangorestframework==3.12.4
djongo==1.3.4
pymongo==3.11.3
pytz==2021.1
sqlparse==0.2.4
```
아무것도 없는 상태에서 시작을 원한다면 간단하게 다음처럼 구성하면 된다.
```
Django
psycopg2
```

docker pull을 이용해 python 이미지를 가져온다.
```
[root@dg-django django-docker-tdd]# docker pull python:3.6-alpine
```

세팅될 파일을 넣기 위한 app 디렉토리를 생성한다.
```
[root@dg-django app]# mkdir app
```

dockerfile을 생성한다.
아래의 파이썬 버전은 자신이 생성한 환경에 맞게 설정해 주면 된다.
https://hub.docker.com/_/python 의 도커 허브로 들어가면 여러 버전이 나타난다. 맞는 걸 pull 해 준다.

```
[root@dg-django django-docker-tdd]# vi dockerfile

FROM python:3.6-alpine

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app
```
Dockerfile은 Docker 의 자체 언어를 사용하여 이미지를 생성하는 과정을 작성한 파일을 말한다.
FROM python:3.6-alpine # 기본 이미지 설정

ENV PYTHONUNBUFFERED 1 # 환경변수 삭제 여부 설정

COPY ./requirements.txt /requirements.txt # 현재 위치 requirements.txt 복사해서 컨테이너에 넣기
RUN pip install -r requirements.txt # docker 내 requirements.txt 파일을 이용하여 패키지 설치

RUN mkdir /app # docker 내에서 /app 폴더 생성
WORKDIR /app # docker 내에서 코드를 실행할 폴더 위치를 /app 으로 지정
COPY ./app /app # 현재 내 디렉토리의 app 디렉토리 복사해서 넣기


그리고 docker build를 해준다.
```
[root@dg-django django-docker-tdd]# docker build .
Sending build context to Docker daemon 3.072 kB
```

도커 compose 설정을 해 준다.
우선 docker-compose를 설치한다.
```
[root@dg-django django-docker-tdd]# yum install -y docker-compose
```
그리고 docker-compose.yml 파일을 만들어 준다.

```
[root@dg-django django-docker-tdd]# vi docker-compose.yml

version: "3"

services:
  app:
    build:
      context: .
    ports:
      - "8000:8000"
    volumes:
      - ./app:/app
    command: >
      sh -c "python manager.py runserver 0.0.0.0:8000"
```

docker-compose를 빌드해 준다.
```
[root@dg-django django-docker-tdd]# docker-compose build
Building app
Step 1/7 : FROM python:3.6-alpine
 ---> 68fbe3f5d554
Step 2/7 : ENV PYTHONUNBUFFERED 1
 ---> Using cache
 ---> 6030f82e7fea
Step 3/7 : COPY ./requirements.txt /requirements.txt
 ---> Using cache
 ---> aade8203c016
Step 4/7 : RUN pip install -r /requirements.txt
 ---> Using cache
 ---> ea912329c674
Step 5/7 : RUN mkdir /app
 ---> Using cache
 ---> b5c964e103e7
Step 6/7 : WORKDIR /app
 ---> Using cache
 ---> 22896504e968
Step 7/7 : COPY ./app /app
 ---> 2991df69d55d
Removing intermediate container 296a802ce539
Successfully built 2991df69d55d
```

docker-compose build가 끝나면 startproject 하기 위해 다음 명령어를 실행한다.
```
[root@dg-django django-docker-tdd]# docker-compose run app sh -c "django-admin.py startproject app ."
Creating network "djangodockertdd_default" with the default driver
[root@dg-django django-docker-tdd]# ls
app  docker-compose.yml  dockerfile  requirements.txt
[root@dg-django django-docker-tdd]# cd app/
[root@dg-django app]# ls
app  manage.py
```
그럼 프로젝트 세팅이 된 걸 확인할 수 있다.


nginx와 gunicorn 으로 django project 배포해 본다.
requirements.txt 에 gunicorn을 추가한다.

docker-compose.yml 에 nginx 내용을 추가하고, app 내의 내용을 수정한다.
```
version: "3"

services:
  app:
    build:
      context: .
    ports:
      - "8000:8000"
    volumes:
      - ./app:/app
    command: gunicorn app.wsgi:application --bind 0.0.0.0:8000
    expose:
      - "8000"
    
  nginx:
    image: nginx:latest # nginx 서비스에서 사용할 도커 이미지
    ports:
      - "80:80"
    volumes:
      - ./app:/app
      - ./config/nginx:/etc/nginx/conf.d
    depends_on: # 서비스 간의 종속성 표현
      - app
 
```
nginx.conf 파일을 만든다.(파일 위치 : ./config/nginx/nginx.conf)
```
  upstream web {
    ip_hash;
    server app:8000; # 서버의 컨테이너 명
  }

  server {
    location / {
          proxy_pass http://app/;
      }
    listen 80;
    server_name localhost;
  }
```
settings.py 에 ALLOWED_HOSTS 를 추가한다.
 ```
 ALLOWED_HOSTS = ['app']
```
아래 명령어를 입력하여 실행한 후(Terminal), 인터넷 브라우저에 localhost를 입력하여 정상적으로 작동하는지 확인한다.
  ```
docker-compose up --build
```
  
 
 ![](https://images.velog.io/images/ddengkun/post/f77e5cff-95b5-42f0-b438-dbbfdcc7e6d5/image.png)
 
 cntl + z를 통해 백그라운드로 돌리고 현재 올라간 컨테이너를 확인해 볼 수 있다.
 ```
[1]+  Stopped                 docker-compose up --build
(env) [root@dg-django django-docker-tdd]# docker ps
CONTAINER ID        IMAGE                 COMMAND                  CREATED             STATUS              PORTS                    NAMES
acf5e11fb161        nginx:latest          "/docker-entrypoin..."   2 minutes ago       Up 2 minutes        0.0.0.0:80->80/tcp       djangodockertdd_nginx_1
84502716c7c6        djangodockertdd_app   "gunicorn app.wsgi..."   2 minutes ago       Up 2 minutes        0.0.0.0:8000->8000/tcp   djangodockertdd_app_1

```
다음과 같이 올라간 걸 확인할 수 있다.
