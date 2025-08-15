# utils/export.py
import csv
from io import StringIO
from flask import Response

def export_departments_csv(departments):
    si = StringIO()
    writer = csv.writer(si)
    writer.writerow(['Name', 'Description'])  # Header
    for dept in departments:
        writer.writerow([dept.name, dept.description])
    
    output = Response(si.getvalue(), mimetype='text/csv')
    output.headers['Content-Disposition'] = 'attachment; filename=departments.csv'
    return output