"""数据存储服务 - 模拟数据库操作层
支持 JSON 文件存储，但通过 execute_sql 函数模拟 SQL 执行过程
"""
import json
import os
import time

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
STUDENTS_FILE = os.path.join(DATA_DIR, 'students.json')
GRADES_FILE = os.path.join(DATA_DIR, 'grades.json')


def ensure_data_files():
    """初始化数据存储"""
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(STUDENTS_FILE):
        _save_json(STUDENTS_FILE, [])
    if not os.path.exists(GRADES_FILE):
        _save_json(GRADES_FILE, [])

def _load_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def _save_json(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def execute_sql(sql, params=None):
    """
    模拟执行 SQL 语句
    :param sql: SQL 语句字符串
    :param params: SQL 参数
    :return: 模拟的执行结果 (列表或影响行数)
    """
    print("-" * 50)
    print(f"Executing SQL: {sql.strip()}")
    if params:
        # 为了让日志看起来更像真实数据库日志，这里格式化一下参数显示
        print(f"Parameters: {params}")
    print("-" * 50)
    
    # 简单的 SQL 解析和路由 (非常基础的模拟)
    sql_upper = sql.strip().upper()
    
    # 1. SELECT 查询
    if sql_upper.startswith("SELECT"):
        return _handle_select(sql, params)
    
    # 2. INSERT 插入
    elif sql_upper.startswith("INSERT"):
        return _handle_insert(sql, params)
        
    # 3. UPDATE 更新
    elif sql_upper.startswith("UPDATE"):
        return _handle_update(sql, params)
        
    # 4. DELETE 删除
    elif sql_upper.startswith("DELETE"):
        return _handle_delete(sql, params)
        
    return None

def _handle_select(sql, params):
    """处理 SELECT 模拟"""
    # 简单判断查哪张表
    if "FROM students" in sql:
        data = _load_json(STUDENTS_FILE)
        # 简单模拟 WHERE 过滤
        if "WHERE student_id =" in sql and params:
            return [s for s in data if s['student_id'] == params['student_id']]
        return data
    elif "FROM grades" in sql:
        data = _load_json(GRADES_FILE)
        if "WHERE student_id =" in sql and params:
             return [g for g in data if g['student_id'] == params['student_id']]
        return data
    return []

def _handle_insert(sql, params):
    """处理 INSERT 模拟"""
    if "INTO students" in sql:
        data = _load_json(STUDENTS_FILE)
        # 构造新记录 (params 必须包含所有字段)
        new_record = params.copy()
        if 'id' not in new_record:
            new_record['id'] = int(time.time() * 1000)
        data.append(new_record)
        _save_json(STUDENTS_FILE, data)
        return 1
    elif "INTO grades" in sql:
        data = _load_json(GRADES_FILE)
        new_record = params.copy()
        if 'id' not in new_record:
            new_record['id'] = int(time.time() * 1000)
        data.append(new_record)
        _save_json(GRADES_FILE, data)
        return 1
    return 0

def _handle_update(sql, params):
    """处理 UPDATE 模拟"""
    if "students" in sql:
        data = _load_json(STUDENTS_FILE)
        count = 0
        for item in data:
            if item['student_id'] == params.get('where_student_id'):
                item.update(params['update_data'])
                count += 1
        if count > 0:
            _save_json(STUDENTS_FILE, data)
        return count
    elif "grades" in sql:
        data = _load_json(GRADES_FILE)
        count = 0
        for item in data:
            if item['id'] == params.get('where_id'):
                item.update(params['update_data'])
                count += 1
        if count > 0:
            _save_json(GRADES_FILE, data)
        return count
    return 0

def _handle_delete(sql, params):
    """处理 DELETE 模拟"""
    if "FROM students" in sql:
        data = _load_json(STUDENTS_FILE)
        initial_len = len(data)
        data = [d for d in data if d['student_id'] != params['student_id']]
        if len(data) < initial_len:
            _save_json(STUDENTS_FILE, data)
            return initial_len - len(data)
    elif "FROM grades" in sql:
        data = _load_json(GRADES_FILE)
        initial_len = len(data)
        data = [d for d in data if d['id'] != params['id']]
        if len(data) < initial_len:
            _save_json(GRADES_FILE, data)
            return initial_len - len(data)
    return 0
