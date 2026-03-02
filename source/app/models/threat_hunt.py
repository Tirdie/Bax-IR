from app import db


class ThreatHunt(db.Model):
    __tablename__ = 'threat_hunts'

    id = db.Column(db.Integer, primary_key=True)
    hypothesis = db.Column(db.Text, nullable=False)
    technique = db.Column(db.String(256), default='')
    data_sources = db.Column(db.String(512), default='')
    notes = db.Column(db.Text, default='')
    status = db.Column(db.String(50), default='active')  # active | completed | cancelled
    outcome = db.Column(db.String(50), default='')       # threat_found | no_threat | inconclusive
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    case_id = db.Column(db.Integer, db.ForeignKey('cases.case_id'), nullable=True)
    created_at = db.Column(db.DateTime)

    def to_dict(self):
        return {
            'id': self.id,
            'hypothesis': self.hypothesis,
            'technique': self.technique,
            'data_sources': self.data_sources,
            'notes': self.notes,
            'status': self.status,
            'outcome': self.outcome,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else ''
        }
