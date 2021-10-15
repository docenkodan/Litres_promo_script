from sys import argv, stdout
import logging

from bot import Bot
from promo_parser import parse_promo


# Config logging to stdout and file. Set format of logging
def initLogging():
    console_out = logging.StreamHandler(stream=stdout)

    logging.basicConfig(level=logging.INFO,
                        format=u'[%(asctime)s] %(levelname)-7s - %(message)s')


if __name__ == "__main__":
    initLogging()
    promo_codes = parse_promo()
    # promo_codes is a list of (promo_code, promo_url)
    # for code in promo_codes:
        # print(code)
    bot = Bot()
    filename, email, password = argv
    if bot.LogIn(email, password):
        for promo_code in promo_codes:
            bot.ActivatePromoCode(promo_code)
    bot.Kill()
