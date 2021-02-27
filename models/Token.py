# coding=utf-8

from sqlalchemy import Column, String, Integer, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from utils import Base


class Token(Base):
    __tablename__ = 'tokens'

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    token_uuid = Column(String)
    creation_date = Column(DateTime)
    exp_date = Column(DateTime)

    customer = relationship("Customer", backref="token", uselist=False)

    def __init__(self, customer_id, token_uuid, creation_date, exp_date):
        self.customer_id = customer_id
        self.token_uuid = token_uuid
        self.creation_date = creation_date
        self.exp_date = exp_date
