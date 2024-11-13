Multi-threaded network pinger for Aigaea using multiple proxies. This tool allows you to run concurrent ping requests through different proxies using HTTP, SOCKS4, or SOCKS5 protocols.

Link register : [Here](https://app.aigaea.net/register?ref=gaBv4hsbaxZuD1)

**Features**

- 🚀 Multi-threading support - each proxy runs in its own thread
- 🔄 Support for multiple proxy protocols (HTTP, SOCKS4, SOCKS5)
- 📝 Easy proxy management through text file
- 🔑 Support for authenticated and non-authenticated proxies
- 📊 Detailed logging system
- ⏰ Dynamic sleep intervals based on server response
- 🛡️ Robust error handling and retry mechanism

**Prerequisites**

- Python 3.7 or higher
- pip (Python package installer)

**Installation**

Install the required packages

```
cd aigae
pip install -r requirements.txt
```

**Configuration**

Create a `.env` file in the project root directory with your credentials:

```
GAEA_TOKEN = 'ey**************'
GAEA_UID = '10**************'
```

Create a `proxies.txt` file with your proxies. Each proxy should be on a new line.

**How to get Token & UID**

1. Open devtoosl -> Console
2. Copy UID To .env
3. Execute this command to getting token copy into .env

```
localStorage.getItem("gaea_token")
```

**Proxy Format Examples**

```
# With scheme and authentication
http://ip:port@username:password
socks5://ip:port@username:password
socks4://ip:port@username:password

```

**Usage**

Run the script using Python:

```python
python aigaea/gaea.py
```