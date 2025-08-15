# routes/departments.py

from flask import Blueprint, render_template, request, redirect, url_for
from extensions import db
from models import Department
from utils.export import export_departments_csv

departments_bp = Blueprint('departments', __name__)

@departments_bp.route('/departments', methods=['GET', 'POST'])
def manage_departments():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')

        if name:
            new_department = Department(name=name, description=description)
            db.session.add(new_department)
            db.session.commit()
            return redirect(url_for('departments.manage_departments'))
    search_query = request.args.get('search')
    if search_query:
        all_departments = Department.query.filter(Department.name.ilike(search_query)).all()
    else:
        departments= Department.query.all()

    
    return render_template('departments.html', departments=departments, search_query=search_query)
@departments_bp.route('/departments/edit/<int:id>', methods=['GET', 'POST'])
def edit_department(id):
    department = Department.query.get_or_404(id)
    if request.method == 'POST':
        department.name = request.form.get('name')
        department.description = request.form.get('description')
        db.session.commit()
        return redirect(url_for('departments.manage_departments'))
    return render_template('edit_department.html', department=department)
@departments_bp.route('/departments/delete/<int:id>', methods=['POST'])
def delete_department(id):
    department = Department.query.get_or_404(id)
    db.session.delete(department)
    db.session.commit()
    return redirect(url_for('departments.manage_departments'))
@departments_bp.route('/departments/export/csv')
def export_csv():
    departments = Department.query.all()
    return export_departments_csv(departments)