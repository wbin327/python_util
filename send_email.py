# coding:utf-8
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import EmailConfig
import os


class SendEmail(object):
    """
    smtp邮件功能封装
    """

    def __init__(self, host: str='', user: str='', password: str='', port: int='', sender: str='', receive: list=''):
        """

        :param host: 邮箱服务器地址
        :param user: 登陆用户名
        :param password: 登陆密码
        :param port: 邮箱服务端口
        :param sender: 邮件发送者
        :param receive: 邮件接收者
        """
        self.HOST = host
        self.USER = user
        self.PASSWORD = password
        self.PORT = port
        self.SENDER = sender
        self.RECEIVE = receive

        # 与邮箱服务器的连接
        self._server = ''
        # 邮件对象,用于构造邮件内容
        self._email_obj = ''

    def load_server_setting_from_obj(self, obj):
        """从对象中加载邮件服务器的配置
        :param obj, 类对象
        HOST, 邮件服务器地址
        USER, 邮件服务器登陆账号
        PASSWORD, 邮件服务器登陆密码
        SENDER, 发送者
        """
        attrs = {key.upper(): values for key, values in obj.__dict__.items() if not key.startswith('__')}
        for key, value in attrs.items():
            self.__setattr__(key, value)

    def connect_smtp_server(self, method='default'):
        """连接到smtp服务器"""
        if method == 'default':
            self._server = smtplib.SMTP(self.HOST, self.PORT, timeout=2)
        if method == 'ssl':
            self._server = smtplib.SMTP_SSL(self.HOST, self.PORT, timeout=2)

        self._server.login(self.USER, self.PASSWORD)

    def construct_email_obj(self, subject='python email'):
        """构造邮件对象
        subject: 邮件主题
        from: 邮件发送方
        to: 邮件接收方
        """

        # mixed参数表示混合类型，这个邮件对象可以添加html,txt,附件等内容
        msg = MIMEMultipart('mixed')
        msg['Subject'] = subject
        msg['From'] = self.SENDER
        msg['To'] = ';'.join(self.RECEIVE)
        self._email_obj = msg

    def add_content(self, content: str, _type: str = 'txt'):
        """给邮件对象添加正文内容"""
        if _type == 'txt':
            text = MIMEText(content, 'plain', 'utf-8')
        if _type == 'html':
            text = MIMEText(content, 'html', 'utf-8')

        self._email_obj.attach(text)

    def add_file(self, file_path: str):
        """
        给邮件对象添加附件
        :param file_path: 文件路径
        :return: None
        """
        # 构造附件1，传送当前目录下的 test.txt 文件
        email_file = MIMEText(open(file_path, 'rb').read(), 'base64', 'utf-8')
        email_file["Content-Type"] = 'application/octet-stream'
        # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
        file_name = os.path.basename(file_path)
        email_file["Content-Disposition"] = f'attachment; filename="{file_name}"'
        self._email_obj.attach(email_file)

    def send_email(self):
        """发送邮件"""
        # 使用send_message方法而不是sendmail,避免编码问题
        self._server.send_message(from_addr=self.SENDER, to_addrs=self.RECEIVE, msg=self._email_obj)

    def quit(self):
        self._server.quit()

    def close(self):
        self._server.close()


if __name__ == '__main__':
    email = SendEmail()
    email.load_server_setting_from_obj(EmailConfig)
    email.connect_smtp_server(method='ssl')
    email.construct_email_obj(subject='python mail test')
    email.add_content(content='hello world')
    email.add_file(file_path='mail_test.txt')
    email.send_email()
    email.close()