from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    asset_type = db.Column(db.String(50), nullable=False)  # HMI, PLC, SCADA, etc.
    manufacturer = db.Column(db.String(100))
    model = db.Column(db.String(100))
    serial_number = db.Column(db.String(100))
    ip_address = db.Column(db.String(45))  # IPv4 or IPv6
    location = db.Column(db.String(200))
    criticality = db.Column(db.String(20), nullable=False)  # Critical, High, Medium, Low
    status = db.Column(db.String(20), default='Active')  # Active, Inactive, Decommissioned
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Asset {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'asset_type': self.asset_type,
            'manufacturer': self.manufacturer,
            'model': self.model,
            'serial_number': self.serial_number,
            'ip_address': self.ip_address,
            'location': self.location,
            'criticality': self.criticality,
            'status': self.status,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

