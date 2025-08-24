from flask import Flask, render_template
from extensions import db
from routes.departments import departments_bp
from routes.users import users_bp
from routes.locations import locations_bp
from routes.categories import categories_bp
from routes.assets import assets_bp
from routes.assignments import assignments_bp
from routes.maintenance import maintenance_bp
from extensions import login_manager
from routes.dashboard import dashboard_bp
from models import User
from routes.auth import auth_bp
from flask_migrate import Migrate
from datetime import timedelta
from routes.categories import categories_bp
 

app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ams.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PERMANENT_SESSION_LIFETIME']=timedelta(minutes=30)
app.config['SECRET_KEY'] = 'secretcgnamskey' 

db.init_app(app)
login_manager.init_app(app)

migrate = Migrate(app, db)
from models import Department

app.register_blueprint(departments_bp)
app.register_blueprint(users_bp)
app.register_blueprint(locations_bp)
app.register_blueprint(categories_bp)
app.register_blueprint(assets_bp)
app.register_blueprint(assignments_bp)
app.register_blueprint(maintenance_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
#@app.route('/dashboard')
#def test_dashboard():
#    return "Dashboard is working!"
if __name__ == '__main__':
    app.run(debug=True)