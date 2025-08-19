from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.assessment import Assessment, AssessmentQuestion

assessment_bp = Blueprint('assessment', __name__)

@assessment_bp.route('/assessments', methods=['GET'])
def get_assessments():
    """Get all assessments"""
    try:
        assessments = Assessment.query.all()
        return jsonify([assessment.to_dict() for assessment in assessments])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@assessment_bp.route('/assessments/<int:assessment_id>', methods=['GET'])
def get_assessment(assessment_id):
    """Get a specific assessment with questions"""
    try:
        assessment = Assessment.query.get_or_404(assessment_id)
        assessment_data = assessment.to_dict()
        questions = AssessmentQuestion.query.filter_by(assessment_id=assessment_id).all()
        assessment_data['questions'] = [question.to_dict() for question in questions]
        return jsonify(assessment_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@assessment_bp.route('/assessments', methods=['POST'])
def create_assessment():
    """Create a new assessment"""
    try:
        data = request.get_json()
        
        assessment = Assessment(
            name=data.get('name'),
            framework=data.get('framework'),
            description=data.get('description'),
            status=data.get('status', 'In Progress')
        )
        
        db.session.add(assessment)
        db.session.commit()
        
        # Create default questions based on framework
        if data.get('framework') == 'IEC62443':
            create_iec62443_questions(assessment.id)
        elif data.get('framework') == 'NIST':
            create_nist_questions(assessment.id)
        
        return jsonify(assessment.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@assessment_bp.route('/assessments/<int:assessment_id>', methods=['PUT'])
def update_assessment(assessment_id):
    """Update an existing assessment"""
    try:
        assessment = Assessment.query.get_or_404(assessment_id)
        data = request.get_json()
        
        assessment.name = data.get('name', assessment.name)
        assessment.framework = data.get('framework', assessment.framework)
        assessment.description = data.get('description', assessment.description)
        assessment.status = data.get('status', assessment.status)
        assessment.overall_score = data.get('overall_score', assessment.overall_score)
        
        db.session.commit()
        
        return jsonify(assessment.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@assessment_bp.route('/assessments/<int:assessment_id>/questions/<int:question_id>', methods=['PUT'])
def update_assessment_question(assessment_id, question_id):
    """Update an assessment question"""
    try:
        question = AssessmentQuestion.query.filter_by(
            id=question_id, 
            assessment_id=assessment_id
        ).first_or_404()
        
        data = request.get_json()
        
        question.answer = data.get('answer', question.answer)
        question.score = data.get('score', question.score)
        question.notes = data.get('notes', question.notes)
        question.evidence = data.get('evidence', question.evidence)
        
        db.session.commit()
        
        # Recalculate overall assessment score
        calculate_assessment_score(assessment_id)
        
        return jsonify(question.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@assessment_bp.route('/assessments/<int:assessment_id>', methods=['DELETE'])
def delete_assessment(assessment_id):
    """Delete an assessment and its questions"""
    try:
        assessment = Assessment.query.get_or_404(assessment_id)
        
        # Delete all questions first
        AssessmentQuestion.query.filter_by(assessment_id=assessment_id).delete()
        
        # Delete the assessment
        db.session.delete(assessment)
        db.session.commit()
        
        return jsonify({'message': 'Assessment deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

def create_iec62443_questions(assessment_id):
    """Create IEC 62443 framework questions"""
    questions = [
        {
            'category': 'Security Governance',
            'question': 'Has the organization established a cybersecurity policy for OT systems?',
        },
        {
            'category': 'Security Governance',
            'question': 'Are cybersecurity roles and responsibilities clearly defined for OT systems?',
        },
        {
            'category': 'Risk Assessment',
            'question': 'Has a comprehensive risk assessment been conducted for OT systems?',
        },
        {
            'category': 'Risk Assessment',
            'question': 'Are risk assessment results regularly updated and reviewed?',
        },
        {
            'category': 'Network Segmentation',
            'question': 'Are OT networks properly segmented from IT networks?',
        },
        {
            'category': 'Network Segmentation',
            'question': 'Are security zones and conduits implemented according to IEC 62443-3-2?',
        },
        {
            'category': 'Access Control',
            'question': 'Is multi-factor authentication implemented for OT system access?',
        },
        {
            'category': 'Access Control',
            'question': 'Are user access rights regularly reviewed and updated?',
        },
        {
            'category': 'Asset Management',
            'question': 'Is there a comprehensive inventory of all OT assets?',
        },
        {
            'category': 'Asset Management',
            'question': 'Are asset configurations documented and maintained?',
        },
        {
            'category': 'Incident Response',
            'question': 'Is there an incident response plan specific to OT environments?',
        },
        {
            'category': 'Incident Response',
            'question': 'Are incident response procedures regularly tested and updated?',
        }
    ]
    
    for q in questions:
        question = AssessmentQuestion(
            assessment_id=assessment_id,
            category=q['category'],
            question=q['question']
        )
        db.session.add(question)
    
    db.session.commit()

def create_nist_questions(assessment_id):
    """Create NIST framework questions"""
    questions = [
        {
            'category': 'Identify',
            'question': 'Are all OT assets identified and documented?',
        },
        {
            'category': 'Identify',
            'question': 'Are business processes and their dependencies on OT systems documented?',
        },
        {
            'category': 'Protect',
            'question': 'Are appropriate safeguards implemented to protect OT systems?',
        },
        {
            'category': 'Protect',
            'question': 'Is access to OT systems controlled and monitored?',
        },
        {
            'category': 'Detect',
            'question': 'Are security monitoring capabilities implemented for OT systems?',
        },
        {
            'category': 'Detect',
            'question': 'Can anomalous activities in OT systems be detected?',
        },
        {
            'category': 'Respond',
            'question': 'Are response procedures established for OT security incidents?',
        },
        {
            'category': 'Respond',
            'question': 'Can the organization effectively contain OT security incidents?',
        },
        {
            'category': 'Recover',
            'question': 'Are recovery procedures established for OT systems?',
        },
        {
            'category': 'Recover',
            'question': 'Can OT systems be restored to normal operations after an incident?',
        }
    ]
    
    for q in questions:
        question = AssessmentQuestion(
            assessment_id=assessment_id,
            category=q['category'],
            question=q['question']
        )
        db.session.add(question)
    
    db.session.commit()

def calculate_assessment_score(assessment_id):
    """Calculate overall assessment score"""
    try:
        questions = AssessmentQuestion.query.filter_by(assessment_id=assessment_id).all()
        
        if not questions:
            return
        
        total_score = 0
        answered_questions = 0
        
        for question in questions:
            if question.score is not None:
                total_score += question.score
                answered_questions += 1
        
        if answered_questions > 0:
            overall_score = (total_score / (answered_questions * 5)) * 100  # Convert to percentage
            
            assessment = Assessment.query.get(assessment_id)
            assessment.overall_score = round(overall_score, 2)
            db.session.commit()
    
    except Exception as e:
        db.session.rollback()
        print(f"Error calculating assessment score: {e}")

