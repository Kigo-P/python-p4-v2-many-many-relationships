# server/models.py

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)
# creating a join table between employees and meetings
employee_meetings = db.Table(
    "employees_meetings",
    metadata,
    db.Column("employee_id", db.Integer, db.ForeignKey("employees.id"), primary_key = True),
    db.Column("meeting_id", db.Integer, db.ForeignKey("meetings.id"), primary_key = True)

)

# An association table to store a many to many relationship between the employees and the project
class Assignment(db.Model):
    # creating a table called assignments
    __tablename__ = "assignments"

    # creating columns for the table
    id = db.Column(db.Integer, primary_key = True)
    role = db.Column(db.String)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    # Foreign key to store the employee id
    employee_id = db.Column(db.Integer, db.ForeignKey("employees.id"))
    # Foreign key to store the project id
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"))

    # a relationship that maps assignments to  related employee
    employee = db.relationship("Employee", back_populates = "assignments")

    # a relationship that maps assignments to related project
    project = db.relationship("Project", back_populates = "assignments")

    #  creating a string representation of the data
    def __repr__(self):
        return f"<Assignment {self.id}, {self.role}, {self.start_date}, {self.end_date}, {self.employee.name}, {self.project.title}>"

class Employee(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    hire_date = db.Column(db.Date)

    # a relationship that maps employees to related assignments
    assignments = db.relationship("Assignment", back_populates = "employee", cascade = "all, delete-orphan" )
    
    # a relationship that maps employees to meetings  via a secondary employee_meetings
    meetings = db.relationship("Meeting", secondary = employee_meetings, back_populates = "employees")
    
    #  Association proxy to get the projects for the employee through assignment
    project = association_proxy("assignments", "project", creator = lambda project_obj: Assignment(project = project_obj))
    
    def __repr__(self):
        return f'<Employee {self.id}, {self.name}, {self.hire_date}>'


class Meeting(db.Model):
    __tablename__ = 'meetings'

    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String)
    scheduled_time = db.Column(db.DateTime)
    location = db.Column(db.String)

    #  a relationship that maps meetings to employees via a secondary employee_meetings
    employees = db.relationship("Employee", secondary = employee_meetings, back_populates = "meetings")
    
    def __repr__(self):
        return f'<Meeting {self.id}, {self.topic}, {self.scheduled_time}, {self.location}>'


class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    budget = db.Column(db.Integer)

    # a relationship that maps projects to related assignments
    assignments = db.relationship("Assignment", back_populates = "project", cascade = "all, delete-orphan" )
    
    # Association to get the employees of a project via Assignment
    employees = association_proxy("assignments", "employee", creator=lambda employee_obj: Assignment(employee = employee_obj))

    def __repr__(self):
        return f'<Review {self.id}, {self.title}, {self.budget}>'
    

