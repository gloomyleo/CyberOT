from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class ConfigurationBaseline(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    asset_type = db.Column(db.String(50), nullable=False)  # PLC, HMI, SCADA, etc.
    description = db.Column(db.Text)
    baseline_config = db.Column(db.Text)  # JSON or text configuration
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<ConfigurationBaseline {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'asset_type': self.asset_type,
            'description': self.description,
            'baseline_config': self.baseline_config,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class ConfigurationDeviation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('asset.id'), nullable=False)
    baseline_id = db.Column(db.Integer, db.ForeignKey('configuration_baseline.id'), nullable=False)
    deviation_type = db.Column(db.String(50), nullable=False)  # Missing, Extra, Modified
    parameter_name = db.Column(db.String(200), nullable=False)
    expected_value = db.Column(db.Text)
    actual_value = db.Column(db.Text)
    risk_level = db.Column(db.String(20), nullable=False)  # Critical, High, Medium, Low
    status = db.Column(db.String(20), default='Open')  # Open, Remediated, Accepted
    remediation_notes = db.Column(db.Text)
    discovered_date = db.Column(db.DateTime, default=datetime.utcnow)
    remediation_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    asset = db.relationship('Asset', backref=db.backref('configuration_deviations', lazy=True))
    baseline = db.relationship('ConfigurationBaseline', backref=db.backref('deviations', lazy=True))

    def __repr__(self):
        return f'<ConfigurationDeviation {self.parameter_name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'asset_id': self.asset_id,
            'asset_name': self.asset.name if self.asset else None,
            'baseline_id': self.baseline_id,
            'baseline_name': self.baseline.name if self.baseline else None,
            'deviation_type': self.deviation_type,
            'parameter_name': self.parameter_name,
            'expected_value': self.expected_value,
            'actual_value': self.actual_value,
            'risk_level': self.risk_level,
            'status': self.status,
            'remediation_notes': self.remediation_notes,
            'discovered_date': self.discovered_date.isoformat() if self.discovered_date else None,
            'remediation_date': self.remediation_date.isoformat() if self.remediation_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

