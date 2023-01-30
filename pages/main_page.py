from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage
from .locators import MainPageLocators
from .log_pass import NewUserData, OldUserData1
from time import sleep

class MainPage(BasePage):

    def __init__(self, *args, **kwargs):
        super(MainPage, self).__init__(*args, **kwargs)


    def should_be_phone_login(self):
        self.should_be_phone_field()
        self.should_be_submit_button()
        self.should_be_email_link()
        self.should_be_step_back_button()

    def should_be_email_login(self):
        self.should_be_email_field()
        self.should_be_submit_button()
        self.should_be_phone_link()
        self.should_be_step_back_button()


    def should_be_phone_field(self):
        ''' Проверка на наличие поля для ввода телефона '''
        assert self.is_element_present(*MainPageLocators.LOGIN_PHONE_FIELD), \
            'Отсутствует поле для ввода номера телефона'
        print('1. Поле для номера телефона')

    def should_be_submit_button(self):
        ''' Проверка на наличие кнопки ПРОДОЛЖИТЬ '''
        assert self.is_element_present(*MainPageLocators.SUBMIT_BUTTON), \
            "Отсутствует кнопка ПРОДОЛЖИТЬ"
        print('2. Кнопка ПРОДОЛЖИТЬ')

    def should_be_email_link(self):
        ''' Проверка на наличие ссылки для ввода e-mail '''
        assert self.is_element_present(*MainPageLocators.LOGIN_MAIL_LINK), \
            'Отсутствует ссылка для ввода e-mail'
        print('3. Ссылка на вход по email')

    def should_be_step_back_button(self):
        ''' Проверка на наличие ссылки "Вернуться назад" '''
        assert self.is_element_present(*MainPageLocators.STEP_BACK_BUTTON), \
            "Отсутствует крестик ВЕРНУТЬСЯ НАЗАД"
        print('4. Крестик ВЕРНУТЬСЯ НАЗАД')

    def click_to_email_link(self):
        email_link = self.browser.find_element(*MainPageLocators.LOGIN_MAIL_LINK)
        email_link.click()


    def should_be_email_field(self):
        ''' Проверка на наличие поля для ввода e-mail '''
        assert self.is_element_present(*MainPageLocators.EMAIL_FIELD), \
            'Отсутствует поле для ввода e-mail'
        print('5. Поле для ввода email')

    def should_be_phone_link(self):
        ''' Проверка на наличие ссылки для ввода номера телефона '''
        assert self.is_element_present(*MainPageLocators.LOGIN_PHONE_LINK), \
            "Отсутствует ссылка на вход по номеру телефона"
        print('6. Ссылка на вход по номеру телефона')

    def should_be_authorized_user(self):
        ''' Проверка авторизации пользователя '''
        avatar = self.browser.find_element(*MainPageLocators.AVATAR).text
        assert avatar, 'Пользователь не зарегистрирован'

    def old_user_password(self):
        password_field = self.browser.find_element(*MainPageLocators.LOGIN_PASSWORD)
        password_field.send_keys(OldUserData1.USER_PASSWORD)
        vojti_button = self.browser.find_element(*MainPageLocators.VOJTI_BUTTON)
        vojti_button.click()

    def pre_login_old_user_phone(self):
        phone = self.browser.find_element(*MainPageLocators.LOGIN_PHONE_FIELD)
        phone.send_keys(OldUserData1.USER_PHONE)
        forth_button = self.browser.find_element(*MainPageLocators.SUBMIT_BUTTON)
        forth_button.click()
        sleep(3)

    def pre_login_new_user_phone(self):
        phone = self.browser.find_element(*MainPageLocators.LOGIN_PHONE_FIELD)
        phone.send_keys(NewUserData.USER_PHONE)
        forth_button = self.browser.find_element(*MainPageLocators.SUBMIT_BUTTON)
        forth_button.click()

    def register_new_user_part2(self):
        user_account = self.browser.find_element(*MainPageLocators.USER_ACCOUNT)
        user_account.click()
        sleep(2)
        personal_data = self.browser.find_element(*MainPageLocators.PERSONAL_DATA_BUTTON)
        personal_data.click()
        sleep(2)
        info_edit = self.browser.find_element(*MainPageLocators.INFO_EDIT)
        info_edit.click()
        sleep(2)
        user_password = self.browser.find_element(*MainPageLocators.USER_PASSWORD)
        user_password.send_keys(NewUserData.USER_PASSWORD)
        save_button = self.browser.find_element(*MainPageLocators.SAVE_BUTTON)
        self.browser.execute_script("return arguments[0].scrollIntoView(true);", save_button)
        save_button.click()

    def should_be_section_sale_hits(self):
        """ Проверка, что имеется раздел ХИТЫ ПРОДАЖ, в нём не менее 10 наименований товаров,
        все товары уникальные"""
        sale_hits_title = self.wait.until(
            EC.presence_of_element_located(MainPageLocators.SALE_HITS_TITLE))
        self.browser.execute_script("return arguments[0].scrollIntoView(true);", sale_hits_title)
        assert sale_hits_title, 'Section SALE HITS is not present'
        assert self.wait.until(
            EC.text_to_be_present_in_element(MainPageLocators.SALE_HITS_TITLE, 'ХИТЫ ПРОДАЖ'),
            'Название раздела не "ХИТЫ ПРОДАЖ"')

        list_image = []
        pos = 0
        loc_check = MainPageLocators.SALE_HITS_ELEMENT
        button_right = self.browser.find_element(*MainPageLocators.SALE_HITS_RIGHT)
        while self.is_element_present(*MainPageLocators.SALE_HITS_RIGHT) and self.is_element_present(*loc_check):
            pos += 1
            locator_el = list(MainPageLocators.SALE_HITS_ELEMENT)
            locator_el[1] = f'.rr-widget-5d11dd3497a528203018b3c3 .slick-slide:nth-child({pos}) img'
            element = self.browser.find_element(*locator_el)
            if element.get_attribute('src') is None:
                button_right.click()
                sleep(1)
            list_image.append(element.get_attribute('src').split('/')[8])
            loc_check = locator_el
            loc_check[1] = f'.rr-widget-5d11dd3497a528203018b3c3 .slick-slide:nth-child({pos+1}) img'
        print(list_image) # Список отличительных элементов в URL хитовых товаров
        assert len(list_image) >= 10, 'Less than 10 items of goods are presented'
        assert len(list_image) == len(set(list_image)), 'There are duplicate products in the hit list'


    def should_be_section_promotions(self):
        """ Проверка, что имеется раздел ТОВАРЫ НЕДЕЛИ И ДРУГИЕ АКЦИИ, в нём не менее 5 наименований товаров,
        все товары уникальные"""
        promo_title = self.wait.until(
            EC.presence_of_element_located(MainPageLocators.PROMO_TITLE))
        self.browser.execute_script("return arguments[0].scrollIntoView(true);", promo_title)
        assert promo_title, 'Section SALE HITS is not present'
        assert self.wait.until(
            EC.text_to_be_present_in_element(MainPageLocators.PROMO_TITLE, 'ТОВАРЫ НЕДЕЛИ И ДРУГИЕ АКЦИИ'),
            'Название раздела не "ТОВАРЫ НЕДЕЛИ И ДРУГИЕ АКЦИИ"')
        assert self.wait.until(
            EC.text_to_be_present_in_element(MainPageLocators.PROMO_BUTTON, 'Все товары недели'.upper()),
            'The button "Все товары недели" is not present')
        self.wait.until(EC.presence_of_element_located(MainPageLocators.PROMO_BUTTON)).click()
        assert self.wait.until(EC.url_to_be('https://www.podvorje.ru/hits.html'), 'Incorrect URL')
        self.browser.back()

        list_image = []
        pos = 0
        loc_check = MainPageLocators.PROMO_ELEMENT
        button_right = self.browser.find_element(*MainPageLocators.PROMO_RIGHT)
        while self.is_element_present(*MainPageLocators.PROMO_RIGHT) and self.is_element_present(*loc_check):
            pos += 1
            locator_el = list(MainPageLocators.PROMO_ELEMENT)
            locator_el[1] = f'.week_item:nth-child({pos}) .week_img'
            element = self.browser.find_element(*locator_el)
            if element.get_attribute('style') is None:
                button_right.click()
                sleep(1)
            list_image.append(element.get_attribute('style').split('/')[-1][:-7])
            loc_check = locator_el
            loc_check[1] = f'.week_item:nth-child({pos+1}) .week_img'
        # print(list_image)  # Список отличительных элементов в фото промо товаров
        assert len(list_image) >= 5, 'Less than 5 items of goods are presented'
        assert len(list_image) == len(set(list_image)), 'There are duplicate products in the hit list'


    def should_be_section_novelties(self):
        """ Проверка, что имеется раздел НОВИНКИ, в нём не менее 5 наименований товаров,
        все товары уникальные"""
        novelties_title = self.wait.until(
            EC.presence_of_element_located(MainPageLocators.NOVELTIES_TITLE))
        self.browser.execute_script("return arguments[0].scrollIntoView(true);", novelties_title)
        assert novelties_title, 'Section НОВИНКИ is not present'
        assert self.wait.until(
            EC.text_to_be_present_in_element(MainPageLocators.NOVELTIES_TITLE, 'НОВИНКИ'),
            'Название раздела не "НОВИНКИ"')
        assert self.wait.until(
            EC.text_to_be_present_in_element(MainPageLocators.NOVELTIES_BUTTON, 'Все новинки'.upper()),
            'The button "Все новинки" is not present')
        self.wait.until(EC.presence_of_element_located(MainPageLocators.NOVELTIES_BUTTON)).click()
        assert self.wait.until(EC.url_to_be('https://www.podvorje.ru/new.html'), 'Incorrect URL')
        self.browser.back()

        list_image = []
        pos = 0
        loc_check = MainPageLocators.NOVELTIES_ELEMENT
        button_right = self.browser.find_element(*MainPageLocators.NOVELTIES_RIGHT)
        while self.is_element_present(*MainPageLocators.NOVELTIES_RIGHT) and self.is_element_present(*loc_check):
            pos += 1
            locator_el = list(MainPageLocators.NOVELTIES_ELEMENT)
            locator_el[1] = f'.sl_item:nth-child({pos}) .ni_img'
            element = self.browser.find_element(*locator_el)
            if element.get_attribute('style') is None:
                button_right.click()
                sleep(1)
            list_image.append(element.get_attribute('style').split('/')[-1][:-7])
            loc_check = locator_el
            loc_check[1] = f'.sl_item:nth-child({pos+1}) .ni_img'
        # print(list_image)  # Список отличительных элементов в фото промо товаров
        assert len(list_image) >= 5, 'Less than 5 items of goods are presented'
        assert len(list_image) == len(set(list_image)), 'There are duplicate products in the hit list'


    def should_be_section_reviews(self):
        """ Проверка, что имеется раздел ОТЗЫВЫ, в нём не менее 3 разных отзывов"""
        otziv_title = self.wait.until(
            EC.presence_of_element_located(MainPageLocators.OTZIV_TITLE))
        self.browser.execute_script("return arguments[0].scrollIntoView(true);", otziv_title)
        assert otziv_title, 'Section REVIEWS is not present'
        assert self.wait.until(
            EC.text_to_be_present_in_element(MainPageLocators.OTZIV_TITLE, 'ОТЗЫВЫ'),
            'Название раздела не "ОТЗЫВЫ"')
        assert self.wait.until(
            EC.text_to_be_present_in_element(MainPageLocators.OTZIV_ALL_BUTTON, 'Все отзывы'.upper()),
            'The button "Все отзывы" is not present')
        assert self.wait.until(
            EC.text_to_be_present_in_element(MainPageLocators.OTZIV_SEND_BUTTON, 'Оставить отзыв'.upper()),
            'The button "Оставить отзыв" is not present')
        self.wait.until(EC.presence_of_element_located(MainPageLocators.OTZIV_SEND_BUTTON)).click()
        assert self.wait.until(EC.url_to_be('https://www.podvorje.ru/reviews.html#addAnswer'), 'Incorrect URL')
        self.browser.back()
        self.wait.until(EC.presence_of_element_located(MainPageLocators.OTZIV_ALL_BUTTON)).click()
        assert self.wait.until(EC.url_to_be('https://www.podvorje.ru/reviews.html'), 'Incorrect URL')
        self.browser.back()

        otziv_block = self.wait.until(
            EC.presence_of_all_elements_located(MainPageLocators.OTZIV_BLOCK))
        otz_list = str(*[elem.text for elem in otziv_block if elem.text != '']).split('\n')[::2]
        # print(len(otz_list))
        # [print(el) for el in otz_list]
        assert len(otz_list) >= 3, 'Less than 3 reviews submitted'
        assert len(otz_list) == len(set(otz_list)), 'There are no duplicate reviews'

    def should_be_section_news(self):
        """ Проверка, что имеется раздел НОВОСТИ, в нём не менее 5 разных новостей,
        имеется кнопка ВСЕ НОВОСТИ для перехода на соответствующую страницу сайта,
        также имеется кнопка RSS для перехода на соответствующую страницу """
        title_news = self.wait.until(
            EC.presence_of_element_located(MainPageLocators.NEWS_TITLE))
        self.browser.execute_script("return arguments[0].scrollIntoView(true);", title_news)
        all_news = self.wait.until(
            EC.presence_of_element_located(MainPageLocators.NEWS_ALL_BUTTON))
        assert self.wait.until(
            EC.text_to_be_present_in_element(MainPageLocators.NEWS_ALL_BUTTON, 'Все новости'.upper()))
        all_news.click()
        assert self.wait.until(EC.url_to_be('https://www.podvorje.ru/news.html'), 'Incorrect URL')
        self.browser.back()
        block_news = self.wait.until(
            EC.presence_of_all_elements_located(MainPageLocators.NEWS_BLOCK))
        news_list = str(*[elem.text for elem in block_news]).split('\n')
        print(len(news_list) // 4)
        [print(f'{date} - {title}') for date, title in zip(news_list[0::4], news_list[1::4])]
        assert len(news_list) // 4 >= 5, 'The number of news items is less than 5'
        assert len(news_list[1::4]) == len(set(news_list[1::4])), 'Not all news is unique'

        rss_news = self.wait.until(
            EC.presence_of_element_located(MainPageLocators.NEWS_RSS_BUTTON))
        original_window = self.browser.current_window_handle
        rss_news.click()
        self.wait.until(EC.number_of_windows_to_be(2))
        for window_handle in self.browser.window_handles:
            if window_handle != original_window:
                self.browser.switch_to.window(window_handle)
                break
        assert self.wait.until(EC.url_to_be('https://www.podvorje.ru/rss.html'), 'Incorrect URL')
        self.browser.close()
        self.browser.switch_to.window(original_window)
