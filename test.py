import os
import wave
import contextlib
import datetime
import shutil

# # Sample dictionary
# my_dict = {"key1": "value1", "key2": "value2"}
#
# # Convert dictionary to JSON string
# json_str = json.dumps(my_dict)
#
# # Write JSON string to log file
# with open('log_file.txt', 'w') as log_file:
#     log_file.write(json_str)
#
# # Read JSON string from log file and load it
# with open('log_file.txt', 'r') as log_file:
#     json_data = log_file.read()
#     loaded_dict = json.loads(json_data)
#
# print(loaded_dict)

modified_date = datetime.datetime.fromtimestamp(os.path.getmtime(r"C:\Users\Ibrahim\Downloads\speechlog-web-app\speechlog-web-app\wwwroot\Uploads\SessionAttachments\2020\7\23\1595505668922.wav"))

with contextlib.closing(wave.open(r"C:\Users\Ibrahim\Downloads\speechlog-web-app\speechlog-web-app\wwwroot\Uploads\SessionAttachments\2020\7\23\1595505668922.wav", 'r')) as wf:
    frames = wf.getnframes()
    rate = wf.getframerate()
    duration = int(frames / float(rate))


destination_dir =r'C:\\traces\07'

source_file = r'C:\traces\Emerging trends and topics (3).png'

year_folder = os.path.join(destination_dir, str(modified_date.year))
month_folder = os.path.join(year_folder, str(modified_date.month).zfill(2))
day_folder = os.path.join(month_folder, str(modified_date.day).zfill(2))


for folder in [year_folder, month_folder, day_folder]:
    if not os.path.exists(folder):
        os.makedirs(folder)



# Move file
destination_file = os.path.join(day_folder, os.path.basename(source_file))
shutil.move(source_file, destination_file)

# shutil.move(r"C:\traces\Emerging trends and topics.png", r"C:\\traces\05")

print (modified_date)

print(duration)