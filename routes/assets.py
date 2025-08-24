from flask import Blueprint, render_template, request, redirect, url_for, flash
from extensions import db
from models import Asset, AssetCategory, Department, Location, MaintenanceLog
from utils.depreciation import calculate_depreciation   
from datetime import datetime
from utils.audit import log_action
from flask_login import current_user, login_required


assets_bp = Blueprint('assets', __name__)

@assets_bp.route('/assets', methods=['GET', 'POST'])
# @login_required
def manage_assets():
    categories = AssetCategory.query.all()
    locations = Location.query.all()
    departments = Department.query.all()

    if request.method == 'POST':
        asset = Asset(
            name=request.form['name'],
            description=request.form['description'],
            serial_number=request.form['serial_number'],
            status=request.form['status'],
            category_id=request.form['category_id'],
            location_id=request.form['location_id'],
            department_id=request.form['department_id'],
            purchase_date=datetime.strptime(request.form['purchase_date'], '%Y-%m-%d') if request.form.get('purchase_date') else None,
            warranty_expiry=datetime.strptime(request.form['warranty_expiry'], '%Y-%m-%d') if request.form.get('warranty_expiry') else None
        )
        db.session.add(asset)
        db.session.commit()
        return redirect(url_for('assets.manage_assets'))
    query = Asset.query

    status = request.args.get('status')
    category_id = request.args.get('category_id')
    department_id = request.args.get('department_id')
    include_disposed = request.args.get('include_disposed')

    if status:
        query = query.filter_by(status=status)
    if category_id:
        query = query.filter_by(category_id=category_id)
    if department_id:
        query = query.filter_by(department_id=department_id)
    if not include_disposed:
        query = query.filter_by(is_disposed=False)

    assets = query.all()
    return render_template('assets.html', assets=assets, categories=categories, locations=locations, departments=departments, calculate_depreciation=calculate_depreciation)
@assets_bp.route('/assets/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_asset(id):
    asset = Asset.query.get_or_404(id)
    categories = AssetCategory.query.all()
    locations = Location.query.all()
    departments = Department.query.all()

    if request.method == 'POST':
        asset.name = request.form['name']
        asset.description = request.form['description']
        asset.serial_number = request.form['serial_number']
        asset.status = request.form['status']
        asset.category_id = request.form['category_id']
        asset.location_id = request.form['location_id']
        asset.department_id = request.form['department_id']
        purchase_date = request.form.get('purchase_date')
        warranty_expiry = request.form.get('warranty_expiry')
        asset.purchase_date = datetime.strptime(purchase_date, '%Y-%m-%d') if purchase_date else None
        asset.warranty_expiry = datetime.strptime(warranty_expiry, '%Y-%m-%d') if warranty_expiry else None

        db.session.commit()
        log_action('Edited asset', target_type='Asset', target_id=asset.id)
        flash('Asset updated successfully!')
        return redirect(url_for('assets.manage_assets'))

    return render_template('edit_asset.html', asset=asset, categories=categories, locations=locations, departments=departments)


@assets_bp.route('/assets/delete/<int:id>', methods=['POST'])
def delete_asset(id):
    asset = Asset.query.get_or_404(id)
    db.session.delete(asset)
    db.session.commit()
    return redirect(url_for('assets.manage_assets'))
@assets_bp.route('/assets/<int:id>/history')
def asset_history(id):
    asset = Asset.query.get_or_404(id)
    assignments = asset.assignments  # via backref
    return render_template('asset_history.html', asset=asset, assignments=assignments)
@assets_bp.route('/assets/<int:id>/maintenance')
def asset_maintenance(id):
    asset = Asset.query.get_or_404(id)
    logs = MaintenanceLog.query.filter_by(asset_id=id).order_by(MaintenanceLog.date.desc()).all()
    return render_template('asset_maintenance.html', asset=asset, logs=logs)
@assets_bp.route('/assets/dispose/<int:id>', methods=['GET', 'POST'])
@login_required
def dispose_asset(id):
   
    if current_user.role != 'Admin':
        flash('You do not have permission to dispose of assets.', 'danger')
        return redirect(url_for('assets.manage_assets'))
    asset = Asset.query.get_or_404(id)
    

    if request.method == 'POST':
        asset.disposal_date = datetime.strptime(request.form['disposal_date'], '%Y-%m-%d')
        asset.disposal_reason = request.form['disposal_reason']
        asset.disposal_method = request.form['disposal_method']
        asset.is_disposed = True
        asset.status = 'Disposed'
        db.session.commit()
        flash('Asset disposed successfully!', 'success')
        log_action('Disposed asset', target_type='Asset', target_id=asset.id)
        return redirect(url_for('assets.manage_assets'))

    return render_template('dispose_asset.html', asset=asset)