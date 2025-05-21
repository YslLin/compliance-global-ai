from fastapi import APIRouter

from cg_ai.controllers import compliance

root_api_router = APIRouter()
# v1
root_api_router.include_router(compliance.router)