# train_ticket
###### 一年一度的天朝大迁徙就要开始了，但是票还是依然的难抢，抢票软件给了钱也抢不到票，人在囧途；为此，博主编写了一个12306抢票脚本，抢票再也不用愁
博客地址：[https://blog.csdn.net/u010123643/article/details/85272481](https://blog.csdn.net/u010123643/article/details/85272481)
## 运行代码
python3

## 系统运行环境
windows、mac、linux

## 使用工具
**chromedriver**</br>
chromedriver下载地址[https://sites.google.com/a/chromium.org/chromedriver/downloads](https://sites.google.com/a/chromium.org/chromedriver/downloads)

## 代理设置
```
PROXY = "119.101.113.139:9999"  #代理ip地址
chrome_options = Options()
chrome_options.add_argument('--proxy-server=http://%s' % PROXY)
使用代理ip访问，免费的最好不要用，12306很容易超时，可以自行购买代理ip
self.driver = Browser(driver_name=self.driver_name, executable_path=self.executable_path,chrome_options=chrome_options) 
```

## 用户信息输入
在config.ini文件中编写即可，代码无需修改

### 运行效果
<img src="https://github.com/zhibuyu/train_ticket/blob/master/show/effect.gif?raw=true" /></br>

<img src="https://github.com/zhibuyu/train_ticket/blob/master/show/successful.png?raw=true" />
