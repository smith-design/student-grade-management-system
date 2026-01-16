from data_storage import execute_sql

def login(username, password):
    """
    用户登录验证
    :param username: 用户名
    :param password: 密码
    :return: 成功返回用户信息，失败返回 None
    """
    sql = "SELECT * FROM users WHERE username = :username"
    users = execute_sql(sql, {'username': username})
    
    if users:
        # 这里只是简单的明文比较，实际项目中应该使用哈希加盐
        user = users[0]
        if user['password'] == password:
            return user
    return None

def get_all_users():
    """获取所有用户"""
    return execute_sql("SELECT * FROM users")

def add_user(user_data):
    """
    添加用户
    :param user_data: 包含 username, password, role 的字典
    :return: 结果字典 {'success': bool, 'message': str}
    """
    # 检查用户名是否已存在
    existing_users = execute_sql("SELECT * FROM users WHERE username = :username", 
                               {'username': user_data['username']})
    if existing_users:
        return {'success': False, 'message': '用户名已存在'}
        
    try:
        execute_sql("INSERT INTO users", user_data)
        return {'success': True, 'message': '用户添加成功'}
    except Exception as e:
        return {'success': False, 'message': str(e)}

def delete_user(user_id):
    """删除用户"""
    try:
        count = execute_sql("DELETE FROM users", {'id': int(user_id)})
        if count > 0:
            return {'success': True, 'message': '用户删除成功'}
        else:
            return {'success': False, 'message': '用户不存在'}
    except Exception as e:
        return {'success': False, 'message': str(e)}

def get_user_by_id(user_id):
    """通过 ID 获取用户"""
    users = get_all_users()
    for user in users:
        if user['id'] == int(user_id):
            return user
    return None
