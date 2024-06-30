import json
from json_repair import repair_json
import re




def get_xml_result(response: str, tags_name: str) -> str | None:
    try:
        pattern = re.compile(r'<{}>(.*?)</{}>'.format(tags_name, tags_name), re.DOTALL)
        match = pattern.search(response)
        if not match:
            print('Tag not found in the string.', tag='warning', tag_color='yallow', color='white')
            return None
        result = match.group(1).strip()
        return result
    except Exception as e:
        print(f"[get_xml_result Error]: return None :{e}", tag='failure', tag_color='red', color='magenta')
        return None


def get_json_result(output: str) -> dict | None:
    try:
        if output is None or output == '':
            return None
        return json.loads(repair_json(output))
    except Exception as e:
        print(f"[get_json_result Error]: return None", tag='failure', tag_color='red', color='magenta')
        return None


def LLM_catch_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"[LLM Error]: return None, {e}", tag='failure', tag_color='red', color='magenta')
            return None, None
    return wrapper