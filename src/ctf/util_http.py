from .util_basic import *


def parseheaders(headers):
    headers = b2s(headers)
    out = {}
    for line in headers.split('\n'):
        line = line.rstrip('\r')
        if len(line) == 0: continue
        name, value = line.split(': ', 2)
        out[name] = value
    return out

if isinstalled('requests'):
    import requests
    def getsession(proxy=False, proxyto='127.0.0.1:8080'):
        proxies = {"http": f"http://{proxyto}", "https": f"http://{proxyto}"}
        s = requests.Session()
        if proxy:
            s.proxies = proxies
            s.verify = False
        return s


if isinstalled('httpx'):
    import httpx
    def getclient(proxy=False, proxyto='127.0.0.1:8080'):
        if proxy:
            return httpx.Client(proxy=f'http://{proxyto}', verify=False, timeout=None)
        else:
            return httpx.Client()


def _http():
    if isinstalled('httpx'):
        return getclient()
    elif isinstalled('requests'):
        return getsession()
    raise Exception('install httpx or requests')

def getwebhook(body="", cors=False, content_type='text/html', status_code=200, onlytoken=False):
    r = _http().post("https://webhook.site/token", json={"default_content": body, "cors": cors, "default_content_type": content_type, "default_status":status_code})
    return r.json()['uuid'] if onlytoken else 'https://webhook.site/'+r.json()['uuid']
def webhook_ui(token):
    token = token.replace('https://webhook.site/','')
    return f'https://webhook.site/#!/view/{token}'
def webhook_results(token):
    token = token.replace('https://webhook.site/','')
    r = _http().get(f'https://webhook.site/token/{token}/requests?sorting=newest')
    return r.json()['data']

