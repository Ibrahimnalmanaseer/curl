import requests
import os
import logging
import json
import time
import pyodbc

class MainAPI:

    recording_inf_list = []
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


    def post_method(self,url1):





        headers1 = {
            'Accept-Language': 'en-us'
        }
        auth_body = {
            "__type": "urn:inin.com:connection:icAuthConnectionRequestSettings",
            "applicationName": "ICWS Example Application",
            "userID": "cicadmin",
            "password": "123456"
        }

        try:

            response1 = requests.post(url1, headers=headers1, json=auth_body, verify=False,timeout=4)
            response1.raise_for_status()  # Raise exception for HTTP errors

            if response1.status_code == 201:
                response_data = response1.json()

                cookies=self.getCookies(response1.cookies, "10.10.11.10")


                csrf_token = response_data.get("csrfToken")
                session_id = response_data.get("sessionId")
                # cookies=response1.cookies


                # self.log_message(f"Post: {response_data}")
                self.log_message(f'Cookie {cookies}')
                requests.session().close()

                return csrf_token,cookies,session_id


        except requests.exceptions.RequestException as e:
            self.log_message_error(f"Post Request Exception: {e}")



    def Get_method(self,csrf_token,cookies,session_id,record_key,record_value):



        headers2 = {

            'ININ-ICWS-CSRF-Token': csrf_token,
            'Cookie': cookies
        }
        self.log_message(f"URL : ,token: {csrf_token}")


        try:
            response = requests.request("GET",f"https://10.10.11.10:8019/icws/{session_id}/recordings/{record_key}/export-uri", headers=headers2, verify=False)
            response.raise_for_status()

            if response.status_code == 200:
                self.log_message(f"URL from Get API : {response.json()['uri']}")

                self.download_file_from_api(response.json()['uri'], record_value)
                response.close()


        except requests.exceptions.RequestException as e:
            self.log_message_error(f"GET: Request Exception: {e}")
            return str(e)



    def getCookies(self,cookie_jar, domain):
        cookie_dict = cookie_jar.get_dict(domain=domain)
        found = ['%s=%s' % (name, value) for (name, value) in cookie_dict.items()]
        return ';'.join(found)

    def download_file_from_api(self, api_url,record_name):
        response = requests.get(api_url)


        # filename_pattern = r'filename=(.+)$'
        # filename_match = re.search(filename_pattern, response.headers['content-disposition'])
        # filename = filename_match.group(1)
        self.log_message(f"*************************** {record_name} **************************************")
        file_path=f"D:\\NCGR_QUICK_WIN\VoiceMail\{record_name}.wav"

        if response.status_code == 200:
            with open(file_path, 'wb') as file:
                file.write(response.content)
            self.log_message(f"File downloaded successfully {record_name} to VoiceMail")
        else:
            self.log_message_error(f"Failed to download file. Status code: {response.status_code}")



    def connect_to_sql_server(self,server, database, username, password,query1):
        try:
            # Connect to SQL Server
            conn = pyodbc.connect(
                f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}')
            cursor = conn.cursor()

            self.log_message(f"success:  conn {conn} | cursor {cursor}")


            while True:

                try:
                    cursor.execute(query1)
                    rows = cursor.fetchall()

                    if rows:

                        for record_key,record_value, _ in rows:
                            self.recording_inf_list.append(record_value)
                            csrf_token, cookies, session_id = self.post_method("https://10.10.11.10:8019/icws/connection")
                            self.log_message(f"using in get method{record_key}:{record_value}")
                            self.Get_method(csrf_token, cookies, session_id, record_key, record_value)

                        # all_files_wav_list = self.get_wav_files("D:\\NCGR_QUICK_WIN\VoiceMail")
                        for wav in self.recording_inf_list:

                                self.send_api_request('http://172.16.54.15:3000/rec_request/', self.token_ourapi, f"D:\\NCGR_QUICK_WIN\VoiceMail\{wav}.wav")

                        quoted_filename=[f"'{filename}'" for filename in self.recording_inf_list]

                        update_query = f"update IVRStaging set status=1 where filename in ({','.join(quoted_filename)})"


                        self.log_message(f'*****{update_query}***')


                        cursor.execute(update_query)

                        conn.commit()
                        self.recording_inf_list=[]


                except Exception as e:

                    self.log_message_error(f'Error : {e}')

                time.sleep(900)








        except pyodbc.Error as e:
            self.log_message_error(f'Error {e}')
            return None, None, False  # Return None for connection and cursor along with failure status and error message



    # def get_api_loop(self,server, database, username, password,query):
    #
    #         # self.connect_to_sql_server(server, database, username, password,query)
    #         csrf_token, cookies, session_id = self.post_method("https://10.10.11.10:8019/icws/connection")
    #         for record_key,record_value in self.recording_inf_dic.items() :
    #             self.log_message(f"using in get method{record_key}:{record_value}")
    #             self.Get_method(csrf_token, cookies,session_id,record_key,record_value)



    def get_wav_files(self,folder_path):
        wav_files = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith(".wav"):
                    full_path = os.path.join(root, file)
                    wav_files.append(full_path)
        return wav_files


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
    api = MainAPI()
    server = '172.16.54.11'
    database = 'Speechlog'
    username = 'sa'
    password = 'Aa@123123'


    query1 = 'select top 3 RecordingId,filename,status from IVRStaging WHERE status = 0'

    query2= 'update IVRStaging set status=1 where status = 0 '


    api.connect_to_sql_server(server, database, username, password,query1)

