import threading
from cg_ai.controllers.base import new_router
from cg_ai.models.schema import PushInfo
from cg_ai.utils import utils

router = new_router("compliance")


@router.post("/push")
def push(push_info: PushInfo):
    from cg_ai.service import service

    company_info = service.get_company_info(push_info.customerId)
    file_info_list = service.get_file_info(push_info.examineId)
    if not company_info or not file_info_list:
        return utils.get_response(500, message="公司信息或文件信息不存在")

    # 创建线程执行合规检查
    thread = threading.Thread(
        target=service.compliance_file,
        args=(push_info.examineId, company_info, file_info_list)
    )
    thread.daemon = True  # 设置为守护线程，这样主程序退出时线程会自动结束
    thread.start()

    return utils.get_response(200, message="合规检查已启动")
