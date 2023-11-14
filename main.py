import json
import os
import subprocess
from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Define your connection parameters

db_host = config['db_host']
db_name = config['db_name']
db_user = config['db_user']
db_password = config['db_password']  # This will be empty as per your config
backup_folder = config['backup_folder']
firebase_bucket = config['firebase_bucket']


# Create a timestamp
current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Define the backup filename with the current date and time
backup_file = f"{backup_folder}{db_name}_backup_{current_time}.sql"  # The backup file will include the date and time

# Ensure the Backups directory exists
if not os.path.exists(backup_folder):
    os.makedirs(backup_folder)
# Full command for mysqldump
command = f"C:\\xampp\\mysql\\bin\\mysqldump.exe -h{db_host} -u{db_user} {db_name}"

# Open a file to write the output to
with open(backup_file, 'w') as output_file:
    try:
        # Call mysqldump to write the output to the file
        subprocess.run(command, shell=True, check=True, stdout=output_file)
        print(f"Database {db_name} exported successfully to {backup_file}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while exporting the database: {e}")


# Initialize Firebase Admin SDK
cred = credentials.Certificate('salaa-super-firebase-adminsdk-r36at-8f1c585512.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': firebase_bucket
})

# Function to upload file
def upload_to_storage(local_file_path, cloud_file_path):
    bucket = storage.bucket()
    blob = bucket.blob(cloud_file_path)
    blob.upload_from_filename(local_file_path)
    print(f"{local_file_path} uploaded to {cloud_file_path}.")

try:
# Call the function with the path to your SQL file
    upload_to_storage(backup_file, backup_file)

    print("\nDatabase Backup Successfully!")
    input("Press Enter to exit...")

except:
    print("\nDatabase Backup Failed!")
    input("Press Enter to exit...")
