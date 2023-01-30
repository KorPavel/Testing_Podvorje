from .base_page import BasePage
from .locators import ProductPageLocators, BasePageLocators
from time import sleep

class ProductPage(BasePage):

    def should_be_elements_on_the_product_page(self):
        self.should_be_product_name()
        self.should_be_product_price()
        self.should_be_product_photo()
        self.should_be_add_to_basket_button()
        self.should_be_product_info_block()
        self.should_be_product_info_table()


    def should_be_product_name(self):
        self.is_element_present(*ProductPageLocators.PRODUCT_NAME), \
            'Product name is not present'

    def should_be_product_price(self):
        self.is_element_present(*ProductPageLocators.PRODUCT_PRICE), \
            'Product price is not present'

    def should_be_product_photo(self):
        self.is_element_present(*ProductPageLocators.PRODUCT_PHOTO), \
            'Product photo is not present'

    def should_be_add_to_basket_button(self):
        self.is_element_present(*ProductPageLocators.BASKET_BUTTON), \
            'Add to basket button is not present'

    def should_be_product_info_table(self):
        self.is_element_present(*ProductPageLocators.PRODUCT_INFO_TABLE), \
            'Product info table is not present'

    def should_be_product_info_block(self):
        self.is_element_present(*ProductPageLocators.PRODUCT_INFO_BLOCK), \
            'Product info block is not present'

    def add_product_to_basket(self):
        product_name = self.browser.find_element(*ProductPageLocators.PRODUCT_NAME).text
        product_price = self.browser.find_element(*ProductPageLocators.PRODUCT_PRICE).text
        before = self.browser.find_element(*BasePageLocators.BASKET_COUNT).text
        print(f'В корзине было {before} товаров')
        self.browser.find_element(*ProductPageLocators.BASKET_BUTTON).click()
        sleep(5)
        after = self.browser.find_element(*BasePageLocators.BASKET_COUNT).text
        print(f'В корзину добавлен товар {product_name}')
        print(f'Количество товаров в корзине: {after}')
        assert int(after) == int(before) + 1, \
            'The product has not been added to the cart'
        return product_name, product_price