# shu-selfreport

## 分支
### web_browser
基于浏览器驱动开发，模拟浏览器的操作填报。只适用于安装有浏览器且有图形化界面的计算机。

注意：该功能分支已经不再更新支持，请使用http_request方式。

### http_request
通过发送http请求填报。每日在8:00和20:00自动填报，成功后，发送填报成功的邮件到指定邮箱。（需要配置smtp，建议使用tmux）

## 配置文件说明（http_request下的config.txt）
* student_id：学号
* student_password：学号的密码
* send_email_id：发件人邮箱地址，如xxxx@qq.com
* send_email_password：发件人smtp密码，请到邮箱网站获取
* send_email_hostname：发件人主机，如QQ邮箱为smtp.qq.com
* receive_email_id：收件人邮箱地址

## 免责声明
本项目只供本人学习交流使用。
