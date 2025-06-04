# 医慧之翼系统配置文件
import os
from typing import Optional

class Config:
    """系统配置类"""

    # 数据库配置
    DATABASE_CONFIG = {
        "host": "localhost",
        "user": "root",
        "password": "root",
        "database": "patient_information"
    }

    # AI服务配置
    class AIConfig:
        # 智谱AI配置
        ZHIPU_API_KEY: Optional[str] = "84d4ce6022864ede852bd018d8db3630.GVPTAKK9RqkoXxMc"
        ZHIPU_URL: str = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
        ZHIPU_MODEL: str = "glm-4"

        @classmethod
        def is_zhipu_available(cls) -> bool:
            """检查智谱AI是否可用"""
            return cls.ZHIPU_API_KEY is not None and cls.ZHIPU_API_KEY != "" and cls.ZHIPU_API_KEY != "your_zhipu_api_key_here"

        @classmethod
        def get_primary_ai(cls) -> str:
            """获取主要AI服务"""
            return "zhipu" if cls.is_zhipu_available() else "baidu"

    # 系统配置
    class SystemConfig:
        # 服务器配置
        HOST: str = "127.0.0.1"
        PORT: int = 8000
        DEBUG: bool = True

        # 安全配置
        SECRET_KEY: str = "your-secret-key-here"

        # 文件上传配置
        MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
        ALLOWED_EXTENSIONS: set = {'.jpg', '.jpeg', '.png', '.gif', '.pdf', '.doc', '.docx'}

        # 日志配置
        LOG_LEVEL: str = "INFO"
        LOG_FILE: str = "app.log"

    # 医疗相关配置
    class MedicalConfig:
        # 急症关键词
        EMERGENCY_KEYWORDS: list = [
            "急症", "晕倒", "休克", "大出血", "呼吸困难",
            "胸痛", "抽搐", "剧烈疼痛", "心脏病发作", "中风",
            "严重外伤", "窒息", "昏迷", "高烧不退", "严重过敏"
        ]

        # 常见症状分类
        SYMPTOM_CATEGORIES: dict = {
            "呼吸系统": ["咳嗽", "气喘", "胸闷", "呼吸困难", "咳痰"],
            "消化系统": ["腹痛", "恶心", "呕吐", "腹泻", "便秘", "胃痛"],
            "神经系统": ["头痛", "头晕", "失眠", "记忆力下降", "注意力不集中"],
            "心血管系统": ["胸痛", "心悸", "气短", "水肿", "高血压"],
            "骨骼肌肉": ["关节痛", "肌肉痛", "腰痛", "颈椎痛", "运动受限"],
            "皮肤": ["皮疹", "瘙痒", "红肿", "脱皮", "色素沉着"],
            "其他": ["发热", "乏力", "体重变化", "食欲不振", "多饮多尿"]
        }

        # 医院等级
        HOSPITAL_LEVELS: list = ["三甲", "三乙", "二甲", "二乙", "一甲", "一乙"]

        # 科室分类
        DEPARTMENTS: list = [
            "内科", "外科", "妇产科", "儿科", "眼科", "耳鼻喉科",
            "口腔科", "皮肤科", "神经科", "精神科", "康复科", "中医科",
            "急诊科", "ICU", "麻醉科", "影像科", "检验科", "药剂科"
        ]

# 配置实例
config = Config()

# 便捷访问
ai_config = Config.AIConfig()
system_config = Config.SystemConfig()
medical_config = Config.MedicalConfig()

def get_ai_service_status():
    """获取AI服务状态"""
    return {
        "zhipu_available": ai_config.is_zhipu_available(),
        "primary_service": ai_config.get_primary_ai(),
        "zhipu_api_key_configured": bool(ai_config.ZHIPU_API_KEY),
        "baidu_configured": True  # 百度配置是硬编码的
    }

def print_config_status():
    """打印配置状态"""
    print("=" * 50)
    print("医慧之翼系统配置状态")
    print("=" * 50)

    # AI服务状态
    ai_status = get_ai_service_status()
    print(f"🤖 AI服务状态:")
    print(f"   智谱AI: {'✅ 可用' if ai_status['zhipu_available'] else '❌ 不可用'}")
    print(f"   百度文心一言: ✅ 可用")
    print(f"   主要服务: {ai_status['primary_service'].upper()}")

    # 数据库状态
    print(f"\n💾 数据库配置:")
    print(f"   主机: {Config.DATABASE_CONFIG['host']}")
    print(f"   数据库: {Config.DATABASE_CONFIG['database']}")

    # 系统配置
    print(f"\n⚙️ 系统配置:")
    print(f"   服务地址: {system_config.HOST}:{system_config.PORT}")
    print(f"   调试模式: {'✅ 开启' if system_config.DEBUG else '❌ 关闭'}")

    print("=" * 50)

if __name__ == "__main__":
    print_config_status()
