from . import db
from . import login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(512))
    

    @property
    def password(self):
        raise AttributeError('cannot read password.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def set_password(self, new_password):
        self.password = new_password
    

    def create_admin_user():
    # 이메일을 통해 사용자 조회
        existing_user = User.query.filter_by(email='admin@admin.com').first()
        
        # 사용자가 존재하지 않는 경우에만 생성
        if not existing_user:
            # 관리자 사용자 생성
            admin = User(email='admin@admin.com', username='admin')
            admin.password = '111'  # 비밀번호 설정

            # 데이터베이스에 추가
            db.session.add(admin)
            db.session.commit()
    

class APILog(db.Model):
    __tablename__ = 'api_logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    endpoint = db.Column(db.String(128))
    method = db.Column(db.String(10))
    timestamp = db.Column(db.DateTime, server_default=func.now())


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



