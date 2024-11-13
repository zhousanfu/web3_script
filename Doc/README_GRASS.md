

<!--
 * @Author: sanford courageux_san@wechat.com
 * @Date: 2024-11-06 22:23:42
 * @LastEditors: sanford courageux_san@wechat.com
 * @LastEditTime: 2024-11-11 23:23:48
 * @FilePath: /web3_script/doc/README_GRASS.md
 * @Description: 
-->
 # Node.js(2.0x) 版本 @
## 功能
✅ 支持多个 UID

✅ 支持自定义代理

## 安装步骤
将此仓库克隆到你的本地环境：

进入项目目录：
 ```bash
cd getgrass-bot
 ```
## 安装所需依赖项：
 ```bash
npm install
 ```

## 使用说明
获取用户 ID：

登录到 GetGrass 网站

打开浏览器开发者工具（通常按 F12 或右键选择“检查”）。

切换到“控制台”选项卡。

输入以下命令并按回车：

```bash
localStorage.getItem('userId');
 ```
复制返回的值，这就是你的用户 ID。

创建用户 ID 文件：

在项目目录中创建一个名为 uid.txt 的文件，每行写一个用户 ID，例如：

```bash
123123213
12313123
```
添加代理信息：

创建一个名为 proxy.txt 的文件，并按行添加你的代理 URL，格式如下：
```bash

http://username:password@hostname:port
socks5://username:password@hostname:port
```
启动机器人：

在终端中执行以下命令运行 GetGrass-Bot：
```bash
npm start

```



# python(1.2x)版本

***
## 代理
示例格式：
```
http://host:port
socks5://host:port
http://user:password@host:port
socks5://user:password@host:port
```

## 使用方法

1.获取必要的的token :

浏览器F2 OR grass/grass_setup.py

```javascript
copy(JSON.parse(localStorage.getItem("userId")))
copy(JSON.parse(localStorage.getItem("accessToken")))
```

写入env文件中
```
GRASS_TOKEN = '***'
CRASS_USERID = '***'
```


2.运行

grass脚本
```python
grass/grass.py
```