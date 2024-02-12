import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime, Date, create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("sqlite:///darbuotojai.db")

Base = declarative_base()


class Darbuotojas(Base):

    __tablename__ = "Darbuotojai"
    id = Column(Integer, primary_key=True)
    vardas = Column("Vardas", String)
    pavarde = Column("Pavarde", String)
    gimimo_data = Column("Gimimo Data", Date)
    pareigos = Column("Pareigos", String)
    atlyginimas = Column("Atlyginimas", Float)
    created_date = Column("Sukurimo data", DateTime, default=datetime.datetime.now)

    def __init__(self, vardas, pavarde, gimimo_data, pareigos, atlyginimas):

        self.vardas = vardas
        self.pavarde = pavarde
        self.gimimo_data = gimimo_data
        self.pareigos = pareigos
        self.atlyginimas = atlyginimas

    def __repr__(self):
        return f"ID: {self.id} Vardas: {self.vardas}, Pavarde: {self.pavarde}, Gimimo data:" \
               f" {self.gimimo_data}, Pareigos: {self.pareigos}, Atlyginimas: {self.atlyginimas}"


Base.metadata.create_all(engine)
