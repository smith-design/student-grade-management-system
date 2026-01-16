"""学生管理服务 - 构造 SQL 并调用模拟引擎"""
import time
from data_storage import execute_sql


def get_all_students():
    """获取所有学生"""
    sql = "SELECT * FROM students"
    return execute_sql(sql)


def get_student_by_id(student_id):
    """根据学号获取学生"""
    sql = "SELECT * FROM students WHERE student_id = :student_id"
    results = execute_sql(sql, {'student_id': student_id})
    return results[0] if results else None


def add_student(student_data):
    """添加学生"""
    # 检查是否存在
    existing = get_student_by_id(student_data['student_id'])
    if existing:
        return {'success': False, 'message': '学号已存在'}
    
    # 验证必填字段
    required_fields = ['student_id', 'name', 'class_name']
    for field in required_fields:
        if field not in student_data or not student_data[field]:
            return {'success': False, 'message': f'缺少必填字段: {field}'}
    
    # 构造 SQL
    sql = """
    INSERT INTO students (student_id, name, class_name, gender, age, phone, email, address, created_at)
    VALUES (:student_id, :name, :class_name, :gender, :age, :phone, :email, :address, :created_at)
    """
    
    # 补充数据
    params = student_data.copy()
    params['created_at'] = time.strftime('%Y-%m-%dT%H:%M:%S')
    
    execute_sql(sql, params)
    return {'success': True, 'message': '添加成功'}


def update_student(student_id, student_data):
    """更新学生信息"""
    existing = get_student_by_id(student_id)
    if not existing:
        return {'success': False, 'message': '学生不存在'}
        
    sql = "UPDATE students SET name=:name, class_name=:class_name, ... WHERE student_id=:student_id"
    
    # 传递给模拟器的参数
    params = {
        'where_student_id': student_id,
        'update_data': student_data
    }
    
    execute_sql(sql, params)
    return {'success': True, 'message': '更新成功'}


def delete_student(student_id):
    """删除学生"""
    sql = "DELETE FROM students WHERE student_id = :student_id"
    count = execute_sql(sql, {'student_id': student_id})
    
    if count > 0:
        return {'success': True, 'message': '删除成功'}
    else:
        return {'success': False, 'message': '学生不存在'}

def search_students(keyword):
    """搜索学生（按姓名或学号）"""
    all_students = get_all_students()
    if not keyword:
        return all_students
    
    keyword = keyword.lower()
    return [
        s for s in all_students 
        if keyword in s['name'].lower() or keyword in s['student_id'].lower()
    ]

