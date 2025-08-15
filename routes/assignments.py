from flask import Blueprint, render_template, request, redirect, url_for
from extensions import db
from models import AssetAssignment, Asset, User, Department
from datetime import datetime
from flask_login import login_required

assignments_bp = Blueprint('assignments', __name__)

@assignments_bp.route('/assignments', methods=['GET', 'POST'])
@login_required
def manage_assignments():
    assets = Asset.query.all()
    users = User.query.all()

    if request.method == 'POST':
        assignment = AssetAssignment(
            asset_id=request.form['asset_id'],
            user_id=request.form['user_id'],
            date_assigned=datetime.strptime(request.form['date_assigned'], '%Y-%m-%d'),
            return_date=datetime.strptime(request.form['return_date'], '%Y-%m-%d') if request.form.get('return_date') else None,
            status=request.form['status']
        )
        db.session.add(assignment)
        db.session.commit()
        return redirect(url_for('assignments.manage_assignments'))

    department_id = request.args.get('department_id')
    status = request.args.get('status')
    query = AssetAssignment.query.join(User).join(Department)

    if department_id:
        query = query.filter(User.department_id == department_id)
    if status:
        query = query.filter(AssetAssignment.status == status)

    assignments = query.all()
    departments = Department.query.all()
    assets = Asset.query.all()
    users = User.query.all()
    return render_template('assignments.html', assignments=assignments, assets=assets, users=users, departments=departments, selected_dpt=department_id, selected_status=status)
@assignments_bp.route('/assignments/edit/<int:id>', methods=['GET', 'POST'])
def edit_assignment(id):
    assignment = AssetAssignment.query.get_or_404(id)
    assets = Asset.query.all()
    users = User.query.all()

    if request.method == 'POST':
        assignment.asset_id = request.form['asset_id']
        assignment.user_id = request.form['user_id']
        assignment.date_assigned = datetime.strptime(request.form['date_assigned'], '%Y-%m-%d')
        return_date = request.form.get('return_date')
        assignment.return_date = datetime.strptime(return_date, '%Y-%m-%d') if return_date else None
        assignment.status = request.form['status']

        db.session.commit()
        return redirect(url_for('assignments.manage_assignments'))

    return render_template('edit_assignment.html', assignment=assignment, assets=assets, users=users)


@assignments_bp.route('/assignments/delete/<int:id>', methods=['POST'])
def delete_assignment(id):
    assignment = AssetAssignment.query.get_or_404(id)
    db.session.delete(assignment)
    db.session.commit()
    return redirect(url_for('assignments.manage_assignments'))