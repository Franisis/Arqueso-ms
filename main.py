from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table, types
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from databases import Database
from sqlalchemy.sql import select
from datetime import date
from sqlalchemy.orm import Session, sessionmaker
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI() #instancia de la aplicación

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

USERNAME = 'jumafe2'
PASSWORD = 'isis2503'
NAME_MEW = '10.128.0.4'
NAME_DB = 'citas_db'
DATABASE_URL = f"postgresql://{USERNAME}:{PASSWORD}@{NAME_MEW}:5432/{NAME_DB}"

Base = declarative_base()
metadata=MetaData()
database = Database(DATABASE_URL)
engine = create_engine(DATABASE_URL)

Session = sessionmaker(bind=engine)
session = Session()

async def startup_db():
    try:
        await database.connect()
        return database
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        raise

def shutdown():
    return database.disconnect()

app.add_event_handler("startup", startup_db)
#app.add_event_handler("shutdown", shutdown)



class Cita(BaseModel):
    #__tablename__ = 'citas'
    #id = int
    paciente = str
    medico = str
    fecha = str
    nota : str


citas_table = Table(
    "citas",
    metadata,
    Column('id', Integer, primary_key=True),
    Column('paciente', String(50)),
    Column('medico', String(50)),
    Column('fecha', String(50)),
    Column("nota", String(100)),
    
)

Base.metadata.create_all(bind=engine)

@app.get('/')
def message():
    return "Rasi Medical"


@app.get('/citas')
async def getCitas():
    query = select(citas_table)
    citas = await database.fetch_all(query)
    return citas

@app.get('/citas/{}')
def getcitaby(algo):
    pass

#citas/?cualquierCosa como cedula o fecha o doctor que atiende

@app.get('/health-check/', status_code=200)
def getHC():
    return "ok"

session.add
"""
------------------------------------------------
funciones relacionadas al create Cita (POST)
"""
def create_post(db: Session, post: Cita):
    db_post = Cita(
        fecha=post.fecha,
        medico=post.medico,
        paciente=post.paciente,
        nota=post.nota
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    

@app.post('/citas/')
async def createCita(post: Cita):
    create_post(db=session, post=post)
    return "Clean"
@app.get('/citas/{}')
def getCitasbysomeshit(someshit):
    #return list(filter(lambda item['someshit'] == stock, products))
    pass