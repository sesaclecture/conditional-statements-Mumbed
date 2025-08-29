users = {
    "Ali123": {"name": "Alice", "birth": "19990102", "id": "Ali123", "pw": "apass!!xx", "role": "admin"},
    "Bob123": {"name": "Bob", "birth": "19980203", "id": "Bob123", "pw": "bpass!!xx", "role": "viewer"},
    "Cha123": {"name": "Charlie", "birth": "19970304", "id": "Cha123", "pw": "cpass!!xx", "role": "editor"}
}

def print_users():
    print("-" * 20 + "사용자 목록" + "-" * 20)
    for user_id, info in users.items():
        print(f"ID: {user_id}, Name: {info['name']}, Birth: {info['birth']}, Role: {info['role']}")

def check_birth(birth):
    if len(birth) != 8 or not birth.isdigit():
        return False
    year = int(birth[:4])
    month = int(birth[4:6])
    day = int(birth[6:])
    if not (1900 <= year <= 2100): return False
    if not (1 <= month <= 12): return False
    month_days = [31,29 if year%4==0 and (year%100!=0 or year%400==0) else 28,31,30,31,30,31,31,30,31,30,31]
    if not (1 <= day <= month_days[month-1]): return False
    return True

def check_pw(pw):
    specials = "!@#$%^&*()-_=+[]{};:'\",.<>/?\\|"
    if len(pw) < 8:
        return False
    for c in pw:
        if c in specials:
            return True
    return False

def signup():
    print("=" * 20 + " 회원가입 " + "=" * 20)
    while True:
        new_id = input("아이디 입력: ")
        if new_id in users:
            print("이미 존재하는 아이디입니다.")
        elif not new_id:
            print("아이디를 입력하세요.")
        else:
            break
    name = input("이름 입력: ")
    while True:
        birth = input("생년월일 입력(YYYYMMDD): ")
        if check_birth(birth):
            break
        else:
            print("생년월일 형식이 올바르지 않습니다.")
    while True:
        pw = input("비밀번호 입력(8자리 이상, 특수문자 포함): ")
        if check_pw(pw):
            break
        else:
            print("비밀번호 규칙에 맞게 다시 입력하세요.")
    role = input("역할 입력(admin/editor/viewer): ")
    users[new_id] = {"name": name, "birth": birth, "id": new_id, "pw": pw, "role": role}
    print("회원가입이 완료되었습니다.")
    print_users()

def login():
    print("=" * 20 + " 로그인 " + "=" * 20)
    user_id = input("아이디: ")
    pw = input("비밀번호: ")
    if user_id in users and users[user_id]["pw"] == pw:
        print(f"{users[user_id]['name']}님 로그인 성공!")
        return user_id
    else:
        print("로그인 실패!")
        return None

def update_user(current_id, current_role):
    print("=" * 20 + " 회원정보 수정 " + "=" * 20)
    if current_role == "viewer":
        target = current_id
    else:
        target = input("수정할 사용자ID 입력: ")
        if target not in users:
            print("해당 ID는 없습니다.")
            return
    # editor, admin은 타인 정보도 수정 가능
    if current_role == "admin" or current_role == "editor" or current_id == target:
        name = input("새 이름: ")
        while True:
            birth = input("새 생년월일 (YYYYMMDD): ")
            if check_birth(birth): break
            else: print("생년월일 형식 오류")
        while True:
            pw = input("새 비밀번호(8자리, 특수문자): ")
            if check_pw(pw): break
            else: print("비밀번호 규칙 오류")
        users[target]["name"] = name
        users[target]["birth"] = birth
        users[target]["pw"] = pw
        print("수정완료.")
        print_users()
    else:
        print("수정 권한이 없습니다.")

def delete_user(current_id, current_role):
    print("=" * 20 + " 회원 탈퇴 " + "=" * 20)
    if current_role == "admin":
        target = input("삭제할 사용자ID 입력: ")
    else:
        target = current_id
    if target not in users:
        print("해당 ID는 없습니다.")
        return
    # admin은 모두, 그 외는 본인만
    if current_role == "admin" or current_id == target:
        del users[target]
        print("회원탈퇴(삭제) 완료.")
        print_users()
    else:
        print("탈퇴 권한이 없습니다.")

def check_info(current_id):
    print("=" * 20 + " 회원 확인 " + "=" * 20)
    uid = input("확인할 ID입력: ")
    if uid in users:
        print(users[uid])
    else:
        print("존재하지 않는 ID.")

while True:
    print_users()
    cmd = input("회원가입:1, 회원조회:2, 종료:3: ")
    if cmd == "1":
        signup()
    elif cmd == "2":
        user_id = login()
        if user_id:
            role = users[user_id]["role"]
            while True:
                act = input("회원수정:1, 회원삭제:2, 회원조회:3, 로그아웃:4: ")
                if act == "1":
                    update_user(user_id, role)
                elif act == "2":
                    delete_user(user_id, role)
                    if role != "admin":
                        break
                elif act == "3":
                    check_info(user_id)
                elif act == "4":
                    print("로그아웃")
                    break
    elif cmd == "3":
        print("종료!")
        break

