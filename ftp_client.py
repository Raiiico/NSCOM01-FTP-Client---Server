import ftplib
import logging
from tqdm import tqdm
import os

# Setup logger
logger = logging.getLogger("Ftp client")
logger.setLevel(logging.DEBUG)
log_handler = logging.StreamHandler()
log_formatter = logging.Formatter('%(levelname)s -- %(name)s -- %(message)s')
log_handler.setFormatter(log_formatter)
logger.addHandler(log_handler)




# Exception handling decorator
def _catch_exception(operation):
    def wrapper():
        try:
            operation()
        except ftplib.all_errors as err:
            print("Error: ", str(err))
    return wrapper

# FTP operations
def dir_list():
    files = []
    ftp.dir(files.append)
    for file in files:
        print(file)

@_catch_exception
def get_size():
    filename = input("[ _+_ ] File name >> ")
    ftp.sendcmd('TYPE I')
    size = ftp.size(filename=filename)
    print(f"Size of {filename}: {size} bytes")

@_catch_exception
def download():
    orig_file = input("File to copy >> ")
    with open(input("Save file as >> "), 'wb') as fp:
        ftp.retrbinary('RETR ' + orig_file, fp.write)
        print("Copied with Success ...")

@_catch_exception
def upload_file():
    file_name = input("File to upload >> ")
    with open(file_name, 'rb') as file:
        ftp.storbinary('STOR ' + input("Save as >> "), file)
        print('Done successfully')

@_catch_exception
def delete():
    ftp.delete(input("Enter file name >> "))

@_catch_exception
def rename():
    ftp.rename(fromname=input("File to rename >> "), toname=input("Rename to >> "))

@_catch_exception
def make_dir():
    ftp.mkd(input("Enter the Dir Name >> "))

@_catch_exception
def remove_dir():
    ftp.rmd(input("Dir to delete >> "))

@_catch_exception
def change_dir():
    ftp.cwd(input("Enter directory name >> "))
    
@_catch_exception
def go_home():
    """Change back to the home directory."""
    ftp.cwd(home_directory)
    print(f"Returned to the home directory: {home_directory}")


def _quit():
    ftp.quit()
    print("Connection closed.")

# User inputs for connection details
host = input("Enter FTP server host (IP address): ")
port = int(input("Enter FTP server port: "))
username = input("Enter username: ")
password = input("Enter password: ")

with ftplib.FTP() as ftp:
    ftp.connect(host, port)
    ftp.login(username, password)
    home_directory = ftp.pwd()  # Store the home directory after login
    logger.info(ftp.getwelcome())

    while True:
        user_operation = input("Enter the operation name >> ").lower().strip()
        if user_operation == 'dir listing':
            dir_list()
        elif user_operation == 'get size':
            get_size()
        elif user_operation == 'download':
            download()
        elif user_operation == 'upload':
            upload_file()
        elif user_operation == 'rename file':
            rename()
        elif user_operation == 'delete':
            delete()
        elif user_operation == 'make dir':
            make_dir()
        elif user_operation == 'remove dir':
            remove_dir()
        elif user_operation == 'change dir':
            change_dir()
        elif user_operation == 'help':
            print("dir listing | get size | download | upload | rename file | delete | change dir | make dir | remove dir | quit ")
            continue
        elif user_operation == 'home':  # Handle 'home' command
            go_home()
        elif user_operation in ['quit']:
            _quit()
            break
        else:
            print("Unknown operation. Type 'help' for available operations.")
