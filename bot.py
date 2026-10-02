import requests, websocket, json, os, time
PAT_TOKEN = os.getenv("PAT_TOKEN", "")
APP_ID = os.getenv("APP_ID", "1089")
print("=== SAVHEX BOT STARTING ===")
print(f"Token: {PAT_TOKEN[:10]}...")
headers = {"Authorization": f"Bearer {PAT_TOKEN}", "Deriv-App-ID": APP_ID}
try:
    print("1. Getting account ID...")
    r = requests.get("https://api.derivws.com/trading/v1/options/accounts", headers=headers)
    print(r.text[:500])
    data = r.json()
    account_id = data['data'][0]['id']
    print(f"Account: {account_id}")
    print("2. Getting WS URL...")
    r2 = requests.post(f"https://api.derivws.com/trading/v1/options/accounts/{account_id}/otp", headers=headers)
    print(r2.text[:500])
    ws_url = r2.json()['data']['url']
    print(f"WS: {ws_url[:80]}...")
    def on_open(ws):
        print("✅ SAVHEX LIVE 24/7 CONNECTED!")
        ws.send(json.dumps({"ticks": "R_75"}))
    def on_message(ws, msg):
        data = json.loads(msg)
        if 'tick' in data:
            print(f"TICK {data['tick']['quote']}")
        else:
            print(msg[:200])
    def on_error(ws, err):
        print(f"Error: {err}")
    ws = websocket.WebSocketApp(ws_url, on_open=on_open, on_message=on_message, on_error=on_error)
    ws.run_forever(ping_interval=30, ping_timeout=10)
except Exception as e:
    print(f"CRASH: {e}")
    time.sleep(5)
