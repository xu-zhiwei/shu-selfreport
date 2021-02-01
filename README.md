# shu-selfreport
用于http请求学习、web工作原理学习、网站开发学习的项目，欢迎大家讨论交流计算机网络的原理。

## 分支

### http_request
通过发送http请求填报。每日在早上8:00自动填报，成功后，发送填报成功的邮件到指定邮箱。（需要配置smtp，建议使用tmux挂载）

## 配置文件说明（http_request下的config.txt）
* student_id：学号
* student_password：学号的密码
* send_email_id：发件人邮箱地址，如xxxx@qq.com
* send_email_password：发件人smtp密码，请到邮箱网站获取
* send_email_hostname：发件人主机，如QQ邮箱为smtp.qq.com
* receive_email_id：收件人邮箱地址
* xian: 县级单位（只支持上海市的某个区，如宝山区）
* address: 具体地址

## 免责声明
本项目只供本人学习交流使用，欢迎交流学习心得，请勿用于其他用途。
