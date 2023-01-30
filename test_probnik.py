from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
# from selenium.webdriver.common import ActionBuilder
from time import sleep


def is_element_located(browser, how, what, timeout=6):
    ''' Метод ищет элемент с явным ожиданием '''
    try:
        browser.implicitly_wait(timeout)
        browser.find_element(how, what)
    except NoSuchElementException:
        return False
    return True


def test_pp(browser):
    browser.get('https://www.podvorje.ru/')
    wait = WebDriverWait(browser, 0)

    btn = wait.until(EC.presence_of_element_located((By.ID, 'puSubscribe_no')))
    browser.execute_script("return arguments[0].scrollIntoView(false);", btn)
    sleep(8)
    btn_yes = wait.until(EC.presence_of_element_located((By.ID, 'puSubscribe_yes')))
    btn_yes.click()
    sleep(6)
    '''
    wait.until(EC.text_to_be_present_in_element(
        (By.CSS_SELECTOR, '.subs_inner'), 'Подпишитесь на нашу рассылку'))
    subscibe_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.subscribe button')),
                             'Кнопка ПОДПИСАТЬСЯ не найдена')
    browser.execute_script("return arguments[0].scrollIntoView(false);", subscibe_button)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.subscribe input')),
               'Поле для ввода e-mail не найдено')
    '''



    '''
    while otziv.text:
        otz_list.extend(otziv.text.split('\n'))
        button_right.click()
        cnt += 1
        otz_curr = (By.CSS_SELECTOR, f'.one_otz:nth-child({cnt})')
        otziv = browser.find_element(*otz_curr)
    print(len(otz_list))
    print(otz_list)
    '''








    """
    
    browser.execute_script("return arguments[0].scrollIntoView(true);", news_title)
    assert news_title, 'Section News is not present'
    assert wait.until(
        EC.text_to_be_present_in_element((By.CSS_SELECTOR, '.new_block .title'), 'НОВИНКИ'),
        'Название раздела не "НОВИНКИ"')
    assert wait.until(
        EC.text_to_be_present_in_element((By.CSS_SELECTOR, '.new_block .btn'), 'Все новинки'.upper()),
        'The button "Все новинки" is not present')

    list_image = []
    pos = 0
    loc_check = (By.CSS_SELECTOR, '.new_block .sl_item:nth-child(1) .ni_img')
    news_right = (By.CSS_SELECTOR, '.new_block .sla_right')
    button_right = browser.find_element(*news_right)
    while is_element_located(browser, *news_right) and is_element_located(browser, *loc_check):
        pos += 1
        locator_el = list(loc_check)
        locator_el[1] = f'.new_block .sl_item:nth-child({pos}) .ni_img'
        element = browser.find_element(*locator_el)
        if element.get_attribute('style') is None:
            button_right.click()
            sleep(1)
        list_image.append(element.get_attribute('style').split('/')[-1][:-7])
        loc_check = locator_el
        loc_check[1] = f'.new_block .sl_item:nth-child({pos + 1}) .ni_img'
    print(list_image)  # Список отличительных элементов в фото промо товаров
    assert len(list_image) >= 5, 'Less than 5 items of goods are presented'
    assert len(list_image) == len(set(list_image)), 'There are duplicate products in the hit list'
    """