import os
import shutil
from io import BytesIO

from httpx import AsyncClient

from src.core.config import app_settings
from src.models.user import User

app_settings.FILE_FOLDER = ''


async def test_ping(client: AsyncClient):
    response = await client.get('/ping/all')
    assert response.status_code == 200
    assert list(response.json().keys()) == ['db']


async def test_save_file(client_auth: AsyncClient):
    filename = 'file.txt'
    # data = {
    #     'username': 'Mike@post.com',
    #     'email': 'Mike@post.com',
    #     'password': '12345'
    # }
    # # headers = {
    # #     "Accept": "application/json",
    # #     "Content-Type": "application/x-www-form-urlencoded"
    # # }
    # response = await client.post('/auth/jwt/login', json=data)
    # assert response.status_code == 200
    # assert response.json() == "Mike@post.com"

    files = {"file": (filename, BytesIO(b'my file contents'))}
    data = dict(
        name='123',
    )

    response = await client_auth.post('/file', files=files, params=data)
    assert response.status_code == 201
    assert response.json().get('path') == filename
    assert response.json().get('name') == '123'
    os.remove(filename)


async def test_get_files_ok(client: AsyncClient, test_user_id, test_file):

    response = await client.post(
        '/auth/jwt/login',
        data={'username': 'Bob@post.com',
              'password': '12345'}
    )
    assert response.status_code == 200
    assert 'access_token' in response.json()
    token = response.json().get('access_token')
    client.headers.update({'Authorization': f'Bearer {token}'})
    response = await client.get('/file/list')
    assert response.status_code == 200
    assert response.json()[0].get('name') == 'fiylishe'
    assert response.json()[0].get('path') == '/file'


async def test_get_files_404(client_auth: AsyncClient):
    response = await client_auth.get('/file/list')
    assert response.status_code == 404

