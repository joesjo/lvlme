from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from models.user_models import Skill, Challenge
from models.database import db
import math

user_routes = Blueprint('user_routes', __name__, template_folder='templates')

@user_routes.route('/')
def first_page():
    skills = Skill.query.all()
    for skill in skills:
        skill.required_experience = 100 * pow(1.1, skill.level-1)
        skill.required_experience = round(skill.required_experience, 2)
        skill.progress = math.floor(skill.experience / skill.required_experience * 100)
    skillColumns = [skills[i::4] for i in range(4)]
    return render_template("index.html", skills=skillColumns, total_level=sum([skill.level for skill in skills]))
    
@user_routes.route('/skills', methods=['GET'])
def get_skills():
    skills = Skill.query.all()
    return jsonify([{'name': skill.name, 'level': skill.level} for skill in skills])

@user_routes.route('/update_skill_up', methods=['POST'])
def update_skill_up():
    data = request.form
    skill = Skill.query.filter_by(name=data['skill']).first()
    if skill:
        skill.level += 1
        db.session.commit()
    return redirect(url_for('user_routes.first_page'))

@user_routes.route('/update_skill_down', methods=['POST'])
def update_skill_down():
    data = request.form
    skill = Skill.query.filter_by(name=data['skill']).first()
    if skill and skill.level > 1:
        skill.level -= 1
        db.session.commit()
    return redirect(url_for('user_routes.first_page'))

@user_routes.route('/update_experience/<int:skill_id>', methods=['POST'])
def update_experience_route(skill_id):
    minutes_spent = request.form.get('minutes_spent')
    if minutes_spent.isdigit():
        update_experience(skill_id, int(minutes_spent))
    return redirect(url_for('user_routes.first_page'))
    
@user_routes.route('/complete_challenge/<int:challenge_id>', methods=['POST'])
def complete_challenge(challenge_id):
    completed = request.form.get('completed') == 'true'
    challenge = Challenge.query.get(challenge_id)
    if challenge and completed:
        # update_experience(challenge_id)
        pass
    return redirect(url_for('user_routes.first_page'))

def update_experience(skill_id, minutes_spent):
    skill = Skill.query.get(skill_id)
    skill.experience += minutes_spent
    base_experience = 100
    required_experience = round(base_experience * pow(1.1, skill.level-1), 2)
    while skill.experience >= required_experience:
        skill.level += 1
        skill.experience -= required_experience
        required_experience = round(base_experience * pow(1.1, skill.level-1), 2)
    db.session.commit()