from flask import Blueprint, render_template, request, redirect, url_for, flash
from extensions import db
from models import Location

locations_bp = Blueprint('locations', __name__)

@locations_bp.route('/locations', methods=['GET', 'POST'])
def manage_locations():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        new_loc = Location(name=name, description=description)
        db.session.add(new_loc)
        db.session.commit()
        flash('Location added successfully.', 'success')
        return redirect(url_for('locations.manage_locations'))

    locations = Location.query.all()
    return render_template('locations.html', locations=locations)
@locations_bp.route('/locations/edit/<int:id>', methods=['GET', 'POST'])
def edit_location(id):
    location = Location.query.get_or_404(id)

    if request.method == 'POST':
        location.name = request.form['name']
        location.description = request.form['description']
        db.session.commit()
        flash('Location updated successfully.', 'success')
        return redirect(url_for('locations.manage_locations'))

    return render_template('edit_location.html', location=location)

@locations_bp.route('/locations/delete/<int:id>', methods=['POST'])
def delete_location(id):
    location = Location.query.get_or_404(id)
    db.session.delete(location)
    db.session.commit()
    flash('Location deleted successfully.', 'success')
    return redirect(url_for('locations.manage_locations'))
