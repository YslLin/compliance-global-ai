from pydantic import BaseModel


class PushInfo(BaseModel):
    """
    推送信息
    """
    examineId: int
    customerId: int


class CompanyInfo(BaseModel):
    """
    公司信息
    """
    id: int
    name: str
    address: str | None = None
    phone: str | None = None
    email: str | None = None
    website: str | None = None


class FileInfo(BaseModel):
    """
    文件信息
    """
    id: int
    customerId: int
    examineId: int
    subjectId: int
    fileId: int
    fileUrl: str
    status: int
    resultDesc: str | None = None
    resultStatus: str | None = None 