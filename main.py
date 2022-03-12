# from dataclasses import replace
from fastapi import FastAPI,HTTPException
# import pandas as pd
# import json
from pydantic import BaseModel
import sqlite3
# from typing import Optional

# --
app=FastAPI()

class Database:
    def __init__(self,dbname='student.db'):
        self.db_connection = sqlite3.connect(dbname)
    
    def execute(self,query):
        db_cusrsor = self.db_connection.cursor()
        result = db_cusrsor.execute(query).fetchall()
        db_cusrsor.close()
        self.db_connection.commit()
        return result

DB=Database()
DB.execute('CREATE TABLE IF NOT EXISTS students (name STRING PRIMARY KEY, lesson1 INTEGER, lesson2 INTEGER, lesson3 INTEGER)')

# df.execute("INSERT INTO number (name, number1, number2) VALUES ('yalda',12,15)")
# conn.commit()
class student(BaseModel):
    name: str
    lesson1: float
    lesson2: float 
    lesson3: float 

@app.get('/')
def read():
    DB=Database()
    students = DB.execute('SELECT * FROM students')
    return students

@app.get('/average')
def average():
    DB=Database()
    result = DB.execute('SELECT name,(lesson1+lesson2 +lesson3 )/3 as average FROM students')
    return result

# ====================================================

@app.post('/insert/')
def insert(student:student):
    DB = Database()
    result = DB.execute(f'SELECT * FROM students WHERE name="{student.name}"')
    if len(result)>0:
        raise HTTPException(status_code=404,detail='This student is available')
    else:
        # df.loc[len(df['name'])]=[student.name,student.number1,student.number2]
        DB.execute(f'INSERT INTO students VALUES ("{student.name}", {student.lesson1}, {student.lesson2},{student.lesson3})')
        return student

    #     df_json = df.to_json(orient='records')
    #     return json.loads(df_json)

# =======================================================
@app.put('/update/{name}')
def update(name:str):
    DB = Database()
    result = DB.execute(f'SELECT * FROM students WHERE name="{name}"')
    if len(result)>0:
        DB.execute(f'UPDATE students SET lesson1 = lesson1+1, lesson2 = lesson2+1, lesson3 = lesson3+1 WHERE name="{name}"')
        return result
    else:
        raise HTTPException(status_code=404,detail='This student is not available')


@app.delete('/delete/{name}')
def delete(name:str):
    DB = Database()
    result = DB.execute(f'SELECT * FROM students WHERE name="{name}"')
    if len(result)>0:
        DB.execute(f'DELETE FROM students WHERE name="{name}"')
    else:
        raise HTTPException(status_code=404,detail='This student is not available')













