"""Classes used within this project"""

import pydantic


class Advisor(pydantic.BaseModel):
    advisor_name: str
    personality_description: str
    llm_name: str

    @pydantic.field_validator("advisor_name")
    def valid_advisor_name(cls, v: str) -> str:
        v = v.strip()
        if not (2 <= len(v) <= 50):
            raise ValueError("Advisor name must be between 2 and 50 characters long")
        return v

    @pydantic.field_validator("personality_description")
    def valid_personality_description(cls, v: str) -> str:
        v = v.strip()
        if not (2 <= len(v) <= 500):
            raise ValueError(
                "Advisor personality description must be between 2 and 500 characters long"
            )
        return v

    @pydantic.field_validator("llm_name")
    def valid_llm_name(cls, v: str) -> str:
        v = v.strip()
        if not (6 <= len(v) <= 300):
            raise ValueError("LLM name must be between 6 and 300 characters long")
        return v
