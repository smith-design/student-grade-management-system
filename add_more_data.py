"""
添加更多示例数据
"""
import requests

BASE_URL = "http://localhost:5001/api"

# 更多学生数据
students = [
    {"student_id": "2024006", "name": "孙八", "class_name": "高一(1)班", "gender": "male", "age": 16, "phone": "13800138006"},
    {"student_id": "2024007", "name": "周九", "class_name": "高一(2)班", "gender": "female", "age": 15, "phone": "13800138007"},
    {"student_id": "2024008", "name": "吴十", "class_name": "高一(1)班", "gender": "male", "age": 17, "phone": "13800138008"},
    {"student_id": "2024009", "name": "郑十一", "class_name": "高一(2)班", "gender": "female", "age": 16, "phone": "13800138009"},
    {"student_id": "2024010", "name": "冯十二", "class_name": "高一(1)班", "gender": "male", "age": 15, "phone": "13800138010"},
    {"student_id": "2024011", "name": "陈十三", "class_name": "高一(2)班", "gender": "male", "age": 16, "phone": "13800138011"},
    {"student_id": "2024012", "name": "褚十四", "class_name": "高一(1)班", "gender": "female", "age": 17, "phone": "13800138012"},
    {"student_id": "2024013", "name": "卫十五", "class_name": "高一(2)班", "gender": "male", "age": 16, "phone": "13800138013"},
]

# 成绩数据 - 为新学生添加成绩
def generate_grades(student_id):
    import random
    subjects = ["语文", "数学", "英语", "物理", "化学"]
    grades = []
    for subject in subjects:
        # 生成随机分数 60-100
        score = random.randint(60, 100)
        grades.append({
            "student_id": student_id,
            "subject": subject,
            "score": score,
            "exam_date": "2024-12-01",
            "exam_type": "期末考试"
        })
    return grades


def add_data():
    print("=" * 50)
    print("添加更多数据")
    print("=" * 50)
    
    # 检查后端
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code != 200:
            print("❌ 后端服务未启动！")
            return
    except:
        print("❌ 无法连接后端服务！")
        return
    
    print("\n【添加学生】")
    added_students = []
    for student in students:
        response = requests.post(f"{BASE_URL}/students", json=student)
        data = response.json()
        if data.get("success"):
            print(f"  ✅ {student['name']} ({student['student_id']}) - {student['class_name']}")
            added_students.append(student['student_id'])
        else:
            print(f"  ⚠️  {student['name']}: {data.get('message')}")
    
    print(f"\n【添加成绩】")
    grade_count = 0
    for student_id in added_students:
        grades = generate_grades(student_id)
        for grade in grades:
            response = requests.post(f"{BASE_URL}/grades", json=grade)
            if response.json().get("success"):
                grade_count += 1
    print(f"  ✅ 添加了 {grade_count} 条成绩记录")
    
    # 获取当前统计
    print("\n" + "=" * 50)
    response = requests.get(f"{BASE_URL}/students")
    student_count = len(response.json().get("data", []))
    
    response = requests.get(f"{BASE_URL}/grades")
    total_grades = len(response.json().get("data", []))
    
    response = requests.get(f"{BASE_URL}/statistics")
    stats = response.json().get("data", {})
    
    print(f"当前数据统计:")
    print(f"  - 学生总数: {student_count} 人")
    print(f"  - 成绩总数: {total_grades} 条")
    print(f"  - 平均分: {stats.get('average')}")
    print(f"  - 最高分: {stats.get('max')}")
    print(f"  - 最低分: {stats.get('min')}")
    print("=" * 50)


if __name__ == "__main__":
    add_data()
