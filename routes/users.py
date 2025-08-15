from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from werkzeug.security import generate_password_hash
from utils.audit import log_action
from extensions import db
from models import User, Department

users_bp = Blueprint('users', __name__)
@users_bp.route('/users/create', methods=['GET', 'POST'])
@login_required
def create_user():
   if current_user.role != 'Admin':
       flash('Only admins can create users.',)
       return redirect(url_for('assets.manage_assets'))
   departments = Department.query.all()
   if request.method == 'POST':
       new_user = User(
              username=request.form['username'],
                password=generate_password_hash(request.form['password']),
                role=request.form['role'],
                department_id=request.form['department_id'])
       db.session.add(new_user)
       db.session.commit()
       log_action('Created user', target_type='User', target_id=new_user.id)
       flash('User created successfully!')
       return redirect(url_for('users.create_user'))
   return render_template('create_user.html', departments=departments)
       

@users_bp.route('/users', methods=['GET', 'POST'])
@login_required
def manage_users():
    if current_user.role != 'Admin':
        flash('Only admins can manage users.')
        return redirect(url_for('assets.manage_assets'))
    departments = Department.query.all()
   
   
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']  # For now, we’ll keep it raw (add hashing later)
        role = request.form['role']
        department_id = request.form['department_id']

        hashed_password = generate_password_hash(password)

        new_user = User(username=username, password=hashed_password, role=role, department_id=department_id)
        db.session.add(new_user)
        db.session.commit()
        log_action('Created user', target_type='User', target_id=new_user.id)
        flash('User created successfully!')
        return redirect(url_for('users.manage_users'))

    query = User.query

    search=request.args.get('search')
    role_filter = request.args.get('role')
    dept_filter = request.args.get('department_id')

    if search:
        query = query.filter(User.username.ilike(f'%{search}%'))
    if role_filter:
        query = query.filter_by(role=role_filter)
    if dept_filter:
        query = query.filter_by(department_id=dept_filter)

    users = query.all()
    return render_template('users.html', users=users, departments=departments, search=search, role_filter=role_filter, dept_filter=dept_filter)

@users_bp.route('/users/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    if current_user.role != 'Admin':
        flash('Only admins can edit users.')
        return redirect(url_for('assets.manage_assets'))
    user = User.query.get_or_404(id)
    departments = Department.query.all()

    if request.method == 'POST':
        user.username = request.form['username']
        user.password = request.form['password']
        user.role = request.form['role']
        user.department_id = request.form['department_id']

        new_password = request.form['password']
        if new_password:
            user.password = generate_password_hash(new_password)
        db.session.commit()
        log_action('Edited user', target_type='User', target_id=user.id)
        flash('User updated successfully!')
        return redirect(url_for('users.manage_users'))

    return render_template('edit_user.html', user=user, departments=departments)


@users_bp.route('/users/delete/<int:id>', methods=['POST'])
@login_required
def delete_user(id):
    if current_user.role != 'Admin':
        flash('Only admins can delete users.')
        return redirect(url_for('assets.manage_assets'))
    
    
    user = User.query.get_or_404(id)
    if user.id == current_user.id:
        flash('You cannot delete your own account.')
        return redirect(url_for('users.manage_users'))
    db.session.delete(user)
    db.session.commit()
    log_action('Deleted user', target_type='User', target_id=user.id)
    flash('User deleted successfully!')
    return redirect(url_for('users.manage_users'))

@users_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        current = request.form['current_password']
        new = request.form['new_password']
        confirm = request.form['confirm_password']

        if not current_user.check_password(current):
            flash('Current password is incorrect.')
            return redirect(url_for('users.change_password'))

        if new != confirm:
            flash('New passwords do not match.')
            return redirect(url_for('users.change_password'))

        current_user.password = generate_password_hash(new)
        db.session.commit()

        log_action('Changed own password', target_type='User', target_id=current_user.id)
        flash('Password updated successfully.')
        return redirect(url_for('assets.manage_assets'))

    return render_template('change_password.html')