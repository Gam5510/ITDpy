from pydantic import BaseModel, ConfigDict

class ITDBaseModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
