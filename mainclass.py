import requests
import os
import logging
import json

import time
class MainAPI:

    wav_files= {}
    token_ourapi = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjdXN0X25hbWUiOiJBYnUgWWFtYW4iLCJjdXN0X2lkIjoyfQ.-3LYg1zcUwAG_Z5omho420alNGIC-nKmSrA7E0wNbMk'

    def __init__(self, log_directory='C:\\traces', log_file_name='api_request_log.txt'):
        self.log_directory = log_directory
        self.log_file_name = log_file_name
        self.log_file_path = os.path.join(log_directory, log_file_name)
        self.setup_logging()


    def setup_logging(self):
        if not os.path.exists(self.log_directory):
            os.makedirs(self.log_directory)
        logging.basicConfig(filename=self.log_file_path, level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')

    def log_message(self, message):
        logging.info(message)


    def log_message_error(self,message):
        logging.info(message)



    def main_method(self,folder_path):

        while True:

            try:

                self.get_wav_files(folder_path)
                self.log_message(f"+++++++{folder_path}")
                for wav,status in self.wav_files.items():
                    if status==0:


                        self.send_api_request('http://172.16.54.15:3000/rec_request/', self.token_ourapi, f"{wav}")
                        self.log_message(f'successful transcription of: {wav}')
                        self.wav_files[wav]=1





            except Exception as e:

                self.log_message_error(f'Errorttttttt: {e}')

            self.log_message(self.wav_files)

            time.sleep(60)






    def get_wav_files(self,folder_path):

        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith(".wav"):
                    full_path = os.path.join(root, file)
                    if full_path not in self.wav_files:
                        self.wav_files[full_path]=0







    def send_api_request(self,api_url, token_value, file_path):
        try:


            file_name_with_extension = os.path.basename(file_path)
            file_name_without_extension = os.path.splitext(file_name_with_extension)[0]
            headers = {'Authorization': f'Bearer {token_value}'}
            response = requests.post(api_url, headers=headers, files={'file': open(file_path, 'rb')})
            if response.status_code == 200:
                words = [item["word"] for item in response.json()["agent"]]

                words_text = " ".join(words)
                with open(f'D:\\NCGR_QUICK_WIN\VoiceMail\{file_name_without_extension}.json', 'w', encoding='utf-8') as f:
                    json.dump(words_text, f, ensure_ascii=False)
                self.log_message("API request successful")
            else:
                self.log_message_error(f"API request failed with status code: {response.status_code}, response: {response.text}")
        except Exception as e:
            self.log_message_error(f"Error sending API request: {e}")


if __name__ == '__main__':

    api=MainAPI()

    api.main_method("D:\\NCGR_QUICK_WIN\Genesys_Calls")
