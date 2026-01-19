# -*- coding: utf-8 -*-
"""
================================================================================
개발자 프롬프트 테스트 케이스 (Development Prompt Test Cases)
================================================================================

## 이 모듈의 목적
코드 리뷰, 문서화 프롬프트의 성능을 검증하기 위한 테스트 케이스

## 테스트 케이스 구성 (총 108개)
| 카테고리 | 개수 | 설명 |
|----------|------|------|
| 코드 리뷰 | 54개 | 일반, 보안, 성능, 리팩토링 |
| 문서화 | 54개 | API문서, README, 주석, 아키텍처 |

## 프로그래밍 언어
- Python, JavaScript/TypeScript, Java, Go, Rust

## 테스트 케이스 설계 원칙
1. 실제 프로덕션 코드와 유사한 복잡도
2. 다양한 문제점/개선점 포함
3. 언어별 관용구와 패턴 반영
4. 평가 가능한 명확한 기준
================================================================================
"""

from typing import Dict, List
from dataclasses import dataclass, field


@dataclass
class DevelopmentTestCase:
    """개발 프롬프트 테스트 케이스"""
    id: str
    category: str  # code_review, documentation
    subcategory: str  # general, security, performance, refactoring / api, readme, comments, architecture
    language: str  # python, javascript, java, go, rust
    code_snippet: str  # 테스트 코드
    expected_issues: List[str]  # 발견해야 할 이슈
    difficulty: str  # easy, medium, hard


# ============================================================================
# 코드 리뷰 테스트 케이스 (54개)
# ============================================================================

