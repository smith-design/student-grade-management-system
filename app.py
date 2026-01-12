"""学生成绩管理系统 - Flask + Jinja2 版"""
from flask import Flask, render_template, request, redirect, url_for, flash
import student_service
import grade_service
from data_storage import ensure_data_files

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# 确保数据文件存在
ensure_data_files()

# 上下文处理器
@app.context_processor
def inject_common_data():
    return {}

# ==================== 页面路由 ====================

@app.route('/')
def index():
    """首页：学生列表"""
    students = student_service.get_all_students()
    return render_template('student_list.html', students=students, active_page='students')


# ----- 学生管理 -----

@app.route('/students/add', methods=['GET', 'POST'])
def add_student_page():
    """添加学生页面 & 处理"""
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
            
    return render_template('student_form.html', student=None, active_page='students')


@app.route('/students/edit/<student_id>', methods=['GET', 'POST'])
def edit_student_page(student_id):
    """编辑学生页面 & 处理"""
    student = student_service.get_student_by_id(student_id)
    if not student:
        flash('学生不存在', 'error')
        return redirect(url_for('index'))

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

    return render_template('student_form.html', student=student, active_page='students')


@app.route('/students/delete/<student_id>', methods=['POST'])
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
def add_grade_page():
    """添加成绩页面 & 处理"""
    students = student_service.get_all_students()
    
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

    return render_template('grade_form.html', grade=None, students=students, active_page='grades')


@app.route('/grades/edit/<int:grade_id>', methods=['GET', 'POST'])
def edit_grade_page(grade_id):
    """编辑成绩页面 & 处理"""
    # 查找成绩（由于现在不是 ORM，直接调 Service）
    all_grades = grade_service.get_all_grades()
    grade = next((g for g in all_grades if g['id'] == grade_id), None)
    
    if not grade:
        flash('成绩记录不存在', 'error')
        return redirect(url_for('grades_page'))
    
    students = student_service.get_all_students()
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

    return render_template('grade_form.html', grade=grade, students=students, active_page='grades')


@app.route('/grades/delete/<int:grade_id>', methods=['POST'])
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
