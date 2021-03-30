import pytest
import dgmarket
import json
import datetime

from dgmarket.models.user_model import User


@pytest.fixture(scope="module")  # 모듈 레벨에서 실행. 한번만 생성되면 됨.
def client():
    app = dgmarket.create_app()
    client = app.test_client()
    yield client


@pytest.fixture(autouse=True, scope="function")  # 함수 레벨에서 사용.
def setup_teardown():
    with dgmarket.create_app().app_context():
        # setup
        # print("setup")
        User.query.delete()
        yield
        # teardown
        User.query.delete()


def test_api_회원가입_화면(client):
    # given

    # when
    html = client.get("/user/regist")

    # then
    assert html.status_code == 200
    assert '<form id="frm">' in str(html.get_data())


def _회원가입(client, login_email, nickname):
    data = dict(
        login_email=login_email,
        nickname=nickname
    )
    data = json.dumps(data)
    result = client.post("/user/regist", data=data,
                         content_type='application/json')
    
    return result


def test_api_회원가입_저장_성공(client):
    # given
    data = dict(
        login_email="key@koeunyeon.com",
        nickname='고은연'
    )

    # when
    result = _회원가입(client, **data)

    # then
    assert result.status_code == 200
    response_data = result.get_json()
    assert response_data['result']
    assert len(response_data['auth_key']) == 10


def test_api_회원가입_저장_실패_이메일_중복(client):
    # given
    data = dict(
        login_email="key@koeunyeon.com",
        nickname='고은연'
    )

    data_email_dup = dict(
        login_email="key@koeunyeon.com",
        nickname='고은연2'
    )

    # when
    _회원가입(client, **data)
    result = _회원가입(client, **data_email_dup)
    
    # then
    assert result.status_code == 400
    response_data = result.get_json()
    assert not response_data['result']
    assert '이미 존재하는 이메일입니다.' in response_data['message']


def test_api_회원가입_저장_실패_닉네임_중복(client):
    # given
    data = dict(
        login_email="key@koeunyeon.com",
        nickname='고은연'
    )

    data_nickname_dup = dict(
        login_email="key2@koeunyeon.com",
        nickname='고은연'
    )

    # when
    _회원가입(client, **data)
    result = _회원가입(client, **data_nickname_dup)
    
    # then
    assert result.status_code == 400
    response_data = result.get_json()
    assert not response_data['result']
    assert '이미 존재하는 별명입니다.' in response_data['message']

def _회원가입_인증(client, user_id, auth_key):
    verify_url = f"/user/regist/verify/{user_id}/{auth_key}"
    verify_result = client.get(verify_url)
    return verify_result

def test_api_회원가입_인증(client):
    # given
    given_data = dict(
        login_email="key@koeunyeon.com",
        nickname='고은연'
    )

    given_result = _회원가입(client, **given_data)
    given_response_data = given_result.get_json()
    auth_key = given_response_data['auth_key']
    user_id = given_response_data['user_id']

    # when
    verify_result = _회원가입_인증(client, user_id, auth_key)

    # then
    assert verify_result.status_code == 200

    user = User.find(user_id)
    assert user.regist_auth_complete_yn == 'Y'


def test_api_로그인_화면(client):
    # given

    # when
    html = client.get("/user/login")

    # then
    assert html.status_code == 200
    assert 'id="login"' in str(html.get_data())

def _회원가입후_인증까지(client, login_email="key@koeunyeon.com", nickname='고은연'):
    given_data = dict(
        login_email=login_email,
        nickname=nickname    )

    given_result = _회원가입(client, **given_data)
    given_response_data = given_result.get_json()
    auth_key = given_response_data['auth_key']
    user_id = given_response_data['user_id']

    _회원가입_인증(client, user_id, auth_key)
    
    # when
    data = json.dumps(
        dict(
            login_email=login_email
        )
    )
    result = client.post("/user/login", data=data,
                         content_type='application/json')
    return result


def test_api_로그인_인증키_발송(client):    
    # given
    login_email="key@koeunyeon.com"
    nickname='고은연'
    
    _회원가입후_인증까지(client, login_email, nickname)
    
    # when
    data = json.dumps(
        dict(
            login_email=login_email
        )
    )
    result = client.post("/user/login", data=data,
                         content_type='application/json')

    # then
    assert result.status_code == 200
    result_json = result.get_json()
    assert result_json['result']
    assert 'user_id' in result_json.keys()
    assert 'expired_date' in result_json.keys()
    assert 'auth_key' in result_json.keys() and len(result_json['auth_key']) == 15

    expired_date = float(result_json['expired_date'])    
    now_date = datetime.datetime.now()
    now_date = float(now_date.strftime("%Y%m%d%H%M%S"))
    assert expired_date > now_date

    #print(result.get_json())


def test_api_로그인_인증_성공(client):
    # given
    login_email="key@koeunyeon.com"
    nickname='고은연'
    
    _회원가입후_인증까지(client, login_email, nickname)

    given_data = json.dumps(
        dict(
            login_email=login_email
        )
    )
    given_result = client.post("/user/login", data=given_data,
                         content_type='application/json')
    
    # when
    given_result_json = given_result.get_json()    
    auth_key = given_result_json['auth_key']    
    user_id = given_result_json['user_id']

    auth_link = f"/user/login/verify/{user_id}/{auth_key}"
    
    when_result = client.get(auth_link)
    assert when_result.status_code == 200

    when_result_json = when_result.get_json()

    
    assert when_result_json['result']
    assert 'token' in when_result_json.keys()
    assert when_result_json['token'] != None

def _로그인_성공(client, login_email):
    data = json.dumps(
        dict(
            login_email=login_email
        )
    )
    authkey_result = client.post("/user/login", data=data,
                         content_type='application/json')
    
    
    authkey_result_json = authkey_result.get_json()    
    auth_key = authkey_result_json['auth_key']    
    user_id = authkey_result_json['user_id']

    auth_link = f"/user/login/verify/{user_id}/{auth_key}"    
    login_result = client.get(auth_link)
    return login_result


def _회원가입_인증_로그인_토큰_발급(client, login_email="key@koeunyeon.com", nickname='고은연'):    
    _회원가입후_인증까지(client, login_email, nickname)
    return _로그인_성공(client, login_email)

    

def test_api_로그인_인증_JWT_체크(client):
    # given
    login_email="key@koeunyeon.com"
    nickname='고은연'

    login_result = _회원가입_인증_로그인_토큰_발급(client, login_email, nickname)
    login_json = login_result.get_json()
    token = login_json['token']

    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = client.get('/user/login/check', headers=headers)
    
    assert response.status_code == 200
    assert response.get_json()['result']
    assert 'user' in response.get_json().keys()

    #print(headers)
    #print (response.get_data())

