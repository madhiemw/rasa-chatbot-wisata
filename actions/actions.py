from rasa_sdk.knowledge_base.storage import InMemoryKnowledgeBase
from rasa_sdk.knowledge_base.actions import ActionQueryKnowledgeBase
import json
import logging
import os
import random
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Action, Tracker, utils
from typing import DefaultDict, Text, Callable, Dict, List, Any, Optional
from collections import defaultdict
import requests
import json 


class ActionMyKB(ActionQueryKnowledgeBase):
    def __init__(self):
        # load knowledge base with data from the given file
        knowledge_base = InMemoryKnowledgeBase("knowledge_base_data.json")

        # overwrite the representation function of the hotel object
        # by default the representation function is just the name of the object
        knowledge_base.set_representation_function_of_object(
           "hotel", lambda obj: obj["name"] + " (" + obj["city"] + ")"
       )
        super().__init__(knowledge_base)

    #    utter_objects(text=f"Found the following objects of type '{object_type}':") 
    async def utter_objects(
        self,
        dispatcher: CollectingDispatcher,
        object_type: Text,
        objects: List[Dict[Text, Any]],   
    ):
        """
        Utters a response to the user that lists all found objects.

        Args:
            dispatcher: the dispatcher
            object_type: the object type
            objects: the list of objects
        """
        if objects:
            dispatcher.utter_message(
                text=f"ada nih beberapa yang ku inget :"
            )
            repr_function = await utils.call_potential_coroutine(
                self.knowledge_base.get_representation_function_of_object(object_type)
            )

            for i, obj in enumerate(objects, 1):
                dispatcher.utter_message(text=f"{i}: {repr_function(obj)}") 
        else:
            dispatcher.utter_message(
                text=f"ngga ketemu jawabannya'{object_type}'."
            )

class ActionFindHistory(Action):
    def name(self) -> Text:
        return "action_find_history"
   
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
                sender_id=( tracker.current_state())["sender_id"]
                id=tracker.sender_id
                url = f"https://skilled-hermit-69.hasura.app/api/rest/users/{id}"
                headers = {"content-type": "application/json"}
                response = requests.get(url=url, json="json", headers=headers)
                a = json.loads(response.content)
                i = len(a["memolive_feed"])
                c = 0
                tampung = []
                while c < i :
                    tampung.append(a["memolive_feed"][c]['lokasi_photo']['nama_lokasi']) 
                    c += 1
                finishing = list(dict.fromkeys(tampung))
                d = len(finishing)
                e = 0
                if i < 1 :
                    dispatcher.utter_message(text ="kamu belum pernah mengunjungi destinasa wisata manapun")
                else :
                    dispatcher.utter_message(text="berikut adalah tempat yang pernah kamu kunjungi")
                    while e < d :
                        (dispatcher.utter_message(text=f"{e}.{finishing[e]}"))
                        e+=1

class ActionFindHistoryDate(Action):
    def name(self) -> Text:
        return "action_find_history_date"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
                sender_id=( tracker.current_state())["sender_id"]
                id=tracker.sender_id
                url = f"https://skilled-hermit-69.hasura.app/api/rest/history/{id}"
                headers = {"content-type": "application/json"}
 
                response = requests.get(url=url, json="json", headers=headers)
                
                a = json.loads(response.content)
                i = len(a["memolive_feed"])
                c = 0
                tampung_tanggal = []
                tampung_lokasi = []
                while c < i :
                    tampung_lokasi.append(a["memolive_feed"][c]['lokasi_photo']['nama_lokasi']) 
                    tampung_tanggal.append(a["memolive_feed"][c]['tgl_posting'])
                    c += 1
                hitungan_print = 0 
                if i < 1 :
                    dispatcher.utter_message(text="kamu belum pernah mengunjungi destinasa wisata manapun")
                else:
                  while hitungan_print < i :
                    dispatcher.utter_message(text = "{hitungan_print}" "{tampung_lokasi[hitungan_print]} pada tanggal {tampung_tanggal[hitungan_print]}" ) 
                    hitungan_print += 1


