from extensions import db
from flask_login import UserMixin
from datetime import datetime

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, unique=True)
    description = db.Column(db.String(255))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)  
    full_name = db.Column(db.String(120), nullable=False, server_default="Default Name")
    department_id= db.Column(db.Integer, db.ForeignKey('department.id'))
    department = db.relationship('Department', backref='users')

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, unique=True)
    description = db.Column(db.String(255))

class AssetCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, unique=True)
    description = db.Column(db.String(255))
class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, unique=True)
    description = db.Column(db.String(255))
    category_id = db.Column(db.Integer, db.ForeignKey('asset_category.id'), nullable=False)
    category = db.relationship('AssetCategory', backref='assets')
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    location = db.relationship('Location', backref='assets')
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    department = db.relationship('Department', backref='assets')
    serial_number = db.Column(db.String(100),  unique=True)
    status = db.Column(db.String(50))
    purchase_date = db.Column(db.Date)
    warranty_expiry = db.Column(db.Date)
    disposal_reason = db.Column(db.String(255))
    disposal_method = db.Column(db.String(100))  # e.g., Sold, Donated, Scrapped
    is_disposed = db.Column(db.Boolean, default=False)
    purchase_cost = db.Column(db.Float)
    salvage_value = db.Column(db.Float)
    useful_life = db.Column(db.Integer)  
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    owner = db.relationship('User', backref='assets')





class AssetAssignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('asset.id'), nullable=False)
    asset = db.relationship('Asset', backref='assignments')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='assignments')
    date_assigned = db.Column(db.Date, nullable=False )
    return_date = db.Column(db.Date)
    status = db.Column(db.String(50))# e.g., 'assigned', 'returned', 'lost'

class MaintenanceLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('asset.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(255))
    cost = db.Column(db.Float)
    service_provider = db.Column(db.String(100))
    status = db.Column(db.String(50))  # e.g., Scheduled, Completed, Pending

    asset = db.relationship('Asset', backref='maintenance_logs')

class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    action = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    target_type = db.Column(db.String(50))  # e.g., 'Asset', 'User'
    target_id = db.Column(db.Integer)

    user = db.relationship('User', backref='audit_logs')   

    

