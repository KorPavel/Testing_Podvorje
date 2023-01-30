from .pages.product_page import ProductPage
from .pages.basket_page import BasketPage
from .pages.main_page import MainPage
import pytest


@pytest.mark.proba
def test_guest_can_add_product_to_basket(browser):
    ''' Гость открывает страницу товара, проверяет элементы информации
    добавляет товар в корзину, проверяет цену корзины и название товара
    затем увеличивает товар на единицу, а после уменьшает количестово товара
    до 0 (до пустой корзины) '''
    link = 'https://www.podvorje.ru/retail/catalogue/roses/rosa-kleopatra.html'
    product_page = ProductPage(browser, link)
    product_page.open()
    product_page.should_be_elements_on_the_product_page()
    product_page.should_be_count_basket_is_null()
    name, price = product_page.add_product_to_basket()
    basket_page = BasketPage(browser, browser.current_url)
    basket_page.go_to_basket_page()
    basket_page.compare_basket_and_product_name(name)
    basket_page.compare_basket_and_product_price(price)
    basket_page.increase_the_amount_of_goods_per_one()
    basket_page.deducting_an_product_from_the_basket()
    basket_page.deducting_an_product_from_the_basket()
    basket_page.should_be_message_empty_basket()


@pytest.mark.proba
class TestOldUserAddToBasketFromProductPage:

    @pytest.fixture(scope="function", autouse=True)
    def setup(self, browser):
        ''' Пользователь логинится на сайте '''
        page = MainPage(browser)
        page.open()
        page.go_to_login()
        page.pre_login_old_user_phone()
        page.old_user_password()
        page.should_be_authorized_user()


    def test_old_user_can_add_product_to_basket(self, browser):
        ''' Пользователь открывает страницу товара, проверяет элементы информации
        добавляет товар в корзину, проверяет цену корзины и название товара
        затем увеличивает этот товар на единицу, а после удаляет товар из корзины'''
        link = 'https://www.podvorje.ru/retail/catalogue/roses/rosa-gorgeous.html'
        product_page = ProductPage(browser, link)
        product_page.open()
        product_page.should_be_elements_on_the_product_page()
        product_page.should_be_count_basket_is_null()
        name, price = product_page.add_product_to_basket()
        basket_page = BasketPage(browser, browser.current_url)
        basket_page.go_to_basket_page()
        basket_page.compare_basket_and_product_name(name)
        basket_page.compare_basket_and_product_price(price)
        basket_page.increase_the_amount_of_goods_per_one()
        basket_page.removing_an_product_from_the_basket()