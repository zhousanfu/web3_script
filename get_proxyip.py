import requests
import threading
import parsel
import random
import time

proxy_path = 'proxy.txt'
valid_path = 'valid.txt'
proxyList = open(proxy_path, encoding='utf-8')
validList= open(valid_path, encoding='utf-8')
# 控制线程
lock = threading.Lock()

# UA池
user_agents = [
		'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60',
		'Opera/8.0 (Windows NT 5.1; U; en)',
		'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
		'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50',
		'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
		'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
		'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2 ',
		'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
		'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
		'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16',
		'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
		'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
		'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11',
		'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
		'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
		'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
		'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0) ',
	]

def getProxy():
    starttime = time.time()
    # 爬取云代理ip
    # http://www.ip3366.net/free
    getCloudProxy()

    # 爬取98代理
    # https: // www.89ip.cn / index_10.html
    get89Proxy()

    # 爬取快代理
    # https://www.kuaidaili.com/free/inha/1/
    # https://www.kuaidaili.com/free/intr/1/
    getQuickProxy()

    endtime = time.time()
    print(f"爬取代理花费{endtime-starttime}s")

def getCloudProxy():
    print("爬取云代理IP中--------")
    num = 0
    import time
    # 打开我们创建的txt文件
    proxyFile = open('proxy.txt', 'a')
    for page in range(1, 8):
        for stype in range(1, 3):
            time.sleep(random.randint(1, 3))
            print(f"正在抓取{stype}的第{page}页数据")
            # 数据地址
            url = f'http://www.ip3366.net/free/?stype={stype}&page={page}'
            # 设置随机请求头
            headers = {
                'User-Agent': random.choice(user_agents)}
            # 发送请求
            response = requests.get(url=url, headers=headers)
            # 自适应编码
            response.encoding = response.apparent_encoding
            html_data = response.text
            # 解析数据
            selector = parsel.Selector(html_data)
            trs = selector.xpath('//table/tbody/tr')
            for tr in trs:
                ip = tr.xpath('./td[1]/text()').get()  # ip
                port = tr.xpath('./td[2]/text()').get()  # 端口
                protocol = tr.xpath('./td[4]/text()').get()  # 协议

                # 将获取到的数据按照规定格式写入txt文本中1
                proxyFile.write('%s|%s|%s\n' % (ip, port, protocol))
                num += 1
    print(f"爬取云代理IP{num}条")

def getQuickProxy():
    print("爬取快代理中------")
    num = 0
    import time
    # 打开我们创建的txt文件
    proxyFile = open('proxy.txt', 'a')
    for page in range(1, 3):
        for type in ['inha', 'intr']:

            time.sleep(random.randint(1, 3))
            print(f"正在抓取类型{type}第{page}页数据")
            # 数据地址
            url = f'https://www.kuaidaili.com/free/{type}/{page}/'
            # 设置随机请求头
            headers = {
                'User-Agent': random.choice(user_agents)
            }
            # 发送请求
            response = requests.get(url=url, headers=headers)
            # 自适应编码
            response.encoding = response.apparent_encoding
            html_data = response.text
            # 解析数据
            selector = parsel.Selector(html_data)
            trs = selector.xpath('//table/tbody/tr')
            for tr in trs:
                ip = tr.xpath('./td[1]/text()').get().strip()  # ip
                port = tr.xpath('./td[2]/text()').get().strip()  # 端口
                protocol = tr.xpath('./td[4]/text()').get().strip()  #协议
                # 将获取到的数据按照规定格式写入txt文本中1
                proxyFile.write('%s|%s|%s\n' % (ip, port, protocol))
                num += 1
    print(f"爬取快代理IP{num}条")

def get89Proxy():
    print("爬取89代理IP中--------")
    num = 0
    import time
    # 打开我们创建的txt文件
    proxyFile = open('proxy.txt', 'a')
    for page in range(1, 156):
        time.sleep(random.randint(1, 3))
        print(f"正在抓取第{page}页数据")
        # 数据地址
        url = f'https://www.89ip.cn/index_{page}.html'
        # 设置随机请求头
        headers = {
            'User-Agent': random.choice(user_agents)
        }
        # 发送请求
        response = requests.get(url=url, headers=headers)
        # 自适应编码
        response.encoding = response.apparent_encoding
        html_data = response.text
        # 解析数据
        selector = parsel.Selector(html_data)
        trs = selector.xpath('//table/tbody/tr')
        for tr in trs:
            ip = tr.xpath('./td[1]/text()').get().strip()  # ip
            port = tr.xpath('./td[2]/text()').get().strip()  # 端口
            protocol = 'HTTP' # 默认协议HTTP
            # 将获取到的数据按照规定格式写入txt文本中1
            proxyFile.write('%s|%s|%s\n' % (ip, port, protocol))
            num += 1
    print(f"爬取89代理IP{num}条")

def verifyProxyList():
    '''
    验证ip有效性并存入valid.txt
    :return:
    '''

    valid = open(valid_path, 'w', encoding='utf-8')
    while True:
        lock.acquire()
        # 读取存放ip的文件
        ipinfo = proxyList.readline().strip()
        lock.release()
        # 读到最后一行
        if len(ipinfo) == 0:
            break
            
        line = ipinfo.strip().split('|')
        ip = line[0]
        port = line[1]
        realip = ip.strip() + ':' + port.strip()
        if line[2] == 'HTTP':
            proxy = {'http': realip}
            realip_h = 'http://' + realip
        elif line[2] == 'HTTPS':
            proxy = {'https': realip}
            realip_h = 'http://' + realip
        code = verifyProxy(proxy)
        # 验证通过
        if code == 200:
            lock.acquire()
            print("---Success:" + realip_h)
            valid.write(realip_h + "\n")
            lock.release()
        else:
            pass
            # print("---Failure:" + ip + ":" + port)

def verifyProxy(proxy):
    '''
    验证代理的有效性
    '''
    # 设置随机请求头
    headers = {'User-Agent': random.choice(user_agents)}
    url = "http://www.baidu.com"
    try:
        code = requests.get(url=url, proxies=proxy, timeout=2, headers = headers).status_code
        return code
    except Exception as e:
        return e

def useProxy():
    lock.acquire()

    ips = []
    # 获取可用ip池
    # 获取IP列表
    valid = open(validList, 'r', encoding='utf-8')
    while True:
        # 读取存放ip的文件
        ipinfo = valid.readline().strip()
        # 读到最后一行
        if len(ipinfo) == 0:
            break
        line = ipinfo.strip().split('|')
        ip = line[0]
        port = line[1]
        realip = ip + ':' + port
        ips.append(realip)

    # 要抓取的目标网站地址
    targetUrl = "https://news.qq.com/"
    for i in range(10):
        # 随机使用ip爬虫
        proxyip = random.choice(ips)
        print(proxyip)
        try:
            response = requests.get(url=targetUrl, proxies={"http": proxyip, "https": proxyip},
                                    verify=False, timeout=15)
        except Exception as e:
            continue
        # 自适应编码
        response.encoding = response.apparent_encoding
        html_data = response.text
        print(html_data)
    # 用完了
    lock.release()

if __name__ == '__main__':
    # 获取代理IP 清空代理列表和有效代理列表
    proxy = open('proxy.txt', 'w')
    proxy.write("")
    proxy.close()
    valid = open('valid.txt', 'w')
    valid.write("")
    valid.close()
    getProxy()

    # 验证ip有效性
    starttime = time.time()
    verifyProxyList()
    endtime = time.time()
    print(f"验证代理IP花费时间{endtime-starttime}s")