import os
import requests
import logging
import json

log_directory = 'C:\\traces'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

log_file_path = os.path.join(log_directory, 'api_request_log_our.txt')
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def send_api_request(api_url, token_value, file_path):
    try:
        headers = {'Authorization': f'Bearer {token_value}'}
        response = requests.post(api_url, headers=headers, files={'file': open(file_path, 'rb')})
        if response.status_code == 200:
            words = [item["word"] for item in response.json()["agent"]]


            words_text = " ".join(words)
            with open('C:\\traces\\respond.json', 'w', encoding='utf-8') as f:
                json.dump(words_text, f, ensure_ascii=False)
            logging.info("API request successful")
        else:
            logging.error(f"API request failed with status code: {response.status_code}, response: {response.text}")
    except Exception as e:
        logging.error(f"Error sending API request: {e}")


if __name__ == "__main__":
    api_url = 'http://172.16.54.15:3000/rec_request/'
    token_value = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjdXN0X25hbWUiOiJBYnUgWWFtYW4iLCJjdXN0X2lkIjoyfQ.-3LYg1zcUwAG_Z5omho420alNGIC-nKmSrA7E0wNbMk'
    file_path = 'C:\\Users\\Administrator\\Desktop\\TEST API\\3001501721_3001501707_6066def1c1ac7703be5804a7.wav'
    send_api_request(api_url, token_value, file_path)


"D:\\NCGR_QUICK_WIN\Downloaded_Calls"