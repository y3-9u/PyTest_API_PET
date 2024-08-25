import json
import requests
import settings
import os
import random


class Pets:
    """API-библиотека к сайту http://34.141.58.52:8000/"""
    def __init__(self):
        self.base_url = 'http://34.141.58.52:8000/'

    def get_token(self) -> json:
        """Запрос к Swagger сайта для получения уникального токена по указанным email и password"""
        data = {"email": settings.VALID_EMAIL,
                "password": settings.VALID_PSW}
        headers = {
            'Content-Type': 'application/json',
            'accept': 'application/json'
        }

        res = requests.post(self.base_url + 'login', headers=headers, data=json.dumps(data))
        my_token = res.json()['token']
        my_id = res.json()['id']
        status = res.status_code
        return my_token, status, my_id

    def get_user_id(self):
        """Запрос к Swagger сайта для получения id пользователя"""
        my_token = Pets.get_token(self)[0]
        headers = {'Authorization': f'Bearer {my_token}'}
        res = requests.get(self.base_url + 'users', headers=headers)
        status = res.status_code
        my_id = res.text
        return status, my_id

    def create_pet(self) -> json:
        """Запрос к Swagger сайта для создания питомца без фото"""
        token_data = Pets.get_token(self)
        my_token = token_data[0]
        my_id = token_data[2]
        headers = {'Authorization': f'Bearer {my_token}'}
        data = {"name": "Fluffy", "type": "cat", "owner_id": my_id}
        res = requests.post(self.base_url + 'pet', headers=headers, data=json.dumps(data))
        pet_id = res.json()['id']
        status = res.status_code
        return pet_id, status

    def create_pet__with_photo(self):
        """Запрос к Swagger сайта для создания питомца с фото"""
        my_token = Pets.get_token(self)[0]
        pet_id = Pets.create_pet(self)[0]
        headers = {'Authorization': f'Bearer {my_token}'}
        file_path = os.path.abspath(os.path.join('pics', 'Fluffy.png'))
        files = {'pic': ('any_value.png', open(file_path, 'rb'), 'image/png')}
        res = requests.post(self.base_url + f'pet/{pet_id}/image', headers=headers, files=files)
        status = res.status_code
        link = res.json()['link']
        print(res.json())
        return status, link

    def get_user_pets(self) -> json:
        """Запрос к Swagger сайта для получения списка питомцев пользователя"""
        token_data = Pets.get_token(self)
        my_token = token_data[0]
        my_id = token_data[2]
        headers = {'Authorization': f'Bearer {my_token}'}
        data = {"user_id": my_id}
        res = requests.post(self.base_url + 'pets', headers=headers, data=json.dumps(data))
        status = res.status_code
        user_pets = res.text
        return status, user_pets

    def add_like(self) -> int:
        """Запрос к Swagger сайта для постановки лайка только что созданному питомцу"""
        token_data = Pets.get_token(self)
        my_token = token_data[0]
        my_id = token_data[2]
        headers = {'Authorization': f'Bearer {my_token}'}
        data = {"name": "Fluffy", "type": "cat", "owner_id": my_id}
        res = requests.post(self.base_url + 'pet', headers=headers, data=json.dumps(data))
        pet_id = res.json()['id']

        res = requests.put(self.base_url + f'pet/{pet_id}/like', headers=headers)
        status = res.status_code
        return status

    def add_comment(self) -> tuple[int, str]:
        """Запрос к Swagger сайта для добавления коммента случайному питомцу из первого отображаемого десятка"""
        data = {"num": 10}
        my_token = Pets.get_token(self)[0]
        headers = {'Authorization': f'Bearer {my_token}'}
        res = requests.post(self.base_url + 'pets', headers=headers, data=json.dumps(data))
        response_data = res.json()

        pet_list = response_data.get('list', [])

        print("Pet list:", pet_list)
        if not pet_list:
            raise ValueError("Pet list is empty")

        pet_id = random.choice(pet_list)['id']
        print(pet_id)

        data = {"message": "Super"}
        res = requests.put(self.base_url + f'pet/{pet_id}/comment', headers=headers, data=json.dumps(data))
        status = res.status_code
        comment_id = res.text
        return status, comment_id
