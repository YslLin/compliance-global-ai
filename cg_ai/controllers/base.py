from fastapi import APIRouter


def new_router(name: str, dependencies=None):
    router = APIRouter()
    router.tags = [name]
    router.prefix = f"/{name}/api/v1"
    # 将认证依赖项应用于所有路由
    if dependencies:
        router.dependencies = dependencies
    return router
