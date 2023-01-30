from .base_page import BasePage
from .locators import LoginPageLocators
from .log_pass import NewUserData
from time import sleep

class LoginPage(BasePage):

    def should_be_login_page(self):
        self.should_be_name_field()
        self.should_be_main_phone_field()
        self.should_be_second_phone_field()
        self.should_be_email_field()
        self.should_be_jura_checkbox()
        self.should_be_news_checkbox()
        self.should_be_zip_checkbox()


    def should_be_name_field(self):
        ''' Проверка на наличие поля для ввода имени пользователя '''
        assert self.is_element_present(*LoginPageLocators.NAME_FIELD), \
            'Отсутствует поле для ввода имени пользователя'
        print('1. Поле для ввода имени пользователя')

    def should_be_main_phone_field(self):
        ''' Проверка на наличие поля для номера основного телефона '''
        assert self.is_element_present(*LoginPageLocators.MAIN_PHONE_NUMBER), \
            "Отсутствует поле для номера основного телефона"
        print('2. Поле для номера основного телефона')

    def should_be_second_phone_field(self):
        ''' Проверка на наличие поля для номера дополнительного телефона '''
        assert self.is_element_present(*LoginPageLocators.SECOND_PHONE_NUMBER), \
            "Отсутствует поле для номера дополнительного телефона"
        print('3. Поле для номера дополнительного телефона')

    def should_be_email_field(self):
        ''' Проверка на наличие поля для email '''
        assert self.is_element_present(*LoginPageLocators.EMAIL_FIELD), \
            "Отсутствует поле для email"
        print('4. Поле для email')

    def should_be_jura_checkbox(self):
        ''' Проверка на наличие чекбокса юр.лица '''
        assert self.is_element_present(*LoginPageLocators.JURA_CHECKBOX), \
            "Отсутствует чекбокс юр.лица"
        print('5. Чекбокс юр.лица')

    def should_be_news_checkbox(self):
        ''' Проверка на наличие чекбокса Статьи, новости... '''
        assert self.is_element_present(*LoginPageLocators.CHECKBOX_NEWS), \
            "Отсутствует чекбокс Статьи, новости ..."
        print('6. Чекбокс Статьи, новости...')

    def should_be_zip_checkbox(self):
        ''' Проверка на наличие чекбокса Молния '''
        assert self.is_element_present(*LoginPageLocators.ZIP_CHECKBOX), \
            "Отсутствует чекбокс Молния"
        print('7. Чекбокс Молния')


    def register_new_user(self):
        name_field = self.browser.find_element(*LoginPageLocators.NAME_FIELD)
        name_field.send_keys(NewUserData.USER_NAME)
        email_field = self.browser.find_element(*LoginPageLocators.EMAIL_FIELD)
        email_field.send_keys(NewUserData.USER_EMAIL)
        checkbox_news = self.browser.find_element(*LoginPageLocators.CHECKBOX_NEWS)
        checkbox_news.click()
        submit_button = self.browser.find_element(*LoginPageLocators.REG_SUBMIT_BUTTON)
        submit_button.click()
