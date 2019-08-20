import telegram
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler  # import modules
import requests
import schedule
import time
import threading

# request
# product_group_code : 0001(파크캠핑빌리지), 0002(테라스캠핑빌리지), 0003(힐링캠핑빌리지), 0004(캐빈캠핑빌리지)
# shopCode : 217820482301(초안산캠핑장)

#response
# {"data":{"bookProductList":[{"status_code":"0","width":20,"product_name":"C01","product_discount_fee":30000,"x_coordinate":562,"product_premium_fee":30000,"product_member_fee":0,"select_yn":"0","height":20,"product_eng_name":"C01","product_code":"00040001","season_code":"0","y_coordinate":78,"sale_product_fee":0,"product_fee":30000}
#                            ,{"status_code":"0","width":20,"product_name":"C02","product_discount_fee":30000,"x_coordinate":588,"product_premium_fee":30000,"product_member_fee":0,"select_yn":"0","height":20,"product_eng_name":"C02","product_code":"00040002","season_code":"0","y_coordinate":78,"sale_product_fee":0,"product_fee":30000}
# 			                 ,{"status_code":"0","width":20,"product_name":"C03","product_discount_fee":30000,"x_coordinate":619,"product_premium_fee":30000,"product_member_fee":0,"select_yn":"0","height":20,"product_eng_name":"C03","product_code":"00040003","season_code":"0","y_coordinate":83,"sale_product_fee":0,"product_fee":30000}]}}

def makeCheckUrl(product_group_code, date, shopCode):

    CHECK_URL = 'https://camp.xticket.kr/Web/Book/GetBookProduct010001.json' \
                '?product_group_code='+product_group_code+\
                '&start_date='+date+\
                '&end_date='+date+\
                '&book_days=1' \
                '&two_stay_days=0' \
                '&shopCode='+shopCode
    return CHECK_URL

# message reply function
def get_message(bot, update) :
    update.message.reply_text("got text")
    update.message.reply_text(update.message.text)

    # if update.message.text == '조회시작':
    # runCheck(bot, update)


def go_command(bot, update) :
    update.message.reply_text("go")
    runCheck(bot, update)




def runCheck(bot, update) :
    threading.Timer(5.0, runCheck).start()
    # date = input("조회일자(yyyymmdd): ")
    # product_group_code = input("캠핑장종류(0001(파크캠핑빌리지), 0002(테라스캠핑빌리지), 0003(힐링캠핑빌리지), 0004(캐빈캠핑빌리지)): ")

    date = '20190826'
    product_group_code = '0001'
    with requests.Session() as s:
        main = s.get(HOME_URL)

        login_res = s.post(LOGIN_URL)
        # update.message.reply_text(login_res.json())

        check_res = s.post(makeCheckUrl(product_group_code, date, shopCode))
        # print(check_res.json()['data']['bookProductList'])
        print(check_res.json()['data']['bookProductList'])
        for result in check_res.json()['data']['bookProductList']:
            print(result)
            if result['select_yn'] == '0':
                update.message.reply_text(result['product_name'] + ' not reserved')

# help reply function
def help_command(bot, update) :
    update.message.reply_text("무엇을 도와드릴까요?")

if __name__ ==  "__main__":
    print('start telegram chat bot')

    id = 'haeseoky'
    pw = 'yunhs1206'
    shopCode = '217820482301'

    date = ''
    product_group_code = ''
    HOME_URL = 'https://camp.xticket.kr/web/main?shopEncode=ff0ecee2292c6ef6976558aeb171cf2a172391f74de8d6f5f290b89b0a68213a'
    LOGIN_URL = 'https://camp.xticket.kr/Web/Member/MemberLogin.json?' \
                'member_id=' + id + \
                '&member_password=' + pw + \
                '&shopCode=' + shopCode
    BOOKING_URL = 'https://camp.xticket.kr/Web/Book/Book010001.json?' \
                  'product_group_code=' + product_group_code + \
                  '&play_date=' + date + \
                  '&product_code=00040003' \
                  '&captcha=1' \
                  '&shopCode=' + shopCode
    my_token = '963244714:AAGeTQYLlBihiPfxLJBcfM4aWYrR9N3xqcE'  # 토큰을 변수에 저장합니다.

    updater = Updater(my_token)


    message_handler = MessageHandler(Filters.text, get_message)
    updater.dispatcher.add_handler(message_handler)

    help_handler = CommandHandler('help', help_command)
    updater.dispatcher.add_handler(help_handler)

    go_handler = CommandHandler('go', go_command)
    updater.dispatcher.add_handler(go_handler)

    updater.start_polling(timeout=3, clean=True)
    updater.idle()


