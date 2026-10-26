from pydantic import AnyHttpUrl, BaseModel


class LinkCreate(BaseModel):
    url: AnyHttpUrl