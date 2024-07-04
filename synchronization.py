import os
import sys
import shutil
import time
import hashlib
import logging
from datetime import datetime
import keyboard

def calculate_md5(file_path):
    # Calculates the MD5 hash of a file.
    md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            md5.update(chunk)
    return md5.hexdigest()

def compare_files(file1,file2):
    # Compares MD5 hashes of two files and returns True if they are the same.
    if not os.path.exists(file1) or not os.path.exists(file1): 
        return False
    if calculate_md5(file1) == calculate_md5(file2):
        return True
    else:
        return False

def delete(file):
    # Deletes a file or a folder
    if os.path.exists(file):
        if os.path.isdir(file):
            shutil.rmtree(file)
        else: os.remove(file)


def copy(file,destination):
    # Copying the file to the destination folder
    file_name = os.path.basename(file)
    destination_file = os.path.join(destination, file_name)
    if os.path.isfile(file):
        shutil.copy2(file, destination_file)
    elif os.path.isdir(file):
        shutil.copytree(file, destination_file)


def sync_folders(source, replica):
    # Synchronization of two folders (after synchronization the replica folder is a copy of the source folder)
    if not os.path.exists(replica):
        os.makedirs(replica)

    for item in os.listdir(source):
        source_item = os.path.join(source, item)
        replica_item = os.path.join(replica, item)

        # if the item is a folder, use recursion
        if os.path.isdir(source_item):
            sync_folders(source_item, replica_item)
            continue

        # if the item is a file and replica_item exists, firstly compare hashes of source and replica file, if it is different, make it correct
        if os.path.exists(replica_item):
            if compare_files(source_item,replica_item) == False:
                log_and_print(f"Copying changes from {source_item} to {replica_item}.")
                delete(replica_item)
                destination = os.path.dirname(replica_item)
                copy(source_item,destination) 
        else: 
            # if the item is a file and replica_item does not exist, create a new file in replica
                destination = os.path.dirname(replica_item)
                log_and_print(f"Creating backup of {source_item} in {destination}.")
                copy(source_item,destination)

    # check whether there is anything more in replica file and delete
    for item in os.listdir(replica):
        replica_item = os.path.join(replica, item)
        source_item = os.path.join(source, item)
        if not os.path.exists(source_item):
            log_and_print(f"Deleting {replica_item}.")
            delete(replica_item)

def log_and_print(message):
    # Writes messages to the console and if it is possible, also to the log file
    try:
        global logger
        logger.info(message)
        print(message)
    except Exception as e:
        print(message)

def logger_setup(log_file_path):
    # Settings for log files
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
    log_file = f'{log_file_path}/log_{current_datetime}.log'
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler = logging.FileHandler(log_file, mode='w') 
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logging.getLogger().addHandler(file_handler)
    logging.getLogger().setLevel(logging.INFO)
    return logging.getLogger()

def set_running_to_false():
    # Helper function for finishing the program after pressing the 'q' at the keyboard
    global running
    running = False
    log_and_print("Last synchronization is in process.")


def validate_inputs():
    # Checking if the input arguments are in right format
    if len(sys.argv) != 5:
        log_and_print("Incorrect number of input arguments: script.py <source_folder> <replica_folder> <interval> <log_file_path>")
        sys.exit(1)
    
    source_folder = str(sys.argv[1])
    replica_folder = str(sys.argv[2])
    interval = sys.argv[3]
    log_file_path = str(sys.argv[4])

    # Validate source_folder
    if not os.path.isdir(source_folder):
        log_and_print(f"Error: {source_folder} is not a valid directory for the source folder.")
        sys.exit(1)

    # Validate replica_folder
    if not os.path.isdir(replica_folder):
        log_and_print(f"Error: {replica_folder} is not a valid directory for the replica folder.")
        sys.exit(1)

    # Validate interval
    try:
        interval = int(interval)
        if interval <= 0:
            raise ValueError
    except ValueError:
        log_and_print(f"Error: {interval} is not a valid positive integer.")
        sys.exit(1)

    # Validate log_file_path
    if not os.path.isdir(log_file_path):
        log_and_print(f"Error: {log_file_path} is not a valid directory for log files.")
        sys.exit(1)
    
    return source_folder, replica_folder, interval, log_file_path

if __name__ == '__main__':

    source_folder, replica_folder, interval, log_file_path = validate_inputs()
    logger = logger_setup(log_file_path)
    running = True
    print("For stopping the program, please press 'q'.")
    keyboard.on_press_key("q", lambda _: set_running_to_false())
    while running:
        sync_folders(source_folder, replica_folder)
        time.sleep(interval)
    sync_folders(source_folder, replica_folder)