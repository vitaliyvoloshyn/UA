from pydantic import BaseModel


class ResultContent(BaseModel):
    header: str = 'Сплата рахунків'
    message_operation: str = ''
    back_ref: str = ''
    back_ref_text: str = ''


class ErrorResultContent(ResultContent):
    status_operation: str = 'ПОМИЛКА!'
    color: str = 'red'
    image: str = 'static/asset/img/404-error-3060993_1280.webp'


class SuccessResultContent(ResultContent):
    status_operation: str = 'УСПІХ!'
    color: str = 'green'
    image: str = 'static/asset/img/follow-up.png'
