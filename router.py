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

API_KEY = "VfiOrBcUm1TQZWzZQD9A9RRW"
SECRET_KEY = "4MCAqWnnJ1IHHtbW8qUJgoVHIBtbwWUX"

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
    if name and location and problem:
        hospital_info = get_hospital_info(location, problem)
        if hospital_info:
            hospital = hospital_info['医院名称']
            address = hospital_info['医院地址']
            phone = hospital_info['联系电话']
            level = hospital_info['医院等级']
            department = hospital_info['重点科室']
            operation = hospital_info['经营方式']
        else:
            hospital = "未知医院"
            address = "未知地址"
            phone = "未知电话"
            level = "未知等级"
            department = "未知科室"
            operation = "未知经营方式"
        
        prompt_template = (
            "请按照以下格式回答问题：\n"
            "问题：我叫{name}，现在在{location}，我的问题是{problem}\n"
            "回答：{name}您好，根据您的描述，为您推荐{location}附近的医院信息如下：\n"
            "医院名称：{hospital}\n"
            "医院地址：{address}\n"
            "联系电话：{phone}\n"
            "医院等级：{level}\n"
            "重点科室：{department}\n"
            "经营方式：{operation}\n"
            "根据{problem}我可以跟您xx建议\n"
            "示例：\n"
            "问题：我叫李四，现在在上海，我的头痛很严重\n"
            "回答：李四您好，根据您的描述，为您推荐上海附近的华山医院，地址：上海市乌鲁木齐中路12号，电话：021-52889999，等级：三级甲等，重点科室：神经内科，经营方式：公立。 根据头痛我可以跟您xx建议"
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