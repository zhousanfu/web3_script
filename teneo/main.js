const WebSocket = require('ws');
const { promisify } = require('util');
const fs = require('fs');
const readline = require('readline');
const axios = require('axios');
const HttpsProxyAgent = require('https-proxy-agent');
const chalk = require('chalk');


console.log(chalk.cyan.bold(`                 ╔═╗╔═╦╗─╔╦═══╦═══╦═══╦═══╗`));
console.log(chalk.cyan.bold(`                 ╚╗╚╝╔╣║─║║╔══╣╔═╗║╔═╗║╔═╗║`));
console.log(chalk.cyan.bold(`                 ─╚╗╔╝║║─║║╚══╣║─╚╣║─║║║─║║`));
console.log(chalk.cyan.bold(`                 ─╔╝╚╗║║─║║╔══╣║╔═╣╚═╝║║─║║`));
console.log(chalk.cyan.bold(`                 ╔╝╔╗╚╣╚═╝║╚══╣╚╩═║╔═╗║╚═╝║`));
console.log(chalk.cyan.bold(`                 ╚═╝╚═╩═══╩═══╩═══╩╝─╚╩═══╝`));
console.log(chalk.cyan.bold(`                 运行Teneo Node BETA CLI版本                 `));
console.log(chalk.cyan.bold(`                 推特用户雪糕战神 @Hy78516012                `));

let socket = null;
let pingInterval;
let countdownInterval;
let potentialPoints = 0;
let countdown = "计算中...";
let pointsTotal = 0;
let pointsToday = 0;

const authorization = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imlra25uZ3JneHV4Z2pocGxicGV5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjU0MzgxNTAsImV4cCI6MjA0MTAxNDE1MH0.DRAvf8nH1ojnJBc3rD_Nw6t1AV8X_g6gmY_HByG2Mag";
const apikey = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imlra25uZ3JneHV4Z2pocGxicGV5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjU0MzgxNTAsImV4cCI6MjA0MTAxNDE1MH0.DRAvf8nH1ojnJBc3rD_Nw6t1AV8X_g6gmY_HByG2Mag";

const readFileAsync = promisify(fs.readFile);
const writeFileAsync = promisify(fs.writeFile);

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

async function getLocalStorage() {
  try {
    const data = await readFileAsync('localStorage.json', 'utf8');
    return JSON.parse(data);
  } catch (error) {
    return {};
  }
}

async function setLocalStorage(data) {
  const currentData = await getLocalStorage();
  const newData = { ...currentData, ...data };
  await writeFileAsync('localStorage.json', JSON.stringify(newData));
}

async function connectWebSocket(userId, proxy) {
  if (socket) return;
  const version = "v0.2";
  const url = "wss://secure.ws.teneo.pro";
  const wsUrl = `${url}/websocket?userId=${encodeURIComponent(userId)}&version=${encodeURIComponent(version)}`;

  const options = {};
  if (proxy) {
    options.agent = new HttpsProxyAgent(proxy);
  }

  socket = new WebSocket(wsUrl, options);

  socket.onopen = async () => {
    const connectionTime = new Date().toISOString();
    await setLocalStorage({ lastUpdated: connectionTime });
    console.log("WebSocket 连接成功，时间：", connectionTime);
    startPinging();
    startCountdownAndPoints();
  };

  socket.onmessage = async (event) => {
    const data = JSON.parse(event.data);
    console.log("从WebSocket接收到消息：", data);
    if (data.pointsTotal !== undefined && data.pointsToday !== undefined) {
      const lastUpdated = new Date().toISOString();
      await setLocalStorage({
        lastUpdated: lastUpdated,
        pointsTotal: data.pointsTotal,
        pointsToday: data.pointsToday,
      });
      pointsTotal = data.pointsTotal;
      pointsToday = data.pointsToday;
    }
  };

  socket.onclose = () => {
    socket = null;
    console.log("WebSocket 断开连接");
    stopPinging();
  };

  socket.onerror = (error) => {
    console.error("WebSocket 错误：", error);
  };
}

function disconnectWebSocket() {
  if (socket) {
    socket.close();
    socket = null;
    stopPinging();
  }
}

function startPinging() {
  stopPinging();
  pingInterval = setInterval(async () => {
    if (socket && socket.readyState === WebSocket.OPEN) {
      socket.send(JSON.stringify({ type: "PING" }));
      await setLocalStorage({ lastPingDate: new Date().toISOString() });
    }
  }, 10000);
}

function stopPinging() {
  if (pingInterval) {
    clearInterval(pingInterval);
    pingInterval = null;
  }
}

process.on('SIGINT', () => {
  console.log('收到 SIGINT. 停止 pinging...');
  stopPinging();
  disconnectWebSocket();
  process.exit(0);
});

function startCountdownAndPoints() {
  clearInterval(countdownInterval);
  updateCountdownAndPoints();
  countdownInterval = setInterval(updateCountdownAndPoints, 1000);
}

