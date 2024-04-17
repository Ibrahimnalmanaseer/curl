import argparse
import requests
import json
import os
import logging
import time
log_directory = 'C:\\traces'
os.makedirs(log_directory, exist_ok=True)
# Configure logging
log_file_path = os.path.join(log_directory, 'api_request_log.txt')
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def make_api_request(url,url1, token, cookie):
    headers1 = {
        'Accept-Language': 'en-us'
    }
    auth_body = {
        "__type": "urn:inin.com:connection:icAuthConnectionRequestSettings",
        "applicationName": "ICWS Example Application",
        "userID": "cicadmin",
        "password": "123456"
    }
    response1 = requests.request("POST", url1, headers=headers1, json=auth_body, verify=False)
    if response1.status_code == 200:
        logging.info(f"{response1.json()}")
    else:
        error_msg = f"Error: {response1.status_code} - {response1.reason} - {response1.text}"
        logging.error(error_msg)
        return error_msg









    payload = json.dumps({})
    headers = {
        'ININ-ICWS-CSRF-Token': f"{token}",
        'Cookie': f"{cookie}",
        'Content-Type': 'application/json'
    }
    logging.info(headers)
    response = requests.request("GET", url, headers=headers, data=payload, verify=False)

    if response.status_code == 200:
        logging.info(f"{response.json()}")
        return response.json()
    else:
        error_msg = f"Error: {response.status_code} - {response.reason} - {response.text}"
        logging.error(error_msg)
        return error_msg


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Make an API request.")
    parser.add_argument("url", help="The URL of the API endpoint.")
    parser.add_argument("token", help="The ININ-ICWS-CSRF-Token value.")
    parser.add_argument("cookie", help="The Cookie value.")
    args = parser.parse_args()

    response_text = make_api_request(args.url,"https://10.10.11.10:8019/icws/connection",args.token, args.cookie)

