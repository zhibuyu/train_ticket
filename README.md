# train_ticket
###### 一年一度的天朝大迁徙就要开始了，但是票还是依然的难抢，抢票软件给了钱也抢不到票，人在囧途；为此，博主编写了一个12306抢票脚本，抢票再也不用愁
博客地址：[https://blog.csdn.net/u010123643/article/details/85272481](https://blog.csdn.net/u010123643/article/details/85272481)
## 运行代码
python3

## 系统运行环境
windows、mac、linux

## 使用工具
**chromedriver**</br>

<font color=#0099ff size=5 face="黑体">请选择与自己Chrome浏览器对应的版本</font>   这个很重要</br>
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

#### 需注意点
config.ini文件 路径信息 executable_path的选择，按照注释所说选择mac的还是windows的路径(如需添加linx,可以仿照mac的编写)
请确定你Chrome版本与chromedriver对应的版本，chromedriver下载版本对应在下载（[http://chromedriver.storage.googleapis.com/index.html](http://chromedriver.storage.googleapis.com/index.html)）时可以通过文件notes.txt查看不同版本的chromedriver对应的Chrome版本

根据下载地址打开选择一个版本进入，我这以2.45为例，便可以进入下图所示界面，点击箭头指向文件notes.txt
<img src="https://img-blog.csdnimg.cn/20200729153037167.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3UwMTAxMjM2NDM=,size_16,color_FFFFFF,t_70" /></br>
便可以看到下图，图中说2.45版本对应的chrome版本为70到72
<img src="https://img-blog.csdnimg.cn/20200729153109476.png" /></br>
那现在我们去查看下我们电脑安装的Chrome的版本号，点击Chrome的设置-->>关于Chrome,便可以看到下图所示截图，我这里的版本是71，则我需要下载的chromedriver版本为2.45
<img src="https://img-blog.csdnimg.cn/20200729153136590.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3UwMTAxMjM2NDM=,size_16,color_FFFFFF,t_70" /></br>
#### chromedriver下载后存放文件位置说明
windows系统的直接存放在项目同级目录下， mac系统则存放在mac文件夹下，linux系统按照mac的一样配置即可
### 运行效果
<img src="https://img-blog.csdnimg.cn/20200729152827938.gif?raw=true" /></br>

<img src="https://img-blog.csdnimg.cn/20200729152911731.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3UwMTAxMjM2NDM=,size_16,color_FFFFFF,t_70" />
哈哈哈哈哈
