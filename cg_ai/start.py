import sys
import os
# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from cg_ai.controllers.asgi import app
from cg_ai.config import config

def main():
    import uvicorn
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = '%(asctime)s - %(levelname)s - %(message)s'
    log_config["formatters"]["default"]["fmt"] = '%(asctime)s - %(levelname)s - %(message)s'
    uvicorn.run(
        app,
        host=config.listen_host,
        port=config.listen_port,
        log_level=config.log_level,
        log_config=log_config,
    )


if __name__ == "__main__":
    main()