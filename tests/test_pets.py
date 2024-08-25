from api import Pets
import os

p = Pets()


def test_get_token():
    my_token, status, my_id = p.get_token()
    assert my_token
    assert status == 200


def test_get_user_id():
    status, my_id = p.get_user_id()
    assert status == 200
    assert my_id


def test_create_pet():
    pet_id, status = p.create_pet()
    assert status == 200
    assert pet_id


def test_create_pet_with_photo():
    os.chdir(os.path.dirname(__file__))  # Поменял текущий рабочий каталог на директорию теста
    status, link = p.create_pet__with_photo()
    assert status == 200
    assert link


def test_get_user_pets():
    status, user_pets = p.get_user_pets()
    assert status == 200
    assert user_pets


def test_add_like():
    status = p.add_like()
    assert status == 200


def test_add_comment():
    status, comment_id = p.add_comment()
    assert status == 200
    assert comment_id
