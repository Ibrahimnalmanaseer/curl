import requests
import os
import logging
import json
import wave
import time
import shutil
import contextlib
import datetime

import pyodbc
import time
class MainAPI:






    token_ourapi = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjdXN0X25hbWUiOiJBYnUgWWFtYW4iLCJjdXN0X2lkIjoyfQ.-3LYg1zcUwAG_Z5omho420alNGIC-nKmSrA7E0wNbMk'

    def __init__(self, log_directory='C:\\traces', log_file_name='api_request_log.txt'):
        self.log_directory = log_directory
        self.log_file_name = log_file_name
        self.log_file_path = os.path.join(log_directory, log_file_name)
        self.setup_logging()
        self.wav_files = []
        self.wav_dur_modified_date={}


    def load_wav_files(self):

        try:
            with open ('C:\\traces\wav_files_dictionary.json',"r") as a:
                json_data = a.read()
                loaded_dict = json.loads(json_data)
                return loaded_dict
        except :
            return {}

    def save_wav_files(self):

        with open('C:\\traces\wav_files_dictionary.json', "w") as b:

            json.dump(self.wav_files,b)


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

                self.get_wav_files_path(folder_path)

                if self.wav_files:
                    for wav in self.wav_files:


                            # self.send_api_request('http://172.16.54.15:3000/rec_request/', self.token_ourapi, f"{wav}")







                            self.wav_dur_modified_date[wav] = {
                                "wav_duration": str(self.get_wav_duration(wav)),
                                "wav_modified_date": str(self.get_wav_modified_date(wav)),
                                "wav_file_name": os.path.basename(wav),
                                "wav_directory": self.move_wav_to_destination(r"C:\\traces",wav,self.get_wav_modified_date(wav))
                            }

                            self.wav_files=[]


                            logging.info(f"dur_modified_date: : {self.wav_dur_modified_date}")





                else:
                    logging.info("no files found in wav_files folder")










            except Exception as e:

                self.log_message_error(f'Error ttt: {e}')


            logging.info("sleep 120")
            time.sleep(120)






    def get_wav_files_path(self,folder_path):

        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith(".wav"):
                    full_path = os.path.join(root, file)
                    if full_path not in self.wav_files:
                        self.wav_files.append(full_path)







    def send_api_request(self,api_url, token_value, file_path):
        try:


            file_name_with_extension = os.path.basename(file_path)
            file_name_without_extension = os.path.splitext(file_name_with_extension)[0]
            headers = {'Authorization': f'Bearer {token_value}'}
            response = requests.post(api_url, headers=headers, files={'file': open(file_path, 'rb')})
            if response.status_code == 200:
                words = [item["word"] for item in response.json()["agent"]]
                words_text = " ".join(words)
                with open(f'D:\\NCGR_QUICK_WIN\VoiceMail\{file_name_without_extension}.txt', 'w', encoding='utf-8') as f:
                    # json.dump(words_text, f, ensure_ascii=False)
                    f.write(words_text)

                with open(f'D:\\Json_Backup\VoiceMail\{file_name_without_extension}.txt', 'w', encoding='utf-8') as f:
                    f.write(words_text)


                self.copy_files("D:\\NCGR_QUICK_WIN\VoiceMail",file_path,file_name_with_extension)
                self.copy_files("D:\\Json_Backup\VoiceMail", file_path, file_name_with_extension)

                self.log_message("API request successful")
            else:
                # call_duration=self.get_wav_duration(file_path)
                self.log_message_error(f"API request failed with status code: {response.status_code}, response: {response.text} ,File Name:{file_name_with_extension}, Call length per Sec : ")

        except FileNotFoundError:
            self.log_message_error(f"File not found: {file_path}")

        except requests.exceptions.RequestException as e:
            self.log_message_error(f"Error sending API request: {e}")

    def get_wav_duration(self,file_path):
        with contextlib.closing(wave.open(file_path, 'r')) as wf:
            frames = wf.getnframes()
            rate = wf.getframerate()
            duration = int(frames / float(rate))

            return duration

    def get_wav_modified_date(self,file_path):

        modified_date = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))

        return modified_date

    def move_wav_to_destination(self,destination_dir,file_path,modified_date):

        

        year_folder = os.path.join(destination_dir, str(modified_date.year))
        month_folder = os.path.join(year_folder, str(modified_date.month).zfill(2))
        day_folder = os.path.join(month_folder, str(modified_date.day).zfill(2))

        for folder in [year_folder, month_folder, day_folder]:
            if not os.path.exists(folder):
                os.makedirs(folder)

        # Move file
        destination_file = os.path.join(day_folder, os.path.basename(file_path))
        shutil.move(file_path, destination_file)
        return day_folder



    def copy_files(self,destination_path,file_path,file_name_with_extension):


        shutil.copyfile(file_path, os.path.join(destination_path, file_name_with_extension))




    def database_connect(self,call_info):

        server = 'ccclustervs,1434'
        database = 'Speechlog_Central'
        username = 'UCCE_CCS'
        password = 'BSFipcc_ist01'

        conn_str = f'DRIVER={{ODBC Driver 13 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

        insert_to_recorded_msgs = """
        INSERT INTO dbo.RecordedMsgs (CallDate, Duration, DirectoryPath, filename, Extension, CallerID, CalledID, AgentID, TrunkNo, IsHeard, Phone, Nature, calltype, RingCount, DialedNumber,
                                      CallerName, Backed, BackCDNum, BackupCallNum, Deleted, SysMode, FileFormat, VideoFileName, IsProtected, PrivateCall, IsEvaluated, AddedDate, isAnalysed, IsAnalyzed, IsNonFCRParent, NonFCRCount, holdtime, CallID)
        SELECT CallDate, Duration, DirectoryPath, filename, Extension, CallerID, CalledID, AgentID, TrunkNo, IsHeard, Phone, Nature, calltype, RingCount, DialedNumber,
               CallerName, Backed, BackCDNum, BackupCallNum, Deleted, SysMode, FileFormat, VideoFileName, IsProtected, PrivateCall, IsEvaluated, AddedDate, isAnalysed, IsAnalyzed, IsNonFCRParent, NonFCRCount, holdtime, CallID
        FROM dbo.processedRecords 
        """

        try:
            conn = pyodbc.connect(conn_str)
            cursor = conn.cursor()
            cursor.execute(insert_to_recorded_msgs)
            conn.commit()

        except Exception as e:
           self.log_message_error(f"Error executing {e}")
           raise

        finally:
            if conn:
                conn.close()

if __name__ == '__main__':

    api=MainAPI()

    api.main_method(r"C:\Users\Ibrahim\Documents")
