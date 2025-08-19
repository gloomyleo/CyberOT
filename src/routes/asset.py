from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.asset import Asset

asset_bp = Blueprint('asset', __name__)

@asset_bp.route('/assets', methods=['GET'])
def get_assets():
    """Get all assets"""
    try:
        assets = Asset.query.all()
        return jsonify([asset.to_dict() for asset in assets])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@asset_bp.route('/assets/<int:asset_id>', methods=['GET'])
def get_asset(asset_id):
    """Get a specific asset"""
    try:
        asset = Asset.query.get_or_404(asset_id)
        return jsonify(asset.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@asset_bp.route('/assets', methods=['POST'])
def create_asset():
    """Create a new asset"""
    try:
        data = request.get_json()
        
        asset = Asset(
            name=data.get('name'),
            asset_type=data.get('asset_type'),
            manufacturer=data.get('manufacturer'),
            model=data.get('model'),
            serial_number=data.get('serial_number'),
            ip_address=data.get('ip_address'),
            location=data.get('location'),
            criticality=data.get('criticality'),
            status=data.get('status', 'Active'),
            description=data.get('description')
        )
        
        db.session.add(asset)
        db.session.commit()
        
        return jsonify(asset.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@asset_bp.route('/assets/<int:asset_id>', methods=['PUT'])
def update_asset(asset_id):
    """Update an existing asset"""
    try:
        asset = Asset.query.get_or_404(asset_id)
        data = request.get_json()
        
        asset.name = data.get('name', asset.name)
        asset.asset_type = data.get('asset_type', asset.asset_type)
        asset.manufacturer = data.get('manufacturer', asset.manufacturer)
        asset.model = data.get('model', asset.model)
        asset.serial_number = data.get('serial_number', asset.serial_number)
        asset.ip_address = data.get('ip_address', asset.ip_address)
        asset.location = data.get('location', asset.location)
        asset.criticality = data.get('criticality', asset.criticality)
        asset.status = data.get('status', asset.status)
        asset.description = data.get('description', asset.description)
        
        db.session.commit()
        
        return jsonify(asset.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@asset_bp.route('/assets/<int:asset_id>', methods=['DELETE'])
def delete_asset(asset_id):
    """Delete an asset"""
    try:
        asset = Asset.query.get_or_404(asset_id)
        db.session.delete(asset)
        db.session.commit()
        
        return jsonify({'message': 'Asset deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@asset_bp.route('/assets/stats', methods=['GET'])
def get_asset_stats():
    """Get asset statistics"""
    try:
        total_assets = Asset.query.count()
        critical_assets = Asset.query.filter_by(criticality='Critical').count()
        high_assets = Asset.query.filter_by(criticality='High').count()
        medium_assets = Asset.query.filter_by(criticality='Medium').count()
        low_assets = Asset.query.filter_by(criticality='Low').count()
        
        active_assets = Asset.query.filter_by(status='Active').count()
        inactive_assets = Asset.query.filter_by(status='Inactive').count()
        
        return jsonify({
            'total_assets': total_assets,
            'by_criticality': {
                'critical': critical_assets,
                'high': high_assets,
                'medium': medium_assets,
                'low': low_assets
            },
            'by_status': {
                'active': active_assets,
                'inactive': inactive_assets
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