CODE_REVIEW_TEST_CASES = [
    # === 일반 코드 리뷰 - Python (7개) ===
    DevelopmentTestCase(
        id="CODE-001",
        category="code_review",
        subcategory="general",
        language="python",
        code_snippet='''
def processData(data):
    result = []
    for i in range(len(data)):
        if data[i] != None:
            x = data[i] * 2
            result.append(x)
    return result
''',
        expected_issues=["PEP8 네이밍 위반", "None 비교는 is 사용", "enumerate 미사용", "리스트 컴프리헨션 가능"],
        difficulty="easy"
    ),
    DevelopmentTestCase(
        id="CODE-002",
        category="code_review",
        subcategory="general",
        language="python",
        code_snippet='''
class userManager:
    def __init__(self):
        self.users = {}

    def addUser(self, id, name, email):
        self.users[id] = {"name": name, "email": email}

    def getUser(self, id):
        if id in self.users:
            return self.users[id]
        else:
            return None

    def deleteUser(self, id):
        if id in self.users:
            del self.users[id]
            return True
        return False
''',
        expected_issues=["클래스명 PascalCase 아님", "메서드명 snake_case 아님", "타입 힌트 없음", "docstring 없음"],
        difficulty="easy"
    ),
    DevelopmentTestCase(
        id="CODE-003",
        category="code_review",
        subcategory="general",
        language="python",
        code_snippet='''
import json
import os
import sys
import re

def load_config():
    f = open("config.json", "r")
    config = json.load(f)
    f.close()
    return config

def save_data(data, filename):
    f = open(filename, "w")
    f.write(str(data))
    f.close()

def process_files(directory):
    files = os.listdir(directory)
    results = []
    for file in files:
        if file.endswith(".txt"):
            f = open(os.path.join(directory, file))
            content = f.read()
            results.append(content)
            f.close()
    return results
''',
        expected_issues=["context manager 미사용", "리소스 누수 위험", "예외 처리 없음", "pathlib 미사용"],
        difficulty="medium"
    ),
    DevelopmentTestCase(
        id="CODE-004",
        category="code_review",
        subcategory="general",
        language="python",
        code_snippet='''
def calculate_statistics(numbers):
    if len(numbers) == 0:
        return {}

    total = 0
    for n in numbers:
        total = total + n
    average = total / len(numbers)

    sorted_nums = sorted(numbers)
    if len(sorted_nums) % 2 == 0:
        median = (sorted_nums[len(sorted_nums)//2-1] + sorted_nums[len(sorted_nums)//2]) / 2
    else:
        median = sorted_nums[len(sorted_nums)//2]

    variance = 0
    for n in numbers:
        variance = variance + (n - average) ** 2
    variance = variance / len(numbers)

    return {"average": average, "median": median, "variance": variance}
''',
        expected_issues=["내장 함수 활용 부족", "중복 계산", "타입 힌트 없음", "statistics 모듈 미사용"],
        difficulty="medium"
    ),
    DevelopmentTestCase(
        id="CODE-005",
        category="code_review",
        subcategory="general",
        language="python",
        code_snippet='''
class Database:
    connection = None

    def connect(self):
        import sqlite3
        self.connection = sqlite3.connect("app.db")

    def query(self, sql):
        cursor = self.connection.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    def insert(self, table, data):
        columns = ", ".join(data.keys())
        values = ", ".join([f"'{v}'" for v in data.values()])
        sql = f"INSERT INTO {table} ({columns}) VALUES ({values})"
        self.connection.cursor().execute(sql)
        self.connection.commit()
''',
        expected_issues=["SQL 인젝션 취약점", "전역 connection", "예외 처리 없음", "파라미터화된 쿼리 미사용"],
        difficulty="hard"
    ),
    DevelopmentTestCase(
        id="CODE-006",
        category="code_review",
        subcategory="general",
        language="python",
        code_snippet='''
def fetch_user_data(user_id):
    import requests
    response = requests.get(f"https://api.example.com/users/{user_id}")
    data = response.json()
    return data

def process_all_users():
    users = []
    for i in range(1, 101):
        user = fetch_user_data(i)
        users.append(user)
    return users
''',
        expected_issues=["HTTP 에러 처리 없음", "N+1 문제", "동시성 미활용", "타임아웃 미설정"],
        difficulty="medium"
    ),
    DevelopmentTestCase(
        id="CODE-007",
        category="code_review",
        subcategory="general",
        language="python",
        code_snippet='''
def parse_log_file(filepath):
    logs = []
    with open(filepath) as f:
        for line in f:
            parts = line.split(" ")
            log = {
                "timestamp": parts[0] + " " + parts[1],
                "level": parts[2],
                "message": " ".join(parts[3:])
            }
            logs.append(log)
    return logs

def filter_errors(logs):
    errors = []
    for log in logs:
        if log["level"] == "ERROR":
            errors.append(log)
    return errors
''',
        expected_issues=["인덱스 에러 가능", "정규식 사용 권장", "리스트 컴프리헨션 가능", "타입 안정성 부족"],
        difficulty="medium"
    ),

    # === 일반 코드 리뷰 - JavaScript (7개) ===
    DevelopmentTestCase(
        id="CODE-008",
        category="code_review",
        subcategory="general",
        language="javascript",
        code_snippet='''
function getUserData(userId) {
    var user = null;
    fetch("/api/users/" + userId)
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            user = data;
        });
    return user;
}
''',
        expected_issues=["var 사용", "async/await 미사용", "비동기 반환 문제", "에러 처리 없음"],
        difficulty="easy"
    ),
    DevelopmentTestCase(
        id="CODE-009",
        category="code_review",
        subcategory="general",
        language="javascript",
        code_snippet='''
function processItems(items) {
    var results = [];
    for (var i = 0; i < items.length; i++) {
        if (items[i].active == true) {
            results.push({
                id: items[i].id,
                name: items[i].name.toUpperCase()
            });
        }
    }
    return results;
}
''',
        expected_issues=["var 사용", "== 대신 === 사용", "filter/map 활용 가능", "구조분해 미사용"],
        difficulty="easy"
    ),
    DevelopmentTestCase(
        id="CODE-010",
        category="code_review",
        subcategory="general",
        language="javascript",
        code_snippet='''
class UserService {
    constructor() {
        this.users = [];
    }

    addUser(user) {
        this.users.push(user);
    }

    findUser(id) {
        for (let i = 0; i < this.users.length; i++) {
            if (this.users[i].id == id) {
                return this.users[i];
            }
        }
        return null;
    }

    updateUser(id, data) {
        let user = this.findUser(id);
        if (user) {
            user.name = data.name;
            user.email = data.email;
        }
    }
}
''',
        expected_issues=["== 대신 === 사용", "find 메서드 활용", "불변성 미고려", "타입 체크 없음"],
        difficulty="medium"
    ),
    DevelopmentTestCase(
        id="CODE-011",
        category="code_review",
        subcategory="general",
        language="javascript",
        code_snippet='''
async function loadData() {
    try {
        const response1 = await fetch("/api/users");
        const users = await response1.json();

        const response2 = await fetch("/api/products");
        const products = await response2.json();

        const response3 = await fetch("/api/orders");
        const orders = await response3.json();

        return { users, products, orders };
    } catch (error) {
        console.log(error);
    }
}
''',
        expected_issues=["Promise.all 미사용", "에러 처리 불충분", "응답 상태 미확인", "undefined 반환 가능"],
        difficulty="medium"
    ),
    DevelopmentTestCase(
        id="CODE-012",
        category="code_review",
        subcategory="general",
        language="javascript",
        code_snippet='''
function debounce(func, wait) {
    let timeout;
    return function() {
        const context = this;
        const args = arguments;
        clearTimeout(timeout);
        timeout = setTimeout(function() {
            func.apply(context, args);
        }, wait);
    };
}

const searchInput = document.getElementById("search");
searchInput.addEventListener("input", debounce(function(e) {
    fetch("/api/search?q=" + e.target.value)
        .then(res => res.json())
        .then(data => {
            document.getElementById("results").innerHTML = data.map(item =>
                "<div>" + item.name + "</div>"
            ).join("");
        });
}, 300));
''',
        expected_issues=["XSS 취약점", "에러 처리 없음", "null 체크 없음", "화살표 함수 권장"],
        difficulty="hard"
    ),
    DevelopmentTestCase(
        id="CODE-013",
        category="code_review",
        subcategory="general",
        language="javascript",
        code_snippet='''
class EventEmitter {
    constructor() {
        this.events = {};
    }

    on(event, listener) {
        if (!this.events[event]) {
            this.events[event] = [];
        }
        this.events[event].push(listener);
    }

    emit(event, data) {
        if (this.events[event]) {
            this.events[event].forEach(listener => listener(data));
        }
    }

    off(event, listener) {
        if (this.events[event]) {
            this.events[event] = this.events[event].filter(l => l != listener);
        }
    }
}
''',
        expected_issues=["== 대신 === 사용", "once 메서드 없음", "에러 처리 없음", "메모리 누수 가능성"],
        difficulty="medium"
    ),
    DevelopmentTestCase(
        id="CODE-014",
        category="code_review",
        subcategory="general",
        language="javascript",
        code_snippet='''
const config = {
    apiUrl: "https://api.example.com",
    apiKey: "sk-1234567890abcdef",
    debug: true
};

async function callApi(endpoint, data) {
    const response = await fetch(config.apiUrl + endpoint, {
        method: "POST",
        headers: {
            "Authorization": "Bearer " + config.apiKey,
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });
    return response.json();
}
''',
        expected_issues=["API 키 하드코딩", "에러 처리 없음", "응답 상태 미확인", "환경변수 미사용"],
        difficulty="medium"
    ),

    # === 보안 코드 리뷰 (14개) ===
    DevelopmentTestCase(
        id="CODE-015",
        category="code_review",
        subcategory="security",
        language="python",
        code_snippet='''
from flask import Flask, request
import sqlite3

app = Flask(__name__)

@app.route("/user")
def get_user():
    user_id = request.args.get("id")
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
    user = cursor.fetchone()
    return {"user": user}
''',
        expected_issues=["SQL 인젝션", "입력값 검증 없음", "연결 닫기 누락", "에러 처리 없음"],
        difficulty="easy"
    ),
    DevelopmentTestCase(
        id="CODE-016",
        category="code_review",
        subcategory="security",
        language="python",
        code_snippet='''
import os
from flask import Flask, request

app = Flask(__name__)

@app.route("/run")
def run_command():
    cmd = request.args.get("cmd")
    result = os.system(cmd)
    return {"result": result}
''',
        expected_issues=["명령어 인젝션", "입력값 검증 없음", "권한 체크 없음", "위험한 API 노출"],
        difficulty="easy"
    ),
    DevelopmentTestCase(
        id="CODE-017",
        category="code_review",
        subcategory="security",
        language="python",
        code_snippet='''
from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route("/greet")
def greet():
    name = request.args.get("name", "Guest")
    template = f"<h1>Hello, {name}!</h1>"
    return render_template_string(template)
''',
        expected_issues=["XSS 취약점", "SSTI 취약점", "입력값 이스케이프 없음"],
        difficulty="medium"
    ),
    DevelopmentTestCase(
        id="CODE-018",
        category="code_review",
        subcategory="security",
        language="python",
        code_snippet='''
import hashlib

def register_user(username, password):
    password_hash = hashlib.md5(password.encode()).hexdigest()
    save_to_db(username, password_hash)

def verify_password(password, stored_hash):
    return hashlib.md5(password.encode()).hexdigest() == stored_hash
''',
        expected_issues=["MD5 취약한 해시", "솔트 미사용", "bcrypt/argon2 권장", "타이밍 공격 취약"],
        difficulty="medium"
    ),
    DevelopmentTestCase(
        id="CODE-019",
        category="code_review",
        subcategory="security",
        language="python",
        code_snippet='''
import jwt
from flask import Flask, request

app = Flask(__name__)
SECRET_KEY = "secret123"

@app.route("/login", methods=["POST"])
def login():
    user = authenticate(request.json)
    if user:
        token = jwt.encode({"user_id": user.id}, SECRET_KEY, algorithm="HS256")
        return {"token": token}

@app.route("/protected")
def protected():
    token = request.headers.get("Authorization")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return {"user_id": payload["user_id"]}
    except:
        return {"error": "Invalid token"}, 401
''',
        expected_issues=["약한 시크릿 키", "토큰 만료 없음", "Bearer 접두사 미처리", "넓은 예외 처리"],
        difficulty="hard"
    ),
    DevelopmentTestCase(
        id="CODE-020",
        category="code_review",
        subcategory="security",
        language="javascript",
        code_snippet='''
app.get("/file", (req, res) => {
    const filename = req.query.name;
    const filepath = "./uploads/" + filename;
    res.sendFile(filepath);
});
''',
        expected_issues=["경로 순회 취약점", "입력값 검증 없음", "절대경로 권장", "파일 존재 확인 없음"],
        difficulty="medium"
    ),
    DevelopmentTestCase(
        id="CODE-021",
        category="code_review",
        subcategory="security",
        language="javascript",
        code_snippet='''
app.post("/login", (req, res) => {
    const { username, password } = req.body;
    const user = db.query(`SELECT * FROM users WHERE username = '${username}' AND password = '${password}'`);
    if (user) {
        req.session.user = user;
        res.json({ success: true });
    } else {
        res.json({ success: false, error: "Invalid credentials" });
    }
});
''',
        expected_issues=["SQL 인젝션", "평문 비밀번호", "세션 관리 불안전", "rate limiting 없음"],
        difficulty="medium"
    ),
    DevelopmentTestCase(
        id="CODE-022",
        category="code_review",
        subcategory="security",
        language="javascript",
        code_snippet='''
app.get("/redirect", (req, res) => {
    const url = req.query.url;
    res.redirect(url);
});
''',
        expected_issues=["오픈 리다이렉트", "URL 검증 없음", "허용 목록 필요", "피싱 공격 가능"],
        difficulty="easy"
    ),
    DevelopmentTestCase(
        id="CODE-023",
        category="code_review",
        subcategory="security",
        language="python",
        code_snippet='''
import pickle
from flask import Flask, request

app = Flask(__name__)

@app.route("/load", methods=["POST"])
def load_data():
    data = request.get_data()
    obj = pickle.loads(data)
    return {"result": str(obj)}
''',
        expected_issues=["Pickle 역직렬화 취약점", "신뢰하지 않는 데이터", "RCE 가능", "안전한 대안 사용"],
        difficulty="hard"
    ),
    DevelopmentTestCase(
        id="CODE-024",
        category="code_review",
        subcategory="security",
        language="python",
        code_snippet='''
import logging

logging.basicConfig(level=logging.DEBUG)

def process_payment(card_number, cvv, amount):
    logging.debug(f"Processing payment: card={card_number}, cvv={cvv}, amount={amount}")
    # payment processing logic
    return True
''',
        expected_issues=["민감정보 로깅", "카드정보 노출", "마스킹 필요", "로그 레벨 부적절"],
        difficulty="easy"
    ),
    DevelopmentTestCase(
        id="CODE-025",
        category="code_review",
        subcategory="security",
        language="java",
        code_snippet='''
public class FileUpload {
    public void upload(MultipartFile file) {
        String filename = file.getOriginalFilename();
        File dest = new File("/uploads/" + filename);
        file.transferTo(dest);
    }
}
''',
        expected_issues=["파일명 검증 없음", "경로 순회 가능", "파일 타입 미확인", "크기 제한 없음"],
        difficulty="medium"
    ),
    DevelopmentTestCase(
        id="CODE-026",
        category="code_review",
        subcategory="security",
        language="java",
        code_snippet='''
public String processXml(String xmlData) {
    DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
    DocumentBuilder builder = factory.newDocumentBuilder();
    Document doc = builder.parse(new InputSource(new StringReader(xmlData)));
    return doc.getDocumentElement().getTextContent();
}
''',
        expected_issues=["XXE 취약점", "외부 엔티티 비활성화 필요", "DTD 비활성화 필요"],
        difficulty="hard"
    ),
    DevelopmentTestCase(
        id="CODE-027",
        category="code_review",
        subcategory="security",
        language="go",
        code_snippet='''
func handler(w http.ResponseWriter, r *http.Request) {
    template := r.URL.Query().Get("template")
    tmpl, _ := template.New("page").Parse(template)
    tmpl.Execute(w, nil)
}
''',
        expected_issues=["SSTI 취약점", "사용자 입력 템플릿", "에러 처리 없음"],
        difficulty="hard"
    ),
    DevelopmentTestCase(
        id="CODE-028",
        category="code_review",
        subcategory="security",
        language="python",
        code_snippet='''
import yaml

def load_config(config_file):
    with open(config_file) as f:
        config = yaml.load(f)
    return config
''',
        expected_issues=["unsafe YAML load", "yaml.safe_load 사용", "RCE 가능", "입력 검증 없음"],
        difficulty="medium"
    ),

    # === 성능 코드 리뷰 (14개) ===
    DevelopmentTestCase(
        id="CODE-029",
        category="code_review",
        subcategory="performance",
        language="python",
        code_snippet='''
def find_duplicates(items):
    duplicates = []
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if items[i] == items[j] and items[i] not in duplicates:
                duplicates.append(items[i])
    return duplicates
''',
        expected_issues=["O(n^2) 복잡도", "set 활용 가능", "중복 리스트 검사 비효율"],
        difficulty="easy"
    ),
    DevelopmentTestCase(
        id="CODE-030",
        category="code_review",
        subcategory="performance",
        language="python",
        code_snippet='''
def process_large_file(filepath):
    with open(filepath) as f:
        content = f.read()
    lines = content.split("\\n")
    results = []
    for line in lines:
        if "ERROR" in line:
            results.append(line)
    return results
''',
        expected_issues=["전체 파일 메모리 로드", "라인 단위 읽기 권장", "제너레이터 활용 가능"],
        difficulty="medium"
    ),
    DevelopmentTestCase(
        id="CODE-031",
        category="code_review",
        subcategory="performance",
        language="python",
        code_snippet='''
def get_user_orders(user_ids):
    orders = []
    for user_id in user_ids:
        user_orders = db.query(f"SELECT * FROM orders WHERE user_id = {user_id}")
        orders.extend(user_orders)
    return orders
''',
        expected_issues=["N+1 쿼리 문제", "벌크 쿼리 사용", "IN 절 활용", "SQL 인젝션도 있음"],
        difficulty="medium"
    ),
    DevelopmentTestCase(
        id="CODE-032",
        category="code_review",
        subcategory="performance",
        language="python",
        code_snippet='''
import re

def validate_emails(emails):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'
    valid = []
    for email in emails:
        if re.match(pattern, email):
            valid.append(email)
    return valid
''',
        expected_issues=["매번 패턴 컴파일", "re.compile 사용", "리스트 컴프리헨션 가능"],
        difficulty="easy"
    ),
    DevelopmentTestCase(
        id="CODE-033",
        category="code_review",
        subcategory="performance",
        language="python",
        code_snippet='''
def merge_data(list1, list2):
    result = list1.copy()
    for item in list2:
        if item not in result:
            result.append(item)
    return result
''',
        expected_issues=["O(n*m) 복잡도", "set 연산 활용", "리스트 in 연산 비효율"],
        difficulty="easy"
    ),
    DevelopmentTestCase(
        id="CODE-034",
        category="code_review",
        subcategory="performance",
        language="javascript",
        code_snippet='''
function renderList(items) {
    const container = document.getElementById("list");
    container.innerHTML = "";
    items.forEach(item => {
        const div = document.createElement("div");
        div.textContent = item.name;
        container.appendChild(div);
    });
}
''',
        expected_issues=["반복적 DOM 조작", "DocumentFragment 사용", "리플로우 다수 발생"],
        difficulty="medium"
    ),
    DevelopmentTestCase(
        id="CODE-035",
        category="code_review",
        subcategory="performance",
        language="javascript",
        code_snippet='''
function processData(data) {
    let result = [];
    for (let i = 0; i < data.length; i++) {
        result = result.concat(data[i].items);
    }
    return result.filter(item => item.active).map(item => item.id);
}
''',
        expected_issues=["concat 반복 비효율", "flat/flatMap 사용", "체인 최적화 가능"],
        difficulty="medium"
    ),
    DevelopmentTestCase(
        id="CODE-036",
        category="code_review",
        subcategory="performance",
        language="javascript",
        code_snippet='''
async function loadAllUsers() {
    const users = await fetch("/api/users").then(r => r.json());
    const enrichedUsers = [];

    for (const user of users) {
        const profile = await fetch(`/api/profiles/${user.id}`).then(r => r.json());
        const orders = await fetch(`/api/orders/${user.id}`).then(r => r.json());
        enrichedUsers.push({ ...user, profile, orders });
    }

    return enrichedUsers;
}
''',
        expected_issues=["순차 API 호출", "Promise.all 활용", "병렬 처리 가능", "배치 API 고려"],
        difficulty="hard"
    ),
    DevelopmentTestCase(
        id="CODE-037",
        category="code_review",
        subcategory="performance",
        language="java",
        code_snippet='''
public String buildReport(List<Item> items) {
    String result = "";
    for (Item item : items) {
        result += item.getName() + ": " + item.getValue() + "\\n";
    }
    return result;
}
''',
        expected_issues=["String 연결 비효율", "StringBuilder 사용", "O(n^2) 문자열 생성"],
        difficulty="easy"
    ),
    DevelopmentTestCase(
        id="CODE-038",
        category="code_review",
        subcategory="performance",
        language="java",
        code_snippet='''
public List<User> findActiveUsers(List<User> users) {
    List<User> active = new ArrayList<>();
    for (User user : users) {
        if (user.isActive()) {
            active.add(user);
        }
    }
    Collections.sort(active, (a, b) -> a.getName().compareTo(b.getName()));
    return active;
}
''',
        expected_issues=["Stream API 활용 가능", "정렬 후 필터 가능", "메서드 참조 사용 가능"],
        difficulty="medium"
    ),
    DevelopmentTestCase(
        id="CODE-039",
        category="code_review",
        subcategory="performance",
        language="go",
        code_snippet='''
func processItems(items []Item) []Result {
    var results []Result
    for _, item := range items {
        result := heavyComputation(item)
        results = append(results, result)
    }
    return results
}
''',
        expected_issues=["슬라이스 용량 미지정", "make로 용량 할당", "goroutine 활용 가능"],
        difficulty="medium"
    ),
    DevelopmentTestCase(
        id="CODE-040",
        category="code_review",
        subcategory="performance",
        language="python",
        code_snippet='''
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

def calculate_sum(n):
    total = 0
    for i in range(n):
        total += fibonacci(i)
    return total
''',
        expected_issues=["지수적 시간 복잡도", "메모이제이션 필요", "반복적 구현 권장"],
        difficulty="medium"
    ),
    DevelopmentTestCase(
        id="CODE-041",
        category="code_review",
        subcategory="performance",
        language="python",
        code_snippet='''
import pandas as pd

def process_dataframe(df):
    results = []
    for index, row in df.iterrows():
        if row["value"] > 100:
            results.append({
                "id": row["id"],
                "doubled": row["value"] * 2
            })
    return pd.DataFrame(results)
''',
        expected_issues=["iterrows 비효율", "벡터화 연산 사용", "apply 또는 마스킹 사용"],
        difficulty="hard"
    ),
    DevelopmentTestCase(
        id="CODE-042",
        category="code_review",
        subcategory="performance",
        language="python",
        code_snippet='''
def search_in_list(items, target):
    for i, item in enumerate(items):
        if item == target:
            return i
    return -1

def search_multiple(items, targets):
    results = {}
    for target in targets:
        results[target] = search_in_list(items, target)
    return results
''',
        expected_issues=["O(n*m) 복잡도", "dict/set으로 O(n+m)", "인덱스 맵 생성 권장"],
        difficulty="medium"
    ),

    # === 리팩토링 (12개) ===
    DevelopmentTestCase(
        id="CODE-043",
        category="code_review",
        subcategory="refactoring",
        language="python",
        code_snippet='''
def process_order(order):
    if order["type"] == "standard":
        if order["amount"] < 100:
            shipping = 10
        elif order["amount"] < 500:
            shipping = 5
        else:
            shipping = 0
        tax = order["amount"] * 0.1
    elif order["type"] == "express":
        if order["amount"] < 100:
            shipping = 20
        elif order["amount"] < 500:
            shipping = 15
        else:
            shipping = 10
        tax = order["amount"] * 0.1
    elif order["type"] == "premium":
        shipping = 0
        tax = order["amount"] * 0.05

    total = order["amount"] + shipping + tax
    return total
''',
        expected_issues=["중첩 조건문", "전략 패턴 적용", "매직 넘버", "중복 코드"],
        difficulty="hard"
    ),
    DevelopmentTestCase(
        id="CODE-044",
        category="code_review",
        subcategory="refactoring",
        language="python",
        code_snippet='''
class UserService:
    def create_user(self, name, email, password, age, address, phone):
        user = User()
        user.name = name
        user.email = email
        user.password = hash_password(password)
        user.age = age
        user.address = address
        user.phone = phone
        self.db.save(user)
        self.send_welcome_email(email)
        self.log_creation(name)
        return user
''',
        expected_issues=["긴 매개변수 목록", "단일 책임 위반", "DTO 패턴 사용", "의존성 주입"],
        difficulty="medium"
    ),
    DevelopmentTestCase(
        id="CODE-045",
        category="code_review",
        subcategory="refactoring",
        language="javascript",
        code_snippet='''
function calculatePrice(product, user, quantity) {
    let price = product.basePrice * quantity;

    // Apply user discount
    if (user.type === "premium") {
        price = price * 0.9;
    } else if (user.type === "vip") {
        price = price * 0.8;
    }

    // Apply quantity discount
    if (quantity > 100) {
        price = price * 0.85;
    } else if (quantity > 50) {
        price = price * 0.9;
    } else if (quantity > 10) {
        price = price * 0.95;
    }

    // Apply seasonal discount
    const month = new Date().getMonth();
    if (month === 11 || month === 0) {
        price = price * 0.9;
    }

    return Math.round(price * 100) / 100;
}
''',
        expected_issues=["함수 길이", "할인 로직 분리", "전략 패턴 적용", "매직 넘버"],
        difficulty="hard"
    ),
    DevelopmentTestCase(
        id="CODE-046",
        category="code_review",
        subcategory="refactoring",
        language="javascript",
        code_snippet='''
class OrderProcessor {
    process(order) {
        // Validate
        if (!order.items || order.items.length === 0) {
            throw new Error("No items");
        }
        if (!order.customer) {
            throw new Error("No customer");
        }

        // Calculate total
        let total = 0;
        for (let item of order.items) {
            total += item.price * item.quantity;
        }

        // Apply discount
        if (order.coupon) {
            total = total * (1 - order.coupon.discount);
        }

        // Save to database
        this.db.save(order);

        // Send email
        this.emailService.send(order.customer.email, "Order confirmed");

        // Update inventory
        for (let item of order.items) {
            this.inventory.decrease(item.id, item.quantity);
        }

        return { success: true, total };
    }
}
''',
        expected_issues=["God 클래스", "단일 책임 위반", "메서드 추출", "의존성 주입"],
        difficulty="hard"
    ),
    DevelopmentTestCase(
        id="CODE-047",
        category="code_review",
        subcategory="refactoring",
        language="python",
        code_snippet='''
def get_user_display_name(user):
    if user is None:
        return "Unknown"
    if user.nickname is not None and user.nickname != "":
        return user.nickname
    if user.first_name is not None and user.last_name is not None:
        return user.first_name + " " + user.last_name
    if user.first_name is not None:
        return user.first_name
    if user.email is not None:
        return user.email.split("@")[0]
    return "User " + str(user.id)
''',
        expected_issues=["Null 체크 반복", "Early return 패턴", "None 체크 간소화", "f-string 사용"],
        difficulty="medium"
    ),
    DevelopmentTestCase(
        id="CODE-048",
        category="code_review",
        subcategory="refactoring",
        language="java",
        code_snippet='''
public class ReportGenerator {
    public String generate(String type, Map<String, Object> data) {
        StringBuilder sb = new StringBuilder();

        if (type.equals("pdf")) {
            sb.append("<pdf>");
            sb.append("<header>").append(data.get("title")).append("</header>");
            sb.append("<body>").append(data.get("content")).append("</body>");
            sb.append("</pdf>");
        } else if (type.equals("html")) {
            sb.append("<html><head><title>");
            sb.append(data.get("title"));
            sb.append("</title></head><body>");
            sb.append(data.get("content"));
            sb.append("</body></html>");
        } else if (type.equals("csv")) {
            sb.append(data.get("title")).append("\\n");
            sb.append(data.get("content"));
        }

        return sb.toString();
    }
}
''',
        expected_issues=["팩토리 패턴 적용", "OCP 위반", "전략 패턴 적용", "다형성 활용"],
        difficulty="hard"
    ),
    DevelopmentTestCase(
        id="CODE-049",
        category="code_review",
        subcategory="refactoring",
        language="python",
        code_snippet='''
class DataProcessor:
    def __init__(self):
        self.db = Database()
        self.cache = Cache()
        self.logger = Logger()
        self.validator = Validator()
        self.notifier = Notifier()

    def process(self, data):
        self.logger.log("Starting process")
        if not self.validator.validate(data):
            self.logger.log("Validation failed")
            return None

        cached = self.cache.get(data.id)
        if cached:
            return cached

        result = self.db.query(data)
        self.cache.set(data.id, result)
        self.notifier.notify("Process complete")
        self.logger.log("Process finished")
        return result
''',
        expected_issues=["의존성 주입 필요", "하드코딩된 의존성", "테스트 어려움", "생성자 과다"],
        difficulty="medium"
    ),
    DevelopmentTestCase(
        id="CODE-050",
        category="code_review",
        subcategory="refactoring",
        language="javascript",
        code_snippet='''
function validateForm(form) {
    const errors = [];

    if (!form.name) {
        errors.push("Name is required");
    } else if (form.name.length < 2) {
        errors.push("Name must be at least 2 characters");
    } else if (form.name.length > 50) {
        errors.push("Name must be less than 50 characters");
    }

    if (!form.email) {
        errors.push("Email is required");
    } else if (!/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(form.email)) {
        errors.push("Email is invalid");
    }

    if (!form.password) {
        errors.push("Password is required");
    } else if (form.password.length < 8) {
        errors.push("Password must be at least 8 characters");
    }

    return errors;
}
''',
        expected_issues=["검증 로직 분리", "체인 패턴", "재사용 불가", "테스트 어려움"],
        difficulty="medium"
    ),
    DevelopmentTestCase(
        id="CODE-051",
        category="code_review",
        subcategory="refactoring",
        language="python",
        code_snippet='''
class ShoppingCart:
    def __init__(self):
        self.items = []
        self.discount = 0
        self.tax_rate = 0.1

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item_id):
        self.items = [i for i in self.items if i.id != item_id]

    def get_subtotal(self):
        return sum(i.price * i.quantity for i in self.items)

    def get_discount_amount(self):
        return self.get_subtotal() * self.discount

    def get_tax(self):
        return (self.get_subtotal() - self.get_discount_amount()) * self.tax_rate

    def get_total(self):
        return self.get_subtotal() - self.get_discount_amount() + self.get_tax()
''',
        expected_issues=["계산 중복 호출", "캐싱 필요", "불변 객체 고려", "상태 변경 추적"],
        difficulty="medium"
    ),
    DevelopmentTestCase(
        id="CODE-052",
        category="code_review",
        subcategory="refactoring",
        language="go",
        code_snippet='''
func ProcessRequest(r *Request) (*Response, error) {
    if r == nil {
        return nil, errors.New("request is nil")
    }
    if r.UserID == "" {
        return nil, errors.New("user id is required")
    }
    if r.Action == "" {
        return nil, errors.New("action is required")
    }

    user, err := getUser(r.UserID)
    if err != nil {
        return nil, err
    }

    if r.Action == "create" {
        // 50 lines of create logic
    } else if r.Action == "update" {
        // 50 lines of update logic
    } else if r.Action == "delete" {
        // 50 lines of delete logic
    }

    return &Response{Success: true}, nil
}
''',
        expected_issues=["함수 길이", "액션별 분리", "커맨드 패턴", "검증 로직 분리"],
        difficulty="hard"
    ),
    DevelopmentTestCase(
        id="CODE-053",
        category="code_review",
        subcategory="refactoring",
        language="python",
        code_snippet='''
def send_notification(user, notification_type, message):
    if notification_type == "email":
        import smtplib
        server = smtplib.SMTP("smtp.example.com")
        server.login("user", "pass")
        server.sendmail("noreply@example.com", user.email, message)
        server.quit()
    elif notification_type == "sms":
        import twilio
        client = twilio.Client("sid", "token")
        client.messages.create(to=user.phone, body=message)
    elif notification_type == "push":
        import firebase_admin
        firebase_admin.messaging.send(user.device_token, message)
''',
        expected_issues=["전략 패턴 적용", "의존성 하드코딩", "함수 내 import", "에러 처리 없음"],
        difficulty="hard"
    ),
    DevelopmentTestCase(
        id="CODE-054",
        category="code_review",
        subcategory="refactoring",
        language="javascript",
        code_snippet='''
class UserRepository {
    async findById(id) {
        const connection = await mysql.createConnection(config);
        const [rows] = await connection.query("SELECT * FROM users WHERE id = ?", [id]);
        await connection.end();
        return rows[0];
    }

    async findByEmail(email) {
        const connection = await mysql.createConnection(config);
        const [rows] = await connection.query("SELECT * FROM users WHERE email = ?", [email]);
        await connection.end();
        return rows[0];
    }

    async findAll() {
        const connection = await mysql.createConnection(config);
        const [rows] = await connection.query("SELECT * FROM users");
        await connection.end();
        return rows;
    }
}
''',
        expected_issues=["연결 관리 중복", "커넥션 풀 사용", "베이스 클래스 추출", "트랜잭션 미지원"],
        difficulty="medium"
    ),
]


