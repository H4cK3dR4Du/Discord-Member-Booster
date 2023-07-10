import httpx
import json
import time

config = json.load(open('config.json','r'))

class Solver:
    def solve_2cap(site_key,page_url):
        _2captcha_api_key = config['captcha_key']
        time_start = time.time()
        url = "https://2captcha.com/in.php?key={}&method=hcaptcha&sitekey={}&pageurl={}".format(_2captcha_api_key,site_key,page_url)
        response = httpx.get(url)
        if response.text[0:2] == 'OK':
            captcha_id = response.text[3:]
            url = "http://2captcha.com/res.php?key={}&action=get&id={}".format(_2captcha_api_key,captcha_id)
            response = httpx.get(url)
            while 'CAPCHA_NOT_READY' in response.text:
                time.sleep(5)
                response = httpx.get(url)
                print(response.text)
            print(response.text)
            return response.text.replace('OK|','') , str(time.time() - time_start)
        else:
            print('Error: {}'.format(response.text))
            return False
    
    def solve_capmonster(site_key,page_url):
        capmonster_key = config['captcha_key']
        url = "https://api.capmonster.cloud/createTask"
        data = {
            "clientKey": capmonster_key,
            "task":
            {
                "type": "HCaptchaTaskProxyless",
                "websiteURL": page_url,
                "websiteKey": site_key
            }
        }
        response = httpx.post(url,json=data)
        if response.json()['errorId'] == 0:
            task_id = response.json()['taskId']
            url = "https://api.capmonster.cloud/getTaskResult"
            data = {
                "clientKey": capmonster_key,
                "taskId": task_id
            }
            response = httpx.post(url,json=data)
            while response.json()['status'] == 'processing':
                time.sleep(3)
                response = httpx.post(url,json=data)
            return response.json()['solution']['gRecaptchaResponse']
        else:
            print('Error: {}'.format(response.json()['errorDescription']))
            return False
    

    def solve_capsolver(website_url, website_key):
        capsolver_key = config['captcha_key']
        json = {
        "clientKey": capsolver_key,
        "task": {
            "type": "HCaptchaTaskProxyLess",
            "websiteURL": website_url,
            "websiteKey": website_key,
        }
    }

        headers = {'Content-Type': 'application/json'}

        response = httpx.post('https://api.capsolver.com/createTask', headers=headers, json=json)
        try:
            taskid = response.json()['taskId']
        except:
            print('Error: {}'.format(response.json()['errorDescription']))
            return 

        json = {"clientKey": capsolver_key, "taskId": taskid}
        while True:
            time.sleep(1.5)
            response = httpx.post('https://api.capsolver.com/getTaskResult', headers=headers, json=json)
            if response.json()['status'] == 'ready':
                captchakey = response.json()['solution']['gRecaptchaResponse']
                return captchakey
            else:
                continue

    