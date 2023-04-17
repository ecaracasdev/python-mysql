from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from utils.db import db, Asset

assetsRouter = Blueprint('assets', __name__)


@assetsRouter.route('/assets/add', methods=['POST'])
def add():
    brand = request.form['brand']
    model = request.form['model']
    type = request.form['type']

    try:
        type_value = Asset.AssetTypeEnum(type)
    except ValueError:
        return jsonify({'success': False, 'message': 'Invalid type value'}), 400

    new_asset = Asset(brand=brand, model=model, type=type_value)
    db.session.add(new_asset)
    db.session.commit()

    return redirect(url_for('assets.list'))


@assetsRouter.route('/assets')
def list():
    assets = Asset.query.all()
    return render_template('assetsList.html', assets=assets)


@assetsRouter.route('/assets/<int:id>/delete')
def delete(id):
    asset = Asset.query.get_or_404(id)
    db.session.delete(asset)
    db.session.commit()
    return redirect(url_for('assets.list'))
