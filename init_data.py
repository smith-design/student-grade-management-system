"""
初始化示例数据脚本
"""
import requests

BASE_URL = "http://localhost:5001/api"

# 示例学生数据
students = [
    {
        "student_id": "2024001",
        "name": "张三",
        "class_name": "高一(1)班",
        "gender": "male",
        "age": 16,
        "address": "北京市海淀区中关村大街1号",
        "phone": "13800138001",
        "email": "zhangsan@example.com"
    },
    {
        "student_id": "2024002",
        "name": "李四",
        "class_name": "高一(1)班",
        "gender": "male",
        "age": 15,
        "address": "北京市朝阳区望京街2号",
        "phone": "13800138002",
        "email": "lisi@example.com"
    },
    {
        "student_id": "2024003",
        "name": "王五",
        "class_name": "高一(2)班",
        "gender": "female",
        "age": 16,
        "address": "北京市西城区金融街3号",
        "phone": "13800138003",
        "email": "wangwu@example.com"
    },
    {
        "student_id": "2024004",
        "name": "赵六",
        "class_name": "高一(2)班",
        "gender": "male",
        "age": 17,
        "address": "北京市东城区王府井4号",
        "phone": "13800138004",
        "email": "zhaoliu@example.com"
    },
    {
        "student_id": "2024005",
        "name": "钱七",
        "class_name": "高一(1)班",
        "gender": "female",
        "age": 16,
        "address": "北京市丰台区科技园5号",
        "phone": "13800138005",
        "email": "qianqi@example.com"
    }
]

# 示例成绩数据
grades = [
    # 张三的成绩
    {"student_id": "2024001", "subject": "语文", "score": 92, "exam_date": "2024-12-01", "exam_type": "期末考试"},
    {"student_id": "2024001", "subject": "数学", "score": 88, "exam_date": "2024-12-01", "exam_type": "期末考试"},
    {"student_id": "2024001", "subject": "英语", "score": 95, "exam_date": "2024-12-01", "exam_type": "期末考试"},
    {"student_id": "2024001", "subject": "物理", "score": 85, "exam_date": "2024-12-01", "exam_type": "期末考试"},
    {"student_id": "2024001", "subject": "化学", "score": 90, "exam_date": "2024-12-01", "exam_type": "期末考试"},
    
    # 李四的成绩
    {"student_id": "2024002", "subject": "语文", "score": 78, "exam_date": "2024-12-01", "exam_type": "期末考试"},
    {"student_id": "2024002", "subject": "数学", "score": 95, "exam_date": "2024-12-01", "exam_type": "期末考试"},
    {"student_id": "2024002", "subject": "英语", "score": 82, "exam_date": "2024-12-01", "exam_type": "期末考试"},
    {"student_id": "2024002", "subject": "物理", "score": 91, "exam_date": "2024-12-01", "exam_type": "期末考试"},
    {"student_id": "2024002", "subject": "化学", "score": 88, "exam_date": "2024-12-01", "exam_type": "期末考试"},
    
    # 王五的成绩
    {"student_id": "2024003", "subject": "语文", "score": 96, "exam_date": "2024-12-01", "exam_type": "期末考试"},
    {"student_id": "2024003", "subject": "数学", "score": 72, "exam_date": "2024-12-01", "exam_type": "期末考试"},
    {"student_id": "2024003", "subject": "英语", "score": 98, "exam_date": "2024-12-01", "exam_type": "期末考试"},
    {"student_id": "2024003", "subject": "物理", "score": 68, "exam_date": "2024-12-01", "exam_type": "期末考试"},
    {"student_id": "2024003", "subject": "化学", "score": 75, "exam_date": "2024-12-01", "exam_type": "期末考试"},
    
    # 赵六的成绩
    {"student_id": "2024004", "subject": "语文", "score": 85, "exam_date": "2024-12-01", "exam_type": "期末考试"},
    {"student_id": "2024004", "subject": "数学", "score": 90, "exam_date": "2024-12-01", "exam_type": "期末考试"},
    {"student_id": "2024004", "subject": "英语", "score": 88, "exam_date": "2024-12-01", "exam_type": "期末考试"},
    {"student_id": "2024004", "subject": "物理", "score": 92, "exam_date": "2024-12-01", "exam_type": "期末考试"},
    {"student_id": "2024004", "subject": "化学", "score": 86, "exam_date": "2024-12-01", "exam_type": "期末考试"},
    
    # 钱七的成绩
    {"student_id": "2024005", "subject": "语文", "score": 94, "exam_date": "2024-12-01", "exam_type": "期末考试"},
    {"student_id": "2024005", "subject": "数学", "score": 76, "exam_date": "2024-12-01", "exam_type": "期末考试"},
    {"student_id": "2024005", "subject": "英语", "score": 91, "exam_date": "2024-12-01", "exam_type": "期末考试"},
    {"student_id": "2024005", "subject": "物理", "score": 79, "exam_date": "2024-12-01", "exam_type": "期末考试"},
    {"student_id": "2024005", "subject": "化学", "score": 83, "exam_date": "2024-12-01", "exam_type": "期末考试"},
]


def init_data():
    """初始化数据"""
    print("=" * 50)
    print("初始化示例数据")
    print("=" * 50)
    
    # 检查后端是否运行
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code != 200:
            print("❌ 后端服务未启动！")
            return
    except:
        print("❌ 无法连接后端服务！请先启动后端。")
        return
    
    print("\n【添加学生】")
    student_count = 0
    for student in students:
        response = requests.post(f"{BASE_URL}/students", json=student)
        data = response.json()
        if data.get("success"):
            print(f"  ✅ 添加学生: {student['name']} ({student['student_id']})")
            student_count += 1
        else:
            print(f"  ⚠️  {student['name']}: {data.get('message')}")
    
    print(f"\n【添加成绩】")
    grade_count = 0
    for grade in grades:
        response = requests.post(f"{BASE_URL}/grades", json=grade)
        data = response.json()
        if data.get("success"):
            grade_count += 1
        else:
            print(f"  ⚠️  {grade['student_id']} {grade['subject']}: {data.get('message')}")
    print(f"  ✅ 添加了 {grade_count} 条成绩记录")
    
    print("\n" + "=" * 50)
    print(f"初始化完成！")
    print(f"  - 学生: {student_count} 人")
    print(f"  - 成绩: {grade_count} 条")
    print("=" * 50)
    
    # 显示统计
    response = requests.get(f"{BASE_URL}/statistics")
    stats = response.json().get("data", {})
    print(f"\n成绩统计:")
    print(f"  - 总记录数: {stats.get('count')}")
    print(f"  - 平均分: {stats.get('average')}")
    print(f"  - 最高分: {stats.get('max')}")
    print(f"  - 最低分: {stats.get('min')}")


if __name__ == "__main__":
    init_data()
