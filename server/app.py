#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request, render_template
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Research, Author, ResearchAuthors

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


class Index(Resource):
    def get(self):
        res = make_response("<h1>Code challenge</h1>", 200)
        return res


api.add_resource(Index, "/")


class ResearchAll(Resource):
    def get(self):
        response_body = [
            r.to_dict() for r in Research.query.order_by(Research.id).all()
        ]

        response = make_response(jsonify(response_body), 200)

        return response


api.add_resource(ResearchAll, "/research")


class ResearchByID(Resource):
    def get(self, id):
        research = Research.query.filter_by(id=id).first()
        if research != None:
            res = make_response(jsonify(research.to_dict()), 200)
        else:
            res = make_response({"error": "Research paper not found"}, 404)
        return res

    def delete(self, id):
        research = Research.query.filter_by(id=id).first()
        if research != None:
            db.session.delete(research)
            db.session.commit()
            res = make_response({"Message": "Research paper has been deleted"}, 204)
        else:
            res = make_response({"error": "Research paper not found"}, 404)
        return res


api.add_resource(ResearchByID, "/research/<int:id>")


class AuthorAll(Resource):
    def get(self):
        response_body = [r.to_dict() for r in Author.query.order_by(Research.id).all()]

        response = make_response(jsonify(response_body), 200)

        return response


api.add_resource(AuthorAll, "/authors")


class ResearchAuthor(Resource):
    def post(self):
        data = request.get_json()
        if data["author_id"] != None and data["research_id"] != None:
            new_RA = ResearchAuthors(
                author_id=data["author_id"], research_id=data["research_id"]
            )
            db.session.add(new_RA)
            db.session.commit()

            author = Author.query.filter_by(id=data["author_id"]).first()

            res = make_response(jsonify(author.to_dict()), 201)
        else:
            res = make_response({"errors": ["validation errors"]}, 200)
        return res


api.add_resource(ResearchAuthor, "/research_author")
if __name__ == "__main__":
    app.run(port=5555, debug=True)
