from selenium import webdriver
from selenium.webdriver.common.by import By
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome('.\drivers\chromedriver.exe')
    # Переходим на страницу авторизации
    pytest.driver.get('http://petfriends.skillfactory.ru/login')
    yield
    pytest.driver.quit()


@pytest.fixture()
def test_show_my_pets():
    # Вводим email
    pytest.driver.find_element(By.ID, 'email').send_keys("rrraaa@yandex.ru")
    # Вводим пароль
    pytest.driver.find_element(By.ID, 'pass').send_keys('123321')
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()


def test_my_pets():
    # Вводим email
    pytest.driver.find_element(By.ID, 'email').send_keys("rrraaa@yandex.ru")
    # Вводим пароль
    pytest.driver.find_element(By.ID, 'pass').send_keys('123321')

    wait = WebDriverWait(pytest.driver, 5)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]')))
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Мои питомцы')))

    pytest.driver.find_element(By.LINK_TEXT, 'Мои питомцы').click()




def test_presence_of_pets(test_show_my_pets):
    """Проверяем, что присутствуют все питомцы"""
    pytest.driver.implicitly_wait(5)
    pytest.driver.find_element(By.LINK_TEXT, 'Мои питомцы').click()
    name = pytest.driver.find_elements(By.XPATH, '//tbody/tr/td[1]')
    my_pets = pytest.driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]')
    quantity_my_pets = my_pets.text.replace("/n", ' ').split()[2]
    quantity_my_pets = int(quantity_my_pets)
    assert quantity_my_pets > 0
    assert len(name) == quantity_my_pets


def test_photo_of_pets(test_show_my_pets):
    """Проверяем, что Хотя бы у половины питомцев есть фото"""
    pytest.driver.implicitly_wait(5)
    pytest.driver.find_element(By.LINK_TEXT, 'Мои питомцы').click()

    images = pytest.driver.find_elements(By.XPATH, '//tbody/tr/th/img')
    name = pytest.driver.find_elements(By.XPATH, '//tbody/tr/td[1]')
    my_pets = pytest.driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]')
    quantity_my_pets = my_pets.text.replace("/n", ' ').split()[2]
    quantity_my_pets = int(quantity_my_pets)
    a = 0
    for i in range(len(name)):
        if (images[i].get_attribute('src')) != '':
            a += 1
        else:
            a += 0
    assert a >= (quantity_my_pets / 2)


def test_descriptions_of_pets(test_show_my_pets):
    """Проверяем, что У всех питомцев есть имя, возраст и порода"""
    pytest.driver.find_element(By.LINK_TEXT, 'Мои питомцы').click()
    name = pytest.driver.find_elements(By.XPATH, '//tbody/tr/td[1]')
    breed = pytest.driver.find_elements(By.XPATH, '//tbody/tr/td[2]')
    age = pytest.driver.find_elements(By.XPATH, '//tbody/tr/td[3]')

    for i in range(len(name)):
        assert name[i].text != ''
        assert breed[i].text != ''
        assert age[i].text != ''


def test_unique_name(test_show_my_pets):
    """Проверяем, что У всех питомцев разные имена"""
    unique = []
    name = pytest.driver.find_elements(By.XPATH, '//tbody/tr/td[1]')

    for i in range(len(name)):
        unique.append(name[i].text)
    unique = [w.lower() for w in unique]
    unique.sort()
    for i in range(len(unique)):
        for n in range(i + 1, len(unique)):
            assert unique[i] != unique[n]


def test_unique_animals(test_show_my_pets):
    """Проверяем, что В списке нет повторяющихся питомцев"""
    name = pytest.driver.find_elements(By.XPATH, '//tbody/tr/td[1]')
    breed = pytest.driver.find_elements(By.XPATH, '//tbody/tr/td[2]')
    age = pytest.driver.find_elements(By.XPATH, '//tbody/tr/td[3]')
    unique = []

    for i in range(len(name)):
        unique.append(name[i].text + breed[i].text + age[i].text)
    unique = [w.lower() for w in unique]
    unique.sort()
    for i in range(len(unique)):
        for n in range(i + 1, len(unique)):
            assert unique[i] != unique[n]






# python -m pytest -v --driver Chrome --driver-path drivers\chromedriver.exe test_new.py
