import os

from dotenv import load_dotenv

load_dotenv()
server_interface = os.environ.get('SERVER_INTERFACE', '127.0.0.1')
server_port = eval(os.environ.get('SERVER_PORT', 8000))