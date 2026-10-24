from pydantic import BaseModel, AnyHttpUrl

class LinkCreate(BaseModel):
    url: AnyHttpUrl