from fastapi import FastAPI, Request, HTTPException, Query
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import requests
import json
import mysql.connector
from decimal import Decimal
from config import ai_config, Config, get_ai_service_status, medical_config

app = FastAPI()

# 允许所有来源的CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = "RAWNJTl7ml69HPXE7urd606c"
SECRET_KEY = "UTuXPncTrMHCIedR3dBXY7afhjJB04k2"

@app.post("/register")
async def register(request: Request):
    data = await request.json()

    # 获取注册数据
    name = data.get('name')
    username = data.get('username')
    password = data.get('password')
    phone = data.get('phone')
    email = data.get('email')
    gender = data.get('gender')
    age = data.get('age')
    location = data.get('location')
    role = data.get('role', 'user')

    # 验证必填字段
    if not all([name, username, password, phone, email, gender, role]):
        raise HTTPException(status_code=400, detail="请填写所有必填信息")

    # 验证用户名是否已存在
    if check_username_exists(username):
        return JSONResponse(content={"code": 400, "message": "用户名已存在"})

    # 验证手机号是否已存在
    if check_phone_exists(phone):
        return JSONResponse(content={"code": 400, "message": "手机号已被注册"})

    # 验证邮箱是否已存在
    if check_email_exists(email):
        return JSONResponse(content={"code": 400, "message": "邮箱已被注册"})

    # 创建用户
    try:
        user_id = create_user(name, username, password, phone, email, gender, age, location, role)
        return JSONResponse(content={"code": 200, "message": "注册成功", "user_id": user_id})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"注册失败: {str(e)}")

def check_username_exists(username):
    """检查用户名是否已存在"""
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="patient_information"
    )
    cursor = connection.cursor()
    query = "SELECT COUNT(*) FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    count = cursor.fetchone()[0]
    cursor.close()
    connection.close()
    return count > 0

def check_phone_exists(phone):
    """检查手机号是否已存在"""
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="patient_information"
    )
    cursor = connection.cursor()
    query = "SELECT COUNT(*) FROM users WHERE phone = %s"
    cursor.execute(query, (phone,))
    count = cursor.fetchone()[0]
    cursor.close()
    connection.close()
    return count > 0

def check_email_exists(email):
    """检查邮箱是否已存在"""
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="patient_information"
    )
    cursor = connection.cursor()
    query = "SELECT COUNT(*) FROM users WHERE email = %s"
    cursor.execute(query, (email,))
    count = cursor.fetchone()[0]
    cursor.close()
    connection.close()
    return count > 0

def create_user(name, username, password, phone, email, gender, age, location, role):
    """创建新用户"""
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="patient_information"
    )
    cursor = connection.cursor()

    # 插入用户数据 - 包含所有必要字段（包括password_hash）
    query = """
    INSERT INTO users (name, username, password, password_hash, phone, email, gender, age, location, role, status)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'active')
    """

    # 使用相同的密码填充password和password_hash字段
    cursor.execute(query, (name, username, password, password, phone, email, gender, age, location, role))
    user_id = cursor.lastrowid
    connection.commit()
    cursor.close()
    connection.close()

    return user_id

@app.post("/login")
async def login(request: Request):
    data = await request.json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    if not username or not password or not role:
        raise HTTPException(status_code=400, detail="用户名、密码和角色是必填项")

    user = authenticate_user(username, password, role)
    if user:
        return JSONResponse(content={
            "code": 200,
            "role": role,
            "message": "登录成功",
            "data": {
                "id": user["user_id"],
                "name": user.get("name", username),
                "username": user["username"],
                "role": user["role"]
            }
        })
    else:
        return JSONResponse(content={"code": 401, "message": "用户名、密码或角色不匹配"})

