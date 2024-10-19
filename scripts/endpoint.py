from typing import Any, Dict, List, Literal, Union

from choices import ACTIONS, PREDICATE
from fastapi import FastAPI, Response
from pydantic import BaseModel, RootModel


class Rules(BaseModel):
    Field: Literal["From", "To", "Subject", "Date"]
    value: str
    predicte: Literal["contains", "does_not_contain", "less_than", "greater_than"]


class PredictRules(BaseModel):
    conditions: List[Rules]
    rule: str


class Action(RootModel[Dict[str, Union[None, List[str], Any]]]):
    # Accept any key-value pairs
    @classmethod
    def validate(
        cls, value: Dict[str, Union[None, List[str], Any]]
    ) -> Dict[str, Union[None, List[str], Any]]:
        # Check if the keys in the dictionary are in the allowed keys list
        invalid_keys = [key for key in value.keys() if key not in ACTIONS]
        if invalid_keys:
            raise ValueError(
                f"Invalid keys: {', '.join(invalid_keys)}. Allowed keys are: {', '.join(ACTIONS)}"
            )
        return value


# Define the main model for the entire request structure
class RuleSet(BaseModel):
    predict: PredictRules
    action: Action


app = FastAPI()


@app.post("/")
async def root(item: RuleSet, response: Response):
    try:
        print(item.dict())
        temp_item = item.dict()
        for i in temp_item["predict"]["conditions"]:
            i["predicte"] = PREDICATE[i["predicte"]]
        print(temp_item)
        from actions_on_email import GmailMessagesActions

        g = GmailMessagesActions()
        g.take_actions(temp_item)
        status_message = "success"
        response_message = {"status": status_message}

    except Exception as exc:
        status_message = "error"
        message = str(exc)
        response_message = {"status": status_message, "message": message}
        response.status_code = 404

    return response_message
