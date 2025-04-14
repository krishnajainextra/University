from app import db

class Department(db.Model):
    __tablename__ = 'departments'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    head_of_department = db.Column(db.String(100), nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)
    
    # Add the foreign key to link to the College model
    college_id = db.Column(db.Integer, db.ForeignKey('colleges.id'), nullable=False)
    
    def __repr__(self):
        return f'<Department {self.name}>'