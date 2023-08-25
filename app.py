from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///skills.db'
db = SQLAlchemy(app)

@app.route('/')
def first_page():
    skills = Skill.query.all()
    return render_template("front.html", skills=skills, totalLevel = sum(skill.level for skill in skills))
    
@app.route('/skills', methods=['GET'])
def get_skills():
    skills = Skill.query.all()
    return jsonify([{'name': skill.name, 'level': skill.level} for skill in skills])

@app.route('/update_skill_up', methods=['POST'])
def update_skill_up():
    data = request.form
    skill = Skill.query.filter_by(name=data['skill']).first()
    if skill:
        skill.level += 1
        db.session.commit()
    skills = Skill.query.all()
    return render_template("front.html", skills=skills)

@app.route('/update_skill_down', methods=['POST'])
def update_skill_down():
    data = request.form
    skill = Skill.query.filter_by(name=data['skill']).first()
    if skill and skill.level > 1:
        skill.level -= 1
        db.session.commit()
    skills = Skill.query.all()
    return render_template("front.html", skills=skills)

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    level = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=True)
    challenges = db.relationship('Challenge', backref='skill', lazy=True)
        
class Challenge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    experience = db.Column(db.Float(100), nullable=False)
    skill_id = db.Column(db.Integer, db.ForeignKey("skill.id"), nullable=False)

if __name__ == '__main__':
    with app.app_context(): db.create_all()
    app.run(debug=True)