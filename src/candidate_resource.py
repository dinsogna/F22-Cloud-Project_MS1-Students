import pymysql
import os
from dotenv import load_dotenv


class CandidateResource:

    def __int__(self):
        pass

    @staticmethod
    def _get_connection():

        load_dotenv() 

        usr = os.getenv("DBUSER")
        pw = os.getenv("DBPW")
        h = os.getenv("DBHOST")
        db = os.getenv("DB")

        conn = pymysql.connect(
            user=usr,
            password=pw,
            host=h,
            database=db,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        return conn

    @staticmethod
    def get_by_key(key):

        sql = "SELECT * FROM cloud_project_db.candidates where candidate_id=%s"
        conn = CandidateResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, args=key)
        result = cur.fetchone()

        return result
    
    @staticmethod
    def get_all():  

        sql = "SELECT * FROM cloud_project_db.candidates;"
        conn = CandidateResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql)  
        result = cur.fetchall()

        return result