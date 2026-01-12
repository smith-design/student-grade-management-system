"""成绩管理服务 - 构造 SQL 并调用模拟引擎"""
from data_storage import execute_sql
import student_service


def get_all_grades():
    """获取所有成绩"""
    sql = "SELECT * FROM grades"
    return execute_sql(sql)


def get_grades_by_student(student_id):
    """获取某个学生的所有成绩"""
    sql = "SELECT * FROM grades WHERE student_id = :student_id"
    return execute_sql(sql, {'student_id': student_id})


def add_grade(grade_data):
    """添加成绩"""
    # 验证学生是否存在
    student = student_service.get_student_by_id(grade_data['student_id'])
    if not student:
        return {'success': False, 'message': '学生不存在'}
    
    # 验证必填字段
    required_fields = ['student_id', 'subject', 'score']
    for field in required_fields:
        if field not in grade_data:
            return {'success': False, 'message': f'缺少必填字段: {field}'}
    
    # 验证分数范围
    score = grade_data['score']
    if not isinstance(score, (int, float)) or score < 0 or score > 100:
        return {'success': False, 'message': '分数必须在 0-100 之间'}
    
    sql = """
    INSERT INTO grades (student_id, subject, score, exam_type, exam_date)
    VALUES (:student_id, :subject, :score, :exam_type, :exam_date)
    """
    
    execute_sql(sql, grade_data)
    return {'success': True, 'message': '添加成功'}


def update_grade(grade_id, grade_data):
    """更新成绩"""
    # 这里稍微麻烦点，因为模拟器需要先查是否存在
    all_grades = get_all_grades()
    exists = any(g['id'] == grade_id for g in all_grades)
    
    if not exists:
         return {'success': False, 'message': '成绩记录不存在'}
         
    if 'score' in grade_data:
        score = grade_data['score']
        if not isinstance(score, (int, float)) or score < 0 or score > 100:
            return {'success': False, 'message': '分数必须在 0-100 之间'}

    sql = "UPDATE grades SET ... WHERE id=:id"
    params = {
        'where_id': grade_id,
        'update_data': grade_data
    }
    
    execute_sql(sql, params)
    return {'success': True, 'message': '更新成功'}


def delete_grade(grade_id):
    """删除成绩"""
    sql = "DELETE FROM grades WHERE id = :id"
    count = execute_sql(sql, {'id': grade_id})
    
    if count > 0:
        return {'success': True, 'message': '删除成功'}
    else:
        return {'success': False, 'message': '成绩记录不存在'}


def get_statistics(student_id=None):
    """获取成绩统计"""
    # 这里直接复用 python 计算，因为 JSON 无法像 SQL 那样直接聚合
    grades = get_all_grades()
    
    if student_id:
        grades = [g for g in grades if g['student_id'] == student_id]
    
    if not grades:
        return {'success': True, 'data': {'count': 0, 'average': 0, 'max': 0, 'min': 0}}
    
    scores = [g['score'] for g in grades]
    return {
        'success': True,
        'data': {
            'count': len(scores),
            'average': round(sum(scores) / len(scores), 2),
            'max': max(scores),
            'min': min(scores)
        }
    }
