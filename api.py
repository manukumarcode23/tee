#!/usr/bin/env python3
"""
Terabox Cookie Regenerator API - Unified File
"""

from flask import Flask, jsonify, request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import subprocess
import json
import os

# --- Automation Class ---

import requests
import urllib.parse

# --- Automation Class ---

class TeraboxAutomation:
    def __init__(self, headless=False, account_name="default", account_number=None):
        self.headless = headless
        self.account_name = account_name
        self.account_number = account_number
        self.driver = None
        self.logged_in = False
        self._setup_driver()
    
    def _setup_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36")
        
        if self.headless:
            chrome_options.add_argument("--headless=new")
        
        try:
            chromium_path = subprocess.run(['which', 'chromium'], capture_output=True, text=True).stdout.strip()
            if chromium_path:
                chrome_options.binary_location = chromium_path
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            print(f"[{self.account_name}] Browser initialized")
        except Exception as e:
            print(f"[{self.account_name}] Failed to initialize driver: {e}")
            raise
    
    def login(self, email, password):
        if not self.driver: return False
        try:
            print(f"[{self.account_name}] Navigating to login page...")
            self.driver.get("https://www.1024terabox.com/main?login")
            time.sleep(8) # Increased wait for page load
            
            # Save screenshot for debugging if it fails
            self.driver.save_screenshot(f"{self.account_name}_login_page.png")
            
            email_selectors = [
                (By.CSS_SELECTOR, "input[type='email']"),
                (By.CSS_SELECTOR, "input[name='email']"),
                (By.XPATH, "//input[@type='email']"),
                (By.XPATH, "//input[contains(@placeholder, 'Email')]"),
                (By.CSS_SELECTOR, "input#email")
            ]
            
            email_field = None
            for by, selector in email_selectors:
                try:
                    print(f"[{self.account_name}] Trying email selector: {selector}")
                    email_field = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((by, selector)))
                    break
                except: continue
            
            if not email_field:
                # Try to find any input field as a last resort
                inputs = self.driver.find_elements(By.TAG_NAME, "input")
                print(f"[{self.account_name}] Found {len(inputs)} inputs. Trying first visible text/email input.")
                for inp in inputs:
                    if inp.is_displayed() and inp.get_attribute("type") in ["text", "email"]:
                        email_field = inp
                        break
            
            if not email_field: 
                print(f"[{self.account_name}] Page Source Snippet: {self.driver.page_source[:500]}")
                raise Exception("Email field not found")
            
            email_field.clear()
            email_field.send_keys(email)
            time.sleep(2)
            
            password_field = None
            try:
                password_field = self.driver.find_element(By.CSS_SELECTOR, "input[type='password']")
            except:
                # Try to find by placeholder
                inputs = self.driver.find_elements(By.TAG_NAME, "input")
                for inp in inputs:
                    if inp.get_attribute("type") == "password" or "password" in inp.get_attribute("placeholder").lower():
                        password_field = inp
                        break
            
            if not password_field: raise Exception("Password field not found")
            
            password_field.clear()
            password_field.send_keys(password)
            password_field.send_keys(Keys.RETURN)
            print(f"[{self.account_name}] Credentials submitted. Waiting for login...")
            time.sleep(12) # Increased wait for redirect
            
            # Navigate to the specific URL requested after login
            print(f"[{self.account_name}] Navigating to target URL for cookie extraction...")
            self.driver.get("https://dm.1024terabox.com/ai/index?clearCache=1")
            time.sleep(8)

            current_url = self.driver.current_url
            print(f"[{self.account_name}] Current URL after redirect: {current_url}")
            
            if "terabox.com" in current_url:
                self.logged_in = True
                self._capture_cookies()
                return True
            return False
        except Exception as e:
            print(f"[{self.account_name}] Login error: {e}")
            self.driver.save_screenshot(f"{self.account_name}_error.png")
            return False
    
    def _capture_cookies(self):
        if not self.driver: return
        try:
            # Capture cookies from the target domain
            cookies = self.driver.get_cookies()
            
            # Define the specific order requested (starting with browserid)
            cookie_order = [
                'browserid', 'lang', 'csrfToken', '__stripe_mid', 'PANWEB', 
                'shareRedirectDomain', '_fbp', '_clck', '__bid_n', '_clsk', 
                '_uetsid', '_uetvid', 'ndut_fmt', 'g_state', 'ndut_fmv', 
                'ab_sr', 'ndus'
            ]
            
            cookie_dict = {cookie['name']: cookie['value'] for cookie in cookies}
            
            # Reconstruct the cookie string in the exact order requested
            ordered_pairs = []
            
            # First add ordered cookies
            for name in cookie_order:
                if name in cookie_dict:
                    ordered_pairs.append(f"{name}={cookie_dict[name]}")
            
            # Then add any remaining cookies that weren't in the list
            for name, value in cookie_dict.items():
                if name not in cookie_order:
                    ordered_pairs.append(f"{name}={value}")
            
            cookie_string = "; ".join(ordered_pairs)
            
            # Construct the Full Request String
            full_request = (
                "GET /ai/index?clearCache=1 HTTP/1.1\n"
                "Host: dm.1024terabox.com\n"
                "Connection: keep-alive\n"
                "Cache-Control: max-age=0\n"
                "sec-ch-ua: \"Android WebView\";v=\"143\", \"Chromium\";v=\"143\", \"Not A(Brand\";v=\"24\"\n"
                "sec-ch-ua-mobile: ?1\n"
                "sec-ch-ua-platform: \"Android\"\n"
                "Upgrade-Insecure-Requests: 1\n"
                f"User-Agent: {self.driver.execute_script('return navigator.userAgent')}\n"
                "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7\n"
                "X-Requested-With: mark.via.gp\n"
                "Sec-Fetch-Site: same-origin\n"
                "Sec-Fetch-Mode: navigate\n"
                "Sec-Fetch-User: ?1\n"
                "Sec-Fetch-Dest: document\n"
                "Referer: https://www.1024terabox.com/\n"
                "Accept-Encoding: gzip, deflate, br, zstd\n"
                "Accept-Language: en-US,en;q=0.9\n"
                f"Cookie: {cookie_string}"
            )
            
            # Save the full request instead of just the cookie string
            self._save_cookies_to_json(full_request)

            # Send only the cookie string to the external API
            if self.account_number:
                try:
                    # Format account number as requested: cookie-NUMBER
                    # Ensure Account 1 becomes cookie-1
                    formatted_number = f"cookie-{self.account_number}"
                    # URL encode the cookie_string
                    encoded_cookies = urllib.parse.quote(cookie_string)
                    external_url = f"https://e843ce9d-bcdb-4006-867b-8422ad0ccf60-00-2u7rgvvwak9pu.sisko.replit.dev/api/cookies?number={formatted_number}&cookies={encoded_cookies}"
                    print(f"[{self.account_name}] Sending cookies to external API with number {formatted_number}...")
                    requests.get(external_url, timeout=10)
                except Exception as e:
                    print(f"[{self.account_name}] Error sending to external API: {e}")
        except Exception as e:
            print(f"[{self.account_name}] Error capturing cookies: {e}")
    
    def _save_cookies_to_json(self, cookie_string):
        cookies_file = "cookies.json"
        try:
            data = {}
            if os.path.exists(cookies_file):
                with open(cookies_file, 'r') as f: data = json.load(f)
            data[self.account_name] = cookie_string
            with open(cookies_file, 'w') as f: json.dump(data, f, indent=2)
        except Exception as e:
            print(f"[{self.account_name}] Error saving cookies: {e}")

    def close(self):
        if self.driver: self.driver.quit()

