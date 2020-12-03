import datetime
import requests
from bs4 import BeautifulSoup
from .get_f_state import get_f_state
import time
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.header import Header


def get_cur_time() -> datetime.datetime:
    """
    获取当前的时间
    :return:
    """
    return datetime.datetime.utcnow() + datetime.timedelta(hours=8)


def get_session(config):
    """
    获取登陆的session
    :param config:
    :return:
    """
    sess = requests.Session()
    r = sess.get('https://selfreport.shu.edu.cn')
    sess.post(r.url, data={'username': config['student_id'], 'password': config['student_password']})
    return sess


def send_email(config, cur_date, is_morning):
    """
    发送填报成功的邮件
    :param config:
    :param cur_date:
    :param is_moring:
    :return:
    """
    email_from = config['send_email_id']                # 发送邮箱
    email_to = config['receive_email_id']               # 接收邮箱
    hostname = config['send_email_hostname']            # smtp服务器地址
    login = config['send_email_id']                     # 发送邮箱的用户名
    password = config['send_email_password']            # 发送邮箱的密码，即开启smtp服务得到的授权码
    subject = '%s%s - %s - 填报成功！' % (cur_date, '上午' if is_morning else '下午', config['student_id'])   # 邮件主题
    text = '%s%s - %s - 填报成功！' % (cur_date, '上午' if is_morning else '下午', config['student_id'])      # 邮件正文内容

    smtp = SMTP_SSL(hostname)                           # SMTP_SSL默认使用465端口
    smtp.login(login, password)

    msg = MIMEText(text, "plain", "utf-8")
    msg["Subject"] = Header(subject, "utf-8")
    msg["from"] = email_from
    msg["to"] = email_to

    smtp.sendmail(email_from, email_to, msg.as_string())
    smtp.quit()


def report(config, cur_date, is_morning):
    """
    根据具体的日期、上午还是下午来填报信息
    :param config:
    :param cur_date:
    :param is_morning:
    :return:
    """
    # 准备好要填报的session和url
    sess = get_session(config)
    t = '1' if is_morning else '2'
    url = 'https://selfreport.shu.edu.cn/XueSFX/HalfdayReport.aspx?day=%s&t=%s' % (cur_date, t)

    # 跳转到健康之路
    while True:
        try:
            sess.get('https://newsso.shu.edu.cn/oauth/authorize?response_type=code&client_id=WUHWfrntnWYHZfzQ5QvXUCVy&'
                     'redirect_uri=https%3a%2f%2fselfreport.shu.edu.cn%2fLoginSSO.aspx%3fReturnUrl%3d%252fDefault.aspx&'
                     'scope=1')
            r = sess.get(url)
        except Exception as e:
            print(e)
            continue
        break

    # 获取view_state和f_state
    soup = BeautifulSoup(r.text, 'html.parser')
    view_state = soup.find('input', attrs={'name': '__VIEWSTATE'})['value']
    f_state = get_f_state(cur_date, t)

    # 填报
    while True:
        try:
            r = sess.post(url, data={
                '__EVENTTARGET': 'p1$ctl00$btnSubmit',
                '__VIEWSTATE': view_state,
                '__VIEWSTATEGENERATOR': 'DC4D08A3',
                'p1$ChengNuo': 'p1_ChengNuo',
                'p1$BaoSRQ': cur_date,
                'p1$DangQSTZK': '良好',
                'p1$TiWen': '37',
                'p1$ZaiXiao': '宝山',
                'p1$ddlSheng$Value': '上海',
                'p1$ddlSheng': '上海',
                'p1$ddlShi$Value': '上海市',
                'p1$ddlShi': '上海市',
                'p1$ddlXian$Value': '宝山区',
                'p1$ddlXian': '宝山区',
                'p1$FengXDQDL': '否',
                'p1$TongZWDLH': '否',
                'p1$XiangXDZ': '上海大学',
                'p1$QueZHZJC$Value': '否',
                'p1$QueZHZJC': '否',
                'p1$DangRGL': '否',
                'p1$GeLDZ': '',
                'p1$CengFWH': '否',
                'p1$CengFWH_RiQi': '',
                'p1$CengFWH_BeiZhu': '',
                'p1$JieChu': '否',
                'p1$JieChu_RiQi': '',
                'p1$JieChu_BeiZhu': '',
                'p1$TuJWH': '否',
                'p1$TuJWH_RiQi': '',
                'p1$TuJWH_BeiZhu': '',
                'p1$JiaRen_BeiZhu': '',
                'p1$SuiSM': '绿色',
                'p1$LvMa14Days': '是',
                'p1$Address2': '',
                'p1_GeLSM_Collapsed': 'false',
                'p1_Collapsed': 'false',
                'F_TARGET': 'p1_ctl00_btnSubmit',
                'F_STATE': f_state
            }, headers={
                'X-Requested-With': 'XMLHttpRequest',
                'X-FineUI-Ajax': 'true'
            }, allow_redirects=False)
        except Exception as e:
            print(e)
            continue
        break

    # 返回填报结果
    return any(i in r.text for i in ['提交成功', '历史信息不能修改', '现在还没到晚报时间', '只能填报当天或补填以前的信息'])


def automatic_report(config):
    morning_ok, evening_ok = False, False
    cur_day = get_cur_time().day

    while True:
        # 填报时间：上午8:00和晚上8:00
        cur_time = get_cur_time()
        cur_date = cur_time.strftime('%Y-%m-%d')
        is_morning = cur_time.hour < 20

        # 如果上午的还未填报，且已经到了填报时间
        if not morning_ok and cur_time.hour >= 8:
            while not report(config, cur_date, is_morning):
                time.sleep(60)  # 如果未成功，隔一分钟之后再次填报一次
            morning_ok = True
            print('%s%s - %s - 填报成功！' % (cur_date, '上午' if is_morning else '下午', config['student_id']))
            send_email(config, cur_date, is_morning)

        # 如果下午的还未填报，且已经到了填报时间
        if not evening_ok and cur_time.hour >= 20:
            while not report(config, cur_date, is_morning):
                time.sleep(60)  # 如果未成功，隔一分钟之后再次填报一次
            evening_ok = True
            print('%s%s - %s - 填报成功！' % (cur_date, '上午' if is_morning else '下午', config['student_id']))
            send_email(config, cur_date, is_morning)

        # 次日，重新填报
        if cur_day != cur_time.day:
            cur_day = cur_time.day
            morning_ok, evening_ok = False, False

        time.sleep(60 * 5)  # 检测频率为5分钟

