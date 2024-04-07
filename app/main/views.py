from flask import render_template
from flask_login import current_user
from .. import db
from . import main
from ..models import APILog,User
from sqlalchemy.sql import func
from flask import request
from collections import defaultdict
from flask_cors import CORS


CORS(main)

@main.route('/')
def index():
    if current_user.is_authenticated:
        user_id = current_user.id  
        total_api_logs = get_total_api_logs(user_id) + 1
        return render_template('main.html', total_api_logs=total_api_logs)
    else:
        return render_template('index.html')

@main.route('/admin')
def admin():
    if current_user.is_authenticated and current_user.username == 'admin':
        # 모든 사용자의 통계 데이터를 가져옴
        user_statistics, statistics = get_user_statistics()
        
        return render_template('admin.html', user_statistics=user_statistics, total_statistics = statistics)
    else:
        return render_template('404.html')

@main.after_request
def record_api_consumption(response):
   
    if current_user.is_authenticated:
        # 사용자가 로그인한 경우에만 API 소비를 카운트
        api_log = APILog(user_id=current_user.id, endpoint=request.endpoint, method=request.method, timestamp=func.now())
        db.session.add(api_log)
        db.session.commit()
    return response

def get_total_api_logs(user_id):
    # total count api
    total_api_logs = APILog.query.filter_by(user_id=user_id).count()
    return total_api_logs


def get_total_requests(user_id, method):
    # 해당 사용자와 메서드로 필터링하여 요청 수를 가져옴
    total_requests = APILog.query.filter_by(user_id=user_id, method=method).count()
    return total_requests

def get_user_statistics():
    # 모든 사용자에 대한 통계 데이터를 계산
    users = User.query.all()
    user_statistics = defaultdict(dict)
    statistics = {'get': 0, 'post': 0, 'put': 0, 'head': 0} 
    for user in users:
        user_id = user.id
        user_email = user.email
        total_get_requests = get_total_requests(user_id, 'GET')
        total_post_requests = get_total_requests(user_id, 'POST')
        total_head_requests = get_total_requests(user_id, 'HEAD')
        total_put_requests = get_total_requests(user_id, 'PUT')
        total_all_requests = total_get_requests + total_post_requests + total_head_requests + total_put_requests
        
        user_statistics[user_id]['username'] = user.username
        user_statistics[user_id]['email'] = user.email
        user_statistics[user_id]['total_get_requests'] = total_get_requests
        user_statistics[user_id]['total_post_requests'] = total_post_requests
        user_statistics[user_id]['total_head_requests'] = total_head_requests
        user_statistics[user_id]['total_put_requests'] = total_put_requests
        user_statistics[user_id]['total_all_requests'] = total_all_requests
        
        statistics['get'] += total_get_requests
        statistics['post'] += total_post_requests
        statistics['put'] += total_put_requests
        statistics['head'] += total_head_requests
        
        
        
    return user_statistics, statistics