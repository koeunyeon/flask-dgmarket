# 프로젝트 루트.
~/monolithic

# virtualenv 생성
cd monolithic

pip install virtualenv
virtualenv venv

# virtualenv 활성화
## windows
venv\Scripts\activate

## linux
. venve/bin/activate

# 의존성 설치
pip install flask
pip install flask-migrate
pip install flask-SQLAlchemy

# 데이터베이스 관련 처리
## 환경 설정
```
cd ~/monolithic

set FLASK_APP=dgmarket
set FLASK_ENV=development
```

## 마이그레이션 초기화
```
flask db init
```

## 마이그레이션 생성. 모델에서 마이그레이션 파일을 생성함.
```
flask db migrate
```

## 실제 테이블 생성
```
flask db upgrade
```

# 웹서버 실행
cd ~/monolithic

set FLASK_APP=dgmarket
set FLASK_ENV=development
flask run

# 트랜젝션 스크립트 방식으로 변경함.
2021.03.22.
최대한 간단하게 유지하기.

# pytest 설치
pip install pytest

# 테스트용 DB 생성
**가능하면 다른 터미널에서**
```
flask db upgrade
```
`init`, `migrate` 안해도 됨. 이미 있는 파일로 `upgrade`만 하면 생성됨.
`dgmarket.test.sqlite`

# 단위 테스트
python -m pytest tests -v -rP