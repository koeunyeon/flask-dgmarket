import pytest
import json
import dgmarket

@pytest.fixture(scope="module")  # 모듈 레벨에서 실행. 한번만 생성되면 됨.
def client():
    app = dgmarket.create_app()
    client = app.test_client()
    yield client

def test_상품_등록(client):
    # given
    data = {
        'seller_id' : 1
    }
    data = json.dumps(data)

    # when
    #result = client.post("/product/enroll", data=data)
    result = client.post("/product/enroll", data=data, content_type='application/json')

    # then
    print (result.get_json())