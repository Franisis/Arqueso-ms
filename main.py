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
app.add_event_handler("shutdown", shutdown)


class Cita(BaseModel):
    __tablename__ = 'citas'

    #id = Column(Integer, primary_key=True, index=True)
    #id = int
    #paciente = Column(String, index=True)
    paciente : str
    #medico = Column(String, index=True)
    medico : str
    #fecha = Column(String)
    fecha : date
    #nota = Column(String)
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
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)
session = Session()

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

"""
------------------------------------------------
funciones relacionadas al create Cita (POST)
"""
def create_post(db: Session, post: Cita):
    db_post = Cita(**post.model_dump)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


@app.post('/citasCreate')
async def createCita(post: Cita):
    cita = create_post(session, post)
    response = {'id':cita.id,
                'paciente': cita.paciente,
                'medico':cita.medico,
                'fecha': cita.fecha,
                'nota': cita.nota
                }
    
    return "Added succesfully"
    


@app.get('/citas/{}')
def getCitasbysomeshit(someshit):
    #return list(filter(lambda item['someshit'] == stock, products))
    pass