import logging
from time import sleep

import selenium.common.exceptions
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

from constants import DRIVER_FN, TIME_WAIT_ELEMENT, LITRES_LOGIN_URL, LITRES_PROMOCODE_URL


class Bot:
    def __init__(self):
        logging.debug('Start Bot')
        self.driver = WebDriver(DRIVER_FN)
        logging.info('Bot started')

    def LogIn(self, email, password):
        logging.debug('Start Login')
        self.GoToUrl(LITRES_LOGIN_URL)
        self.FillElement('xpath',
                         '//*[@id="frm_login"]/table/tbody/tr[1]/td[2]/input',
                         email)
        self.FillElement('xpath',
                         '//*[@id="open_pwd_main"]',
                         password + '\n')
        return self.IsLoggedIn()

    def IsLoggedIn(self):
        try:
            fail_message = self.WaitElementLoad('xpath', '/html/body/div[19]/p', 5).text
            logging.error('Failed login: %s', fail_message)
            return False
        except selenium.common.exceptions.TimeoutException:
            logging.info('Success login')
            return True

    def ActivatePromoCode(self, promo_code: tuple):
        if promo_code[0] is None:
            self.GoToUrl(promo_code[1])
            try:
                self.WaitElementLoad('xpath', '//*[@id="landing_button"]', 5)
                self.ClickElement('xpath', '//*[@id="landing_button"]')
                logging.info('Promo code activated: %s', promo_code[1])
            except selenium.common.exceptions.TimeoutException:
                logging.info('Broke promo code: %s', promo_code[1])
        else:
            self.GoToUrl(LITRES_PROMOCODE_URL)
            self.FillElement('xpath', '//*[@id="code1"]', promo_code[0] + '\n')
            try:
                fail_message = self.WaitElementLoad('xpath', '/html/body/div[20]/p', 5).text
                logging.info('Broke promo code: %s', promo_code[0] + ' : ' + fail_message)
            except selenium.common.exceptions.TimeoutException:
                logging.info('Promo code activated: %s', promo_code[0])

    def GoToUrl(self, url):
        logging.debug('Going to %s', url)
        self.driver.get(url)

    def Refresh(self):
        logging.debug('Refreshing the page')
        self.driver.refresh()

    def Kill(self):
        logging.debug('Closing driver')
        self.driver.close()

    def WaitElementLoad(self, by_, locator, time_to_wait=TIME_WAIT_ELEMENT):
        logging.debug('Waiting element with locator %s by %s for %s seconds', by_, locator, time_to_wait)
        return WebDriverWait(self.driver, time_to_wait).until(
            lambda x: x.find_element(by=by_, value=locator))

    def FillElement(self, by_, locator, value):
        element = self.WaitElementLoad(by_, locator)
        logging.debug('Filling element with locator %s by %s and value %s', by_, locator, value)
        element.clear()
        element.send_keys(value)

    def ClickElement(self, by_, locator):
        logging.debug('Clicking to element with locator %s by %s', by_, locator)
        self.WaitElementLoad(by_, locator).click()
