from .base_page import BasePage
from .locators import BasketPageLocators
from time import sleep

class BasketPage(BasePage):

    def compare_basket_and_product_name(self, name):
        ''' Проверка на сравнение названия товара и товара в корзине '''
        message_name = self.browser.find_element(*BasketPageLocators.PRODUCT_NAME_IN_BASKET).text
        print(f'Товар {message_name} лежит в корзине.')
        name = name.split('\n')[0]
        assert message_name in name, f'Product {name} not found on message'

    def compare_basket_and_product_price(self, price):
        ''' Проверка на сравнение цены товара и цены корзины '''
        basket_price = self.browser.find_element(*BasketPageLocators.BASKET_PRICE).text.split()[0]
        print(f'Цена корзины составила: {basket_price}.')
        price = price.split()[0]
        assert price in basket_price, 'Product price and basket price is not equal'

    def increase_the_amount_of_goods_per_one(self):
        ''' Увеличение количества конкретного товара на единицу '''
        before = self.total_amount_of_products_in_the_basket()
        plus_button = self.browser.find_element(*BasketPageLocators.PRODUCT_AMOUNT_PLUS)
        plus_button.click()
        sleep(3)
        after = self.total_amount_of_products_in_the_basket()
        assert after == before + 1, 'Adding to the cart did not happen'

    def total_amount_of_products_in_the_basket(self):
        message = self.browser.find_element(*BasketPageLocators.TOTAL_COUNT_PRODUCT_IN_BASKET)
        message_count_product = message.text.split()[3]
        print(f'Общее количество товаров в корзине: {message_count_product}')
        return int(message_count_product)

    def should_be_message_empty_basket(self):
        ''' Проверка наличия сообщения о пустой корзине '''
        message = self.browser.find_element(*BasketPageLocators.EMPTY_BASKET).text
        assert 'пуста' in message, 'There is no message about an empty basket'
        print('Корзина пуста!')

    def should_be_basket_is_not_empty(self):
        ''' Проверка того, что корзина не пуста '''
        message = self.browser.find_element(*BasketPageLocators.TOTAL_COUNT_PRODUCT_IN_BASKET)
        message = message.text.split()[3]
        print(f'Общее количество товаров в корзине: {message}')
        assert message, 'The basket is empty'

    def deducting_an_product_from_the_basket(self):
        ''' Вычитание товара из корзины через кнопку "-" '''
        self.should_be_basket_is_not_empty()
        self.browser.find_element(*BasketPageLocators.PRODUCT_AMOUNT_MINUS).click()
        sleep(3)
        # self.total_amount_of_products_in_the_basket()

    def removing_an_product_from_the_basket(self):
        ''' Удаление товара из корзины через кнопку "корзинка" '''
        self.should_be_basket_is_not_empty()
        self.browser.find_element(*BasketPageLocators.PRODUCT_DELETE_BUTTON).click()
        sleep(3)
        self.should_be_message_empty_basket()