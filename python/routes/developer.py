from flask import Blueprint, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from utils.db import db, Developer, License, Asset, developer_assets, developer_licenses
import json

developersRouter = Blueprint('developers', __name__, url_prefix='/developers')


@developersRouter.route('/add', methods=['POST'])
@login_required
def add():
    # Get the JSON data from the request body
    data = json.loads(request.data)

    # Retrieve the name and active status from the JSON data
    fullname = data.get('fullname')
    active = data.get('active', False)

    # Create a new developer object with the retrieved data
    developer = Developer(fullname=fullname, active=active)

    # Add the developer to the database session and commit the changes
    db.session.add(developer)
    db.session.commit()

    # Redirect the user to the developers list page
    return redirect(url_for('developers.list'))


@developersRouter.route('/', methods=['GET'])
def list():
    developers = Developer.query.all()
    developers_list = []
    for developer in developers:
        developer_dict = {
            'id': developer.id,
            'fullname': developer.fullname,
            'active': developer.active
        }
        assets = developer.assets
        if assets:
            asset_list = []
            for asset in assets:
                asset_dict = {
                    'id': asset.id,
                    'brand': asset.brand,
                    'model': asset.model,
                    'type': asset.type
                    # add other attributes as needed
                }
                asset_list.append(asset_dict)
            developer_dict['assets'] = asset_list
        licenses = developer.licenses
        if licenses:
            license_list = []
            for license in licenses:
                license_dict = {
                    'id': license.id,
                    'software': license.software,
                }
                license_list.append(license_dict)
            developer_dict['licenses'] = license_list
        developers_list.append(developer_dict)
    return jsonify(developers_list)


@developersRouter.route('/<int:id>', methods=['GET'])
def get(id):
    developer = Developer.query.get(id)
    if developer:
        developer_dict = {
            'id': developer.id,
            'fullname': developer.fullname,
            'active': developer.active
        }

        # check if 'property' query param is present and has a valid value
        property_value = request.args.get('property')
        if property_value == 'asset':
            assets = developer.assets
            if assets:
                asset_list = []
                for asset in assets:
                    asset_dict = {
                        'id': asset.id,
                        'brand': asset.brand,
                        'model': asset.model,
                        'type': asset.type
                        # add other attributes as needed
                    }
                    asset_list.append(asset_dict)
                developer_dict['assets'] = asset_list
            else:
                developer_dict['assets'] = []

        elif property_value == 'license':
            licenses = developer.licenses
            if licenses:
                license_list = []
                for license in licenses:
                    license_dict = {
                        'id': license.id,
                        'software': license.software,
                    }
                    license_list.append(license_dict)
                developer_dict['licenses'] = license_list
            else:
                developer_dict['licenses'] = []

        # if 'property' query param is empty or invalid, return all details
        else:
            assets = developer.assets
            if assets:
                asset_list = []
                for asset in assets:
                    asset_dict = {
                        'id': asset.id,
                        'brand': asset.brand,
                        'model': asset.model,
                        'type': asset.type
                        # add other attributes as needed
                    }
                    asset_list.append(asset_dict)
                developer_dict['assets'] = asset_list
            licenses = developer.licenses
            if licenses:
                license_list = []
                for license in licenses:
                    license_dict = {
                        'id': license.id,
                        'software': license.software,
                    }
                    license_list.append(license_dict)
                developer_dict['licenses'] = license_list

        return jsonify(developer_dict)
    else:
        return jsonify({'message': 'Developer not found'})


@developersRouter.route('/deactivate/<int:id>', methods=['POST'])
def deactivate(id):
    # Find the developer in the database
    developer = Developer.query.get(id)

    if developer:
        # Set the developer as inactive
        developer.active = False

        # Remove the developer's licenses
        licenses = License.query.join(developer_licenses).\
            filter(developer_licenses.c.developer_id == id).all()
        if licenses:
            for license in licenses:
                db.session.delete(license)

        # Remove the developer's assets
        assets = Asset.query.join(developer_assets).\
            filter(developer_assets.c.developer_id == id).all()
        if assets:
            for asset in assets:
                db.session.delete(asset)

        # Save the changes to the database
        db.session.commit()

        flash('Developer deactivated successfully', 'success')
    else:
        flash('Developer not found', 'danger')

    return redirect(url_for('developers.list'))


@developersRouter.route('/addassets/<int:id>', methods=['POST'])
def add_assets(id):
    # Find the developer in the database
    developer = Developer.query.get(id)

    if developer:
        # Get the asset ids from the request JSON data
        data = request.get_json()
        asset_ids = data.get('assets')

        # Add the assets to the developer
        for asset_id in asset_ids:
            asset = Asset.query.get(asset_id)
            if asset:
                developer.assets.append(asset)

        # Save the changes to the database
        db.session.commit()

        return jsonify({'success': True, 'message': 'Assets added successfully'})
    else:
        return jsonify({'success': False, 'message': 'Developer not found'})


@developersRouter.route('/addlicenses/<int:id>', methods=['POST'])
def add_licenses(id):
    # Find the developer in the database
    developer = Developer.query.get(id)

    if developer:
        # Get the license ids from the request JSON data
        data = request.get_json()
        license_ids = data.get('licenses')

        # Add the licenses to the developer
        for license_id in license_ids:
            license = License.query.get(license_id)
            if license:
                developer.licenses.append(license)

        # Save the changes to the database
        db.session.commit()

        return jsonify({'success': True, 'message': 'Licenses added successfully'})
    else:
        return jsonify({'success': False, 'message': 'Developer not found'})


@developersRouter.route('/removeassets/<int:id>', methods=['POST'])
def remove_assets(id):
    # Find the developer in the database
    developer = Developer.query.get(id)

    if developer:
        # Get the asset ids from the request JSON data
        data = request.get_json()
        asset_ids = data.get('assets')

        # Remove the assets from the developer
        for asset_id in asset_ids:
            asset = Asset.query.get(asset_id)
            if asset and asset in developer.assets:
                developer.assets.remove(asset)

        # Save the changes to the database
        db.session.commit()

        return jsonify({'success': True, 'message': 'Assets removed successfully'})
    else:
        return jsonify({'success': False, 'message': 'Developer not found'})


@developersRouter.route('/removelicenses/<int:id>', methods=['POST'])
def remove_licenses(id):
    # Find the developer in the database
    developer = Developer.query.get(id)

    if developer:
        # Get the license ids from the request JSON data
        data = request.get_json()
        license_ids = data.get('licenses')

        # Remove the licenses from the developer
        for license_id in license_ids:
            license = License.query.get(license_id)
            if license and license in developer.licenses:
                developer.licenses.remove(license)

        # Save the changes to the database
        db.session.commit()

        return jsonify({'success': True, 'message': 'Licenses removed successfully'})
    else:
        return jsonify({'success': False, 'message': 'Developer not found'})
