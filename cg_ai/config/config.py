import os


log_level = os.getenv("log_level", "debug")
listen_host = os.getenv("listen_host", "0.0.0.0")
listen_port = os.getenv("listen_port", 8000)
project_name = os.getenv("project_name", "compliance-global-ai")
project_description = os.getenv(
    "project_description",
    "<a href='https://github.com/'>https://github.com/</a>",
)
project_version = os.getenv("project_version", "1.0.0")


file_check = {
    "0": ["name_check"],
    "1": ["name_check", "valid_period_check"],
}

java_api = {
    "base_url": "http://localhost:8080",
    # 获取公司信息
    "get_company_info": "/customer/infoById",
    # 获取文件信息
    "get_file_info": "/cus/examine/fileList",
    # 保存合规结果
    "save_compliance_result": "/cus/examine/saveFileResultList",
}