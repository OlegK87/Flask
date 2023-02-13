from pydantic import BaseModel
from pydantic import ValidationError
from errors import HttpError

class CreateAdvertisement(BaseModel):
    header: str
    description: str
    owner: int

def validate_create_advertisement(json_data):
    try:
        advertisement_schema = CreateAdvertisement(**json_data)
        return advertisement_schema.dict()
    except ValidationError as er:
        raise HttpError(status_code=400, message=er.errors())
