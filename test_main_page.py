from .pages.main_page import MainPage
from .pages.login_page import LoginPage
import pytest
from time import sleep



def test_guest_should_see_the_elements_in_the_header(browser):
    ''' Тест-кейс проверяет наличие элементов в хедере сайта '''
    page = MainPage(browser)
    page.open()
    page.should_be_header()
    page.should_be_main_menu()

@pytest.mark.proba
def test_guest_should_see_send_message_menu(browser):
    ''' Тест-кейс проверяет меню "послать сообщения" '''
    page = MainPage(browser)
    page.open()
    # page.should_be_send_message_field()
    page.should_be_send_message_field_var2()

#@pytest.mark.proba
def test_guest_should_see_sale_hits(browser):
    page = MainPage(browser)
    page.open()
    page.should_be_section_sale_hits()

#@pytest.mark.proba
def test_guest_should_see_promotions(browser):
    page = MainPage(browser)
    page.open()
    page.should_be_section_promotions()

#@pytest.mark.proba
def test_guest_should_see_novelties(browser):
    page = MainPage(browser)
    page.open()
    page.should_be_section_novelties()

#@pytest.mark.proba
def test_guest_should_see_reviews(browser):
    page = MainPage(browser)
    page.open()
    page.should_be_section_reviews()

#@pytest.mark.proba
def test_guest_should_see_news(browser):
    page = MainPage(browser)
    page.open()
    page.should_be_section_news()


class TestLoginFromMainPage:

    def test_guest_can_go_to_login_form(self, browser):
        ''' Гость открывает страницу входа и проверяет наличие
        элементов в форме входа '''
        page = MainPage(browser)
        page.open()
        page.go_to_login()
        page.should_be_phone_login()
        page.click_to_email_link()
        page.should_be_email_login()


    def test_guest_can_go_to_login_page(self, browser):
        ''' Гость переходит на страницу регистрации и
        проверяет наличие элементов на странице '''
        page = MainPage(browser)
        page.open()
        page.go_to_login()
        page.pre_login_new_user_phone()
        sleep(10)
        login_page = LoginPage(browser, browser.current_url)
        login_page.should_be_login_page()


class TestUserAddToBasketFromProductPage:
    # @pytest.fixture(scope="function", autouse=True)

    def test_registering_a_new_user(self, browser):
        ''' Регистрация нового пользователя на сайте '''
        page = MainPage(browser)
        page.open()
        page.go_to_login()
        page.pre_login_new_user_phone()
        sleep(10)
        login_page = LoginPage(browser, browser.current_url)
        login_page.register_new_user()
        sleep(10)
        page.register_new_user_part2()
        page.should_be_authorized_user()


    def test_old_user_login(self, browser):
        ''' Вход старого пользователя на сайт '''
        page = MainPage(browser)
        page.open()
        page.go_to_login()
        page.pre_login_old_user_phone()
        sleep(3)
        page.old_user_password()
        page.should_be_authorized_user()
