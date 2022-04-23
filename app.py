import os
import random
from flask import Flask, jsonify, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class Wall(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(80), unique=True, nullable=False)

    image = db.Column(db.String(80), unique=True, nullable=False)

class Hold(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    wall_id = db.Column(db.Integer, db.ForeignKey('wall.id'))
    wall = db.relationship('Wall', backref=db.backref('holds', lazy=True))

    app_uuid = db.Column(db.String(80))

    location_x = db.Column(db.Float, nullable=False)
    location_y = db.Column(db.Float, nullable=False)
    location_radius = db.Column(db.Float, nullable=False)

    row = db.Column(db.Integer)
    col = db.Column(db.Integer)

class Route(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    wall_id = db.Column(db.Integer, db.ForeignKey('wall.id'))
    wall = db.relationship('Wall', backref=db.backref('routes', lazy=True))

    setter_id = db.Column(db.Integer, db.ForeignKey('climber.id'))
    setter = db.relationship('Climber', backref=db.backref('setters', lazy=True))

    name = db.Column(db.String(180))
    description = db.Column(db.String(180))
    setter_username = db.Column(db.String(80))
    app_uuid = db.Column(db.String(80))
    created_at = db.Column(db.String(80))

class Placement(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    route_id = db.Column(db.Integer, db.ForeignKey('route.id'))
    route = db.relationship('Route', backref=db.backref('placements', lazy=True))

    hold_id = db.Column(db.Integer, db.ForeignKey('hold.id'))
    hold = db.relationship('Hold', backref=db.backref('placements', lazy=True))

class Climber(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(80), unique=False, nullable=False)

class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    tag = db.Column(db.String(80), unique=True, nullable=False)

    difficulty_index = db.Column(db.Integer, unique=False, nullable=False)

class Attempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    route_id = db.Column(db.Integer, db.ForeignKey('route.id'))
    route = db.relationship('Route', backref=db.backref('attempts', lazy=True))

    proposed_grade_id = db.Column(db.Integer, db.ForeignKey('grade.id'))
    grade = db.relationship('Grade', backref=db.backref('attempts', lazy=True))

    climber_id = db.Column(db.Integer, db.ForeignKey('climber.id'))
    climber = db.relationship('Climber', backref=db.backref('attempts', lazy=True))

    angle = db.Column(db.Float, nullable=False)

@app.route("/")
def index():
    route = random.choice(Route.query.all())

    wall = Wall.query.filter_by(id = route.wall_id).first()

    placements = Placement.query.filter_by(route_id=route.id)

    holds = Hold.query.all()

    placementsVisual = []

    for placement in placements:
        hold = Hold.query.filter_by(id=placement.hold_id).first()
        placementsVisual.append([hold.location_x, hold.location_y, hold.location_radius])

    return render_template("index.html",
                            mytitle="title",
                            mycontent="Hello World",
                            wall=wall,
                            placements=placementsVisual,
                            route=route,)
@app.route("/search")
def search():
    args = request.args

    route = Route.query.filter_by(name = args.get("RouteName")).first()

    if route== None:
        return redirect('/')

    wall = Wall.query.filter_by(id = route.wall_id).first()
    placements = Placement.query.filter_by(route_id=route.id)

    holds = Hold.query.all()

    placementsVisual = []

    for placement in placements:
        hold = Hold.query.filter_by(id=placement.hold_id).first()
        placementsVisual.append([hold.location_x, hold.location_y, hold.location_radius])

    return render_template("index.html",
                            wall=wall,
                            placements=placementsVisual,
                            route=route,)


if __name__ == "__main__":
    app.run(debug = True, host='0.0.0.0')
