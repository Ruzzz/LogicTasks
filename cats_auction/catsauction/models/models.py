from sqlalchemy import Column, Float, ForeignKey, Integer, String, Index, UniqueConstraint

from catsauction.models.meta import db


class User(db.Model):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    balance = Column(Integer)


class Animals(db.Model):
    __tablename__ = 'animals'

    id = Column(Integer, primary_key=True)
    breed = Column(String)
    alias = Column(String)
    owner_id = Column(Integer, ForeignKey('user.id'))

    __table_args__ = Index('ix_animals_owner_id', owner_id),


class Lot(db.Model):
    __tablename__ = 'lot'

    id = Column(Integer, primary_key=True)
    price = Column(Float)
    animal_id = Column(Integer, ForeignKey('animals.id'))
    owner_id = Column(Integer, ForeignKey('user.id'))

    __table_args__ = (
        UniqueConstraint(owner_id, animal_id),
    )


class Bet(db.Model):
    __tablename__ = 'bet'

    id = Column(Integer, primary_key=True)
    value = Column(Float)
    lot_id = Column(Integer, ForeignKey('lot.id'))
    owner_id = Column(Integer, ForeignKey('user.id'))

    __table_args__ = (
        UniqueConstraint(owner_id, lot_id),
    )
