from pydantic import BaseModel, Field


class CampaignBrief(BaseModel):
    brand: str = Field("Custom Brand", min_length=2)
    product: str = Field(..., min_length=2)
    audience: str = Field(..., min_length=2)
    goal: str = Field(..., min_length=2)
    budget: int = Field(..., gt=0)
    channel: str = Field(..., min_length=2)
    tone: str = Field(..., min_length=2)
    duration_days: int = Field(..., gt=0)
    cta: str = Field(..., min_length=2)

    def brief_summary(self):
        return self.model_dump()
