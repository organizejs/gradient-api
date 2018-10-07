from gradient import db, ma
from enum import Enum


class IncomeType(Enum):
  INDIVIDUAL = 0
  HOUSEHOLD = 1


class MaritalStatus(Enum):
  SINGLE = "single"
  MARRIED = "married"
  DIVORCED = "divorced"
  WIDOWED = "widowed"


class CustomerModel(db.Model):
  __tablename__ = "customer"

  id = db.Column(db.Integer, primary_key=True)
  income = db.Column(db.Integer)
  dependents = db.Column(db.Integer)
  marital_status = db.Column(db.Enum(MaritalStatus))


  def income_type(self):
    return IncomeType.HOUSEHOLD \
      if self.marital_status is MaritalStatus.MARRIED \
      else IncomeType.INDIVIDUAL


  def save(self):
    db.session.add(self)
    db.session.commit()


  def delete(self):
    db.session.delete(self)
    db.session.commit()


  @classmethod
  def get_all(cls):
    return cls.query.all()


  @classmethod
  def get(cls, user_id):
    return cls.query.get(user_id)


  def __repr__(self):
    return "<Customer income: {}>".format(self.income)


class CustomerSchema(ma.ModelSchema):
  class meta:
    model = CustomerModel
