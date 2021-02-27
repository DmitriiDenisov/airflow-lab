# coding=utf-8

from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from utils import Base


class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    customer_id_from = Column(Integer, ForeignKey('customers.id'))
    customer_id_to = Column(Integer, ForeignKey('customers.id'))

    customer_from = relationship("Customer", foreign_keys=[customer_id_from], backref="trans_from")
    customer_to = relationship("Customer", foreign_keys=[customer_id_to], backref="trans_to")

    usd_amt = Column(Float)
    eur_amt = Column(Float)
    aed_amt = Column(Float)

    def __init__(self, customer_id_from, customer_id_to, usd_amt=0, eur_amt=0, aed_amt=0):
        self.customer_id_from = customer_id_from
        self.customer_id_to = customer_id_to
        self.usd_amt = usd_amt
        self.eur_amt = eur_amt
        self.aed_amt = aed_amt
