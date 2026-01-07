from datetime import datetime
from typing import Optional, Dict
from pydantic import BaseModel
import uuid

class Event(BaseModel):
    event_id: str
    event_type: str
    event_time: datetime
    user_id: Optional[str]
    session_id: str
    page_url: str
    element_id: Optional[str]
    metadata: Dict[str, str]

    @classmethod
    def from_payload(cls, payload: dict) -> "Event":
        raw = (
            payload["event_type"]
            + payload.get("user_id", "")
            + payload["session_id"]
            + payload["event_time"]
            + str(payload.get("metadata", {}))
        )

        event_id = str(uuid.uuid5(uuid.NAMESPACE_OID, raw))

        return cls(event_id=event_id, **payload)

    @property
    def event_date(self):
        return self.event_time.date()
