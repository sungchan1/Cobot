import jwt   # PyJWT
import uuid
from dotenv import load_dotenv
import os
import requests
import json  # JSON 포매팅용 모듈

# .env 파일 로드
load_dotenv()

access_key = os.environ['UPBIT_OPEN_API_ACCESS_KEY']
secret_key = os.environ['UPBIT_OPEN_API_SECRET_KEY']
server_url = os.environ['UPBIT_OPEN_API_SERVER_URL']

payload = {
    'access_key': access_key,
    'nonce': str(uuid.uuid4()),
}

jwt_token = jwt.encode(payload, secret_key)
authorization_token = 'Bearer {}'.format(jwt_token)

headers = {
  'Authorization': authorization_token,
}

res = requests.get(server_url + '/v1/accounts', headers=headers)

# JSON 응답 예쁘게 출력
if res.status_code == 200:
    pretty_json = json.dumps(res.json(), indent=4, ensure_ascii=False)
    print(pretty_json)
else:
    print(f"Error {res.status_code}: {res.text}")
