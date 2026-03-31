from . import db
from datetime import datetime

class PlacementDrive(db.Model):
    drive_id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    
    job_title = db.Column(db.String(255), nullable=False)
    job_description = db.Column(db.Text, nullable=False)
    
    # Eligibility Criteria
    eligible_branch = db.Column(db.String(100), nullable=True) # e.g., 'CSE', 'All'
    min_cgpa = db.Column(db.Float, default=0.0)
    eligible_year = db.Column(db.Integer, nullable=True) # e.g., 2026
    
    application_deadline = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='Pending') # Pending, Approved, Closed
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    applications = db.relationship('Application', backref='drive', cascade="all, delete-orphan")

    ALLOWED_FIELDS = {
        'job_title', 'job_description', 'eligible_branch', 
        'min_cgpa', 'eligible_year', 'application_deadline', 'status'
    }

    def to_dict(self):
        return {
            'drive_id': self.drive_id,
            'company_id': self.company_id,
            'job_title': self.job_title,
            'job_description': self.job_description,
            'eligible_branch': self.eligible_branch,
            'min_cgpa': self.min_cgpa,
            'eligible_year': self.eligible_year,
            'deadline': self.application_deadline.isoformat(),
            'status': self.status,
            'created_at': self.created_at.isoformat()
        }

    def updateData(self, data):
        for key, value in data.items():
            if key in PlacementDrive.ALLOWED_FIELDS:
                if key == 'application_deadline' and isinstance(value, str):
                    value = datetime.fromisoformat(value)
                setattr(self, key, value)
        db.session.commit()
        return True

class Application(db.Model):
    application_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    drive_id = db.Column(db.Integer, db.ForeignKey('placement_drive.drive_id'), nullable=False)
    
    application_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Applied') # Applied, Shortlisted, Selected, Rejected
    

    def to_dict(self):
        return {
            'application_id': self.application_id,
            'student_id': self.student_id,
            'drive_id': self.drive_id,
            'date': self.application_date.isoformat(),
            'status': self.status,
        }

    def updateStatus(self, new_status):
        self.status = new_status
        db.session.commit()
        return True