# --- API Logic ---

app = Flask(__name__)

def load_accounts():
    try:
        if not os.path.exists('accounts.json'): return []
        with open('accounts.json', 'r') as f:
            data = json.load(f)
            accounts = data.get('accounts', [])
            for acc in accounts:
                if 'name' in acc: acc['name'] = str(acc['name'])
            return accounts
    except Exception as e:
        print(f"Error loading accounts: {e}")
        return []

def get_account_by_number(account_number):
    accounts = load_accounts()
    if 0 < account_number <= len(accounts):
        return accounts[account_number - 1]
    return None

@app.route('/regenerate', methods=['GET'])
def regenerate_cookies():
    number_param = request.args.get('number')
    if not number_param:
        return jsonify({'status': 'error', 'message': 'Missing account number parameter'}), 400
    
    try:
        account_number = int(number_param)
        account = get_account_by_number(account_number)
    except:
        return jsonify({'status': 'error', 'message': 'Invalid account number'}), 400

    if not account:
        return jsonify({'status': 'error', 'message': f'Account {account_number} not found'}), 404
    
    try:
        account_name = account.get('name', f'Account {account_number}')
        email = account.get('email')
        password = account.get('password')
        
        automation = TeraboxAutomation(headless=True, account_name=account_name, account_number=account_number)
        success = automation.login(email, password)
        automation.close()
        
        if success:
            if os.path.exists('cookies.json'):
                with open('cookies.json', 'r') as f:
                    cookies_data = json.load(f)
                    return jsonify({
                        'status': 'success',
                        'account_name': account_name,
                        'cookie': cookies_data.get(account_name, ''),
                        'message': 'Cookies regenerated'
                    }), 200
        return jsonify({'status': 'error', 'message': 'Failed to login'}), 500
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/add_account', methods=['GET'])
def add_account_get():
    try:
        email = request.args.get('email')
        password = request.args.get('password')
        number = request.args.get('number')
        
        if not email or not password:
            return jsonify({'status': 'error', 'message': 'Missing email or password query parameters'}), 400
        
        accounts = load_accounts()
        # Automatically assign the next number (1, 2, 3...)
        next_number = len(accounts) + 1
        name = str(next_number)
        
        new_account = {
            'email': email,
            'password': password,
            'name': name
        }
        
        accounts.append(new_account)
        
        with open('accounts.json', 'w') as f:
            json.dump({'accounts': accounts}, f, indent=2)
        
        return jsonify({
            'status': 'success', 
            'message': 'Account added successfully',
            'account_number': len(accounts),
            'name': name
        }), 201
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/accounts', methods=['GET', 'POST'])
def handle_accounts():
    if request.method == 'POST':
        try:
            new_account = request.get_json()
            if not new_account or 'email' not in new_account or 'password' not in new_account:
                return jsonify({'status': 'error', 'message': 'Missing email or password'}), 400
            
            accounts = load_accounts()
            # Set a default name if not provided
            if 'name' not in new_account:
                new_account['name'] = f"Account {len(accounts) + 1}"
            
            accounts.append(new_account)
            
            with open('accounts.json', 'w') as f:
                json.dump({'accounts': accounts}, f, indent=2)
            
            return jsonify({
                'status': 'success', 
                'message': 'Account added successfully',
                'account_number': len(accounts)
            }), 201
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
            
    # GET logic
    accounts = load_accounts()
    return jsonify({
        'status': 'success',
        'accounts': [{'number': i+1, 'name': a.get('name')} for i, a in enumerate(accounts)]
    }), 200

@app.route('/cookies', methods=['GET'])
def get_all_cookies():
    if os.path.exists('cookies.json'):
        with open('cookies.json', 'r') as f:
            return jsonify({'status': 'success', 'cookies': json.load(f)}), 200
    return jsonify({'status': 'error', 'message': 'No cookies found'}), 404

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
