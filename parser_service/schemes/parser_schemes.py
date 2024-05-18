from pydantic import BaseModel
from typing import List, Dict, Optional


class ParseRequest(BaseModel):
    n_bars: int


class ParseResponse(BaseModel):
    status: str
    lost_exchanges: Optional[Dict[str, List[str]]] = None
