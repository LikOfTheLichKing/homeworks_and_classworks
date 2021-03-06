from pydantic import BaseModel, Field


class CreationSurveyModel(BaseModel):
    name: str = Field(min_length=3, max_length=25)
    description: str = Field(max_length=300)
    answers: list[str] = Field(min_items=2)
    privacy: int


class SurveyModel(BaseModel):
    name: str
    description: str
    creator_name: str
    answers_and_statistic: dict
    privacy: int
