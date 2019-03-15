#author py chen

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.header import Header
import smtplib

import requests,json,time

from common import *

HEADER={ "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36"
    "(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"}

WEATHER_API = "http://api.map.baidu.com/telematics/v3/weather?location={city}&output=json&ak=TueGDhCvwI6fOrQnLM0qmXxY9N0OkOiQ&callback=?"#


CONTENT_FORMAT = (
    "你好，傻宝宝 😄 :\n\n\t"
    "今天是 {_date}，{_week}。\n\t"
    "首先，今天已经是我们相恋的第 {_loving_days} 天了喔 💓。然后我就要来播送天气预报了！！\n\n\t"
    "👧 {_g_city}今天{_g_weather_low}~{_g_weather_high}，天气 {_g_weather_type} 风力 💨 {_g_weather_wind}。\n\n\t"
    "👘 穿衣指数：{_g_weather_wear}\n\n\t"
    "🤒 感冒指数：{_g_weather_cold}别感冒了哦。 \n\n\t"
    "🏄‍ 运动指数：{_g_weather_sport}\n\n\t"
    "🛴 洗车指数：{_g_weather_wash}\n\n\t"
    "🔅 紫外线指数：{_g_weather_sun}\n\n\t"

    "👧 {_g_city}明天{_g_weather_tomorrow_low}~{_g_weather_tomorrow_high}，天气 {_g_weather_tomorrow_type} 风力 💨 {_g_weather_tomorrow_wind}\n\n\t"
    "👦 {_b_city}今天{_b_weather_low}~{_b_weather_high}，天气 {_b_weather_type}。"
    "{_b_weather_wear}\n\n\t"


)



girl_CITY="杭州"
boy_CITY="嘉兴"

def seach_weather_info(WEATHER_API):

    girl_CITY_WEATHER= requests.get(WEATHER_API.format(city=girl_CITY),HEADER).json()

    boy_CITY_WEATHER=requests.get(WEATHER_API.format(city=boy_CITY),HEADER).json()


    g_status=girl_CITY_WEATHER["status"]
    b_status=girl_CITY_WEATHER["status"]
    if g_status  == "success" and b_status == "success":

        g_main_info=girl_CITY_WEATHER["results"]
        b_main_info=boy_CITY_WEATHER["results"]


        g_city=g_main_info[0]["currentCity"]
        b_city=b_main_info[0]["currentCity"]

        #总的天气信息中的内容
        g_weather_data=g_main_info[0]["weather_data"]
        b_weather_data=b_main_info[0]["weather_data"]

        # 当天天气情况
        #当天日期
        time_info=g_weather_data[0]["date"]
        _week=time_info.split(' ')[0]
        _date=girl_CITY_WEATHER['date']
        #当天天气
        g_today_weather=g_weather_data[0]["weather"]

        g_today_wind=g_weather_data[0]["wind"]
        g_today_temperature_high=g_weather_data[0]["temperature"].split('~')[0].strip(' ')+"℃"
        g_today_temperature_low=g_weather_data[0]["temperature"].split('~')[1].strip(' ')
        g_today_index=g_main_info[0]["index"]
        g_today_wear=g_today_index[0]["des"]
        g_today_cold=g_today_index[2]["des"]
        g_today_sport=g_today_index[3]["des"]
        g_today_wash_car=g_today_index[3]["des"]
        g_today_zwx=g_today_index[4]["des"]

        #第二天天气情况
        g_tomorrow_weather=g_weather_data[1]["weather"]
        g_tomorrow_wind=g_weather_data[1]["wind"]
        g_tomorrow_temperature_high=g_weather_data[1]["temperature"].split('~')[0].strip(' ')+"℃"
        g_tomorrow_temperature_low=g_weather_data[1]["temperature"].split('~')[1].strip(' ')

        b_tomorrow_weather=b_weather_data[1]["weather"]
        b_tomorrow_temperature_high=b_weather_data[1]["temperature"].split('~')[0].strip(' ')+"℃"
        b_tomorrow_temperature_low=b_weather_data[1]["temperature"].split('~')[1].strip(' ')
        b_tomorrow_index=b_main_info[0]["index"]
        b_tomorrow_wear=b_tomorrow_index[0]["des"]

        loving_days=get_loving_days()
        return CONTENT_FORMAT.format(
            _date=_date,
            _week=_week,
            _loving_days=loving_days,
            _g_city=g_city,
            _g_weather_high=g_today_temperature_high,
            _g_weather_low=g_today_temperature_low,
            _g_weather_type=g_today_weather,
            _g_weather_wind=g_today_wind,
            _g_weather_wear=g_today_wear,
            _g_weather_cold=g_today_cold,
            _g_weather_sport=g_today_sport,
            _g_weather_wash=g_today_wash_car,
            _g_weather_sun=g_today_zwx,
            _g_weather_tomorrow_high=g_tomorrow_temperature_high,
            _g_weather_tomorrow_low=g_tomorrow_temperature_low,
            _g_weather_tomorrow_type=g_tomorrow_weather,
            _g_weather_tomorrow_wind=g_tomorrow_wind,
            _b_city=b_city,
            _b_weather_high=b_tomorrow_temperature_high,
            _b_weather_low=b_tomorrow_temperature_low,
            _b_weather_type=b_tomorrow_weather,
            _b_weather_wear=b_tomorrow_wear,

        )

    else:
        print("weather_api error")


def sendEmail(authInfo, fromAdd, toAdd, subject):

    strFrom = fromAdd

    server = authInfo.get('server')

    sslPort = 465
    user = authInfo.get('user')
    passwd = authInfo.get('password')

    if not (server and user and passwd):
        print('incomplete login info, exit now')
        return

    msgRoot = MIMEMultipart('related')
    # 邮件标题
    msgRoot['Subject'] = subject
    # 发件人
    msgRoot['From'] = Header(strFrom)
    # 收件人
    msgRoot['To'] = Header('A pretty girl', 'utf-8')

    CONTENT_FORMAT = seach_weather_info(WEATHER_API)

    msgText = MIMEText(CONTENT_FORMAT, 'plain', 'utf-8')

    msgRoot.attach(msgText)

    try:

        smtp = smtplib.SMTP_SSL()
        smtp.connect(server, sslPort)

        smtp.login(user, passwd)
        smtp.sendmail(strFrom, toAdd, msgRoot.as_string())
        smtp.quit()
        print("邮件发送成功!")

    except Exception as e:
        print("失败：" + str(e))





if __name__ == '__main__':

    authInfo={}
    authInfo['server'] = MAIL_SERVER

    #
    authInfo['user'] = USER_MAIL

    authInfo['password'] = PASS_MAIL

    fromAdd = SEND_MAIL

    toAdd =  TO_MAIL
    if type(toAdd) is str:
        toAdd = toAdd.split(',')
    subject = '😘 男朋友的日常问候'

    sendEmail(authInfo, fromAdd, toAdd, subject)


