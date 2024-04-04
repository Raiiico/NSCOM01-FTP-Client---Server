import os
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

# Users dictionary
users = {
    "john": "1234",
    "jane": "5678",
    "joe": "qwerty",
}

def main():
    # Instantiate a dummy authorizer for managing 'virtual' users
    authorizer = DummyAuthorizer()

    # Setup the FTP root directory
    ftp_root = './ftp'
    if not os.path.exists(ftp_root):
        os.makedirs(ftp_root)

    # Define users from the dictionary with full r/w permissions
    for username, password in users.items():
        # Each user has their own directory for this example
        user_dir = os.path.join(ftp_root, username)
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)
        authorizer.add_user(username, password, homedir=user_dir, perm='elradfmwMT')

    # Instantiate FTP handler class
    handler = FTPHandler
    handler.authorizer = authorizer

    # Define a customized banner (string returned when client connects)
    handler.banner = "Welcome to the FTP server."

    # Instantiate FTP server class and listen on 127.0.0.1:2121
    address = ('127.0.0.1', 2121)
    server = FTPServer(address, handler)

    # Set a limit for connections
    server.max_cons = 256
    server.max_cons_per_ip = 5

    # Start the FTP server
    print("Starting FTP server. Connect at {}:{}".format(*address))
    server.serve_forever()

if __name__ == '__main__':
    main()
