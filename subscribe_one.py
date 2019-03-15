from  pyppeteer import launch
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.header import Header
import smtplib
import asyncio
from common import *

HTML = """
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
</head>
<body>
    <div align="center">
        <h2>😘 Daily</h2>
        <p>傻宝宝，今天已经是我们相恋的第 {loving_days} 天了喔 💓。</p>
        <br/>
        <img style="padding: 0.60em; background: white; box-shadow: 1px 1px 10px #999;" src="cid:one" />
    </div>
</body>
</html>
"""

IMAGE_NAME='one.png'


async  def fetch_pict():
    brower=await launch( {"args": ["--no-sandbox", "--disable-setuid-sandbox"]})
    page =await brower.newPage()
    await page.goto('http://wufazhuce.com/')
    # clip 指明要裁剪的图片的位置，path存储在本地的路径
    await page.screenshot({'path':IMAGE_NAME,"clip": {"x": 60, "y": 120, "height": 570, "width": 700},})

    await brower.close()

def sendEmail(authInfo, fromAdd, toAdd, subject,loving_days):

    strFrom = fromAdd
    strTo = '; '.join(toAdd)

    server = authInfo.get('server')

    sslPort = 465
    user = authInfo.get('user')
    passwd = authInfo.get('password')

    if not (server and user and passwd):
        print('incomplete login info, exit now')
        return

    # 设定root信息 创建一个邮件实例
    msgRoot = MIMEMultipart('related')
    # 邮件标题
    msgRoot['Subject'] = subject
    # 发件人
    msgRoot['From'] = Header('A handsome boy', 'utf-8')
    # 收件人
    msgRoot['To'] = Header('A pretty girl', 'utf-8')

    msgAlternative = MIMEMultipart('alternative')

    msgRoot.attach(msgAlternative)
    print(loving_days)
    New_HTML=HTML.replace("{loving_days}",str(loving_days))


    msgAlternative.attach(MIMEText(New_HTML, 'html', 'utf-8'))

    # 设定内置图片信息
    fp = open('one.png', 'rb')
    msgImage = MIMEImage(fp.read())
    msgImage["Content-Type"] = 'application/octet-stream'
    # filename可自定义，供邮件中显示
    msgImage["Content-Disposition"] = 'attachment; filename="one.png"'
    fp.close()
    #上面html中定义了 one 这里如果插入图片名字也要相同 为one
    msgImage.add_header('Content-ID', 'one')
    msgAlternative.attach(msgImage)


    # 发送邮件
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
    try:
        asyncio.get_event_loop().run_until_complete(fetch_pict())
    except:
        asyncio.get_event_loop().run_until_complete(fetch_pict())

    loving_days=get_loving_days()

    authInfo = {}
    authInfo['server'] = MAIL_SERVER
    #
    authInfo['user'] = USER_MAIL
    #
    authInfo['password'] = PASS_MAIL
    #
    fromAdd = SEND_MAIL

    # 如果想要将邮件发给多人，就可以指定一个列表


    toAdd =  TO_MAIL
    if type(toAdd) is str:
        toAdd = toAdd.split(',')

    # 邮件标题
    subject = 'daily'

    sendEmail(authInfo, fromAdd, toAdd, subject,loving_days)










