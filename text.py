import requests
import json
import logging
import time
import os


def make_api_request(url1):
    log_directory = 'C:\\traces'
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    log_file_path = os.path.join(log_directory, 'api_request_log.txt')
    logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    headers1 = {
        'Accept-Language': 'en-us' ,'Connection': 'close'
    }
    auth_body = {
        "__type": "urn:inin.com:connection:icAuthConnectionRequestSettings",
        "applicationName": "ICWS Example Application",
        "userID": "cicadmin",
        "password": "123456"
    }

    try:
        response1 = requests.request("POST", url1, headers=headers1, json=auth_body, verify=False)
        response1.raise_for_status()  # Raise exception for HTTP errors

        if response1.status_code == 201:
            response_data = response1.json()
            csrf_token = response_data.get("csrfToken")
            session_id = response_data.get("sessionId")
            url2 = f"https://10.10.11.10:8019/icws/{session_id}/recordings/0DE0C017-CD4F-D013-8E31-18D8B7470001/export-uri"

            headers2 = {

                'ININ-ICWS-CSRF-Token': csrf_token,
                'Cookie': session_id
            }
            logging.info(f"{url2},token: {csrf_token}")
            time.sleep(10)

            try:
                response = requests.request("GET", url2, headers=headers2, verify=False)
                response.raise_for_status()

                if response.status_code == 200:
                    return response.json()

            except requests.exceptions.RequestException as e:
                logging.error(f"11Request Exception: {e}")
                return str(e)
    except requests.exceptions.RequestException as e:
        logging.error(f"22Request Exception: {e}")
        return str(e)


if __name__ == "__main__":
    response_text = make_api_request("https://10.10.11.10:8019/icws/connection")

