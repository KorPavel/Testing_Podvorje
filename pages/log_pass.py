from faker import Faker

# https://codeby.net/threads/generiruem-fejkovye-lichnosti-s-pomoschju-faker-i-mimesis-v-python.79947/


faker = Faker('ru_RU')

class NewUserData:
    email = faker.free_email()
    phone = faker.kpp()
    bban = faker.bban()
    first_name = faker.first_name_female()
    last_name = faker.last_name_female()
    middle_name = faker.middle_name_female()
    USER_EMAIL = email
    USER_PHONE = '9' + phone
    USER_PASSWORD = bban
    USER_NAME = f'{last_name} {first_name} {middle_name}'

class OldUserData1:
    ''' Этот пользователь зарегистрирован '''
    USER_EMAIL = "012347@fg.org"
    USER_PHONE = '9585342320'
    USER_PASSWORD = 'QWerTY00112233'
    USER_NAME = 'Сидоров Сидор Сидорович'

class OldUserData2:
    ''' Этот пользователь зарегистрирован тоже '''
    USER_EMAIL = "12345@fg.org"
    USER_PHONE = '9197773637'
    USER_PASSWORD = 'QWerTY11223344'
    USER_NAME = 'Иванов Иван Иванович'