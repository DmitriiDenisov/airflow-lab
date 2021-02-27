# coding=utf-8

from sqlalchemy import Column, Integer, Float, DateTime

from utils import Base


class Stats(Base):
    __tablename__ = 'stats'

    id = Column(Integer, primary_key=True)
    num_custs = Column(Integer)
    num_tokens = Column(Integer)
    count_transactions = Column(Integer)
    sum_transactions_aed = Column(Float)
    sum_transactions_usd = Column(Float)
    sum_transactions_eur = Column(Float)
    max_transaction_aed = Column(Float)
    max_transaction_usd = Column(Float)
    max_transaction_eur = Column(Float)
    sum_balances_aed = Column(Float)
    sum_balances_usd = Column(Float)
    sum_balances_eur = Column(Float)
    date = Column(DateTime)

    def __init__(self, num_custs, num_tokens, count_transactions, sum_transactions_aed, sum_transactions_usd,
                 sum_transactions_eur, max_transaction_aed, max_transaction_usd, max_transaction_eur,
                 sum_balances_aed, sum_balances_usd, sum_balances_eur, date
                 ):
        self.num_custs = num_custs
        self.num_tokens = num_tokens
        self.count_transactions = count_transactions
        self.sum_transactions_aed = sum_transactions_aed
        self.sum_transactions_usd = sum_transactions_usd
        self.sum_transactions_eur = sum_transactions_eur
        self.max_transaction_aed = max_transaction_aed
        self.max_transaction_usd = max_transaction_usd
        self.max_transaction_eur = max_transaction_eur
        self.sum_balances_aed = sum_balances_aed
        self.sum_balances_usd = sum_balances_usd
        self.sum_balances_eur = sum_balances_eur
        self.date = date
