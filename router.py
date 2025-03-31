from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import requests
import json
import mysql.connector
from decimal import Decimal

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
        return JSONResponse(content={"code": 200, "role": role, "message": "登录成功", "id": user["id"]})
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

@app.get("/{role}/{id}")
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

@app.put("/{role}/{id}")
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

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    message = data.get('message')
    name = data.get('name')
    location = data.get('location')
    problem = data.get('problem')
    response = get_response(message, name, location, problem)
    return JSONResponse(content={"response": response})

@app.post("/submit")
async def submit(request: Request):
    form_data = await request.json()
    save_to_database(form_data)
    return JSONResponse(content={"message": "表单提交成功", "data": form_data})

def save_to_database(form_data):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="patient_information"
    )
    cursor = connection.cursor()
    add_form_data = ("INSERT INTO patient_information"
                     "(name, location, problem) "
                     "VALUES (%s, %s, %s)")
    

    data_form = (form_data['name'], form_data['location'], form_data['problem'])
    cursor.execute(add_form_data, data_form)
    connection.commit()
    cursor.close()
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

def get_response(message, name, location, problem):
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token=" + get_access_token()
    
    # 检查是否为急症
    emergency_keywords = ["急症", "晕倒", "休克", "大出血", "呼吸困难", "胸痛", "抽搐", "剧烈疼痛"]
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
        
        emergency_notice = "【注意】您描述的症状可能是急症，建议立即前往最近医院急诊科就诊，或拨打120急救电话！\n\n" if is_emergency else ""

        prompt_template = (
            "你是一位专业的医疗咨询助手，请根据用户提供的信息，给出专业、准确的医院推荐和健康建议。\n\n"
            f"{emergency_notice}"
            "规则说明：\n"
            "1. 回答必须简洁明了，包含所有医院信息\n"
            "2. 提供针对患者症状的专业就医建议\n"
            "3. 语气要亲切专业\n"
            "4. 不要提供任何诊断，只提供就医建议\n"
            "5. 不要改变或添加医院的实际信息\n\n"
            
            "用户信息：\n"
            "姓名：{name}\n"
            "位置：{location}\n"
            "症状/问题：{problem}\n\n"
            
            "医院信息：\n"
            "医院名称：{hospital}\n"
            "医院地址：{address}\n"
            "联系电话：{phone}\n"
            "医院等级：{level}\n"
            "重点科室：{department}\n"
            "经营方式：{operation}\n\n"
            
            "请回复格式如下：\n"
            "{name}您好，根据您的描述，为您推荐{location}附近的医院信息如下：\n"
            "医院名称：{hospital}\n"
            "医院地址：{address}\n"
            "联系电话：{phone}\n"
            "医院等级：{level}\n"
            "重点科室：{department}\n"
            "经营方式：{operation}\n\n"
            "针对您的问题\"{problem}\"，我的建议是：\n"
            "[此处提供2-3条针对性的就医建议，如建议就诊科室、就医前准备、注意事项等]"
        )

        
        prompt = prompt_template.format(
            name=name, 
            location=location, 
            problem=problem, 
            hospital=hospital, 
            address=address, 
            phone=phone, 
            level=level, 
            department=department, 
            operation=operation
        )
    else:
        prompt = message
    
    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, data=payload)
    return response.json()["result"]


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

def get_access_token():
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)