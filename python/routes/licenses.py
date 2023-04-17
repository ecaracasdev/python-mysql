from flask import Blueprint, render_template, request, redirect, url_for
from utils.db import db, License

licensesRouter = Blueprint('licenses', __name__, url_prefix='/licenses')


@licensesRouter.route('/add', methods=['POST'])
def add():
    software = request.form['software']
    new_license = License(software=software)
    db.session.add(new_license)
    db.session.commit()

    return redirect(url_for('licenses.list'))


@licensesRouter.route('/')
def list():
    licenses = License.query.all()
    return render_template('licensesList.html', licenses=licenses)


@licensesRouter.route('/<int:id>/delete')
def delete(id):
    license = License.query.get_or_404(id)
    db.session.delete(license)
    db.session.commit()
    return redirect(url_for('licenses.list'))
