from gradient import db, ma

class UserModel(db.Model):
  __tablename__ = "users"

  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String, unique=True, nullable=False)
  given_name = db.Column(db.String, nullable=False)
  family_name = db.Column(db.String, nullable=False)


  def __init__(self, email, given_name, family_name):
    self.email = email
    self.given_name = given_name
    self.family_name = family_name


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


  @classmethod
  def get_by_email(cls, email):
    return cls.query.filter_by(email=email).first()


  def __repr__(self):
    return "<User {}>".format(self.email)


class UserSchema(ma.ModelSchema):
  class meta:
    model = UserModel


