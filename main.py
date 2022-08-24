import connexion as connexion
from database import db
from ma import ma

connexion_app = connexion.FlaskApp(__name__, specification_dir='openapi/')
app = connexion_app.app
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1234sally@localhost:3306/coffeshop'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'


@app.before_first_request
def before_request_func():
    db.create_all()


if __name__ == "__main__":
    db.init_app(app)
    ma.init_app(app)
    connexion_app.add_api('coffeshop.yaml')
    app.run(debug=True, host='0.0.0.0')
    
    
