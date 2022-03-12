from fastapi import FastAPI,HTTPException
# import pandas as pd
from pydantic import BaseModel
import sqlite3
import requests


app = FastAPI()
app2=FastAPI()

class Database:
    def __init__(self,dbname='student.db'):
        self.db_connection = sqlite3.connect(dbname)
    
    def execute(self,query):
        db_cursor = self.db_connection.cursor()
        result = db_cursor.execute(query).fetchall()
        db_cursor.close()
        self.db_connection.commit()
        return result

DB=Database()
DB.execute("""
            CREATE TABLE IF NOT EXISTS students 
            (name STRING PRIMARY KEY,
            lesson1 INTEGER, 
            lesson2 INTEGER, 
            lesson3 INTEGER)
""")


class Student(BaseModel):
    name: str
    lesson1: float
    lesson2: float 
    lesson3: float 

@app.get('/')
def read():
    DB = Database()
    students = DB.execute('SELECT * FROM students')
    return students

@app.get('/average')
def average():
    DB = Database()
    result = DB.execute("""
                SELECT name, 
                (lesson1+ lesson2+ lesson3 )/3 
                as average FROM students
    """)
    return result

# ====================================================

@app.post('/insert/')
def insert(student:Student):
    DB = Database()
    result = DB.execute(f'SELECT * FROM students WHERE name="{student.name}"')
    if len(result)>0:
        raise HTTPException(status_code=404,detail='This student is available')
    else:
        DB.execute(
            f'INSERT INTO students VALUES \
            ("{student.name}", {student.lesson1}, \
            {student.lesson2},{student.lesson3})')
        return student

# =======================================================
@app.put('/update/{name}')
def update(name:str):
    DB = Database()
    result = DB.execute(f'SELECT * FROM students WHERE name="{name}"')
    if len(result)>0:
        DB.execute(
            f'UPDATE students SET lesson1 = lesson1+1, \
             lesson2 = lesson2+1, lesson3 = lesson3+1 WHERE name="{name}"')
        return result
    else:
        raise HTTPException(status_code=404,detail='This student is not available')

# ===========================================================
@app.delete('/delete/{name}')
def delete(name:str):
    DB = Database()
    result = DB.execute(f'SELECT * FROM students WHERE name="{name}"')
    if len(result)>0:
        DB.execute(f'DELETE FROM students WHERE name="{name}"')
    else:
        raise HTTPException(status_code=404,detail='This student is not available')




@app2.get('/')
def read_app2():
    return {'msg':'App 2'}


@app2.get('/avg')
def avg():
    result=requests.get('https://shrouded-cliffs-86202.herokuapp.com/average')
    return result.json()








