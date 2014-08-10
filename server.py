from flask import Flask
from flask import redirect
from flask.ext.sqlalchemy import SQLAlchemy

from models import Account
from models import Transaction

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


@app.route('/user/<id>')
def user(id):
    return '<pre>' + str(Account.query.filter_by(id=id).first()) + '</pre>'


@app.route('/create/<name>/<balance>')
def create(name, balance):
    account = Account(name, balance)
    db.session.add(account)
    db.session.commit()
    return redirect('/user/%d' % account.id, code=302)


if __name__ == '__main__':
    app.run()
