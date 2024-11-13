import json
import os
import time
import uuid
import asyncio
import aiohttp
import aiofiles
from aiohttp import ClientSession
from aiohttp_socks import ProxyConnector, ProxyType
from termcolor import colored
from dotenv import load_dotenv
load_dotenv()





async def ask_question(prompt):
    return input(prompt)

async def coday(url, method, payload_data=None, proxy=None, headers=None):
    try:
        connector = None
        if proxy:
            if proxy.startswith("http://") or proxy.startswith("https://"):
                connector = aiohttp.TCPConnector()
            elif proxy.startswith("socks5://"):
                connector = ProxyConnector.from_url(proxy)
            else:
                print(f"未知的代理类型: {proxy}")
                return None

        async with ClientSession(connector=connector) as session:
            async with session.request(method, url, json=payload_data, headers=headers) as response:
                try:
                    return await response.json()
                except aiohttp.ContentTypeError:
                    text = await response.text()
                    print(f'无法解析响应为JSON, 代理: {proxy}, 响应内容: {text}')
                    return None
    except Exception as e:
        print(f'代理出错: {proxy}, 错误: {e}')

def generate_browser_id():
    return str(uuid.uuid4())

async def load_browser_ids(file_path):
    if os.path.exists(file_path):
        async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
            content = await f.read()
            try:
                return json.loads(content)
            except json.JSONDecodeError as e:
                print(f'加载浏览器ID时解析JSON出错: {e}')
                return {}
    return {}

async def save_browser_ids(file_path, browser_ids):
    async with aiofiles.open(file_path, 'w', encoding='utf-8') as f:
        await f.write(json.dumps(browser_ids, ensure_ascii=False, indent=2))
    print('已将浏览器ID保存到文件。')

async def get_browser_id(proxy, file_path):
    browser_ids = await load_browser_ids(file_path)
    if proxy in browser_ids:
        print(f'为代理 {proxy} 使用现有的 browser_id')
        return browser_ids[proxy]
    else:
        new_browser_id = generate_browser_id()
        browser_ids[proxy] = new_browser_id
        await save_browser_ids(file_path, browser_ids)
        print(f'为代理 {proxy} 生成新 browser_id: {new_browser_id}')
        return new_browser_id

def get_current_timestamp():
    return int(time.time())

async def ping_proxy(proxy, browser_id, uid, headers, file_path):
    timestamp = get_current_timestamp()
    ping_payload = {"uid": uid, "browser_id": browser_id, "timestamp": timestamp, "version": "1.0.0"}

    while True:
        try:
            ping_response = await coday('https://api.aigaea.net/api/network/ping', 'POST', ping_payload, proxy, headers)
            if ping_response:
                print(f'代理 {proxy} 的 ping 成功:', ping_response)

                if ping_response.get('data') and ping_response['data'].get('score', 100) < 50:
                    print(f'代理 {proxy} 的得分低于 50，正在重新认证...')
                    await handle_auth_and_ping(proxy, headers, file_path)
                    break
            else:
                print(f'代理 {proxy} 的 ping 失败: 无法获取有效响应')
        except Exception as e:
            print(f'代理 {proxy} 的 ping 失败:', e)
        await asyncio.sleep(60)  # 等待10分钟后再执行下一个 ping

async def handle_auth_and_ping(proxy, headers, file_path):
    payload = {}
    auth_response = await coday("https://api.aigaea.net/api/auth/session", 'POST', payload, proxy, headers)

    if auth_response and auth_response.get('data'):
        uid = auth_response['data']['uid']
        browser_id = await get_browser_id(proxy, file_path)
        print(f'代理 {proxy} 验证成功，uid: {uid}, browser_id: {browser_id}')

        # 开始 ping
        await ping_proxy(proxy, browser_id, uid, headers, file_path)
    else:
        print(f'代理 {proxy} 的认证失败')

async def main():
    # 添加 logo 输出
    banner = """

               ╔═╗╔═╦╗─╔╦═══╦═══╦═══╦═══╗
               ╚╗╚╝╔╣║─║║╔══╣╔═╗║╔═╗║╔═╗║
               ─╚╗╔╝║║─║║╚══╣║─╚╣║─║║║─║║
               ─╔╝╚╗║║─║║╔══╣║╔═╣╚═╝║║─║║
               ╔╝╔╗╚╣╚═╝║╚══╣╚╩═║╔═╗║╚═╝║
               ╚═╝╚═╩═══╩═══╩═══╩╝─╚╩═══╝
               我的gihub：github.com/Gzgod
               我的推特：推特雪糕战神@Hy78516012       
                
    """
    print(banner)

    # try:
    #     async with aiofiles.open('id.txt', 'r', encoding='utf-8') as f:
    #         access_token = await f.read()
    #         access_token = access_token.strip()  # 去除可能的空白字符
    # except FileNotFoundError:
    #     print("未找到 id.txt 文件")
    #     return
    # except Exception as e:
    #     print(f"读取 id.txt 文件时出错: {e}")
    #     return
    access_token = os.getenv("GAEA_TOKEN")
    
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}',
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
    }

    browser_id_file_path = os.path.join(os.path.dirname(__file__), 'browser_ids.json')

    try:
        async with aiofiles.open('Proxies/proxies.txt', 'r', encoding='utf-8') as f:
            proxy_list = await f.read()
        proxies = [proxy.strip() for proxy in proxy_list.split('\n') if proxy.strip()]

        if not proxies:
            print("在 proxy.txt 中未找到代理")
        else:
            tasks = []
            for proxy in proxies:
                tasks.append(handle_auth_and_ping(proxy, headers, browser_id_file_path))
            await asyncio.gather(*tasks)
    except FileNotFoundError:
        print("未找到 proxy.txt 文件")
    except Exception as e:
        print(f"读取 proxy.txt 文件时出错: {e}")

if __name__ == "__main__":
    asyncio.run(main())