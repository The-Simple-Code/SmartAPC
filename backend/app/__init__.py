"""
SmartAPC Flask App Factory (stub)
"""
from flask import Flask

def create_app(config_name: str = "development"):
    app = Flask(__name__)
    # NOTE: 실제 설정/확장/블루프린트 등록은 이후 단계에서 추가
    return app
