import datetime
import requests
from bs4 import BeautifulSoup
from .get_f_state import get_f_state
import time
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.header import Header
import base64


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
    state = eval(base64.b64decode(r.url.split('/')[-1]).decode("utf-8"))['state']
    sess.post(r.url, data={'username': config['student_id'], 'password': config['student_password']})
    return sess, state


def send_email(config, cur_date):
    """
    发送填报成功的邮件
    :param config:
    :param cur_date:
    :param is_morning:
    :return:
    """
    email_from = config['send_email_id']  # 发送邮箱
    email_to = config['receive_email_id']  # 接收邮箱
    hostname = config['send_email_hostname']  # smtp服务器地址
    login = config['send_email_id']  # 发送邮箱的用户名
    password = config['send_email_password']  # 发送邮箱的密码，即开启smtp服务得到的授权码
    subject = '%s %s - 填报成功！' % (cur_date, config['student_id'])  # 邮件主题
    text = '%s %s - 填报成功！' % (cur_date, config['student_id'])  # 邮件正文内容

    smtp = SMTP_SSL(hostname)  # SMTP_SSL默认使用465端口
    smtp.login(login, password)

    msg = MIMEText(text, "plain", "utf-8")
    msg["Subject"] = Header(subject, "utf-8")
    msg["from"] = email_from
    msg["to"] = email_to

    smtp.sendmail(email_from, email_to, msg.as_string())
    smtp.quit()


def report(config, cur_date):
    """
    根据具体的日期、上午还是下午来填报信息
    :param config:
    :param cur_date:
    :param is_morning:
    :return:
    """
    # 准备好要填报的session和url
    sess, state = get_session(config)
    url = 'https://selfreport.shu.edu.cn/DayReport.aspx'

    # 跳转到健康之路
    while True:
        try:
            r = sess.get(f'https://newsso.shu.edu.cn/oauth/authorize?response_type=code&client_id=WUHWfrntnWYHZfzQ5QvXU'
                         f'CVy&redirect_uri=https%3a%2f%2fselfreport.shu.edu.cn%2fLoginSSO.aspx%3fReturnUrl%3d%252fDefa'
                         f'ult.aspx&scope=1&state={state}')
            r = sess.get(url)
        except Exception as e:
            print(e)
            continue
        break

    # 获取view_state和f_state
    soup = BeautifulSoup(r.text, 'html.parser')
    view_state = soup.find('input', attrs={'name': '__VIEWSTATE'})['value']
    f_state = get_f_state(cur_date)

    # 填报
    while True:
        try:
            r = sess.post(url, data={
                '__EVENTTARGET': 'p1$ctl00$btnSubmit',
                '__VIEWSTATE': view_state,
                '__VIEWSTATEGENERATOR': '7AD7E509',
                'p1$ChengNuo': 'p1_ChengNuo',
                'p1$BaoSRQ': cur_date,
                'p1$DangQSTZK': '良好',
                'p1$TiWen': '',
                'p1$JiuYe_ShouJHM': '',
                'p1$JiuYe_Email': '',
                'p1$JiuYe_Wechat': '',
                'p1$QiuZZT': '',
                'p1$JiuYKN': '',
                'p1$JiuYSJ': '',
                'p1$ZaiXiao': '不在校',
                'p1$MingTDX': '不到校',
                'p1$BanChe_1$Value:': '0',
                'p1$BanChe_1': '不需要乘班车',
                'p1$BanChe_2$Value': '0',
                'p1$BanChe_2': '不需要乘班车',
                'p1$GuoNei': '国内',
                'p1$ddlGuoJia$Value': '-1',
                'p1$ddlGuoJia': '选择国家',
                'p1$ShiFSH': '是',
                'p1$ShiFZX': '否',
                'p1$ddlSheng$Value': '上海',
                'p1$ddlSheng': '上海',
                'p1$ddlShi$Value': '上海市',
                'p1$ddlShi': '上海市',
                'p1$ddlXian$Value': config['xian'],
                'p1$ddlXian': config['xian'],
                'p1$XiangXDZ': config['address'],
                'p1$FengXDQDL': '否',
                'p1$TongZWDLH': '否',
                'p1$CengFWH': '否',
                'p1$CengFWH_RiQi': '',
                'p1$CengFWH_BeiZhu': '',
                'p1$JieChu': '否',
                'p1$JieChu_RiQi': '',
                'p1$JieChu_BeiZhu': '',
                'p1$TuJWH': '否',
                'p1$TuJWH_RiQi': '',
                'p1$TuJWH_BeiZhu': '',
                'p1$QueZHZJC$Value': '否',
                'p1$QueZHZJC': '否',
                'p1$DangRGL': '否',
                'p1$GeLDZ': '',
                'p1$FanXRQ': '',
                'p1$WeiFHYY': '',
                'p1$ShangHJZD': '',
                'p1$DaoXQLYGJ': '否',
                'p1$DaoXQLYCS': '否',
                'p1$JiaRen_BeiZhu': '',
                'p1$SuiSM': '绿色',
                'p1$LvMa14Days': '是',
                'p1$Address2': '',
                'F_TARGET': 'p1_ctl00_btnSubmit',
                'p1_ContentPanel1_Collapsed': 'true',
                'p1_GeLSM_Collapsed': 'false',
                'p1_Collapsed': 'false',
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


def daily_report(config, cur_date) -> bool:
    count = 0
    while not report(config, cur_date):
        time.sleep(2 * 60)  # 如果未成功，隔两分钟之后再填报一次
        count += 1
        if count == 10:  # 如果连报10次均为成功，中断程序运行，防止bug
            return False
    print('%s %s - 填报成功！' % (cur_date, config['student_id']))
    send_email(config, cur_date)
    return True


def automatic_report(config):
    ok = False
    cur_day = get_cur_time().day

    while True:
        # 填报时间：上午8:00
        cur_time = get_cur_time()
        cur_date = cur_time.strftime('%Y-%m-%d')

        # 如果还未填报，且已经到了填报时间
        if not ok and 8 <= cur_time.hour:
            if daily_report(config, cur_date):
                ok = True
            else:
                break

        # 次日，重新填报
        if cur_day != cur_time.day:
            cur_day = cur_time.day
            ok = False

        time.sleep(60 * 5)  # 检测频率为5分钟
