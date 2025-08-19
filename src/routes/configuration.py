from flask import Blueprint, request, jsonify
from datetime import datetime
from src.models.user import db
from src.models.configuration import ConfigurationBaseline, ConfigurationDeviation

configuration_bp = Blueprint('configuration', __name__)

@configuration_bp.route('/configuration-baselines', methods=['GET'])
def get_configuration_baselines():
    """Get all configuration baselines"""
    try:
        baselines = ConfigurationBaseline.query.all()
        return jsonify([baseline.to_dict() for baseline in baselines])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@configuration_bp.route('/configuration-baselines/<int:baseline_id>', methods=['GET'])
def get_configuration_baseline(baseline_id):
    """Get a specific configuration baseline"""
    try:
        baseline = ConfigurationBaseline.query.get_or_404(baseline_id)
        return jsonify(baseline.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@configuration_bp.route('/configuration-baselines', methods=['POST'])
def create_configuration_baseline():
    """Create a new configuration baseline"""
    try:
        data = request.get_json()
        
        baseline = ConfigurationBaseline(
            name=data.get('name'),
            asset_type=data.get('asset_type'),
            description=data.get('description'),
            baseline_config=data.get('baseline_config')
        )
        
        db.session.add(baseline)
        db.session.commit()
        
        return jsonify(baseline.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@configuration_bp.route('/configuration-baselines/<int:baseline_id>', methods=['PUT'])
def update_configuration_baseline(baseline_id):
    """Update an existing configuration baseline"""
    try:
        baseline = ConfigurationBaseline.query.get_or_404(baseline_id)
        data = request.get_json()
        
        baseline.name = data.get('name', baseline.name)
        baseline.asset_type = data.get('asset_type', baseline.asset_type)
        baseline.description = data.get('description', baseline.description)
        baseline.baseline_config = data.get('baseline_config', baseline.baseline_config)
        
        db.session.commit()
        
        return jsonify(baseline.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@configuration_bp.route('/configuration-baselines/<int:baseline_id>', methods=['DELETE'])
def delete_configuration_baseline(baseline_id):
    """Delete a configuration baseline"""
    try:
        baseline = ConfigurationBaseline.query.get_or_404(baseline_id)
        db.session.delete(baseline)
        db.session.commit()
        
        return jsonify({'message': 'Configuration baseline deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@configuration_bp.route('/configuration-deviations', methods=['GET'])
def get_configuration_deviations():
    """Get all configuration deviations"""
    try:
        deviations = ConfigurationDeviation.query.all()
        return jsonify([deviation.to_dict() for deviation in deviations])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@configuration_bp.route('/configuration-deviations/<int:deviation_id>', methods=['GET'])
def get_configuration_deviation(deviation_id):
    """Get a specific configuration deviation"""
    try:
        deviation = ConfigurationDeviation.query.get_or_404(deviation_id)
        return jsonify(deviation.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@configuration_bp.route('/configuration-deviations', methods=['POST'])
def create_configuration_deviation():
    """Create a new configuration deviation"""
    try:
        data = request.get_json()
        
        deviation = ConfigurationDeviation(
            asset_id=data.get('asset_id'),
            baseline_id=data.get('baseline_id'),
            deviation_type=data.get('deviation_type'),
            parameter_name=data.get('parameter_name'),
            expected_value=data.get('expected_value'),
            actual_value=data.get('actual_value'),
            risk_level=data.get('risk_level'),
            status=data.get('status', 'Open'),
            remediation_notes=data.get('remediation_notes'),
            discovered_date=datetime.fromisoformat(data.get('discovered_date')) if data.get('discovered_date') else datetime.utcnow()
        )
        
        db.session.add(deviation)
        db.session.commit()
        
        return jsonify(deviation.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@configuration_bp.route('/configuration-deviations/<int:deviation_id>', methods=['PUT'])
def update_configuration_deviation(deviation_id):
    """Update an existing configuration deviation"""
    try:
        deviation = ConfigurationDeviation.query.get_or_404(deviation_id)
        data = request.get_json()
        
        deviation.asset_id = data.get('asset_id', deviation.asset_id)
        deviation.baseline_id = data.get('baseline_id', deviation.baseline_id)
        deviation.deviation_type = data.get('deviation_type', deviation.deviation_type)
        deviation.parameter_name = data.get('parameter_name', deviation.parameter_name)
        deviation.expected_value = data.get('expected_value', deviation.expected_value)
        deviation.actual_value = data.get('actual_value', deviation.actual_value)
        deviation.risk_level = data.get('risk_level', deviation.risk_level)
        deviation.status = data.get('status', deviation.status)
        deviation.remediation_notes = data.get('remediation_notes', deviation.remediation_notes)
        
        if data.get('remediation_date'):
            deviation.remediation_date = datetime.fromisoformat(data.get('remediation_date'))
        
        db.session.commit()
        
        return jsonify(deviation.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@configuration_bp.route('/configuration-deviations/<int:deviation_id>', methods=['DELETE'])
def delete_configuration_deviation(deviation_id):
    """Delete a configuration deviation"""
    try:
        deviation = ConfigurationDeviation.query.get_or_404(deviation_id)
        db.session.delete(deviation)
        db.session.commit()
        
        return jsonify({'message': 'Configuration deviation deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@configuration_bp.route('/configuration-deviations/stats', methods=['GET'])
def get_configuration_deviation_stats():
    """Get configuration deviation statistics"""
    try:
        total_deviations = ConfigurationDeviation.query.count()
        critical_deviations = ConfigurationDeviation.query.filter_by(risk_level='Critical').count()
        high_deviations = ConfigurationDeviation.query.filter_by(risk_level='High').count()
        medium_deviations = ConfigurationDeviation.query.filter_by(risk_level='Medium').count()
        low_deviations = ConfigurationDeviation.query.filter_by(risk_level='Low').count()
        
        open_deviations = ConfigurationDeviation.query.filter_by(status='Open').count()
        remediated_deviations = ConfigurationDeviation.query.filter_by(status='Remediated').count()
        accepted_deviations = ConfigurationDeviation.query.filter_by(status='Accepted').count()
        
        return jsonify({
            'total_deviations': total_deviations,
            'by_risk_level': {
                'critical': critical_deviations,
                'high': high_deviations,
                'medium': medium_deviations,
                'low': low_deviations
            },
            'by_status': {
                'open': open_deviations,
                'remediated': remediated_deviations,
                'accepted': accepted_deviations
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

