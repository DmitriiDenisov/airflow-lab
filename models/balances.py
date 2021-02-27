# coding=utf-8

from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship, backref
from models.customer import Customer
from utils import Base


class Balance(Base):
    __tablename__ = 'balances'

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    # Relationship means that python object will have separate field which is connected to value from another table
    # backref means that in Customer
    customer = relationship("Customer", backref=backref("bal", uselist=False))
    usd_amt = Column(Float)
    eur_amt = Column(Float)
    aed_amt = Column(Float)

    def __init__(self, customer, usd_amt, eur_amt, aed_amt):
        self.customer = customer
        self.usd_amt = usd_amt
        self.eur_amt = eur_amt
        self.aed_amt = aed_amt
