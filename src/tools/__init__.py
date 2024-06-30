import traceback

def catch_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            traceback.print_exc()
            print(f'[Exception Error] {e}')
            return None
    return wrapper

@catch_error
def format_docs(docs: list) -> str:
    return "\n\n".join([d.page_content for d in docs])

@catch_error
def convert_str_to_xml(text: str, tag: str) -> str:
    return f"<{tag}>{text}</{tag}>"