# shu-selfreport based on web browser

## 使用方法


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
