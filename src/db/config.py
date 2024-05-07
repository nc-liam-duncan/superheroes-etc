from dotenv import load_dotenv
import os

TESTING = os.getenv("TESTING")

if TESTING:
    load_dotenv('.env.test', override=True)
else:
    load_dotenv('.env.development', override=True)

user = os.getenv('PGUSER')
password = os.getenv('PGPASSWORD')
database = os.getenv('PGDATABASE')
host = os.getenv('PGHOST')
port = int(os.getenv('PGPORT'))
