

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable=False,
                            unique=True)

    def __repr__(self):
        return f' Item {self.name}'


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/market')
def market_page():
    items = Item.query.all()
    return render_template('market.html', items=items)


if __name__ == '__main__':
    with app.app_context():
        # Criar todas as tabelas no banco de dados
        db.create_all()

        # Adicionar itens ao banco de dados
        item1 = Item(name="Phone", price=500, barcode='893212299897',
                     description='Description of Phone')
        item2 = Item(name="Laptop", price=900, barcode='123985473165',
                     description='Description of Laptop')
        item3 = Item(name="Keyboard", price=150, barcode='231985128446',
                     description='Description of Keyboard')

        # Verificar se a descrição do item já existe antes de adicioná-lo
        if not Item.query.filter_by(description=item1.description).first():
            db.session.add(item1)

        if not Item.query.filter_by(description=item2.description).first():
            db.session.add(item2)

        if not Item.query.filter_by(description=item3.description).first():
            db.session.add(item3)

        db.session.commit()

    # Executar o aplicativo Flask
    app.run(debug=True)

    if __name__ == '__main__':
        app.run(debug=True)

