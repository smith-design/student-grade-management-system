from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, Float, Date, ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class Student(db.Model):
    __tablename__ = 'students'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(String(20), unique=True, nullable=False, comment='学号')
    name = Column(String(50), nullable=False, comment='姓名')
    class_name = Column(String(50), nullable=False, comment='班级')
    gender = Column(String(10), nullable=True, comment='性别')
    age = Column(Integer, nullable=True, comment='年龄')
    phone = Column(String(20), nullable=True, comment='电话')
    email = Column(String(100), nullable=True, comment='邮箱')
    address = Column(String(200), nullable=True, comment='地址')
    
    # 关联成绩
    grades = relationship('Grade', backref='student', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'name': self.name,
            'class_name': self.class_name,
            'gender': self.gender,
            'age': self.age,
            'phone': self.phone,
            'email': self.email,
            'address': self.address
        }

class Grade(db.Model):
    __tablename__ = 'grades'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(String(20), ForeignKey('students.student_id', ondelete='CASCADE'), nullable=False, comment='学号')
    subject = Column(String(50), nullable=False, comment='科目')
    score = Column(Float, nullable=False, comment='分数')
    exam_type = Column(String(50), nullable=True, comment='考试类型')
    exam_date = Column(String(20), nullable=True, comment='考试日期')

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'subject': self.subject,
            'score': self.score,
            'exam_type': self.exam_type,
            'exam_date': self.exam_date
        }
