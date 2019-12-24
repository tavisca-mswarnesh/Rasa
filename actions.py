# This files contains your custom actions which can be used to run
# custom Python code.

# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List, Union
from rasa_sdk.events import SlotSet
from rasa_sdk import Action, Tracker 
from rasa_sdk.forms import FormAction
from rasa_sdk.executor import CollectingDispatcher
import requests
import json

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_greet"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("Working")
        dispatcher.utter_message(text="This is from action.py")

        return []
class ActionJoke(Action):

    def name(self) -> Text:
        return "action_joke"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        url="https://api.chucknorris.io/jokes/random"
        response=requests.get(url)
        print(json.loads(response.text))
        dispatcher.utter_message(text=json.loads(response.text)["value"])

        return []


class Testing(FormAction):
    def name(self) -> Text:
        return "restaurant_form"
    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["cuisine"]

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any],) -> List[Dict]:
        dispatcher.utter_message(template="utter_submit")
        return []
    @staticmethod
    def cuisine_db() -> List[Text]:
        return [
            "caribbean",
            "chinese",
            "french",
            "greek",
            "indian",
            "italian",
            "mexican",
        ]
    def validate(self,dispatcher,tracker,domain):
        value:str=tracker.get_slot("cuisine")
        print(value)
    
        if value and value.lower() in self.cuisine_db():
            dispatcher.utter_message("Success")
            return [SlotSet("cuisine",value)]
        else:
            dispatcher.utter_template("utter_wrong_cuisine",tracker)
            return [SlotSet("cuisine",None)]
