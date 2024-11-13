# coding=utf-8
'''
Author: sanford courageux_san@wechat.com
Date: 2024-11-03 11:08:22
LastEditors: sanford courageux_san@wechat.com
LastEditTime: 2024-11-13 22:39:07
FilePath: /web3_script/grass/grass.py
Description: proxy2.wynd.network: 可用的端口是80,4650,4444
'''

import os
import uuid
import json
import aiohttp
import argparse
from datetime import datetime, timezone
from fake_useragent import UserAgent
from colorama import *
from dotenv import load_dotenv, set_key
load_dotenv()



green = Fore.LIGHTGREEN_EX
red = Fore.LIGHTRED_EX
magenta = Fore.LIGHTMAGENTA_EX
white = Fore.LIGHTWHITE_EX
black = Fore.LIGHTBLACK_EX
reset = Style.RESET_ALL
yellow = Fore.LIGHTYELLOW_EX


class Grass:
    def __init__(self, userid, proxy):
        self.userid = userid
        self.proxy = proxy
        self.ses = aiohttp.ClientSession()

    def log(self, msg):
        now = datetime.now(tz=timezone.utc).isoformat(" ").split(".")[0]
        print(f"{black}[{now}] {reset}{msg}{reset}")

    @staticmethod
    async def ipinfo(proxy=None):
        async with aiohttp.ClientSession() as client:
            result = await client.get("https://api.ipify.org/", proxy=proxy)
            return await result.text()

    async def start(self):
        max_retry = 10
        retry = 1
        proxy = self.proxy
        if proxy is None:
            proxy = await Grass.ipinfo()
        browser_id = uuid.uuid5(uuid.NAMESPACE_URL, proxy)
        useragent = UserAgent().random
        headers = {
            "Host": "proxy2.wynd.network:80",
            "Connection": "Upgrade",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "User-Agent": useragent,
            "Upgrade": "websocket",
            "Origin": "chrome-extension://lkbnfiajjmbhnfledhphioinpickokdi",
            "Sec-WebSocket-Version": "13",
            "Accept-Language": "en-US,en;q=0.9,id;q=0.8",
        }
        while True:
            try:
                if retry >= max_retry:
                    self.log(f"{yellow}max retrying reacted, skip the proxy !")
                    await self.ses.close()
                    return
                async with self.ses.ws_connect(
                    "wss://proxy2.wynd.network:80/",
                    headers=headers,
                    proxy=self.proxy,
                    timeout=1000,
                    autoclose=False,
                ) as wss:
                    res = await wss.receive_json()
                    auth_id = res.get("id")
                    if auth_id is None:
                        self.log(f"{red}auth id is None")
                        return None
                    auth_data = {
                        "id": auth_id,
                        "origin_action": "AUTH",
                        "result": {
                            "browser_id": browser_id.__str__(),
                            "user_id": self.userid,
                            "user_agent": useragent,
                            "timestamp": int(datetime.now().timestamp()),
                            "device_type": "desktop",
                            "version": "4.26.2",
                            "desktop_id": "lkbnfiajjmbhnfledhphioinpickokdi",
                        },
                    }
                    await wss.send_json(auth_data)
                    self.log(f"{green}成功连接 {white}到服务器!")
                    retry = 1
                    while True:
                        ping_data = {
                            "id": uuid.uuid4().__str__(),
                            "version": "1.0.0",
                            "action": "PING",
                            "data": {},
                        }
                        await wss.send_json(ping_data)
                        self.log(f"{white}发送 {green}ping {white}到服务器 !")
                        pong_data = {"id": "F3X", "origin_action": "PONG"}
                        await wss.send_json(pong_data)
                        self.log(f"{white}发送 {magenta}pong {white}到服务器 !")
                        # you can edit the countdown in code below
                        await countdown(120)
            except KeyboardInterrupt:
                await self.ses.close()
                exit()
            except Exception as e:
                # self.log(f"{red}error : {white}{e}")
                retry += 1
                continue


async def countdown(t):
    for i in range(t, 0, -1):
        minute, seconds = divmod(i, 60)
        hour, minute = divmod(minute, 60)
        seconds = str(seconds).zfill(2)
        minute = str(minute).zfill(2)
        hour = str(hour).zfill(2)
        print(f"waiting for {hour}:{minute}:{seconds} ", flush=True, end="\r")
        await asyncio.sleep(1)


async def main():
    arg = argparse.ArgumentParser()
    arg.add_argument(
        "--proxy", "-P", default="Proxies/proxies.txt", help="Custom proxy input file "
    )
    args = arg.parse_args()
    os.system("cls" if os.name == "nt" else "clear")
    # token = os.getenv("GRASS_TOKEN_1")
    userids = os.getenv("CRASS_USERID").split(",")
    print(userids, type(userids))
    if len(userids) <= 0:
        print(f"{red}错误 : {white}请先输入您的用户ID!")
        exit()
    if not os.path.exists(args.proxy):
        print(f"{red}{args.proxy} 未找到，请确保 {args.proxy} 可用！")
        exit()
    proxies = open(args.proxy, "r").read().splitlines()
    if len(proxies) <= 0:
        proxies = [None]

    i_use = int(len(proxies)/len(userids))
    for i, u in enumerate(userids):
        tasks = [Grass(u, proxy).start() for proxy in proxies[:(i+1) * i_use]]
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    try:
        import asyncio
        if os.name == "nt":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(main())
    except KeyboardInterrupt:
        exit()