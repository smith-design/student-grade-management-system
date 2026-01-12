"""
学生成绩管理系统 - API 测试脚本
测试所有后端 API 接口功能
"""
import requests
import json
import sys

BASE_URL = "http://localhost:5001/api"

# 测试结果统计
results = {"passed": 0, "failed": 0, "tests": []}


def log_result(test_name, passed, message=""):
    """记录测试结果"""
    status = "✅ PASS" if passed else "❌ FAIL"
    results["tests"].append({
        "name": test_name,
        "passed": passed,
        "message": message
    })
    if passed:
        results["passed"] += 1
    else:
        results["failed"] += 1
    print(f"{status} | {test_name}" + (f" - {message}" if message else ""))


def test_health_check():
    """测试健康检查接口"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        data = response.json()
        passed = response.status_code == 200 and data.get("status") == "ok"
        log_result("健康检查", passed, data.get("message", ""))
        return passed
    except Exception as e:
        log_result("健康检查", False, str(e))
        return False


# ==================== 学生管理测试 ====================

def test_add_student():
    """测试添加学生"""
    try:
        student_data = {
            "student_id": "TEST001",
            "name": "测试学生",
            "class_name": "测试班级",
            "gender": "male",
            "age": 18,
            "address": "测试地址",
            "phone": "13800000001",
            "email": "test@example.com"
        }
        response = requests.post(f"{BASE_URL}/students", json=student_data)
        data = response.json()
        passed = response.status_code == 201 and data.get("success") == True
        log_result("添加学生", passed, data.get("message", ""))
        return passed
    except Exception as e:
        log_result("添加学生", False, str(e))
        return False


def test_add_duplicate_student():
    """测试添加重复学号学生"""
    try:
        student_data = {
            "student_id": "TEST001",
            "name": "重复学生",
            "class_name": "测试班级"
        }
        response = requests.post(f"{BASE_URL}/students", json=student_data)
        data = response.json()
        # 应该返回失败
        passed = response.status_code == 400 and data.get("success") == False
        log_result("添加重复学号（应失败）", passed, data.get("message", ""))
        return passed
    except Exception as e:
        log_result("添加重复学号（应失败）", False, str(e))
        return False


def test_get_all_students():
    """测试获取所有学生"""
    try:
        response = requests.get(f"{BASE_URL}/students")
        data = response.json()
        passed = response.status_code == 200 and data.get("success") == True
        student_count = len(data.get("data", []))
        log_result("获取所有学生", passed, f"共 {student_count} 名学生")
        return passed
    except Exception as e:
        log_result("获取所有学生", False, str(e))
        return False


def test_get_student_by_id():
    """测试根据学号获取学生"""
    try:
        response = requests.get(f"{BASE_URL}/students/TEST001")
        data = response.json()
        passed = response.status_code == 200 and data.get("success") == True
        student_name = data.get("data", {}).get("name", "")
        log_result("根据学号获取学生", passed, f"学生姓名: {student_name}")
        return passed
    except Exception as e:
        log_result("根据学号获取学生", False, str(e))
        return False


def test_get_nonexistent_student():
    """测试获取不存在的学生"""
    try:
        response = requests.get(f"{BASE_URL}/students/NOTEXIST")
        data = response.json()
        passed = response.status_code == 404 and data.get("success") == False
        log_result("获取不存在学生（应返回404）", passed, data.get("message", ""))
        return passed
    except Exception as e:
        log_result("获取不存在学生（应返回404）", False, str(e))
        return False


def test_update_student():
    """测试更新学生信息"""
    try:
        update_data = {
            "name": "测试学生（已更新）",
            "age": 19
        }
        response = requests.put(f"{BASE_URL}/students/TEST001", json=update_data)
        data = response.json()
        passed = response.status_code == 200 and data.get("success") == True
        log_result("更新学生信息", passed, data.get("message", ""))
        return passed
    except Exception as e:
        log_result("更新学生信息", False, str(e))
        return False


# ==================== 成绩管理测试 ====================

def test_add_grade():
    """测试添加成绩"""
    try:
        grade_data = {
            "student_id": "TEST001",
            "subject": "数学",
            "score": 95,
            "exam_date": "2024-12-08",
            "exam_type": "期末考试"
        }
        response = requests.post(f"{BASE_URL}/grades", json=grade_data)
        data = response.json()
        passed = response.status_code == 201 and data.get("success") == True
        global test_grade_id
        test_grade_id = data.get("data", {}).get("id")
        log_result("添加成绩", passed, f"成绩ID: {test_grade_id}")
        return passed
    except Exception as e:
        log_result("添加成绩", False, str(e))
        return False


def test_add_invalid_grade():
    """测试添加无效成绩（分数超出范围）"""
    try:
        grade_data = {
            "student_id": "TEST001",
            "subject": "语文",
            "score": 150  # 超出 0-100 范围
        }
        response = requests.post(f"{BASE_URL}/grades", json=grade_data)
        data = response.json()
        passed = response.status_code == 400 and data.get("success") == False
        log_result("添加无效成绩（应失败）", passed, data.get("message", ""))
        return passed
    except Exception as e:
        log_result("添加无效成绩（应失败）", False, str(e))
        return False


def test_add_grade_nonexistent_student():
    """测试为不存在的学生添加成绩"""
    try:
        grade_data = {
            "student_id": "NOTEXIST",
            "subject": "英语",
            "score": 80
        }
        response = requests.post(f"{BASE_URL}/grades", json=grade_data)
        data = response.json()
        passed = response.status_code == 400 and data.get("success") == False
        log_result("为不存在学生添加成绩（应失败）", passed, data.get("message", ""))
        return passed
    except Exception as e:
        log_result("为不存在学生添加成绩（应失败）", False, str(e))
        return False


def test_get_all_grades():
    """测试获取所有成绩"""
    try:
        response = requests.get(f"{BASE_URL}/grades")
        data = response.json()
        passed = response.status_code == 200 and data.get("success") == True
        grade_count = len(data.get("data", []))
        log_result("获取所有成绩", passed, f"共 {grade_count} 条成绩")
        return passed
    except Exception as e:
        log_result("获取所有成绩", False, str(e))
        return False


def test_get_grades_by_student():
    """测试获取学生成绩"""
    try:
        response = requests.get(f"{BASE_URL}/grades?student_id=TEST001")
        data = response.json()
        passed = response.status_code == 200 and data.get("success") == True
        grade_count = len(data.get("data", []))
        log_result("获取学生成绩", passed, f"TEST001 共 {grade_count} 条成绩")
        return passed
    except Exception as e:
        log_result("获取学生成绩", False, str(e))
        return False


def test_update_grade():
    """测试更新成绩"""
    try:
        if not test_grade_id:
            log_result("更新成绩", False, "没有可更新的成绩ID")
            return False
        update_data = {"score": 98}
        response = requests.put(f"{BASE_URL}/grades/{test_grade_id}", json=update_data)
        data = response.json()
        passed = response.status_code == 200 and data.get("success") == True
        log_result("更新成绩", passed, data.get("message", ""))
        return passed
    except Exception as e:
        log_result("更新成绩", False, str(e))
        return False


# ==================== 统计测试 ====================

def test_get_statistics():
    """测试获取成绩统计"""
    try:
        response = requests.get(f"{BASE_URL}/statistics")
        data = response.json()
        passed = response.status_code == 200 and data.get("success") == True
        stats = data.get("data", {})
        log_result("获取成绩统计", passed, 
                   f"数量:{stats.get('count')} 平均:{stats.get('average')} 最高:{stats.get('max')} 最低:{stats.get('min')}")
        return passed
    except Exception as e:
        log_result("获取成绩统计", False, str(e))
        return False


def test_get_student_statistics():
    """测试获取学生成绩统计"""
    try:
        response = requests.get(f"{BASE_URL}/statistics?student_id=TEST001")
        data = response.json()
        passed = response.status_code == 200 and data.get("success") == True
        stats = data.get("data", {})
        log_result("获取学生成绩统计", passed, f"平均分: {stats.get('average')}")
        return passed
    except Exception as e:
        log_result("获取学生成绩统计", False, str(e))
        return False


# ==================== 清理测试数据 ====================

def test_delete_grade():
    """测试删除成绩"""
    try:
        if not test_grade_id:
            log_result("删除成绩", False, "没有可删除的成绩ID")
            return False
        response = requests.delete(f"{BASE_URL}/grades/{test_grade_id}")
        data = response.json()
        passed = response.status_code == 200 and data.get("success") == True
        log_result("删除成绩", passed, data.get("message", ""))
        return passed
    except Exception as e:
        log_result("删除成绩", False, str(e))
        return False


def test_delete_student():
    """测试删除学生"""
    try:
        response = requests.delete(f"{BASE_URL}/students/TEST001")
        data = response.json()
        passed = response.status_code == 200 and data.get("success") == True
        log_result("删除学生", passed, data.get("message", ""))
        return passed
    except Exception as e:
        log_result("删除学生", False, str(e))
        return False


# ==================== 主测试函数 ====================

test_grade_id = None

def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("学生成绩管理系统 - API 测试")
    print("=" * 60)
    print(f"后端地址: {BASE_URL}")
    print("=" * 60)
    
    # 健康检查
    print("\n【健康检查】")
    if not test_health_check():
        print("\n❌ 后端服务未启动，请先启动后端服务！")
        print("   运行命令: cd backend && python3 app.py")
        sys.exit(1)
    
    # 学生管理测试
    print("\n【学生管理测试】")
    test_add_student()
    test_add_duplicate_student()
    test_get_all_students()
    test_get_student_by_id()
    test_get_nonexistent_student()
    test_update_student()
    
    # 成绩管理测试
    print("\n【成绩管理测试】")
    test_add_grade()
    test_add_invalid_grade()
    test_add_grade_nonexistent_student()
    test_get_all_grades()
    test_get_grades_by_student()
    test_update_grade()
    
    # 统计测试
    print("\n【统计功能测试】")
    test_get_statistics()
    test_get_student_statistics()
    
    # 清理测试数据
    print("\n【清理测试数据】")
    test_delete_grade()
    test_delete_student()
    
    # 输出测试报告
    print("\n" + "=" * 60)
    print("测试报告")
    print("=" * 60)
    total = results["passed"] + results["failed"]
    print(f"总计: {total} 项测试")
    print(f"通过: {results['passed']} ✅")
    print(f"失败: {results['failed']} ❌")
    print(f"通过率: {results['passed']/total*100:.1f}%")
    print("=" * 60)
    
    if results["failed"] > 0:
        print("\n失败的测试:")
        for test in results["tests"]:
            if not test["passed"]:
                print(f"  - {test['name']}: {test['message']}")
    
    return results["failed"] == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