def authenticate_user(username, password, role):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="patient_information"
    )
    cursor = connection.cursor(dictionary=True)
    query = ("SELECT * FROM users WHERE username = %s AND password = %s AND role = %s")
    cursor.execute(query, (username, password, role))
    user = cursor.fetchone()
    cursor.close()
    connection.close()
    return user

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    message = data.get('message')
    name = data.get('name')
    location = data.get('location')
    problem = data.get('problem')
    conversation_style = data.get('conversationStyle', 'natural')  # 获取对话风格，默认为自然
    response = get_response(message, name, location, problem, conversation_style)
    return JSONResponse(content={"response": response})

@app.post("/submit")
async def submit(request: Request):
    try:
        form_data = await request.json()

        # 验证必填字段
        required_fields = ['name', 'location', 'problem']
        missing_fields = [field for field in required_fields if not form_data.get(field)]

        if missing_fields:
            return JSONResponse(
                status_code=400,
                content={
                    "code": 400,
                    "message": f"缺少必填字段: {', '.join(missing_fields)}",
                    "missing_fields": missing_fields
                }
            )

        # 保存到数据库
        save_to_database(form_data)

        return JSONResponse(content={
            "code": 200,
            "message": "表单提交成功",
            "data": {
                "name": form_data['name'],
                "location": form_data['location'],
                "problem": form_data['problem'],
                "urgency": form_data.get('urgency', 'low'),
                "timestamp": "已保存"
            }
        })

    except Exception as e:
        print(f"提交表单时发生错误: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "code": 500,
                "message": "服务器内部错误，请稍后重试",
                "error": str(e)
            }
        )

@app.get("/api/status")
async def get_api_status():
    """获取API服务状态"""
    status = get_ai_service_status()
    return JSONResponse(content={
        "system_status": "online",
        "ai_services": status,
        "database_status": "connected",
        "emergency_keywords_count": len(medical_config.EMERGENCY_KEYWORDS),
        "supported_departments": len(medical_config.DEPARTMENTS)
    })

def save_to_database(form_data):
    """保存表单数据到数据库，支持字段兼容性"""
    connection = None
    cursor = None

    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="patient_information"
        )
        cursor = connection.cursor()

        # 首先检查表结构，确定可用字段
        cursor.execute("DESCRIBE patient_information")
        columns = [row[0] for row in cursor.fetchall()]
        print(f"数据库表字段: {columns}")

        # 根据可用字段构建插入语句
        base_fields = ['name', 'location', 'problem']
        base_values = [form_data['name'], form_data['location'], form_data['problem']]

        # 检查可选字段
        optional_fields = []
        optional_values = []

        if 'urgency' in columns and 'urgency' in form_data:
            optional_fields.append('urgency')
            optional_values.append(form_data['urgency'])

        if 'created_at' in columns:
            optional_fields.append('created_at')
            optional_values.append('NOW()')

        # 构建SQL语句
        all_fields = base_fields + optional_fields
        all_values = base_values + optional_values

        # 处理NOW()函数
        placeholders = []
        actual_values = []
        for value in all_values:
            if value == 'NOW()':
                placeholders.append('NOW()')
            else:
                placeholders.append('%s')
                actual_values.append(value)

        sql = f"INSERT INTO patient_information ({', '.join(all_fields)}) VALUES ({', '.join(placeholders)})"

        print(f"执行SQL: {sql}")
        print(f"参数值: {actual_values}")

        cursor.execute(sql, actual_values)
        connection.commit()

        print(f"✅ 成功保存用户数据: {form_data['name']} - {form_data['problem']}")
        return True

    except mysql.connector.Error as e:
        print(f"❌ 数据库错误: {e}")
        raise e
    except Exception as e:
        print(f"❌ 保存数据时发生错误: {e}")
        raise e
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

import mysql.connector

def get_hospital_info(location, problem):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="patient_information"
    )
    cursor = connection.cursor(dictionary=True)
    query = ("SELECT 医院名称, 医院地址, 联系电话, 医院等级, 重点科室, 经营方式 FROM hospital_sum "
             "WHERE 医院地址 LIKE %s AND 重点科室 LIKE %s LIMIT 1")
    cursor.execute(query, (f"%{location}%", f"%{problem}%"))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result

