# shu-selfreport
关键词：上海大学、健康之路、每日一报、每日两报、在校学生日报、报送历史

服务于上海大学健康之路平台(https://selfreport.shu.edu.cn)的工具。
该工具具有在校学生日报、报送历史补填功能。

PS：由于没有测试账号，非在校学生的日报功能暂无法提供，请有意愿的好心人能提供测试账号，帮助完成这项功能，本人保证绝不泄露个人信息。

## 使用方法
1. 打开config参数，填写自己的个人信息，参数解释如下：
    * operating_system：操作系统（win32、mac64、linux64）
    * student_id：学号
    * password：密码
    * campus：当天是否在校（0 - 不在校、1 - 宝山校区、2 - 延长校区、3 - 嘉定校区、4 - 新闸路校区）
    * 
    
    
## 常见问题
### 解决mac无法验证此app不包含恶意软件
```
sudo xattr -rd com.apple.quarantine 
```
