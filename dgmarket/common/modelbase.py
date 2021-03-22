from .. import db
import datetime

import datetime
class ModelBase(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    insert_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    update_date = db.Column(db.DateTime, nullable=True, onupdate=datetime.datetime.now)

    def select(self, **kwargs):
        return self.__class__.query.filter_by(**kwargs)

    def insert(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update(self):
        db.session.commit()
        return self

    def save(self):
        if self.id is None:
            self.insert()
        else:
            self.update()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self
    
    @classmethod
    def select(cls, **kwargs):
        return cls.query.filter_by(**kwargs)

    @classmethod
    def all(cls, **kwargs):
        return cls.query.filter_by(**kwargs).all()
    
    @classmethod
    def find(cls, id):
        return cls.query.filter_by(id=id).first()
    
    @classmethod
    def first(cls, **kwargs):
        return cls.query.filter_by(**kwargs).first()
    
    @classmethod
    def exist(cls, **kwargs):        
        return cls.query.filter_by(**kwargs).count() > 0