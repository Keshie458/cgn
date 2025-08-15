from flask import Blueprint, render_template, request, redirect, url_for
from extensions import db
from models import AssetCategory

categories_bp = Blueprint('categories', __name__)

@categories_bp.route('/categories', methods=['GET', 'POST'])
def manage_categories():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        new_cat = AssetCategory(name=name, description=description)
        db.session.add(new_cat)
        db.session.commit()
        return redirect(url_for('categories.manage_categories'))

    categories = AssetCategory.query.all()
    return render_template('categories.html', categories=categories)
@categories_bp.route('/categories/edit/<int:id>', methods=['GET', 'POST'])
def edit_category(id):
    category = AssetCategory.query.get_or_404(id)

    if request.method == 'POST':
        category.name = request.form['name']
        category.description = request.form['description']
        db.session.commit()
        return redirect(url_for('categories.manage_categories'))

    return render_template('edit_category.html', category=category)


@categories_bp.route('/categories/delete/<int:id>', methods=['POST'])
def delete_category(id):
    category = AssetCategory.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for('categories.manage_categories'))