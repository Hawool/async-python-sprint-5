import os
from io import BytesIO

from httpx import AsyncClient

import src.api.v1.file_storage


async def test_ping(client: AsyncClient):
    response = await client.get('/ping/all')
    assert response.status_code == 200
    assert list(response.json().keys()) == ['db']


async def test_save_file(client_auth: AsyncClient):
    filename = 'file.txt'

    files = {"file": (filename, BytesIO(b'my file contents'))}
    data = dict(
        name='123',
    )

    response = await client_auth.post('/file', files=files, params=data)
    assert response.status_code == 201
    assert response.json().get('path') == filename
    assert response.json().get('name') == '123'
    os.remove(filename)


async def test_save_file_big_file(client_auth: AsyncClient):
    filename = 'file.txt'

    files = {"file": (filename, BytesIO(b'my file contents'*100000))}
    data = dict(
        name='123',
    )

    response = await client_auth.post('/file', files=files, params=data)
    assert response.status_code == 413
    assert response.json() == {'detail': 'File more than 1 Mb'}


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
    assert response.json()[0].get('path') == 'conftest.py'


async def test_get_files_404(client_auth: AsyncClient):
    response = await client_auth.get('/file/list')
    assert response.status_code == 404


async def test_get_usage_memory(client: AsyncClient, mocker, test_user_id, test_file):
    mocker.patch(
        'src.api.v1.file_storage.calculate_file_size',
        return_value=10
    )
    response = await client.post(
        '/auth/jwt/login',
        data={'username': 'Bob@post.com',
              'password': '12345'}
    )
    assert response.status_code == 200
    assert 'access_token' in response.json()
    token = response.json().get('access_token')
    client.headers.update({'Authorization': f'Bearer {token}'})
    response = await client.get('/file/usage_memory')
    assert response.status_code == 200
    assert response.json().get('files') == 10


async def test_get_usage_memory_404(client: AsyncClient, mocker, test_user_id):

    response = await client.post(
        '/auth/jwt/login',
        data={'username': 'Bob@post.com',
              'password': '12345'}
    )
    assert response.status_code == 200
    assert 'access_token' in response.json()
    token = response.json().get('access_token')
    client.headers.update({'Authorization': f'Bearer {token}'})
    response = await client.get('/file/usage_memory')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Not found'}


async def test_download_404(client: AsyncClient, test_user_id, test_file):

    response = await client.post(
        '/auth/jwt/login',
        data={'username': 'Bob@post.com',
              'password': '12345'}
    )
    assert response.status_code == 200
    assert 'access_token' in response.json()
    token = response.json().get('access_token')
    client.headers.update({'Authorization': f'Bearer {token}'})
    response = await client.get('/download')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Not Found'}
