from data_storage import execute_sql

# ----- 班级管理 -----

def get_all_classes():
    """获取所有班级"""
    return execute_sql("SELECT * FROM classes")

def add_class(name):
    """添加班级"""
    if not name:
        return {'success': False, 'message': '班级名称不能为空'}
    
    # 检查是否存在
    classes = get_all_classes()
    for c in classes:
        if c['name'] == name:
            return {'success': False, 'message': '该班级已存在'}
            
    execute_sql("INSERT INTO classes", {'name': name})
    return {'success': True, 'message': '班级添加成功'}

def delete_class(class_id):
    """删除班级"""
    try:
        count = execute_sql("DELETE FROM classes", {'id': int(class_id)})
        if count > 0:
            return {'success': True, 'message': '班级删除成功'}
        else:
            return {'success': False, 'message': '班级不存在'}
    except Exception as e:
        return {'success': False, 'message': str(e)}


# ----- 课程管理 -----

def get_all_courses():
    """获取所有课程"""
    return execute_sql("SELECT * FROM courses")

def add_course(name, credit):
    """添加课程"""
    if not name:
        return {'success': False, 'message': '课程名称不能为空'}
    
    # 检查是否存在
    courses = get_all_courses()
    for c in courses:
        if c['name'] == name:
            return {'success': False, 'message': '该课程已存在'}
            
    try:
        credit = float(credit)
    except ValueError:
        return {'success': False, 'message': '学分必须是数字'}

    execute_sql("INSERT INTO courses", {'name': name, 'credit': credit})
    return {'success': True, 'message': '课程添加成功'}

def delete_course(course_id):
    """删除课程"""
    try:
        count = execute_sql("DELETE FROM courses", {'id': int(course_id)})
        if count > 0:
            return {'success': True, 'message': '课程删除成功'}
        else:
            return {'success': False, 'message': '课程不存在'}
    except Exception as e:
        return {'success': False, 'message': str(e)}
