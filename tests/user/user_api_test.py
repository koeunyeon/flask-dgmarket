import pytest
import dgmarket
import json

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
        print("setup")
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


def test_api_회원가입_저장_성공(client):
    # given
    data = dict(
        login_email="key@koeunyeon.com",
        nickname='고은연'
    )
    data = json.dumps(data)

    # when
    result = client.post("/user/regist", data=data,
                         content_type='application/json')

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
    data = json.dumps(data)

    # when
    result = client.post("/user/regist", data=data,
                         content_type='application/json')
    
    # 일부러 두 번. 이메일만 남겨둔다.
    data = dict(
        login_email="key@koeunyeon.com",
        nickname='고은연2'
    )
    data = json.dumps(data)

    result = client.post("/user/regist", data=data,
                         content_type='application/json')
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
    data = json.dumps(data)

    # when
    result = client.post("/user/regist", data=data,
                         content_type='application/json')
    
    # 일부러 두 번. 이름만 그대로 둠.
    data = dict(
        login_email="key2@koeunyeon.com",
        nickname='고은연'
    )
    data = json.dumps(data)
    result = client.post("/user/regist", data=data,
                         content_type='application/json')
    # then
    assert result.status_code == 400
    response_data = result.get_json()
    assert not response_data['result']
    assert '이미 존재하는 별명입니다.' in response_data['message']     

def test_api_회원가입_인증(client):
    # given
    given_data = dict(
        login_email="key@koeunyeon.com",
        nickname='고은연'
    )
    given_data = json.dumps(given_data)
    given_result = client.post("/user/regist", data=given_data,
                         content_type='application/json')

    given_response_data = given_result.get_json()
    auth_key = given_response_data['auth_key']
    user_id = given_response_data['user_id']

    # when
    verify_url = f"/user/regist/verify/{user_id}/{auth_key}"
    verify_result = client.get(verify_url)
    
    #print (verify_result.get_data())

    # then
    assert verify_result.status_code == 200

    user = User.find(user_id)
    assert user.regist_auth_complete_yn == 'Y'

