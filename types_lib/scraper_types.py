from typing import List, Optional
from pydantic import BaseModel


class ScraperInputType(BaseModel):
    apps: List[str]


class ScraperResponse(BaseModel):
    app: str
    category: Optional[str] = None
    distraction_value: Optional[int] = None

# ---- request body model ----
class GenresRequest(BaseModel):
    apps: List[str]


# ---- response ----
class GenresResponse(BaseModel):
    results: List[ScraperResponse]