def get_response(message, name, location, problem, conversation_style='natural'):
    """获取AI回复，使用智谱AI"""
    try:
        print("使用智谱AI...")
        return get_zhipu_response(message, name, location, problem, conversation_style)
    except Exception as e:
        print(f"智谱AI调用失败: {e}")
        return "抱歉，AI服务暂时不可用。请检查网络连接或稍后重试。如有紧急情况，请立即就医或拨打120。"

def get_zhipu_response(message, name, location, problem, conversation_style='natural'):
    """使用智谱AI进行对话"""

    # 检查智谱AI是否可用
    if not ai_config.is_zhipu_available():
        raise Exception("智谱AI API密钥未配置，请检查配置文件")

    # 检查是否为急症
    emergency_keywords = medical_config.EMERGENCY_KEYWORDS
    is_emergency = any(keyword in problem for keyword in emergency_keywords) if problem else False

    if name and location and problem:
        hospital_info = get_hospital_info(location, problem)

        # 如果找不到匹配，尝试只按地址查询
        if not hospital_info:
            try:
                connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="root",
                    database="patient_information"
                )
                cursor = connection.cursor(dictionary=True)
                query = ("SELECT 医院名称, 医院地址, 联系电话, 医院等级, 重点科室, 经营方式 FROM hospital_sum "
                        "WHERE 医院地址 LIKE %s LIMIT 1")
                cursor.execute(query, (f"%{location}%",))
                hospital_info = cursor.fetchone()
                cursor.close()
                connection.close()
            except:
                hospital_info = None

        if hospital_info:
            hospital = hospital_info['医院名称']
            address = hospital_info['医院地址']
            phone = hospital_info['联系电话']
            level = hospital_info['医院等级']
            department = hospital_info['重点科室']
            operation = hospital_info['经营方式']
        else:
            hospital = "未能找到精确匹配的医院"
            address = f"{location}周边医院"
            phone = "建议查询当地医院热线"
            level = "建议前往三甲医院"
            department = "相关科室"
            operation = "公立或私立医院均可"

        emergency_notice = "【紧急提醒】您描述的症状可能是急症，建议立即前往最近医院急诊科就诊，或拨打120急救电话！\n\n" if is_emergency else ""

        # 根据对话风格选择不同的提示词
        if conversation_style == 'formal':
            # 正式回复模式 - 结构化的专业回复
            prompt = f"""你是一位经验丰富的AI专业医生，具备全科医学知识和丰富的临床经验。请以专业医生的身份，为患者提供详细、专业的医疗咨询。

{emergency_notice}**患者信息：**
- **患者姓名：** {name}
- **所在地区：** {location}
- **主要症状：** {problem}
- **当前咨询：** {message}

**医疗资源信息：**
- **推荐医院：** {hospital}
- **医院地址：** {address}
- **联系电话：** {phone}
- **医院等级：** {level}
- **重点科室：** {department}

请按以下格式提供详细的医疗咨询（使用Markdown格式）：

## 👨‍⚕️ 专业医疗分析

### 🔍 症状评估与分析
基于您描述的症状，进行专业的医学分析

### 💊 专业治疗建议
提供基于循证医学的治疗建议

### 🏥 就医指导
推荐科室和就医时机

### 📋 医嘱与注意事项
用药注意事项和复诊建议

### ⚕️ 医疗声明
本建议基于您提供的症状描述，仅供参考。如症状持续或加重，请及时就医。

请用专业、亲切的医生语气回复，提供详细的医学分析。"""
        else:
            # 自然对话模式 - 更像真实医生的对话
            prompt = f"""你是一位经验丰富的全科医生，有着20多年的临床经验。现在有一位患者来咨询，请以自然、亲切的医生语气与患者对话。

{emergency_notice}患者信息：
- 姓名：{name}
- 地区：{location}
- 主要症状：{problem}
- 当前咨询：{message}

附近医疗资源：
- 推荐医院：{hospital}（{address}，电话：{phone}）
- 医院等级：{level}，重点科室：{department}

请以真实医生的口吻回复，要求：
1. 语气自然亲切，像面对面交流一样
2. 不要使用过多的标题和格式化符号
3. 可以适当使用一些医生常用的表达方式
4. 根据症状给出专业但易懂的分析
5. 如果需要，可以推荐合适的科室和检查
6. 提醒患者注意事项，但不要过于正式
7. 如果患者咨询非医疗问题，礼貌地引导他们回到健康话题

请直接开始对话，不需要固定的格式框架。"""
    else:
        # 对于一般咨询，根据对话风格选择提示词
        if conversation_style == 'formal':
            # 正式回复模式
            prompt = f"""你是Dr. AI Assistant，一位经验丰富的AI专业医生，具备全科医学知识和丰富的临床经验。

患者咨询：{message}

请按照以下格式以专业医生身份回复：

## 👨‍⚕️ Dr. AI Assistant 专业医疗咨询

### 🔍 针对您的咨询
[基于医学专业知识分析患者的问题]

### 💊 专业医疗建议
[提供基于循证医学的专业建议]

### 🏥 就医指导
[如需要，提供科室选择和就医建议]

### ⚠️ 医疗提醒
[重要的医疗注意事项]

### ⚕️ 医疗声明
作为AI医生，我的建议基于医学知识库，仅供参考。如有严重症状或疑问，请及时就医。

请用专业、亲切的医生语气回复。如果患者咨询非医疗问题，请礼貌地引导他们回到医疗健康话题。"""
        else:
            # 自然对话模式
            prompt = f"""你是一位经验丰富的全科医生，有着丰富的临床经验。现在有患者向你咨询健康问题。

患者咨询：{message}

请以自然、亲切的医生语气回复，要求：
1. 语气自然，像真实医生与患者面对面交流
2. 不要使用过多的标题和格式化符号
3. 根据问题给出专业但通俗易懂的回答
4. 如果是医疗相关问题，给出合理的建议
5. 如果不是医疗问题，礼貌地引导回到健康话题
6. 适当提醒患者就医或注意事项

请直接开始对话，用自然的语言回复。"""

    headers = {
        'Authorization': f'Bearer {ai_config.ZHIPU_API_KEY}',
        'Content-Type': 'application/json'
    }

    payload = {
        "model": "glm-4",
        "messages": [
            {
                "role": "system",
                "content": "你是一位经验丰富的全科医生，请以自然、亲切的语气与患者对话，避免过度格式化的回复。"
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.8,  # 提高创造性，让回复更自然
        "max_tokens": 1200,  # 适当减少长度，避免过长的回复
        "top_p": 0.9,       # 增加多样性
        "frequency_penalty": 0.1  # 减少重复表达
    }

    print(f"发送到智谱AI的请求: {json.dumps(payload, ensure_ascii=False, indent=2)}")

    response = requests.post(ai_config.ZHIPU_URL, headers=headers, json=payload, timeout=30)

    print(f"智谱AI响应状态码: {response.status_code}")
    print(f"智谱AI响应内容: {response.text}")

    if response.status_code == 200:
        result = response.json()

        # 检查响应格式
        if 'choices' in result and len(result['choices']) > 0:
            choice = result['choices'][0]

            # 检查是否有工具调用
            if 'message' in choice:
                message = choice['message']

                # 如果有工具调用，返回错误信息
                if 'tool_calls' in message and message['tool_calls']:
                    print("检测到工具调用，返回错误信息")
                    return "抱歉，AI服务出现了技术问题。作为您的专业AI医生，我建议您重新描述症状，我会为您提供专业的医疗建议。如有紧急情况，请立即就医。"

                # 返回正常的文本内容
                if 'content' in message and message['content']:
                    return message['content']
                else:
                    return "抱歉，我没有收到完整的回复。请重新描述您的症状，我会为您提供专业的医疗建议。"
            else:
                return "抱歉，AI服务响应格式异常。请重新咨询，我会为您提供专业的医疗建议。"
        else:
            return "抱歉，AI服务暂时不可用。请稍后重试，或如有紧急情况请立即就医。"
    else:
        print(f"智谱AI API调用失败: {response.status_code}, 响应: {response.text}")
        raise Exception(f"智谱AI API调用失败: {response.status_code}")


class APIDoctorRequest(BaseModel):
    search: str

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

@app.post("/api/doctors")
async def get_doctors(request: APIDoctorRequest):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="patient_information"
        )
        cursor = connection.cursor(dictionary=True)
        query = ("SELECT 医生姓名 as name, 职称 as position, 科室 as department, 医院 as hospital, 评分 as rating, 患者数 as patientCount, 擅长 as specialty, 挂号费 as registrationFee, 门诊费 as consultationFee, 医生主页 as url FROM doctors WHERE 擅长 LIKE %s")
        cursor.execute(query, (f"%{request.search}%",))
        doctors = cursor.fetchall()
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
    return JSONResponse(content=json.loads(json.dumps(doctors, default=decimal_default)))

@app.get("/api/hospitals")
async def search_hospitals(
    hospitalName: str = Query(None, description="医院名称"),
    hospitalLevel: str = Query(None, description="医院等级"),
    department: str = Query(None, description="科室"),
    location: str = Query(None, description="地区"),
    page: int = Query(1, description="页码", ge=1),
    pageSize: int = Query(200, description="每页数量", ge=1, le=500)
):
    """搜索医院信息"""
    connection = None
    cursor = None

    try:
        print(f"接收到的参数: hospitalName={hospitalName}, hospitalLevel={hospitalLevel}, department={department}, location={location}")

        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="patient_information"
        )
        cursor = connection.cursor(dictionary=True)

        # 构建查询条件，过滤空值和无效值
        conditions = []
        params = []

        if hospitalName and hospitalName.strip() and hospitalName.strip() != '':
            conditions.append("医院名称 LIKE %s")
            params.append(f"%{hospitalName.strip()}%")

        if hospitalLevel and hospitalLevel.strip() and hospitalLevel.strip() != '':
            level_keyword = hospitalLevel.strip()

            # 优化医院等级搜索逻辑
            level_conditions = []
            level_params = []

            # 1. 直接匹配
            level_conditions.append("医院等级 = %s")
            level_params.append(level_keyword)

            # 2. 模糊匹配（处理可能的格式差异）
            level_conditions.append("医院等级 LIKE %s")
            level_params.append(f"%{level_keyword}%")

            # 3. 处理简称到全称的映射
            level_mapping = {
                '三甲': '三级甲等',
                '三乙': '三级乙等',
                '二甲': '二级甲等',
                '二乙': '二级乙等',
                '一甲': '一级甲等',
                '专科': '专科医院'
            }

            if level_keyword in level_mapping:
                full_level = level_mapping[level_keyword]
                level_conditions.append("医院等级 = %s")
                level_params.append(full_level)
                level_conditions.append("医院等级 LIKE %s")
                level_params.append(f"%{full_level}%")

            # 组合等级条件（使用OR连接）
            if level_conditions:
                conditions.append(f"({' OR '.join(level_conditions)})")
                params.extend(level_params)

        if department and department.strip() and department.strip() != '':
            conditions.append("重点科室 LIKE %s")
            params.append(f"%{department.strip()}%")

        if location and location.strip() and location.strip() != '' and location.strip() != '当前位置':
            location_keyword = location.strip()

            # 优化地址搜索逻辑，支持多种匹配方式
            location_conditions = []
            location_params = []

            # 1. 直接匹配
            location_conditions.append("医院地址 LIKE %s")
            location_params.append(f"%{location_keyword}%")

            # 2. 如果是城市名，也尝试匹配省份
            city_to_province = {
                '大连': '辽宁',
                '沈阳': '辽宁',
                '北京': '北京',
                '上海': '上海',
                '广州': '广东',
                '深圳': '广东',
                '天津': '天津',
                '重庆': '重庆'
            }

            if location_keyword in city_to_province:
                province = city_to_province[location_keyword]
                location_conditions.append("医院地址 LIKE %s")
                location_params.append(f"%{province}%")

            # 3. 如果包含省市关键词，尝试提取核心地名
            if '省' in location_keyword or '市' in location_keyword:
                core_name = location_keyword.replace('省', '').replace('市', '').replace('自治区', '')
                if core_name and core_name != location_keyword:
                    location_conditions.append("医院地址 LIKE %s")
                    location_params.append(f"%{core_name}%")

            # 组合地址条件（使用OR连接）
            if location_conditions:
                conditions.append(f"({' OR '.join(location_conditions)})")
                params.extend(location_params)

        # 构建完整的SQL查询
        base_query = "SELECT 医院名称, 医院地址, 联系电话, 医院等级, 重点科室, 经营方式 FROM hospital_sum"

        # 计算分页偏移量
        offset = (page - 1) * pageSize

        if conditions:
            query = f"{base_query} WHERE {' AND '.join(conditions)} LIMIT {pageSize} OFFSET {offset}"
        else:
            query = f"{base_query} LIMIT {pageSize} OFFSET {offset}"

        print(f"执行查询: {query}")
        print(f"查询参数: {params}")

        cursor.execute(query, params)
        hospitals = cursor.fetchall()

        # 查询总数
        count_query = "SELECT COUNT(*) as total FROM hospital_sum"
        if conditions:
            count_query = f"{count_query} WHERE {' AND '.join(conditions)}"

        cursor.execute(count_query, params)
        total_count = cursor.fetchone()['total']

        print(f"找到 {len(hospitals)} 家医院，总共 {total_count} 家")

        # 确保返回的数据不为空
        if not hospitals:
            hospitals = []

        # 返回包含分页信息的数据
        return JSONResponse(content={
            "hospitals": hospitals,
            "total": total_count,
            "page": page,
            "pageSize": pageSize,
            "totalPages": (total_count + pageSize - 1) // pageSize
        })

    except mysql.connector.Error as e:
        print(f"数据库错误: {e}")
        # 返回空数据而不是抛出异常，避免前端报错
        return JSONResponse(content={
            "hospitals": [],
            "total": 0,
            "page": page,
            "pageSize": pageSize,
            "totalPages": 0
        })
    except Exception as e:
        print(f"查询医院时发生错误: {e}")
        # 返回空数据而不是抛出异常，避免前端报错
        return JSONResponse(content={
            "hospitals": [],
            "total": 0,
            "page": page,
            "pageSize": pageSize,
            "totalPages": 0
        })
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# 用户信息相关路由 - 使用更具体的路径避免路由冲突
@app.get("/api/user/{role}/{id}")
async def get_user_info(role: str, id: int):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="patient_information"
    )
    cursor = connection.cursor(dictionary=True)
    query = ("SELECT * FROM users WHERE id = %s AND role = %s")
    cursor.execute(query, (id, role))
    user_info = cursor.fetchone()
    cursor.close()
    connection.close()
    if user_info:
        return JSONResponse(content=user_info)
    else:
        raise HTTPException(status_code=404, detail="用户未找到")

@app.put("/api/user/{role}/{id}")
async def update_user_info(role: str, id: int, request: Request):
    data = await request.json()
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="patient_information"
    )
    cursor = connection.cursor()
    update_query = ("UPDATE users SET name = %s, username = %s, password = %s, phone = %s, email = %s WHERE id = %s AND role = %s")
    cursor.execute(update_query, (data['name'], data['username'], data['password'], data['phone'], data['email'], id, role))
    connection.commit()
    cursor.close()
    connection.close()
    return JSONResponse(content={"message": "用户信息更新成功"})

# 百度API访问令牌函数已移除


if __name__ == '__main__':
    import uvicorn
    print("🚀 启动医慧之翼后端服务...")
    print("📡 服务地址: http://127.0.0.1:8000")
    print("📋 API文档: http://127.0.0.1:8000/docs")
    print("=" * 50)
    uvicorn.run(app, host='127.0.0.1', port=8000)