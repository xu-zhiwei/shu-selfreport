# shu-selfreport
关键词：上海大学、健康之路、每日一报、每日两报、在校学生日报、报送历史、上海大学每日一报

服务于上海大学健康之路平台(https://selfreport.shu.edu.cn)的工具。
该工具具有在校学生日报、报送历史补填功能。

PS：由于没有测试账号，非在校学生的日报功能暂无法提供，请有意愿的好心人能提供测试账号，帮助完成这项功能，本人保证绝不泄露个人信息。

## 现在已经完成的部分
运行代码后单次每日一报。

自动按时每日一报工具正在研发中，预计2-3天内发布。

## 使用方法
1. 打开config参数，填写自己的个人信息，参数解释如下：
    * operating_system：操作系统（win32、mac64、linux64）
    * student_id：学号
    * password：密码
    * campus：当天是否在校（0 - 不在校、1 - 宝山校区、2 - 延长校区、3 - 嘉定校区、4 - 新闸路校区）
    * address：具体地址
    
    
## 常见问题
### mac无法验证此app不包含恶意软件
```
sudo xattr -rd com.apple.quarantine 
```

### 浏览器与驱动的版本对不齐
selenium.common.exceptions.SessionNotCreatedException: Message: session not created: This version of ChromeDriver only supports Chrome version xx
Current browser version is xx.x.xxxx.xxx with binary path /Applications/Google Chrome.app/Contents/MacOS/Google Chrome

```
# 1. 更新repo
cd <shu-selfreport文件夹>
git checkout . -f
git pull

# 2. 更新浏览器到最新版本
```
