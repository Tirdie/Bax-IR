import datetime
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user

from app import db
from app.models.threat_hunt import ThreatHunt
from app.iris_engine.access_control.utils import ac_current_user_has_case_access
from app.util import response_success, response_error, ac_case_requires_access_read

threat_hunting_blueprint = Blueprint(
    'threat_hunting',
    __name__,
    url_prefix=''
)


@threat_hunting_blueprint.route('/threat-hunting', methods=['GET'])
@login_required
def threat_hunting_view():
    return render_template('pages/threat_hunting.html')


@threat_hunting_blueprint.route('/api/threat-hunting', methods=['GET'])
@login_required
def get_hunts():
    caseid = request.args.get('cid', 0, type=int)
    hunts = ThreatHunt.query.filter_by(case_id=caseid).order_by(ThreatHunt.id.desc()).all()
    return response_success('', data=[h.to_dict() for h in hunts])


@threat_hunting_blueprint.route('/api/threat-hunting', methods=['POST'])
@login_required
def create_hunt():
    caseid = request.args.get('cid', 0, type=int)
    data = request.get_json()
    if not data or not data.get('hypothesis'):
        return response_error('Hypothesis is required')

    hunt = ThreatHunt(
        hypothesis=data['hypothesis'],
        technique=data.get('technique', ''),
        data_sources=data.get('data_sources', ''),
        notes=data.get('notes', ''),
        outcome=data.get('outcome', ''),
        status=data.get('status', 'active'),
        created_by=current_user.id,
        case_id=caseid,
        created_at=datetime.datetime.utcnow()
    )
    db.session.add(hunt)
    db.session.commit()
    return response_success('Hunt created', data=hunt.to_dict())


@threat_hunting_blueprint.route('/api/threat-hunting/<int:hunt_id>', methods=['POST'])
@login_required
def update_hunt(hunt_id):
    caseid = request.args.get('cid', 0, type=int)
    hunt = ThreatHunt.query.filter_by(id=hunt_id, case_id=caseid).first()
    if not hunt:
        return response_error('Hunt not found')

    data = request.get_json()
    if not data or not data.get('hypothesis'):
        return response_error('Hypothesis is required')

    hunt.hypothesis = data['hypothesis']
    hunt.technique = data.get('technique', hunt.technique)
    hunt.data_sources = data.get('data_sources', hunt.data_sources)
    hunt.notes = data.get('notes', hunt.notes)
    hunt.outcome = data.get('outcome', hunt.outcome)
    hunt.status = data.get('status', hunt.status)
    db.session.commit()
    return response_success('Hunt updated', data=hunt.to_dict())


@threat_hunting_blueprint.route('/api/threat-hunting/<int:hunt_id>', methods=['DELETE'])
@login_required
def delete_hunt(hunt_id):
    caseid = request.args.get('cid', 0, type=int)
    hunt = ThreatHunt.query.filter_by(id=hunt_id, case_id=caseid).first()
    if not hunt:
        return response_error('Hunt not found')

    db.session.delete(hunt)
    db.session.commit()
    return response_success('Hunt deleted')
