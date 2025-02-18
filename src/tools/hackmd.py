import os
import json
import time
import pytz
from datetime import datetime




def isPrivate(tags: list) -> bool:
    return 'Private' in tags

def isExpire(last_save_time: float, limit_time_minute: int) -> bool:
    if not last_save_time:
        return True
    limit_time_seconds = limit_time_minute * 60
    current_timestamp: float = time.time()
    return (current_timestamp - last_save_time) > limit_time_seconds

def update(hackmd_api_instance, note_list_data: list) -> tuple[list, float]:
    new_note_list_data: list = hackmd_api_instance.get_note_list()
    remove_diff_notes(new_note_list_data, note_list_data)
    write_note_list_data(new_note_list_data)
    current_timestamp = time.time()
    return new_note_list_data, current_timestamp

def get_note_list_data(hackmd_api_instance) -> list:
    try:
        local_path: str = 'db/note_list_data.json'
        if not os.path.exists(local_path):
            return hackmd_api_instance.get_note_list()
        with open(local_path, 'r', encoding='utf-8') as note_list_data:
            return json.load(note_list_data)
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def write_note_list_data(new_data: list) -> None:
    local_path: str = 'db/note_list_data.json'
    if not os.path.exists(local_path):
        with open(local_path, 'w', encoding='utf-8') as note_list_data:
            json.dump(new_data, note_list_data)

def remove_diff_notes(new_data: list, old_data: list) -> None:
    old_data_dict: dict = {item["id"]: item for item in old_data}
    new_data_dict: dict = {item["id"]: item for item in new_data}

    for old_id, old_item in old_data_dict.items():
        new_item = new_data_dict.get(old_id)
        if new_item is None or old_item != new_item:
            remove_local_note_data(f'notes/{old_id}.json')

def get_note_data(hackmd_api_instance, data_path: str, nid: str) -> list:
    if not os.path.exists(data_path):
        return hackmd_api_instance.get_note(nid)
    with open(data_path, 'r', encoding='utf-8') as note_data:
        return json.load(note_data)

def write_note_data(data_path: str, new_data: list) -> None:
    if not os.path.exists(data_path):
        with open(data_path, 'w', encoding='utf-8') as note_data:
            json.dump(new_data, note_data)

def set_note_data(data: dict):
    dt_object = datetime.fromtimestamp(data['lastChangedAt'] / 1000)
    yyyymmdd_date = dt_object.strftime('%Y-%m-%d')

    note_data = {}
    note_data['id'] =  data['id']
    note_data['title'] = data['title']
    note_data['tags'] = data['tags'][0]
    note_data['content'] = data['content']
    note_data['lastUpdate'] = str(yyyymmdd_date)
    return note_data

def remove_local_note_data(data_path: str) -> None:
    if os.path.exists(data_path):
        os.remove(data_path)

def get_notes_id_list(data: list) -> set:
    id_list = []
    for note in data:
        if note['tags'] and not isPrivate(note['tags']): id_list.append(note['id'])
    return set(id_list)

def check_notes_id_exist(hackmd_api_instance, note_id: str) -> bool:
    note_list_data = get_note_list_data(hackmd_api_instance)
    note_id_list = get_notes_id_list(note_list_data)
    return note_id in note_id_list