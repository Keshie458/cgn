from flask import Blueprint, render_template, request, redirect, url_for
from extensions import db
from models import MaintenanceLog, Asset
from datetime import datetime

maintenance_bp = Blueprint('maintenance', __name__)

@maintenance_bp.route('/maintenance', methods=['GET', 'POST'])
def manage_maintenance():
    assets = Asset.query.all()

    if request.method == 'POST':
        log = MaintenanceLog(
            asset_id=request.form['asset_id'],
            date=datetime.strptime(request.form['date'], '%Y-%m-%d'),
            description=request.form['description'],
            cost=float(request.form['cost']) if request.form['cost'] else 0.0,
            service_provider=request.form['service_provider'],
            status=request.form['status']
        )
        db.session.add(log)
        db.session.commit()
        return redirect(url_for('maintenance.manage_maintenance'))

    logs = MaintenanceLog.query.order_by(MaintenanceLog.date.desc()).all()
    return render_template('maintenance.html', logs=logs, assets=assets)
@maintenance_bp.route('/maintenance/edit/<int:id>', methods=['GET', 'POST'])
def edit_maintenance(id):
    log = MaintenanceLog.query.get_or_404(id)
    assets = Asset.query.all()

    if request.method == 'POST':
        log.asset_id = request.form['asset_id']
        log.date = datetime.strptime(request.form['date'], '%Y-%m-%d')
        log.description = request.form['description']
        log.cost = float(request.form['cost']) if request.form['cost'] else 0.0
        log.service_provider = request.form['service_provider']
        log.status = request.form['status']
        db.session.commit()
        return redirect(url_for('maintenance.manage_maintenance'))

    return render_template('edit_maintenance.html', log=log, assets=assets)


@maintenance_bp.route('/maintenance/delete/<int:id>', methods=['POST'])
def delete_maintenance(id):
    log = MaintenanceLog.query.get_or_404(id)
    db.session.delete(log)
    db.session.commit()
    return redirect(url_for('maintenance.manage_maintenance'))