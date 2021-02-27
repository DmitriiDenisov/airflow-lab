from sqlalchemy import Column, String, Integer, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, ForeignKey

Base = declarative_base()


class DailyRate(Base):
    __tablename__ = 'daily_rates'

    id = Column(Integer, primary_key=True)
    aed = Column(Float)
    usd = Column(Float)
    eur = Column(Float)
    date = Column(DateTime)

    def __init__(self, aed, usd, eur, date):
        self.aed = aed
        self.usd = usd
        self.eur = eur
        self.date = date

