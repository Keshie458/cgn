from flask import Blueprint, render_template
from flask_login import login_required
from datetime import date
from models import Asset  
from extensions import db

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
#@login_required
def dashboard():
    today = date.today()

    total_assets = Asset.query.count()
    in_use = Asset.query.filter_by(status='In Use').count()
    under_repair = Asset.query.filter_by(status='Under Repair').count()
    disposed = Asset.query.filter_by(is_disposed=True).count()

    warranty_expiring_soon = Asset.query.filter(
        Asset.warranty_expiry <= today.replace(month=today.month + 1)
    ).count()

    return render_template('dashboard.html', summary={
        'total': total_assets,
        'in_use': in_use,
        'repair': under_repair,
        'disposed': disposed,
        'warranty_expiring': warranty_expiring_soon
    })