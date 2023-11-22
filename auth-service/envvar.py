import os
# Set environment variables
def setVar():
    os.environ['MYSQL_HOST'] = 'localhost'
    os.environ['MYSQL_USER'] = 'root'
    os.environ['MYSQL_PASSWORD'] = '123456'
    os.environ['MYSQL_DB'] = 'microservices'
    os.environ['MYSQL_PORT'] = '3306'
    os.environ['JWT_SECRET'] = 'akkiitsme@1234'
    