async function updateCountdownAndPoints() {
  const { lastUpdated } = await getLocalStorage();
  if (lastUpdated) {
    const nextHeartbeat = new Date(lastUpdated);
    nextHeartbeat.setMinutes(nextHeartbeat.getMinutes() + 15);
    const now = new Date();
    const diff = nextHeartbeat.getTime() - now.getTime();

    if (diff > 0) {
      const minutes = Math.floor(diff / 60000);
      const seconds = Math.floor((diff % 60000) / 1000);
      countdown = `${minutes}分 ${seconds}秒`;

      const maxPoints = 25;
      const timeElapsed = now.getTime() - new Date(lastUpdated).getTime();
      const timeElapsedMinutes = timeElapsed / (60 * 1000);
      let newPoints = Math.min(maxPoints, (timeElapsedMinutes / 15) * maxPoints);
      newPoints = parseFloat(newPoints.toFixed(2));

      if (Math.random() < 0.1) {
        const bonus = Math.random() * 2;
        newPoints = Math.min(maxPoints, newPoints + bonus);
        newPoints = parseFloat(newPoints.toFixed(2));
      }

      potentialPoints = newPoints;
    } else {
      countdown = "计算中...";
      potentialPoints = 25;
    }
  } else {
    countdown = "计算中...";
    potentialPoints = 0;
  }

  await setLocalStorage({ potentialPoints, countdown });
}
async function getUserId(proxy) {
  const loginUrl = "https://ikknngrgxuxgjhplbpey.supabase.co/auth/v1/token?grant_type=password";
  
  rl.question('电子邮件: ', (email) => {
    rl.question('密码: ', async (password) => {
      try {
        const response = await axios.post(loginUrl, {
          email: email,
          password: password
        }, {
          headers: {
            'Authorization': authorization,
            'apikey': apikey
          }
        });

        const userId = response.data.user.id;
        console.log('用户ID:', userId);

        const profileUrl = `https://ikknngrgxuxgjhplbpey.supabase.co/rest/v1/profiles?select=personal_code&id=eq.${userId}`;
        const profileResponse = await axios.get(profileUrl, {
          headers: {
            'Authorization': authorization,
            'apikey': apikey
          }
        });

        console.log('个人资料数据:', profileResponse.data);
        await setLocalStorage({ userId });
        await startCountdownAndPoints();
        await connectWebSocket(userId, proxy);
      } catch (error) {
        console.error('错误:', error.response ? error.response.data : error.message);
      } finally {
        rl.close();
      }
    });
  });
}

async function registerUser() {
  const signupUrl = "https://ikknngrgxuxgjhplbpey.supabase.co/auth/v1/signup";

  rl.question('请输入您的电子邮件: ', (email) => {
    rl.question('请输入您的密码: ', (password) => {
      rl.question('请输入邀请者代码，可以填我的KWgDK送2500积分: ', async (invitedBy) => {
        try {
          const response = await axios.post(signupUrl, {
            email: email,
            password: password,
            data: { invited_by: "KGWku" },
            gotrue_meta_security: {},
            code_challenge: null,
            code_challenge_method: null
          },{
          headers: {
            'Authorization': authorization,
            'apikey': apikey
          }
        });

          console.log('注册成功，请到您的邮箱里确认您的电子邮件：', email);
        } catch (error) {
          console.error('注册期间出错:', error.response ? error.response.data : error.message);
        } finally {
          rl.close();
        }
      });
    });
  });
}

async function main() {
  const localStorageData = await getLocalStorage();
  let userId = localStorageData.userId;

  rl.question('您是否要使用代理？（使用输入y/不使用输入n）: ', async (useProxy) => {
    let proxy = null;
    if (useProxy.toLowerCase() === 'y') {
      proxy = await new Promise((resolve) => {
        rl.question('请输入您的代理URL（例如：http://username:password@host:port）: ', (inputProxy) => {
          resolve(inputProxy);
        });
      });
    }

    if (!userId) {
      rl.question('未找到用户ID。您想要：\n1. 注册账户\n2. 登录您的账户\n3. 手动输入用户ID\n选择一个选项: ', async (option) => {
        switch (option) {
          case '1':
            await registerUser();
            break;
          case '2':
            await getUserId(proxy);
            break;
          case '3':
            rl.question('请输入您的用户ID: ', async (inputUserId) => {
              userId = inputUserId;
              await setLocalStorage({ userId });
              await startCountdownAndPoints();
              await connectWebSocket(userId, proxy);
              rl.close();
            });
            break;
          default:
            console.log('无效选项。退出...');
            process.exit(0);
        }
      });
    } else {
      rl.question('菜单：\n1. 注销\n2. 开始运行节点\n选择一个选项: ', async (option) => {
        switch (option) {
          case '1':
            fs.unlink('localStorage.json', (err) => {
              if (err) throw err;
            });
            console.log('注销成功。');
            process.exit(0);
            break;
          case '2':
            await startCountdownAndPoints();
            await connectWebSocket(userId, proxy);
            break;
          default:
            console.log('无效选项。退出...');
            process.exit(0);
        }
      });
    }
  });
}

main();
