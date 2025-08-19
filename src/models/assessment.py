from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class Assessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    framework = db.Column(db.String(50), nullable=False)  # IEC62443, NIST
    overall_score = db.Column(db.Float)
    status = db.Column(db.String(20), default='In Progress')  # In Progress, Completed, Draft
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Assessment {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'framework': self.framework,
            'overall_score': self.overall_score,
            'status': self.status,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class AssessmentQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessment.id'), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.String(20))  # Yes, No, Partial, N/A
    score = db.Column(db.Integer)  # 0-5 scale
    notes = db.Column(db.Text)
    evidence = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    assessment = db.relationship('Assessment', backref=db.backref('questions', lazy=True))

    def __repr__(self):
        return f'<AssessmentQuestion {self.question[:50]}>'

    def to_dict(self):
        return {
            'id': self.id,
            'assessment_id': self.assessment_id,
            'category': self.category,
            'question': self.question,
            'answer': self.answer,
            'score': self.score,
            'notes': self.notes,
            'evidence': self.evidence,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

