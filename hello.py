import argparse
import requests
import json
import os
import logging
log_directory = 'C:\\traces'
os.makedirs(log_directory, exist_ok=True)
# Configure logging
log_file_path = os.path.join(log_directory, 'api_request_log.txt')
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



url = "https://10.10.11.10:8019/icws/2444387001/recordings/0DE0C017-CD4F-D013-8E31-18D8B7470001/export-uri"

payload = json.dumps({})
headers = {
  'ININ-ICWS-CSRF-Token': 'WAhjaWNhZG1pblgYSUNXUyBFeGFtcGxlIEFwcGxpY2F0aW9uWCQxMWVjOTNhZC01ZDk3LTQ2MzUtYTNhZC1jYjBkYzU3NDEwODdYDDE3Mi4xNi41NC4xMQ==',
  'Cookie': '2444387001; icws_2444387001=9a020325-a5fb-4423-a021-4ae29a9ae31b|languageId=en-us',
  'Content-Type': 'application/json'
}

response = requests.request("GET", url, headers=headers, data=payload, verify=False)

if response.status_code == 200:
    logging.info(f"{response.json()}")

else:
    error_msg = f"Error: {response.status_code} - {response.reason}"
    logging.error(error_msg)
