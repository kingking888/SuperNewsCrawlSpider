# author: lzc
# update: 2019.7.25
# email:  18410820@qq.com
import logging
import smtplib
from os import path
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


def isContainChinese(string):
    # 判断字符串是否含有中文
    for s in string:
        if '\u4e00' <= s <= '\u9fa5':
            return True
    return False



class EmailSender(object):
    # 初始化
    msg = MIMEMultipart()
    client = ''

    # def __init__(self, email_host='smtp.qq.com', email_port=265, email_pass=''):
    def __init__(self, email_host='smtp.163.com', email_port=25, email_pass=''):
        self.logger = logging.getLogger(__name__)
        self.email_host = email_host
        self.email_port = email_port
        if email_pass:
            self.email_pass = email_pass
        else:
            # 可以设置一个初始值，避免每次都输入授权码
            self.email_pass = 'ping1688'
            # self.logger.error('Please Enter The  Password!')

    def init(self, from_addr, to_addrs, subject):
        # 初始化，填入以下信息
        # from_addr = '发件人'
        # to_addrs = '收件人'  （ 收件人为字符串时，视其为一个仅含该字符串的列表 ）
        # subject = '邮件标题'
        if isinstance(to_addrs, list):
            pass
        elif isinstance(to_addrs, str):
            to_addrs = [to_addrs]
        else:
            self.logger.error('[ to_addrs ] must be a str or list.')
            return '[ to_addrs ] must be a str or list.'

        self.msg['From'] = from_addr
        # 需为用 ';' 连接的字符串
        self.msg['To'] = ';'.join(to_addrs)
        self.msg['Subject'] = subject

        try:
            # 在创建客户端对象的同时，使用SSL加密连接到邮箱服务器
            self.client = smtplib.SMTP_SSL(host=self.email_host, port=self.email_port)
            login_result = self.client.login(from_addr, self.email_pass)
            if login_result and login_result[0] == 235:
                print('[ EmailSender ] Login successful.')
            else:
                print('[ EmailSender ] Login failed: ', login_result[0], login_result[1])
        except Exception as e:
            self.logger.error('[ EmailSender ] Connection to mail server error: %s.' % e)

    def attach_text(self, text=''):
        # 添加邮件正文 （ 纯文本 ）
        msg_text = MIMEText(text, 'plain', 'utf8')
        self.msg.attach(msg_text)

    def attach_html(self, text=''):
        # 添加邮件正文 （ html ）
        # html 格式不固定，故请将 html 源码全部输入
        # 此处不通过 MIMEImage 定义图片ID，在 HTML 文本中引用 （ ... ）
        msg_text = MIMEText(text, 'html', 'utf8')
        self.msg.attach(msg_text)

    def attach_file(self, file=''):
        # 添加邮件附件
        if not file:
            self.logger.error('Please enter the filename that contains the full path.')
            return None
        with open(file, 'rb') as f:
            # 不使用这种，没有文件关闭操作
            # att = MIMEText(open(file, 'rb').read(), 'base64', 'utf-8')
            att = MIMEText(f.read(), 'base64', 'utf-8')
            att['Content-Type'] = 'application/octet-stream'
            # 获取文件名
            filename = path.split(file)[1]
            # 判断文件名是否含有中文
            if isContainChinese(filename):
                # 处理中文文件名 （ add_header的第三种写法 ）
                att.add_header("Content-Disposition", "attachment", filename=("gbk", "", filename))
            else:
                # 文件名不含中文 （ add_header的第一种写法 ）
                att.add_header('content-disposition', 'attachment', filename=filename)
                # 或者可以这样写
                # att['Content-Disposition'] = 'attachment;filename="%s"' % filename
            self.msg.attach(att)

    def send(self):
        if self.client:
            from_addr = self.msg['From']
            # 需为一个 list
            to_addrs = self.msg['To'].split(';')
            try:
                self.client.sendmail(from_addr, to_addrs, self.msg.as_string())
                print('[ EmailSender ] Email sent successfully.')
            except Exception as e:
                self.logger.error('[ EmailSender ] e-mail sending failed: %s.' % e)
        else:
            self.logger.error('[ EmailSender ] You must first connect to the mail server by using [ init ].')

    def close(self):
        # 关闭对邮件服务器的连接
        if self.client:
            self.client.close()
            print('[ EmailSender ] Closed.')
        else:
            self.logger.error('[ EmailSender ] You must first connect to the mail server by using [ init ].')


if __name__ == '__main__':
    email = EmailSender(email_host='smtp.qq.com', email_pass='xxx')
    content = '这是...发送过来的邮件。请注意查收！'
    email.init(from_addr='xxx@qq.com', to_addrs=['xxx@qq.com'], subject='测-试')
    email.attach_text(text=content)
    email.attach_file(r'C:\xxx\xx.jpg')
    email.attach_file(r'C:\xxx\xx.txt')
    email.send()
