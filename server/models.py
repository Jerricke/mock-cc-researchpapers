from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)

# Add models here


class Research(db.Model, SerializerMixin):
    __tablename__ = "researches"

    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String)
    year = db.Column(db.Integer)
    page_count = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    authors = db.relationship(
        "ResearchAuthors", cascade="all, delete-orphan", backref="researches"
    )

    serialize_rules = ("-authors.researches",)

    @validates("year")
    def validate_year(self, key, value):
        if not 999 < value <= 9999:
            raise ValueError("Invalid year input")
        return value


class ResearchAuthors(db.Model, SerializerMixin):
    __tablename__ = "researchAuthors"

    serialize_rules = (
        "-authors.researches",
        "-researches.authors",
    )

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("authors.id"))
    research_id = db.Column(db.Integer, db.ForeignKey("researches.id"))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())


class Author(db.Model, SerializerMixin):
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    field_of_study = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    researches = db.relationship(
        "ResearchAuthors", cascade="all, delete-orphan", backref="authors"
    )

    serialize_rules = ("-researches.authors",)

    @validates("field_of_study")
    def validate_fos(self, key, value):
        if value not in [
            "AI",
            "Robotics",
            "Machine Learning",
            "Vision",
            "Cybersecurity",
        ]:
            raise ValueError("Not a valid field of study!")
        return value
