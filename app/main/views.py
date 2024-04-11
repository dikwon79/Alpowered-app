from flask import render_template
from flask_login import current_user
from .. import db
from . import main
from ..models import APILog,User
from sqlalchemy.sql import func
from flask import request,jsonify
from collections import defaultdict


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
        query_statics , query_total = get_query_statistics()
        
        return render_template('admin.html', user_statistics=user_statistics, total_statistics = statistics, query_statistics=query_statics , query_total=query_total)
    else:
        return render_template('404.html')
    
@main.route('/docs')  
def docs():   
    return render_template('docs.html')

@main.route('/count',  methods=['POST'])
def record_api_consumption(response):
    if current_user.is_authenticated:
        api_log = APILog(user_id=current_user.id, endpoint=request.endpoint, method=request.method, timestamp=func.now())
        db.session.add(api_log)
        db.session.commit()
    return response


 
@main.route('/update', methods=['POST'])
def update_role():
    role = request.json.get('role')
    id = request.json.get('id')
  
  
    user = User.query.get(id)
    print(user)
    if user:
        # 사용자의 역할을 업데이트합니다.
        user.role = role
        db.session.commit()
        return jsonify({'message': 'Role updated successfully'})
    else:
        return jsonify({'error': 'User not found'}), 404

@main.route('/delete', methods=['POST'])
def delete_user():
    try:
        # 요청에서 사용자 ID를 가져옵니다.
        user_id = request.json.get('id')
        
        # 사용자를 데이터베이스에서 가져옵니다.
        user = User.query.get(user_id)
        
        if user:
            # 사용자를 삭제합니다.
            db.session.delete(user)
            db.session.commit()
            return jsonify({'message': f'User {user.username} deleted successfully'}), 200
        else:
            return jsonify({'error': 'User not found'}), 404

    except Exception as e:
        # 예외가 발생하면 에러 메시지를 반환합니다.
        return jsonify({'error': str(e)}), 500
    
@main.after_request
def record_api_consumption(response):
    if request.path == "/delete":
        router = "DELETE"
    elif request.path == "/update":
        router = "PATCH"
    else:
        router = request.method    
    
    api_log = APILog(type='QUERY', endpoint=request.path, method=router, timestamp=func.now())
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

def get_query_requests(method, endpoint):
    # 해당 사용자와 메서드로 필터링하여 요청 수를 가져옴
    query_requests = APILog.query.filter_by(method=method, endpoint=endpoint).count()
    return query_requests


def get_endpoints():
   
    endpoints = APILog.query.with_entities(APILog.endpoint).distinct().all()
    
    
    endpoint_list = [endpoint[0] for endpoint in endpoints]
    
    return endpoint_list
       
def get_query_statistics():
    # 모든 사용자에 대한 통계 데이터를 계산
    methods = ['GET', 'POST', 'PATCH', 'DELETE']
    endpoints = get_endpoints()
    
    query_statistics = defaultdict(dict)
    query_total = defaultdict(int)  # 수정: defaultdict를 사용하여 초기화
    
    for endpoint in endpoints:
        for method in methods:
            total_requests = get_query_requests(method, endpoint)
            query_statistics[endpoint][method] = total_requests
            query_total[method] += total_requests  # 수정: 각 메서드별 합계를 계산하여 누적
            print(method)
    
    return query_statistics, query_total
  


def get_user_statistics():
    # 모든 사용자에 대한 통계 데이터를 계산
    users = User.query.all()
    user_statistics = defaultdict(dict)
    statistics = {'get': 0, 'post': 0, 'patch': 0, 'delete': 0} 
    for user in users:
        user_id = user.id
        user_email = user.email
        total_get_requests = get_total_requests(user_id, 'GET')
        total_post_requests = get_total_requests(user_id, 'POST')
        total_patch_requests = get_total_requests(user_id, 'PATCH')
        total_delete_requests = get_total_requests(user_id, 'DELETE')
        total_all_requests = total_get_requests + total_post_requests + total_patch_requests + total_delete_requests
        
        user_statistics[user_id]['username'] = user.username
        user_statistics[user_id]['email'] = user.email
        user_statistics[user_id]['role'] = user.role
        user_statistics[user_id]['id'] = user.id
        
        user_statistics[user_id]['total_get_requests'] = total_get_requests
        user_statistics[user_id]['total_post_requests'] = total_post_requests
        user_statistics[user_id]['total_patch_requests'] = total_patch_requests
        user_statistics[user_id]['total_delete_requests'] = total_delete_requests
        user_statistics[user_id]['total_all_requests'] = total_all_requests
        
        statistics['get'] += total_get_requests
        statistics['post'] += total_post_requests
        statistics['patch'] += total_patch_requests
        statistics['delete'] += total_delete_requests
        
        
        
    return user_statistics, statistics