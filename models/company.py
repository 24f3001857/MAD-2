from . import db

class Company(db.Model):
    company_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    hr_contact = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    zip = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    website = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(100), nullable=False)

    ALLOWED_FIELDS = {
        'name', 'email', 'hr_contact', 'address', 'city', 
        'state', 'zip', 'country', 'website', 'status'
    }

    def __repr__(self):
        return f'<Company {self.name}>'

    def to_dict(self):
        return {
            'company_id': self.company_id,
            'name': self.name,
            'email': self.email,
            'hr_contact': self.hr_contact,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zip': self.zip,
            'country': self.country,
            'website': self.website,
            'status': self.status
        }

    def updateData(self, data):
        for key, value in data.items():
            if key in Company.ALLOWED_FIELDS:
                setattr(self, key, value)
        db.session.commit()
        return True
    
    