from tools import catch_error
from tools.hackmd import (get_note_list_data, 
                        write_note_list_data,
                        get_note_data,
                        write_note_data,
                        set_note_data,
                        isPrivate,
                        check_notes_id_exist)

@catch_error
def get_notes_list(hackmd_api_instance) -> list | None:
    note_list_data: list = get_note_list_data(hackmd_api_instance)
    write_note_list_data(note_list_data)

    filter_note_list_data = []
    for note in note_list_data:
        if not note['tags']:
            continue
        if isPrivate(note['tags']):
            continue
        filter_note_list_data.append(note)
    
    # check result
    if not filter_note_list_data or len(filter_note_list_data) == 0:
        return None

    return filter_note_list_data

def get_notes_content_by_tag(hackmd_api_instance, note_list_data: list, tag: str) -> list:
    if tag == 'None':
        # get all
        id_list = [note_data['id'] for note_data in note_list_data]
    else:
        # get by tag
        id_list = [note_data['id'] for note_data in note_list_data if tag in note_data['tags']]
    
    notes_content_list = []
    for id in id_list:
        note = get_note_by_id(hackmd_api_instance, id)
        notes_content_list.append(note)
    
    return notes_content_list


def get_note_by_id(hackmd_api_instance, nid):
    data_path: str = f'notes/{nid}.json'

    # check nid exist
    if not check_notes_id_exist(hackmd_api_instance, nid):
        return None

    # check path exist
    note_data = get_note_data(hackmd_api_instance, data_path, nid)
    write_note_data(data_path, note_data)
    result = set_note_data(note_data)

    # check result
    if len(result) == 0: 
        return None

    return result