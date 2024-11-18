# coding=utf-8
'''
Author: sanford courageux_san@wechat.com
Date: 2024-11-17 23:04:43
LastEditors: sanford courageux_san@wechat.com
LastEditTime: 2024-11-18 22:15:19
FilePath: /web3_script/pipe-network/pipe_network.py
Description: 
'''
import sys
import json
import logging
import aiohttp
import asyncio
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler
from typing import Optional, Dict, List



load_dotenv()
sleep_time = 300
base_url = 'https://pipe-network-backend.pipecanary.workers.dev/api'
login_url = f'{base_url}/login'
points_url = f'{base_url}/points'
nodes_url = f'{base_url}/nodes'


def read_proxy_from_file(proxy_file: str) -> List[str]:
    """从文件中读取代理配置"""
    proxys = []
    try:
        with open(proxy_file, 'r') as f:
            proxy = f.readlines()
            for line in proxy:
                proxys.append(line.strip())
    except FileNotFoundError:
        logger.warning(f"代理配置文件 {proxy_file} 不存在")
    except Exception as e:
        logger.error(f"读取代理配置文件失败: {e}")
    logger.info(f"从{proxy_file}读取到代理: {len(proxys)}个")
    return proxys

def read_accounts_from_file(accounts_file: str) -> List[Dict[str, str]]:
    """从文件中读取账号配置"""
    accounts = []
    try:
        with open(accounts_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    username, password = line.split(':')
                    accounts.append({
                        'username': username.strip(),
                        'password': password.strip()
                    })
    except FileNotFoundError:
        logger.warning(f"账号配置文件 {accounts_file} 不存在")
    except Exception as e:
        logger.error(f"读取账号配置文件失败: {e}")
    logger.info(f"从{accounts_file}读取到账号: {len(accounts)}个")
    return accounts

def setup_logging():
    logger = logging.getLogger('pipe_network')
    logger.setLevel(logging.INFO)
    
    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    
    # 文件处理器
    file_handler = RotatingFileHandler(
        'pipe_network.log',
        maxBytes=1024*1024,  # 1MB
        backupCount=5
    )
    file_handler.setLevel(logging.INFO)
    
    # 设置日志格式
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

logger = setup_logging()

async def create_session(proxie: Optional[str] = None) -> aiohttp.ClientSession:
    """创建异步会话"""
    session = aiohttp.ClientSession()
    return session

async def login(session: aiohttp.ClientSession, username: str, password: str, proxie: str) -> Optional[Dict]:
    """异步登录"""
    session.headers.update({
        "accept": "*/*",
        "accept-encoding": "utf-8",
        "accept-language": "zh-CN,zh;q=0.9",
        "content-type": "application/json",
        "origin": "chrome-extension://gelgmmdfajpefjbiaedgjkpekijhkgbe",
        "priority": "u=1, i",
        "sec-ch-ua": '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "none",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
    })
    
    login_data = {
        "email": username,
        "password": password
    }
    
    try:
        proxy = None if proxie == "None" else proxie
        async with session.post(login_url, json=login_data, proxy=proxy) as response:
            response.raise_for_status()
            text = await response.text()
            return json.loads(text)
    except Exception as e:
        logger.error(f"登录失败: {e}")
        return None

async def get_points(session: aiohttp.ClientSession, proxie: str) -> Optional[Dict]:
    """异步获取积分"""
    session.headers.update({
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9",
        "priority": "u=1, i",
        "sec-ch-ua": '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "none",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
    })
    
    try:
        proxy = None if proxie == "None" else proxie
        async with session.get(points_url, proxy=proxy) as response:
            response.raise_for_status()
            text = await response.text()
            print(f"积分响应: {text}")
            return json.loads(text)
    except Exception as e:
        logger.error(f"获取积分失败: {e}")
        return None

async def get_nodes(session: aiohttp.ClientSession, proxie: str) -> Optional[Dict]:
    """异步获取节点"""
    session.headers.update({
        "accept": "*/*",
        "accept-encoding": "utf-8",
        "accept-language": "zh-CN,zh;q=0.9",
        "priority": "u=1, i",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "none",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
    })
    
    try:
        proxy = None if proxie == "None" else proxie
        async with session.get(nodes_url, proxy=proxy) as response:
            response.raise_for_status()
            text = await response.text()
            print(f"节点响应: {text}")
            return json.loads(text)
    except Exception as e:
        logger.error(f"获取节点失败: {e}")
        return None

async def pin(session: aiohttp.ClientSession, url, proxie: str):
    try:
        proxy = None if proxie == "None" else proxie
        async with session.get(f'http://{url}', proxy=proxy) as response:
            response.raise_for_status()
            return "online"
    except Exception as e:
        return "offline"

async def test_node(session: aiohttp.ClientSession, proxie: str, node_id: str, ip: str, status: str) -> Optional[Dict]:
    """异步测试节点"""
    session.headers.update({
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9",
        "content-type": "application/json",
        "origin": "chrome-extension://gelgmmdfajpefjbiaedgjkpekijhkgbe",
        "priority": "u=1, i",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "none",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
    })
    
    test_url = f'{base_url}/test'
    try:
        latency = 6 if status == "online" else -1
        test_data = {
            "node_id": node_id,
            "ip": ip,
            "latency": latency,
            "status": status
        }
        proxy = None if proxie == "None" else proxie
        async with session.post(test_url, json=test_data, proxy=proxy) as response:
            response.raise_for_status()
            text = await response.text()
            print(f"测试节点响应: {text}")
            return json.loads(text)
    except Exception as e:
        logger.error(f"测试节点失败: {e}")
        return None

async def process_single_account_proxy(account: Dict[str, str], proxie: str) -> Dict:
    """处理单个账号在单个代理上的所有请求"""
    async with await create_session(proxie) as session:
        try:
            login_result = await login(session, account['username'], account['password'], proxie=proxie)
            if not login_result:
                logger.error(f"账号 {account['username']} 在代理 {proxie} 上登录失败")
                return
            
            if 'token' not in login_result:
                logger.error(f"账号 {account['username']} 登录响应中没有token: {login_result}")
                return
            
            token = login_result['token']
            session.headers.update({"authorization": f"Bearer {token}"})
            await asyncio.sleep(2)
            
            points = await get_points(session, proxie)
            if points:
                logger.info(f"账号 {account['username']} 在代理 {proxie} 上处理成功, points: {points}")
            else:
                logger.error(f"账号 {account['username']} 获取积分失败")

            await asyncio.sleep(2)

            while True:
                nodes = await get_nodes(session, proxie)
                if nodes:
                    logger.info(f"账号 {account['username']} 在代理 {proxie} 获取nodes: {len(nodes)}个")
                else:
                    logger.error(f"账号 {account['username']} 获取节点失败")

                for node in nodes:
                    status = await pin(session, node['ip'], proxie)
                    await asyncio.sleep(1)
                    await test_node(session, proxie, node['node_id'], node['ip'], status)
                    await asyncio.sleep(1)

                await asyncio.sleep(sleep_time)

        except Exception as e:
            logger.error(f"账号 {account['username']} 在代理 {proxie} 上处理失败: {e}")

async def main_test():
    logger.info("开始运行pipe_network脚本")

    proxys = read_proxy_from_file('proxie.txt')
    accounts = read_accounts_from_file('accounts.txt')

    await process_single_account_proxy(
        {"username": accounts[0]['username'], "password": accounts[0]['password']}, 
        proxys[0]
    )

async def main():
    """主异步函数"""
    logger.info("开始运行pipe_network脚本")

    proxys = read_proxy_from_file('proxie.txt')
    accounts = read_accounts_from_file('accounts.txt')

    tasks = [
        process_single_account_proxy(account, proxy)
        for account in accounts
        for proxy in proxys
    ]
    
    await asyncio.gather(*tasks, return_exceptions=True)
    
if __name__ == "__main__":
    try:    
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("脚本被用户中断")

