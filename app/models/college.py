from app import db

class College(db.Model):
    __tablename__ = 'colleges'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    
    # Relationships
    departments = db.relationship('Department', backref='college', lazy=True)
    contacts = db.relationship('CollegeContact', backref='college', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<College {self.name}>'

class CollegeContact(db.Model):
    __tablename__ = 'college_contacts'
    
    id = db.Column(db.Integer, primary_key=True)
    college_id = db.Column(db.Integer, db.ForeignKey('colleges.id'), nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)
    
    def __repr__(self):
        return f'<CollegeContact {self.contact_number}>'