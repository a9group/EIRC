from fastapi import FastAPI, Request, Header
import configparser, irc.client, ssl, requests

app = FastAPI()
config = configparser.ConfigParser()
config.read('config.ini')

irc_server = config['IRC']['server']
irc_port = int(config['IRC']['port'])
use_ssl = config['IRC'].getboolean('use_ssl')
irc_nickname = config['IRC']['nickname']
irc_channel = config['IRC']['channel']
slack_webhook = config['Slack']['webhook_url']
forward_to_slack = config['Options'].getboolean('forward_to_slack')

def send_to_irc(message):
    client = irc.client.Reactor()
    ssl_factory = irc.connection.Factory(wrapper=ssl.wrap_socket) if use_ssl else None
    conn = client.server().connect(irc_server, irc_port, irc_nickname, connect_factory=ssl_factory)
    conn.add_global_handler("welcome", lambda c, e: [c.join(irc_channel), c.privmsg(irc_channel, message), c.quit()])
    client.process_forever(timeout=5)

def send_to_slack(message):
    if forward_to_slack:
        requests.post(slack_webhook, json={"text": message})

@app.post("/webhooks/jira")
async def jira_webhook(payload: Request):
    data = await payload.json()
    message = f"[Jira] {data.get('issue', {}).get('key')} updated."
    send_to_irc(message)
    send_to_slack(message)
    return {"status": "sent"}

@app.post("/webhooks/github")
async def github_webhook(payload: Request, x_github_event: str = Header(None)):
    data = await payload.json()
    message = f"[GitHub] Event: {x_github_event}"
    send_to_irc(message)
    send_to_slack(message)
    return {"status": "sent"}