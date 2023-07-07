from mysql.connector import connect
from dotenv import load_dotenv
import os

load_dotenv()
sql = connect(
    host=os.getenv("sql_host"),
    user=os.getenv("sql_user"),
    password=os.getenv("sql_pass")
)


# create database
def create_database():
    cursor = sql.cursor()
    command = """
    create database db_01
    """
    try:
        cursor.execute(command)
    except Exception as e:
        return "table already exist"


# create table
def create_table():
    cursor = sql.cursor()
    command = """
    CREATE TABLE db_01.users (
        `USER_ID` bigint(20) NOT NULL,
        `FIRST_NAME` varchar(100) DEFAULT NULL,
        `LAST_NAME` varchar(100) DEFAULT NULL,
        `SEX` varchar(100) DEFAULT NULL,
        `AGE` int(11) DEFAULT NULL,
        `JOB` varchar(100) DEFAULT NULL,
        primary key (USER_ID)
    );
    """
    try:
        cursor.execute(command)
    except Exception as e:
        return "table already exist"


def add_user(user_id):
    command = f"""
    INSERT INTO db_01.users(`USER_ID`) VALUES (
        {user_id}
    );
    """
    cursor = sql.cursor()
    try:
        cursor.execute(command)
        sql.commit()
    except Exception as e:
        return "user already exist"
