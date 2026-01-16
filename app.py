"""学生成绩管理系统 - Flask + Jinja2 版"""
from flask import Flask, render_template, request, redirect, url_for, flash, session
from functools import wraps
import student_service
import grade_service
import user_service
import school_service
from data_storage import ensure_data_files
import csv
import io
from flask import Response

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# 确保数据文件存在
ensure_data_files()

# 登录验证装饰器
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# 上下文处理器
@app.context_processor
def inject_common_data():
    return {}

# ==================== 页面路由 ====================

@app.route('/login', methods=['GET', 'POST'])
def login():
    """登录页面"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = user_service.login(username, password)
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user.get('role', 'user')
            flash('登录成功', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('用户名或密码错误', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    """退出登录"""
    session.clear()
    flash('已退出登录', 'success')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def dashboard():
    """系统仪表盘"""
    # 聚合数据
    students = student_service.get_all_students()
    classes = school_service.get_all_classes()
    courses = school_service.get_all_courses()
    grades = grade_service.get_all_grades()
    
    stats = {
        'student_count': len(students),
        'class_count': len(classes),
        'course_count': len(courses),
        'failed_count': len([g for g in grades if g['score'] < 60])
    }
    
    # 获取最近添加的5个学生（假设列表是按时间顺序或者我们直接取最后5个倒序）
    recent_students = students[-5:][::-1]
    
    return render_template('dashboard.html', stats=stats, recent_students=recent_students, active_page='dashboard')

@app.route('/students')
@login_required
def index():
    """学生列表页面（带搜索）"""
    keyword = request.args.get('keyword')
    if keyword:
        students = student_service.search_students(keyword)
    else:
        students = student_service.get_all_students()
        
    return render_template('student_list.html', students=students, active_page='students', keyword=keyword)

@app.route('/students/export')
@login_required
def export_students_action():
    """导出学生数据为CSV"""
    students = student_service.get_all_students()
    
    # 使用 StringIO 在内存中生成 CSV
    si = io.StringIO()
    cw = csv.writer(si)
    # 写入表头
    cw.writerow(['学号', '姓名', '班级', '性别', '年龄', '电话', '邮箱', '地址'])
    # 写入数据
    for s in students:
        cw.writerow([
            s.get('student_id'),
            s.get('name'),
            s.get('class_name'),
            s.get('gender'),
            s.get('age'),
            s.get('phone'),
            s.get('email'),
            s.get('address')
        ])
        
    output = si.getvalue()
    # 解决中文乱码，添加 BOM
    output = '\ufeff' + output
    
    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=students_export.csv"}
    )



@app.route('/users')
@login_required
def user_list_page():
    """用户列表页面"""
    if session.get('role') != 'admin':
        flash('无权访问', 'error')
        return redirect(url_for('index'))
    users = user_service.get_all_users()
    return render_template('user_list.html', users=users, active_page='users')

@app.route('/users/add', methods=['POST'])
@login_required
def add_user_action():
    """添加用户"""
    if session.get('role') != 'admin':
        flash('无权操作', 'error')
        return redirect(url_for('index'))
        
    user_data = {
        'username': request.form.get('username'),
        'password': request.form.get('password'),
        'role': request.form.get('role')
    }
    result = user_service.add_user(user_data)
    if result['success']:
        flash('用户添加成功', 'success')
    else:
        flash(result['message'], 'error')
    return redirect(url_for('user_list_page'))

@app.route('/users/delete/<int:user_id>', methods=['POST'])
@login_required
def delete_user_action(user_id):
    """删除用户"""
    if session.get('role') != 'admin':
        flash('无权操作', 'error')
        return redirect(url_for('index'))
        
    # 防止删除自己
    if user_id == session.get('user_id'):
        flash('不能删除当前登录账号', 'error')
        return redirect(url_for('user_list_page'))
        
    result = user_service.delete_user(user_id)
    if result['success']:
        flash('用户删除成功', 'success')
    else:
        flash(result['message'], 'error')
    return redirect(url_for('user_list_page'))


# ----- 班级管理 -----

@app.route('/classes')
@login_required
def class_list_page():
    """班级列表页面"""
    classes = school_service.get_all_classes()
    return render_template('class_list.html', classes=classes, active_page='classes')

@app.route('/classes/add', methods=['POST'])
@login_required
def add_class_action():
    """添加班级"""
    name = request.form.get('name')
    result = school_service.add_class(name)
    if result['success']:
        flash('班级添加成功', 'success')
    else:
        flash(result['message'], 'error')
    return redirect(url_for('class_list_page'))

@app.route('/classes/delete/<int:class_id>', methods=['POST'])
@login_required
def delete_class_action(class_id):
    """删除班级"""
    result = school_service.delete_class(class_id)
    if result['success']:
        flash('班级删除成功', 'success')
    else:
        flash(result['message'], 'error')
    return redirect(url_for('class_list_page'))


# ----- 课程管理 -----

@app.route('/courses')
@login_required
def course_list_page():
    """课程列表页面"""
    courses = school_service.get_all_courses()
    return render_template('course_list.html', courses=courses, active_page='courses')

@app.route('/courses/add', methods=['POST'])
@login_required
def add_course_action():
    """添加课程"""
    name = request.form.get('name')
    credit = request.form.get('credit')
    result = school_service.add_course(name, credit)
    if result['success']:
        flash('课程添加成功', 'success')
    else:
        flash(result['message'], 'error')
    return redirect(url_for('course_list_page'))

@app.route('/courses/delete/<int:course_id>', methods=['POST'])
@login_required
def delete_course_action(course_id):
    """删除课程"""
    result = school_service.delete_course(course_id)
    if result['success']:
        flash('课程删除成功', 'success')
    else:
        flash(result['message'], 'error')
    return redirect(url_for('course_list_page'))


# ----- 学生管理 -----

@app.route('/students/add', methods=['GET', 'POST'])
@login_required
def add_student_page():
    """添加学生页面 & 处理"""
    classes = school_service.get_all_classes()
    
    if request.method == 'POST':
        student_data = {
            'student_id': request.form.get('student_id'),
            'name': request.form.get('name'),
            'class_name': request.form.get('class_name'),
            'gender': request.form.get('gender'),
            'age': request.form.get('age'),
            'phone': request.form.get('phone'),
            'email': request.form.get('email'),
            'address': request.form.get('address')
        }
        
        if student_data['age']:
            student_data['age'] = int(student_data['age'])
        else:
            student_data.pop('age')
            
        result = student_service.add_student(student_data)
        if result['success']:
            flash('学生添加成功', 'success')
            return redirect(url_for('index'))
        else:
            flash(result['message'], 'error')
            
    return render_template('student_form.html', student=None, classes=classes, active_page='students')


@app.route('/students/edit/<student_id>', methods=['GET', 'POST'])
@login_required
def edit_student_page(student_id):
    """编辑学生页面 & 处理"""
    student = student_service.get_student_by_id(student_id)
    if not student:
        flash('学生不存在', 'error')
        return redirect(url_for('index'))

    classes = school_service.get_all_classes()

    if request.method == 'POST':
        student_data = {
            'name': request.form.get('name'),
            'class_name': request.form.get('class_name'),
            'gender': request.form.get('gender'),
            'age': request.form.get('age'),
            'phone': request.form.get('phone'),
            'email': request.form.get('email'),
            'address': request.form.get('address')
        }
        if student_data['age']:
            student_data['age'] = int(student_data['age'])
        else:
             student_data.pop('age')

        result = student_service.update_student(student_id, student_data)
        if result['success']:
            flash('学生信息更新成功', 'success')
            return redirect(url_for('index'))
        else:
            flash(result['message'], 'error')

    return render_template('student_form.html', student=student, classes=classes, active_page='students')


@app.route('/students/delete/<student_id>', methods=['POST'])
@login_required
def delete_student_action(student_id):
    """删除学生操作"""
    result = student_service.delete_student(student_id)
    if result['success']:
        flash('学生已删除', 'success')
    else:
        flash(result['message'], 'error')
    return redirect(url_for('index'))


# ----- 成绩管理 -----

@app.route('/grades')
@login_required
def grades_page():
    """成绩列表页面"""
    student_id = request.args.get('student_id')
    if student_id:
        grades = grade_service.get_grades_by_student(student_id)
    else:
        grades = grade_service.get_all_grades()
    
    # 补充学生姓名信息
    students = student_service.get_all_students()
    student_map = {s['student_id']: s['name'] for s in students}
    
    for grade in grades:
        grade['student_name'] = student_map.get(grade['student_id'], '未知')
        
    return render_template('grade_list.html', grades=grades, active_page='grades')


@app.route('/grades/add', methods=['GET', 'POST'])
@login_required
def add_grade_page():
    """添加成绩页面 & 处理"""
    students = student_service.get_all_students()
    courses = school_service.get_all_courses()
    
    if request.method == 'POST':
        grade_data = {
            'student_id': request.form.get('student_id'),
            'subject': request.form.get('subject'),
            'score': request.form.get('score'),
            'exam_type': request.form.get('exam_type'),
            'exam_date': request.form.get('exam_date')
        }
        
        try:
            grade_data['score'] = float(grade_data['score'])
            result = grade_service.add_grade(grade_data)
            if result['success']:
                flash('成绩添加成功', 'success')
                return redirect(url_for('grades_page'))
            else:
                flash(result['message'], 'error')
        except ValueError:
            flash('分数格式错误', 'error')

    return render_template('grade_form.html', grade=None, students=students, courses=courses, active_page='grades')


@app.route('/grades/edit/<int:grade_id>', methods=['GET', 'POST'])
@login_required
def edit_grade_page(grade_id):
    """编辑成绩页面 & 处理"""
    # 查找成绩（由于现在不是 ORM，直接调 Service）
    all_grades = grade_service.get_all_grades()
    grade = next((g for g in all_grades if g['id'] == grade_id), None)
    
    if not grade:
        flash('成绩记录不存在', 'error')
        return redirect(url_for('grades_page'))
    
    students = student_service.get_all_students()
    courses = school_service.get_all_courses()
    
    # 补充当前成绩的学生姓名
    student_name = next((s['name'] for s in students if s['student_id'] == grade['student_id']), '未知')
    grade['student_name'] = student_name

    if request.method == 'POST':
        grade_data = {
            'subject': request.form.get('subject'),
            'score': request.form.get('score'),
            'exam_type': request.form.get('exam_type'),
            'exam_date': request.form.get('exam_date')
        }
        
        try:
            grade_data['score'] = float(grade_data['score'])
            result = grade_service.update_grade(grade_id, grade_data)
            if result['success']:
                flash('成绩更新成功', 'success')
                return redirect(url_for('grades_page'))
            else:
                flash(result['message'], 'error')
        except ValueError:
            flash('分数格式错误', 'error')

    return render_template('grade_form.html', grade=grade, students=students, courses=courses, active_page='grades')


@app.route('/grades/delete/<int:grade_id>', methods=['POST'])
@login_required
def delete_grade_action(grade_id):
    """删除成绩操作"""
    result = grade_service.delete_grade(grade_id)
    if result['success']:
        flash('成绩已删除', 'success')
    else:
        flash(result['message'], 'error')
    return redirect(url_for('grades_page'))


# ----- 统计 -----

@app.route('/statistics')
@login_required
def statistics_page():
    """数据统计页面"""
    student_id = request.args.get('student_id')
    result = grade_service.get_statistics(student_id)
    
    students = student_service.get_all_students()
    
    return render_template('statistics.html', 
                         stats=result['data'], 
                         students=students, 
                         current_student_id=student_id,
                         active_page='statistics')


if __name__ == '__main__':
    print("学生成绩管理系统 (Flask) 启动中...")
    print("访问地址: http://localhost:5002")
    app.run(debug=True, host='0.0.0.0', port=5002)
