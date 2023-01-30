from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from .locators import BasePageLocators, BasketPageLocators
from time import sleep

class BasePage:
    def __init__(self, browser, url='https://www.podvorje.ru/', timeout=10):
        self.browser = browser
        self.url = url
        self.browser.implicitly_wait(timeout)
        self.wait = WebDriverWait(browser, timeout)

    def open(self):
        self.browser.get(self.url)

    def is_element_located(self, how, what):
        ''' Метод ищет элемент с явным ожиданием '''
        try:
            self.wait.until(
                EC.presence_of_element_located((how, what)),
                f'CSS Selector "\x1B[1m{what}\x1B[0m" is not find')
        except NoSuchElementException:
            return False
        return True

    def is_element_present(self, how, what):
        ''' Метод проверяет, что элемент присутствует на странице '''
        try:
            self.browser.find_element(how, what)
        except NoSuchElementException:
            print(f'Элемент с локатором {what} не найден')
            return False
        return True

    def is_elements_present(self, how, what):
        ''' Метод ищет группу элементов на странице по локаатору '''
        try:
            self.browser.find_elements(how, what)
        except NoSuchElementException:
            print(f'Элементы с локатором {what} не найдены')
            return False
        return True

    def go_to_login(self):
        link = self.browser.find_element(*BasePageLocators.LOGIN_LINK)
        link.click()

    def go_to_main_page(self):
        link = self.browser.find_element(*BasePageLocators.LOGO)
        link.click()

    def go_to_basket_page(self):
        link = self.browser.find_element(*BasePageLocators.BASKET_ICON)
        link.click()

    def should_be_header(self):
        ''' Проверка наличия элементов в хедере сайта '''
        assert self.is_element_located(*BasePageLocators.LOGIN_LINK), \
            "Login link is not presented"
        assert self.is_element_located(*BasePageLocators.SEARCH_FIELD), \
            "Search field is not presented"
        assert self.is_element_located(*BasePageLocators.LOGO), \
            "Logo is not presented"
        assert self.is_element_located(*BasePageLocators.PHONE1), \
            "Phone number (495)108-53-72 is not presented"
        assert self.is_element_located(*BasePageLocators.PHONE2), \
            "Phone number 8-(800)700-40-94 is not presented"
        assert self.is_element_located(*BasePageLocators.PHONE3), \
            "Phone number (495)108-53-25 is not presented"
        assert self.is_element_located(*BasePageLocators.PHONE4), \
            "Phone number (495)481-38-42 is not presented"
        assert self.is_element_located(*BasePageLocators.BASKET_ICON), \
            "Basket icon is not presented"
        assert self.is_element_located(*BasePageLocators.BASKET_DELAY), \
            "Basket delay is not presented"


    def should_be_main_menu(self):
        ''' Проверка наличия главного меню сайта и его рубрик '''
        catalog = self.browser.find_element(*BasePageLocators.CATALOG)
        assert 'КАТАЛОГ' in catalog.text, "Catalog is not presented"
        delivery = self.browser.find_element(*BasePageLocators.DELIVERY)
        assert 'ОПЛАТА' in delivery.text, "Delivery and payment is not presented"
        articles = self.browser.find_element(*BasePageLocators.ARTICLES)
        assert 'СТАТЬИ' in articles.text, "Articles and videos is not presented"
        about_us = self.browser.find_element(*BasePageLocators.ABOUT_US)
        assert 'О НАС' in about_us.text, "About us is not presented"
        contacts = self.browser.find_element(*BasePageLocators.CONTACTS)
        assert 'КОНТАКТЫ' in contacts.text, "Contacts is not presented"

        catalog.click()
        block_categories = self.wait.until(
            EC.presence_of_all_elements_located(BasePageLocators.BLOCK_CATEGORIES))
        categories = ['Прием заказов на ВЕСНУ–2023', 'Розы', 'Многолетники', 'Луковичные',
                      'Декоративно-лиственные', 'Хвойные', 'Семена', 'Рассада',
                      'Плодово-ягодные', 'Комнатные растения', 'Сопутствующие товары',
                      'Консервирование', 'Подарочные сертификаты', 'Акции', 'Открыть весь каталог']
        sleep(2)
        all_categories = self.browser.find_element(*BasePageLocators.ALL_CATEGORIES)
        self.browser.execute_script("return arguments[0].scrollIntoView(false);", all_categories)
        for el, i in zip(block_categories, categories):
            assert i in el.text, f'the category {i} does not match'

        delivery.click()
        assert self.wait.until(
            EC.url_to_be('https://www.podvorje.ru/retail/orders.html'),
            'Incorrect URL ')

        self.browser.find_element(*BasePageLocators.ARTICLES).click()
        sleep(3)
        block_arts = self.wait.until(
            EC.presence_of_all_elements_located(BasePageLocators.BLOCK_ARTS))
        arts_expected_list = ['Статьи', 'Шпаргалки садовода', 'Видео']
        arts_actual_list = str(*[el.text for el in block_arts]).split('\n')[::2]
        for el_exp, el_act in zip(arts_expected_list, arts_actual_list):
            assert el_exp == el_act, f'The category {el_exp} does not match'

        self.browser.find_element(*BasePageLocators.ABOUT_US).click()
        assert WebDriverWait(self.browser, 5).until(
            EC.url_to_be('https://www.podvorje.ru/retail/about.html'),
            'Incorrect URL ')

        self.browser.find_element(*BasePageLocators.CONTACTS).click()
        assert WebDriverWait(self.browser, 5).until(
            EC.url_to_be('https://www.podvorje.ru/contacts.html'),
            'Incorrect URL ')
        self.go_to_main_page()


    def should_be_send_message_field(self):
        ''' Проверка наличия форм для отправки сообщений через собственный чат,
        с помощью Телеграм-бота, с помощью бота ВКонтакте, через WhatsApp,
        и собственного чата (разработчики меняют этот блок, поэтому ниже есть ...var2)'''
        original_window = self.browser.current_window_handle
        green_send_message = self.wait.until(
            EC.presence_of_element_located(BasePageLocators.GREEN_ASK_QUESTION_BTN))
        assert green_send_message, 'Send message button is not present'
        assert self.wait.until(
            EC.text_to_be_present_in_element(BasePageLocators.GREEN_ASK_QUESTION, 'Задать вопрос'),
            'Incorrect button name. It should be "Задать вопрос"')
        green_send_message.click()
        assert self.wait.until(EC.text_to_be_present_in_element(
            BasePageLocators.MESSAGE_FORM_TITLE, 'Напишите ваше сообщение'),
            'Incorrect button name. It should be "Напишите ваше сообщение"')
        self.wait.until(EC.presence_of_element_located(BasePageLocators.CLOSE_MESSAGE_FORM)).click()
        green_send_message = self.wait.until(
            EC.presence_of_element_located(BasePageLocators.GREEN_ASK_QUESTION_BTN))
        ActionChains(self.browser).move_to_element(green_send_message).perform()
        telegram_link = self.wait.until(
            EC.presence_of_element_located(BasePageLocators.TELEGRAM_LINK),
            'Send message by Telegram is not find')
        assert self.wait.until(EC.text_to_be_present_in_element(
            BasePageLocators.TELEGRAM_LINK, 'Telegram'),
            'Incorrect button name. It should be "Telegram"')
        telegram_link.click()
        self.go_to_message_window('https://t.me/PodvorjeBot')

        vkontakte_link = self.wait.until(
            EC.presence_of_element_located(BasePageLocators.VK_LINK),
            'Send message by VK is not find')
        assert self.wait.until(EC.text_to_be_present_in_element(
            BasePageLocators.VK_LINK, 'Сообщение ВКонтакте'),
            'Incorrect button name. It should be "Сообщение ВКонтакте"')
        vkontakte_link.click()
        self.go_to_message_window('https://vk.com/')

        whatsapp_link = self.wait.until(
            EC.presence_of_element_located(BasePageLocators.WHATSAPP_LINK),
            'Send message by WhatsApp is not find')
        assert self.wait.until(EC.text_to_be_present_in_element(
            BasePageLocators.WHATSAPP_LINK, 'WhatsApp'),
            'Incorrect button name. It should be "WhatsApp"')
        whatsapp_link.click()
        self.go_to_message_window('https://api.whatsapp.com/send/')

        easy_message = self.wait.until(
            EC.presence_of_element_located(BasePageLocators.EASY_MESSAGE_LINK),
            'Send "Написать в чат" is not find')
        assert self.wait.until(EC.text_to_be_present_in_element(
            BasePageLocators.EASY_MESSAGE_LINK, 'Написать в чат'),
            'Incorrect button name. It should be "Написать в чат"')
        easy_message.click()
        assert self.wait.until(EC.text_to_be_present_in_element(
            BasePageLocators.MESSAGE_FORM_TITLE, 'Напишите ваше сообщение'),
            'Incorrect button name. It should be "Напишите ваше сообщение"')
        self.wait.until(EC.presence_of_element_located(
            BasePageLocators.CLOSE_MESSAGE_FORM)).click()
        ActionBuilder(self.browser).clear_actions()


    def go_to_message_window(self, link):
        ''' Метод проверяет, что появилось окно с мессенджером,
        проверяет, что URL соответствует мессенджеру, закрывает
        окно мессенджера и переходит в главное окно сайта '''
        original_window = self.browser.current_window_handle
        self.wait.until(EC.number_of_windows_to_be(2))
        for window_handle in self.browser.window_handles:
            if window_handle != original_window:
                self.browser.switch_to.window(window_handle)
                break
        assert self.wait.until(EC.url_contains(link), 'Incorrect URL')
        self.browser.close()
        self.browser.switch_to.window(original_window)


    def should_be_send_message_field_var2(self):
        ''' Проверка наличия форм для отправки сообщений через собственный чат,
        с помощью Телеграм-бота, с помощью бота ВКонтакте, через WhatsApp,
        и собственного чата'''
        green_send_message = self.wait.until(
            EC.presence_of_element_located(BasePageLocators.GREEN_ASK_QUESTION_BTN))
        assert green_send_message, 'Send message button is not present'
        assert self.wait.until(
            EC.text_to_be_present_in_element(BasePageLocators.GREEN_ASK_QUESTION, 'Отправьте нам сообщение'),
            'Incorrect button name. It should be "Отправьте нам сообщение"')
        green_send_message.click()
        assert self.wait.until(EC.text_to_be_present_in_element(
            BasePageLocators.MESSAGE_FORM_TITLE, 'Отправьте нам сообщение'),
            'Incorrect button name. It should be "Отправьте нам сообщение"')
        self.wait.until(EC.presence_of_element_located(BasePageLocators.CLOSE_MESSAGE_FORM)).click()
        green_send_message = self.wait.until(
            EC.presence_of_element_located(BasePageLocators.GREEN_ASK_QUESTION_BTN))
        ActionChains(self.browser).move_to_element(green_send_message).perform()
        telegram_link = self.wait.until(
            EC.presence_of_element_located(BasePageLocators.TELEGRAM_LINK),
            'Send message by Telegram is not find')
        assert self.wait.until(EC.text_to_be_present_in_element(
            BasePageLocators.TELEGRAM_LINK, 'Telegram'),
            'Incorrect button name. It should be "Telegram"')
        telegram_link.click()
        self.go_to_message_window('https://t.me/PodvorjeBot')

        vkontakte_link = self.wait.until(
            EC.presence_of_element_located(BasePageLocators.VK_LINK),
            'Send message by VK is not find')
        assert self.wait.until(EC.text_to_be_present_in_element(
            BasePageLocators.VK_LINK, 'Сообщение ВКонтакте'),
            'Incorrect button name. It should be "Сообщение ВКонтакте"')
        vkontakte_link.click()
        self.go_to_message_window('https://vk.com/')

        whatsapp_link = self.wait.until(
            EC.presence_of_element_located(BasePageLocators.WHATSAPP_LINK),
            'Send message by WhatsApp is not find')
        assert self.wait.until(EC.text_to_be_present_in_element(
            BasePageLocators.WHATSAPP_LINK, 'WhatsApp'),
            'Incorrect button name. It should be "WhatsApp"')
        whatsapp_link.click()
        self.go_to_message_window('https://api.whatsapp.com/send/')

        easy_message = self.wait.until(
            EC.presence_of_element_located(BasePageLocators.EASY_MESSAGE_LINK),
            'Send "Написать в чат" is not find')
        assert self.wait.until(EC.text_to_be_present_in_element(
            BasePageLocators.EASY_MESSAGE_LINK, 'Оставить сообщение'),
            'Incorrect button name. It should be "Оставить сообщение"')
        easy_message.click()
        assert self.wait.until(EC.text_to_be_present_in_element(
            BasePageLocators.MESSAGE_FORM_TITLE, 'Отправьте нам сообщение'),
            'Incorrect button name. It should be "Отправьте нам сообщение"')
        self.wait.until(EC.presence_of_element_located(
            BasePageLocators.CLOSE_MESSAGE_FORM)).click()
        ActionBuilder(self.browser).clear_actions()




    def should_be_count_basket_is_null(self):
        count = self.browser.find_element(*BasePageLocators.BASKET_COUNT).text
        assert '0' in count, 'Basket is not empty'




    def click_to_send_message_link(self):
        self.browser.find_element(*BasePageLocators.SEND_MESSAGE).click()
        sleep(6)
        self.browser.find_element(*BasePageLocators.CLOSE_MESSAGE).click()