# ============================================================================
# 문서화 테스트 케이스 (54개)
# ============================================================================

DOCUMENTATION_TEST_CASES = [
    # === API 문서화 (14개) ===
    DevelopmentTestCase(
        id="DOC-001",
        category="documentation",
        subcategory="api",
        language="python",
        code_snippet='''
@app.route("/api/users", methods=["POST"])
def create_user():
    data = request.json
    user = User(name=data["name"], email=data["email"])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201
''',
        expected_issues=["엔드포인트 설명", "요청 파라미터", "응답 형식", "에러 케이스"],
        difficulty="easy"
    ),
    DevelopmentTestCase(
        id="DOC-002",
        category="documentation",
        subcategory="api",
        language="python",
        code_snippet='''
@app.route("/api/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify(product.to_dict())
''',
        expected_issues=["경로 파라미터", "응답 예시", "404 케이스", "인증 요구사항"],
        difficulty="easy"
    ),
    DevelopmentTestCase(
        id="DOC-003",
        category="documentation",
        subcategory="api",
        language="javascript",
        code_snippet='''
router.get("/orders", authenticate, async (req, res) => {
    const { status, page = 1, limit = 10 } = req.query;
    const orders = await Order.find({ userId: req.user.id, status })
        .skip((page - 1) * limit)
        .limit(parseInt(limit));
    res.json({ orders, page, limit, total: orders.length });
});
''',
        expected_issues=["쿼리 파라미터", "페이지네이션", "인증 필요", "응답 구조"],
        difficulty="medium"
    ),
    DevelopmentTestCase(
        id="DOC-004",
        category="documentation",
        subcategory="api",
        language="javascript",
        code_snippet='''
router.post("/payments", async (req, res) => {
    const { amount, currency, source, description } = req.body;
    try {
        const charge = await stripe.charges.create({
            amount, currency, source, description
        });
        res.json({ success: true, chargeId: charge.id });
    } catch (error) {
        res.status(400).json({ success: false, error: error.message });
    }
});
''',
        expected_issues=["요청 본문", "성공/실패 응답", "에러 처리", "외부 서비스 연동"],
        difficulty="medium"
    ),
    DevelopmentTestCase(
        id="DOC-005",
        category="documentation",
        subcategory="api",
        language="go",
        code_snippet='''
func (h *Handler) CreateOrder(w http.ResponseWriter, r *http.Request) {
    var order Order
    if err := json.NewDecoder(r.Body).Decode(&order); err != nil {
        http.Error(w, err.Error(), http.StatusBadRequest)
        return
    }
    if err := h.service.Create(&order); err != nil {
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }
    w.WriteHeader(http.StatusCreated)
    json.NewEncoder(w).Encode(order)
}
''',
        expected_issues=["요청 형식", "응답 코드", "에러 응답", "예시"],
        difficulty="medium"
    ),
    DevelopmentTestCase(
        id="DOC-006",
        category="documentation",
        subcategory="api",
        language="java",
        code_snippet='''
@PostMapping("/api/v1/files/upload")
public ResponseEntity<FileResponse> uploadFile(
    @RequestParam("file") MultipartFile file,
    @RequestHeader("Authorization") String token
) {
    validateToken(token);
    String fileUrl = storageService.store(file);
    return ResponseEntity.ok(new FileResponse(fileUrl, file.getOriginalFilename()));
}
''',
        expected_issues=["파일 업로드", "헤더 파라미터", "응답 형식", "제한 사항"],
        difficulty="medium"
    ),
    DevelopmentTestCase(
        id="DOC-007",
        category="documentation",
        subcategory="api",
        language="python",
        code_snippet='''
@app.route("/api/search", methods=["GET"])
def search():
    q = request.args.get("q", "")
    category = request.args.get("category")
    min_price = request.args.get("min_price", type=float)
    max_price = request.args.get("max_price", type=float)
    sort = request.args.get("sort", "relevance")

    results = search_service.search(q, category, min_price, max_price, sort)
    return jsonify({"results": results, "count": len(results)})
''',
        expected_issues=["검색 파라미터", "필터 옵션", "정렬 옵션", "응답 구조"],
        difficulty="hard"
    ),
    DevelopmentTestCase(
        id="DOC-008",
        category="documentation",
        subcategory="api",
        language="javascript",
        code_snippet='''
router.patch("/users/:id", authenticate, authorize("admin"), async (req, res) => {
    const updates = Object.keys(req.body);
    const allowedUpdates = ["name", "email", "role"];
    const isValidOperation = updates.every(update => allowedUpdates.includes(update));

    if (!isValidOperation) {
        return res.status(400).json({ error: "Invalid updates" });
    }

    const user = await User.findByIdAndUpdate(req.params.id, req.body, { new: true });
    res.json(user);
});
''',
        expected_issues=["부분 업데이트", "허용 필드", "권한 요구", "에러 케이스"],
        difficulty="hard"
    ),
    DevelopmentTestCase(
        id="DOC-009",
        category="documentation",
        subcategory="api",
        language="python",
        code_snippet='''
class WebhookView(APIView):
    def post(self, request):
        signature = request.headers.get("X-Signature")
        if not verify_signature(request.data, signature):
            return Response({"error": "Invalid signature"}, status=401)

        event_type = request.data.get("type")
        if event_type == "payment.completed":
            handle_payment_completed(request.data)
        elif event_type == "subscription.cancelled":
            handle_subscription_cancelled(request.data)

        return Response({"received": True})
''',
        expected_issues=["웹훅 이벤트", "서명 검증", "이벤트 타입", "페이로드 구조"],
        difficulty="hard"
    ),
    DevelopmentTestCase(
        id="DOC-010",
        category="documentation",
        subcategory="api",
        language="go",
        code_snippet='''
func (h *Handler) BatchDelete(w http.ResponseWriter, r *http.Request) {
    var req struct {
        IDs []string `json:"ids"`
    }
    json.NewDecoder(r.Body).Decode(&req)

    results := make(map[string]string)
    for _, id := range req.IDs {
        if err := h.service.Delete(id); err != nil {
            results[id] = err.Error()
        } else {
            results[id] = "deleted"
        }
    }
    json.NewEncoder(w).Encode(results)
}
''',
        expected_issues=["배치 작업", "요청 형식", "부분 실패 처리", "응답 형식"],
        difficulty="medium"
    ),
    DevelopmentTestCase(
        id="DOC-011",
        category="documentation",
        subcategory="api",
        language="javascript",
        code_snippet='''
io.on("connection", (socket) => {
    socket.on("join-room", (roomId) => {
        socket.join(roomId);
        socket.to(roomId).emit("user-joined", socket.id);
    });

    socket.on("message", ({ roomId, message }) => {
        io.to(roomId).emit("new-message", { userId: socket.id, message });
    });

    socket.on("disconnect", () => {
        socket.rooms.forEach(room => {
            socket.to(room).emit("user-left", socket.id);
        });
    });
});
''',
        expected_issues=["WebSocket 이벤트", "이벤트 페이로드", "룸 관리", "연결 상태"],
        difficulty="hard"
    ),
    DevelopmentTestCase(
        id="DOC-012",
        category="documentation",
        subcategory="api",
        language="python",
        code_snippet='''
@app.route("/api/export", methods=["POST"])
def export_data():
    data = request.json
    format_type = data.get("format", "csv")
    filters = data.get("filters", {})

    task_id = celery.send_task("export_task", args=[format_type, filters])
    return jsonify({"task_id": task_id, "status_url": f"/api/tasks/{task_id}"})

@app.route("/api/tasks/<task_id>")
def get_task_status(task_id):
    result = celery.AsyncResult(task_id)
    return jsonify({"status": result.status, "result": result.result})
''',
        expected_issues=["비동기 작업", "작업 상태", "폴링 방법", "다운로드 URL"],
        difficulty="hard"
    ),
    DevelopmentTestCase(
        id="DOC-013",
        category="documentation",
        subcategory="api",
        language="java",
        code_snippet='''
@GetMapping("/api/reports/{id}")
public ResponseEntity<Resource> downloadReport(@PathVariable Long id) {
    Report report = reportService.findById(id);
    Resource resource = storageService.loadAsResource(report.getFilePath());

    return ResponseEntity.ok()
        .contentType(MediaType.APPLICATION_OCTET_STREAM)
        .header(HttpHeaders.CONTENT_DISPOSITION,
            "attachment; filename=\\"" + report.getFileName() + "\\"")
        .body(resource);
}
''',
        expected_issues=["파일 다운로드", "Content-Type", "파일명", "에러 케이스"],
        difficulty="medium"
    ),
    DevelopmentTestCase(
        id="DOC-014",
        category="documentation",
        subcategory="api",
        language="python",
        code_snippet='''
@app.route("/api/graphql", methods=["POST"])
def graphql():
    data = request.json
    query = data.get("query")
    variables = data.get("variables", {})

    result = schema.execute(query, variable_values=variables, context={"user": g.user})

    if result.errors:
        return jsonify({"errors": [str(e) for e in result.errors]}), 400
    return jsonify({"data": result.data})
''',
        expected_issues=["GraphQL 엔드포인트", "쿼리 형식", "변수", "에러 형식"],
        difficulty="hard"
    ),

    # === README 문서화 (14개) ===
    DevelopmentTestCase(
        id="DOC-015",
        category="documentation",
        subcategory="readme",
        language="python",
        code_snippet='''
# Simple Flask API starter
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World"

if __name__ == "__main__":
    app.run()
''',
        expected_issues=["프로젝트 설명", "설치 방법", "실행 방법", "API 예시"],
        difficulty="easy"
    ),
    DevelopmentTestCase(
        id="DOC-016",
        category="documentation",
        subcategory="readme",
        language="javascript",
        code_snippet='''
// React component library
export { Button } from "./Button";
export { Input } from "./Input";
export { Modal } from "./Modal";
export { Table } from "./Table";
export { Form } from "./Form";
''',
        expected_issues=["컴포넌트 목록", "설치 방법", "사용 예시", "Props 문서"],
        difficulty="medium"
    ),
    DevelopmentTestCase(
        id="DOC-017",
        category="documentation",
        subcategory="readme",
        language="python",
        code_snippet='''
# CLI tool for data processing
import click

@click.command()
@click.option("--input", "-i", required=True, help="Input file")
@click.option("--output", "-o", required=True, help="Output file")
@click.option("--format", "-f", default="csv", help="Output format")
def process(input, output, format):
    """Process data files"""
    # processing logic
    pass

if __name__ == "__main__":
    process()
''',
        expected_issues=["CLI 사용법", "옵션 설명", "예시 명령어", "출력 형식"],
        difficulty="medium"
    ),
    DevelopmentTestCase(
        id="DOC-018",
        category="documentation",
        subcategory="readme",
        language="go",
        code_snippet='''
package main

import (
    "github.com/gin-gonic/gin"
)

func main() {
    r := gin.Default()
    r.GET("/ping", func(c *gin.Context) {
        c.JSON(200, gin.H{"message": "pong"})
    })
    r.Run(":8080")
}
''',
        expected_issues=["빠른 시작", "요구사항", "설정 방법", "엔드포인트"],
        difficulty="easy"
    ),
    DevelopmentTestCase(
        id="DOC-019",
        category="documentation",
        subcategory="readme",
        language="javascript",
        code_snippet='''
// npm package for date utilities
export function formatDate(date, format) { /* ... */ }
export function parseDate(str, format) { /* ... */ }
export function addDays(date, days) { /* ... */ }
export function diffDays(date1, date2) { /* ... */ }
export function isWeekend(date) { /* ... */ }
''',
        expected_issues=["기능 목록", "설치 방법", "API 문서", "예시 코드"],
        difficulty="medium"
    ),
    DevelopmentTestCase(
        id="DOC-020",
        category="documentation",
        subcategory="readme",
        language="python",
        code_snippet='''
# Machine learning model wrapper
class TextClassifier:
    def __init__(self, model_path):
        self.model = load_model(model_path)

    def predict(self, text):
        return self.model.predict([text])[0]

    def predict_batch(self, texts):
        return self.model.predict(texts)

    def train(self, X, y, epochs=10):
        self.model.fit(X, y, epochs=epochs)
''',
        expected_issues=["모델 설명", "요구사항", "사용 예시", "성능 지표"],
        difficulty="hard"
    ),
    DevelopmentTestCase(
        id="DOC-021",
        category="documentation",
        subcategory="readme",
        language="rust",
        code_snippet='''
pub struct Cache<K, V> {
    capacity: usize,
    map: HashMap<K, V>,
}

impl<K: Hash + Eq, V> Cache<K, V> {
    pub fn new(capacity: usize) -> Self { /* ... */ }
    pub fn get(&self, key: &K) -> Option<&V> { /* ... */ }
    pub fn set(&mut self, key: K, value: V) { /* ... */ }
    pub fn clear(&mut self) { /* ... */ }
}
''',
        expected_issues=["라이브러리 설명", "Cargo 설치", "사용 예시", "제네릭 설명"],
        difficulty="medium"
    ),
    DevelopmentTestCase(
        id="DOC-022",
        category="documentation",
        subcategory="readme",
        language="javascript",
        code_snippet='''
// Docker compose setup
module.exports = {
    services: {
        web: { build: ".", ports: ["3000:3000"] },
        db: { image: "postgres:13", volumes: ["db-data:/var/lib/postgresql/data"] },
        redis: { image: "redis:6" },
        worker: { build: ".", command: "npm run worker" }
    }
};
''',
        expected_issues=["아키텍처 설명", "서비스 구성", "실행 방법", "환경 변수"],
        difficulty="hard"
    ),
    DevelopmentTestCase(
        id="DOC-023",
        category="documentation",
        subcategory="readme",
        language="python",
        code_snippet='''
# pytest plugin
def pytest_configure(config):
    config.addinivalue_line("markers", "slow: mark test as slow")

@pytest.fixture
def db_session():
    session = create_session()
    yield session
    session.rollback()
''',
        expected_issues=["플러그인 설명", "설치 방법", "설정 옵션", "사용 예시"],
        difficulty="medium"
    ),
    DevelopmentTestCase(
        id="DOC-024",
        category="documentation",
        subcategory="readme",
        language="javascript",
        code_snippet='''
// VS Code extension
export function activate(context) {
    let disposable = vscode.commands.registerCommand("extension.helloWorld", () => {
        vscode.window.showInformationMessage("Hello World!");
    });
    context.subscriptions.push(disposable);
}
export function deactivate() {}
''',
        expected_issues=["확장 설명", "설치 방법", "명령어 목록", "설정 옵션"],
        difficulty="medium"
    ),
    DevelopmentTestCase(
        id="DOC-025",
        category="documentation",
        subcategory="readme",
        language="go",
        code_snippet='''
// Kubernetes operator
type MyResourceSpec struct {
    Replicas int32  `json:"replicas"`
    Image    string `json:"image"`
}

func (r *MyResourceReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    // reconciliation logic
    return ctrl.Result{}, nil
}
''',
        expected_issues=["오퍼레이터 설명", "CRD 정의", "설치 방법", "사용 예시"],
        difficulty="hard"
    ),
    DevelopmentTestCase(
        id="DOC-026",
        category="documentation",
        subcategory="readme",
        language="python",
        code_snippet='''
# GitHub Action
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install -r requirements.txt
      - run: pytest
''',
        expected_issues=["액션 설명", "트리거 이벤트", "입력/출력", "사용 예시"],
        difficulty="medium"
    ),
    DevelopmentTestCase(
        id="DOC-027",
        category="documentation",
        subcategory="readme",
        language="javascript",
        code_snippet='''
// Webpack plugin
class MyWebpackPlugin {
    apply(compiler) {
        compiler.hooks.emit.tapAsync("MyPlugin", (compilation, callback) => {
            // plugin logic
            callback();
        });
    }
}
module.exports = MyWebpackPlugin;
''',
        expected_issues=["플러그인 설명", "설치 방법", "설정 옵션", "동작 방식"],
        difficulty="hard"
    ),
    DevelopmentTestCase(
        id="DOC-028",
        category="documentation",
        subcategory="readme",
        language="python",
        code_snippet='''
# Terraform module
variable "instance_type" { default = "t2.micro" }
variable "ami" { type = string }

resource "aws_instance" "main" {
    ami           = var.ami
    instance_type = var.instance_type
}

output "instance_ip" { value = aws_instance.main.public_ip }
''',
        expected_issues=["모듈 설명", "입력 변수", "출력 값", "사용 예시"],
        difficulty="medium"
    ),

    # === 코드 주석 (13개) ===
    DevelopmentTestCase(
        id="DOC-029",
        category="documentation",
        subcategory="comments",
        language="python",
        code_snippet='''
def calculate_discount(price, user_type, quantity):
    base_discount = 0
    if user_type == "premium":
        base_discount = 0.1
    elif user_type == "vip":
        base_discount = 0.2

    quantity_discount = min(quantity * 0.01, 0.15)
    total_discount = min(base_discount + quantity_discount, 0.3)

    return price * (1 - total_discount)
''',
        expected_issues=["함수 docstring", "파라미터 설명", "반환값 설명", "로직 설명"],
        difficulty="easy"
    ),
    DevelopmentTestCase(
        id="DOC-030",
        category="documentation",
        subcategory="comments",
        language="python",
        code_snippet='''
class OrderProcessor:
    def __init__(self, db, payment_gateway, notification_service):
        self.db = db
        self.payment = payment_gateway
        self.notifier = notification_service

    def process(self, order):
        self._validate(order)
        self._reserve_inventory(order)
        charge = self._process_payment(order)
        self._confirm_order(order, charge)
        self._send_notification(order)
        return order

    def _validate(self, order):
        if not order.items:
            raise ValueError("Empty order")
''',
        expected_issues=["클래스 docstring", "메서드 설명", "예외 설명", "의존성 설명"],
        difficulty="medium"
    ),
    DevelopmentTestCase(
        id="DOC-031",
        category="documentation",
        subcategory="comments",
        language="javascript",
        code_snippet='''
function debounce(func, wait, immediate = false) {
    let timeout;
    return function executedFunction(...args) {
        const context = this;
        const later = function() {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(context, args);
    };
}
''',
        expected_issues=["JSDoc 주석", "파라미터 설명", "반환값", "사용 예시"],
        difficulty="medium"
    ),
    DevelopmentTestCase(
        id="DOC-032",
        category="documentation",
        subcategory="comments",
        language="java",
        code_snippet='''
public class BinarySearchTree<T extends Comparable<T>> {
    private Node<T> root;

    public void insert(T value) {
        root = insertRec(root, value);
    }

    private Node<T> insertRec(Node<T> node, T value) {
        if (node == null) return new Node<>(value);
        if (value.compareTo(node.value) < 0)
            node.left = insertRec(node.left, value);
        else if (value.compareTo(node.value) > 0)
            node.right = insertRec(node.right, value);
        return node;
    }
}
''',
        expected_issues=["Javadoc 주석", "클래스 설명", "메서드 설명", "복잡도 설명"],
        difficulty="medium"
    ),
    DevelopmentTestCase(
        id="DOC-033",
        category="documentation",
        subcategory="comments",
        language="go",
        code_snippet='''
func (s *Server) handleWebSocket(w http.ResponseWriter, r *http.Request) {
    conn, err := upgrader.Upgrade(w, r, nil)
    if err != nil {
        return
    }
    defer conn.Close()

    client := &Client{conn: conn, send: make(chan []byte, 256)}
    s.register <- client

    go client.writePump()
    client.readPump()
}
''',
        expected_issues=["GoDoc 주석", "함수 설명", "파라미터", "에러 처리"],
        difficulty="medium"
    ),
    DevelopmentTestCase(
        id="DOC-034",
        category="documentation",
        subcategory="comments",
        language="python",
        code_snippet='''
async def fetch_all(urls, max_concurrent=10):
    semaphore = asyncio.Semaphore(max_concurrent)
    async def fetch_one(url):
        async with semaphore:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    return await response.text()

    tasks = [fetch_one(url) for url in urls]
    return await asyncio.gather(*tasks, return_exceptions=True)
''',
        expected_issues=["비동기 함수 설명", "동시성 제한", "예외 처리", "반환값"],
        difficulty="hard"
    ),
    DevelopmentTestCase(
        id="DOC-035",
        category="documentation",
        subcategory="comments",
        language="typescript",
        code_snippet='''
interface PaginationOptions {
    page?: number;
    limit?: number;
    sortBy?: string;
    sortOrder?: 'asc' | 'desc';
}

function paginate<T>(items: T[], options: PaginationOptions): {
    data: T[];
    total: number;
    page: number;
    totalPages: number;
} {
    const { page = 1, limit = 10, sortBy, sortOrder = 'asc' } = options;
    // pagination logic
}
''',
        expected_issues=["인터페이스 설명", "제네릭 설명", "옵션 설명", "반환 타입"],
        difficulty="medium"
    ),
    DevelopmentTestCase(
        id="DOC-036",
        category="documentation",
        subcategory="comments",
        language="python",
        code_snippet='''
@contextmanager
def transaction(connection):
    cursor = connection.cursor()
    try:
        yield cursor
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
''',
        expected_issues=["컨텍스트 매니저", "트랜잭션 설명", "예외 처리", "사용 예시"],
        difficulty="medium"
    ),
    DevelopmentTestCase(
        id="DOC-037",
        category="documentation",
        subcategory="comments",
        language="javascript",
        code_snippet='''
class EventEmitter {
    #listeners = new Map();

    on(event, callback) {
        if (!this.#listeners.has(event)) {
            this.#listeners.set(event, new Set());
        }
        this.#listeners.get(event).add(callback);
        return () => this.off(event, callback);
    }

    emit(event, ...args) {
        this.#listeners.get(event)?.forEach(cb => cb(...args));
    }
}
''',
        expected_issues=["클래스 설명", "private 필드", "메서드 설명", "반환값"],
        difficulty="medium"
    ),
    DevelopmentTestCase(
        id="DOC-038",
        category="documentation",
        subcategory="comments",
        language="rust",
        code_snippet='''
pub fn merge_sort<T: Ord + Clone>(arr: &mut [T]) {
    let len = arr.len();
    if len <= 1 { return; }

    let mid = len / 2;
    merge_sort(&mut arr[..mid]);
    merge_sort(&mut arr[mid..]);

    let mut merged = Vec::with_capacity(len);
    // merge logic
}
''',
        expected_issues=["함수 설명", "제네릭 제약", "알고리즘 설명", "복잡도"],
        difficulty="hard"
    ),
    DevelopmentTestCase(
        id="DOC-039",
        category="documentation",
        subcategory="comments",
        language="python",
        code_snippet='''
def retry(max_attempts=3, delay=1, backoff=2, exceptions=(Exception,)):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            current_delay = delay
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    attempts += 1
                    if attempts == max_attempts:
                        raise
                    time.sleep(current_delay)
                    current_delay *= backoff
        return wrapper
    return decorator
''',
        expected_issues=["데코레이터 설명", "파라미터 설명", "재시도 로직", "사용 예시"],
        difficulty="hard"
    ),
    DevelopmentTestCase(
        id="DOC-040",
        category="documentation",
        subcategory="comments",
        language="java",
        code_snippet='''
@FunctionalInterface
public interface Predicate<T> {
    boolean test(T t);

    default Predicate<T> and(Predicate<? super T> other) {
        return t -> test(t) && other.test(t);
    }

    default Predicate<T> or(Predicate<? super T> other) {
        return t -> test(t) || other.test(t);
    }

    default Predicate<T> negate() {
        return t -> !test(t);
    }
}
''',
        expected_issues=["인터페이스 설명", "함수형 인터페이스", "default 메서드", "제네릭"],
        difficulty="hard"
    ),
    DevelopmentTestCase(
        id="DOC-041",
        category="documentation",
        subcategory="comments",
        language="go",
        code_snippet='''
type RateLimiter struct {
    rate     float64
    capacity float64
    tokens   float64
    lastTime time.Time
    mu       sync.Mutex
}

func (rl *RateLimiter) Allow() bool {
    rl.mu.Lock()
    defer rl.mu.Unlock()

    now := time.Now()
    elapsed := now.Sub(rl.lastTime).Seconds()
    rl.tokens = math.Min(rl.capacity, rl.tokens+elapsed*rl.rate)
    rl.lastTime = now

    if rl.tokens >= 1 {
        rl.tokens--
        return true
    }
    return false
}
''',
        expected_issues=["구조체 설명", "필드 설명", "알고리즘 설명", "동시성 처리"],
        difficulty="hard"
    ),

    # === 아키텍처 문서 (13개) ===
    DevelopmentTestCase(
        id="DOC-042",
        category="documentation",
        subcategory="architecture",
        language="python",
        code_snippet='''
# Layered architecture
# app/
#   api/          # Presentation layer
#   services/     # Business logic layer
#   repositories/ # Data access layer
#   models/       # Domain models
#   schemas/      # DTOs

from app.services import UserService
from app.repositories import UserRepository

class UserController:
    def __init__(self):
        self.service = UserService(UserRepository())
''',
        expected_issues=["레이어 설명", "책임 분리", "의존성 흐름", "디렉토리 구조"],
        difficulty="medium"
    ),
    DevelopmentTestCase(
        id="DOC-043",
        category="documentation",
        subcategory="architecture",
        language="javascript",
        code_snippet='''
// Microservices communication
// Services: user-service, order-service, payment-service, notification-service

// Event-driven architecture using message broker
class OrderService {
    async createOrder(order) {
        await this.db.save(order);
        await this.messageBroker.publish("order.created", order);
    }
}

class PaymentService {
    constructor() {
        this.messageBroker.subscribe("order.created", this.processPayment);
    }
}
''',
        expected_issues=["서비스 목록", "통신 방식", "이벤트 흐름", "데이터 일관성"],
        difficulty="hard"
    ),
    DevelopmentTestCase(
        id="DOC-044",
        category="documentation",
        subcategory="architecture",
        language="go",
        code_snippet='''
// Clean Architecture
// internal/
//   domain/     # Entities, Value Objects
//   usecase/    # Application business rules
//   interface/  # Controllers, Gateways
//   infra/      # DB, External services

type UserUseCase struct {
    repo UserRepository
}

func (uc *UserUseCase) Register(input RegisterInput) (*User, error) {
    user := domain.NewUser(input.Email, input.Password)
    return uc.repo.Save(user)
}
''',
        expected_issues=["계층 설명", "의존성 규칙", "유즈케이스", "인터페이스"],
        difficulty="hard"
    ),
    DevelopmentTestCase(
        id="DOC-045",
        category="documentation",
        subcategory="architecture",
        language="java",
        code_snippet='''
// CQRS pattern
@Service
public class OrderCommandHandler {
    @Autowired
    private EventStore eventStore;

    public void handle(CreateOrderCommand cmd) {
        Order order = new Order(cmd.getOrderId());
        order.apply(new OrderCreatedEvent(cmd));
        eventStore.save(order.getChanges());
    }
}

@Service
public class OrderQueryHandler {
    @Autowired
    private ReadModelRepository repository;

    public OrderDTO getOrder(String orderId) {
        return repository.findById(orderId);
    }
}
''',
        expected_issues=["CQRS 설명", "Command/Query 분리", "이벤트 소싱", "읽기 모델"],
        difficulty="hard"
    ),
    DevelopmentTestCase(
        id="DOC-046",
        category="documentation",
        subcategory="architecture",
        language="python",
        code_snippet='''
# API Gateway pattern
class APIGateway:
    def __init__(self):
        self.services = {
            "users": "http://user-service:8001",
            "orders": "http://order-service:8002",
            "products": "http://product-service:8003"
        }

    async def route(self, request):
        service = self._get_service(request.path)
        await self._authenticate(request)
        await self._rate_limit(request)
        return await self._forward(service, request)
''',
        expected_issues=["게이트웨이 역할", "라우팅", "인증/인가", "Rate limiting"],
        difficulty="hard"
    ),
    DevelopmentTestCase(
        id="DOC-047",
        category="documentation",
        subcategory="architecture",
        language="javascript",
        code_snippet='''
// State management architecture (Redux-like)
const store = createStore(
    combineReducers({
        users: usersReducer,
        orders: ordersReducer,
        ui: uiReducer
    }),
    applyMiddleware(thunk, logger)
);

// Action -> Middleware -> Reducer -> Store -> View
function fetchUsers() {
    return async (dispatch) => {
        dispatch({ type: "USERS_LOADING" });
        const users = await api.getUsers();
        dispatch({ type: "USERS_LOADED", payload: users });
    };
}
''',
        expected_issues=["상태 관리 흐름", "리듀서 구조", "미들웨어", "비동기 액션"],
        difficulty="medium"
    ),
    DevelopmentTestCase(
        id="DOC-048",
        category="documentation",
        subcategory="architecture",
        language="go",
        code_snippet='''
// Worker pool pattern
type Job struct {
    ID   int
    Data interface{}
}

type Worker struct {
    ID      int
    JobChan chan Job
    Quit    chan bool
}

type Dispatcher struct {
    WorkerPool chan chan Job
    MaxWorkers int
    JobQueue   chan Job
}

func (d *Dispatcher) dispatch() {
    for job := range d.JobQueue {
        worker := <-d.WorkerPool
        worker <- job
    }
}
''',
        expected_issues=["워커 풀 패턴", "채널 사용", "동시성 처리", "작업 분배"],
        difficulty="hard"
    ),
    DevelopmentTestCase(
        id="DOC-049",
        category="documentation",
        subcategory="architecture",
        language="python",
        code_snippet='''
# Plugin architecture
class PluginManager:
    def __init__(self):
        self.plugins = {}

    def register(self, name, plugin):
        if not isinstance(plugin, BasePlugin):
            raise TypeError("Must implement BasePlugin")
        self.plugins[name] = plugin

    def execute_hook(self, hook_name, *args, **kwargs):
        for plugin in self.plugins.values():
            if hasattr(plugin, hook_name):
                getattr(plugin, hook_name)(*args, **kwargs)

class BasePlugin(ABC):
    @abstractmethod
    def on_init(self): pass
    @abstractmethod
    def on_shutdown(self): pass
''',
        expected_issues=["플러그인 구조", "훅 시스템", "인터페이스", "등록 메커니즘"],
        difficulty="medium"
    ),
    DevelopmentTestCase(
        id="DOC-050",
        category="documentation",
        subcategory="architecture",
        language="java",
        code_snippet='''
// Hexagonal Architecture
// Ports
public interface OrderRepository {
    Order save(Order order);
    Optional<Order> findById(String id);
}

public interface PaymentGateway {
    PaymentResult charge(Payment payment);
}

// Adapters
@Repository
public class JpaOrderRepository implements OrderRepository { }

@Component
public class StripePaymentAdapter implements PaymentGateway { }
''',
        expected_issues=["헥사고날 설명", "포트/어댑터", "의존성 역전", "테스트 용이성"],
        difficulty="hard"
    ),
    DevelopmentTestCase(
        id="DOC-051",
        category="documentation",
        subcategory="architecture",
        language="javascript",
        code_snippet='''
// Serverless architecture
// Functions:
//   api/users.js    - User CRUD
//   api/orders.js   - Order processing
//   workers/email.js - Email sending
//   workers/report.js - Report generation

exports.handler = async (event) => {
    const { httpMethod, path, body } = event;
    // Cold start handling, context reuse
    // Event-driven triggers
};
''',
        expected_issues=["서버리스 구조", "함수 목록", "트리거 유형", "콜드 스타트"],
        difficulty="medium"
    ),
    DevelopmentTestCase(
        id="DOC-052",
        category="documentation",
        subcategory="architecture",
        language="python",
        code_snippet='''
# Circuit Breaker pattern
class CircuitBreaker:
    def __init__(self, failure_threshold=5, recovery_timeout=30):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.state = "CLOSED"
        self.last_failure_time = None

    def call(self, func, *args, **kwargs):
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = "HALF_OPEN"
            else:
                raise CircuitOpenError()
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise
''',
        expected_issues=["서킷 브레이커 설명", "상태 전이", "임계값", "복구 로직"],
        difficulty="hard"
    ),
    DevelopmentTestCase(
        id="DOC-053",
        category="documentation",
        subcategory="architecture",
        language="go",
        code_snippet='''
// Saga pattern for distributed transactions
type OrderSaga struct {
    steps []SagaStep
}

type SagaStep struct {
    Action     func() error
    Compensate func() error
}

func (s *OrderSaga) Execute() error {
    completedSteps := []SagaStep{}
    for _, step := range s.steps {
        if err := step.Action(); err != nil {
            s.compensate(completedSteps)
            return err
        }
        completedSteps = append(completedSteps, step)
    }
    return nil
}
''',
        expected_issues=["사가 패턴 설명", "보상 트랜잭션", "단계별 실행", "롤백 처리"],
        difficulty="hard"
    ),
    DevelopmentTestCase(
        id="DOC-054",
        category="documentation",
        subcategory="architecture",
        language="javascript",
        code_snippet='''
// BFF (Backend for Frontend) pattern
// bff-web/     - Web application BFF
// bff-mobile/  - Mobile application BFF
// services/    - Shared microservices

class WebBFF {
    async getDashboard(userId) {
        const [user, orders, recommendations] = await Promise.all([
            this.userService.getUser(userId),
            this.orderService.getRecentOrders(userId, 5),
            this.recommendationService.getTopPicks(userId, 10)
        ]);

        return {
            user: this.formatUserForWeb(user),
            orders: orders.map(this.formatOrderForWeb),
            recommendations
        };
    }
}
''',
        expected_issues=["BFF 패턴 설명", "클라이언트별 최적화", "데이터 집계", "응답 포맷팅"],
        difficulty="hard"
    ),
]


# ============================================================================
# 테스트 케이스 접근 함수
# ============================================================================

def get_all_development_test_cases() -> List[DevelopmentTestCase]:
    """모든 개발 테스트 케이스 반환 (108개)"""
    return CODE_REVIEW_TEST_CASES + DOCUMENTATION_TEST_CASES


def get_code_review_test_cases() -> List[DevelopmentTestCase]:
    """코드 리뷰 테스트 케이스 반환 (54개)"""
    return CODE_REVIEW_TEST_CASES


def get_documentation_test_cases() -> List[DevelopmentTestCase]:
    """문서화 테스트 케이스 반환 (54개)"""
    return DOCUMENTATION_TEST_CASES


def get_test_cases_by_subcategory(subcategory: str) -> List[DevelopmentTestCase]:
    """서브카테고리별 테스트 케이스 반환"""
    all_cases = get_all_development_test_cases()
    return [tc for tc in all_cases if tc.subcategory == subcategory]


def get_test_cases_by_language(language: str) -> List[DevelopmentTestCase]:
    """프로그래밍 언어별 테스트 케이스 반환"""
    all_cases = get_all_development_test_cases()
    return [tc for tc in all_cases if tc.language.lower() == language.lower()]
