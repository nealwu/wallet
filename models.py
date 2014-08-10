from datetime import datetime

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    balance = db.Column(db.Integer) # in cents
    created_at = db.Column(db.DateTime)

    def __init__(self, name, balance=0, created_at=None):
        self.name = name
        self.balance = balance

        if created_at is None:
            created_at = datetime.now()

        self.created_at = created_at

    def __repr__(self):
        return '[Account for %r with balance %r]' % (self.name, self.balance)


# class Consumer(Account):
#     fb_auth = ...


# class Merchant(Account):


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    from_account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    from_account = db.relationship('Account',
        backref=db.backref('sent_transactions', lazy='dynamic'),
        foreign_keys=[from_account_id])

    to_account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    to_account = db.relationship('Account',
        backref=db.backref('received_transactions', lazy='dynamic'),
        foreign_keys=[to_account_id])

    amount = db.Column(db.Integer)
    description = db.Column(db.String(255))
    time = db.Column(db.DateTime)

    def __init__(self, from_account, to_account, amount, description='', time=None):
        self.from_account = from_account
        self.to_account = to_account
        self.amount = amount
        self.description = description

        if time is None:
            time = datetime.now()

        self.time = time

    def __repr__(self):
        return '[Transaction from %r to %r for %r]' % (self.from_account, self.to_account, self.amount)


def execute(transaction):
    if transaction.from_account.balance < transaction.amount:
        return False

    transaction.from_account.balance -= transaction.amount
    transaction.to_account.balance += transaction.amount
    transaction.time = datetime.now()
    return True


db.create_all()
