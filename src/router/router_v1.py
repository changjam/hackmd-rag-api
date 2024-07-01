from PyHackMD import API
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema.document import Document

from tools.lib import *
from tools.prompt_lib import RAG_SYSTEM_PROMPT, RAG_USER_PROMPT, CHOSEN_TAGS_PROMPT
from tools.data import get_notes_list, get_notes_content_by_tag, clear_json_files
from tools.get_result import get_json_result
from tools import format_docs, convert_str_to_xml, catch_error


router = APIRouter(prefix="/api/v1", tags=['v1'])


@router.get("/ping")
def ping():
    return JSONResponse(content={"result": "alive"}, status_code=200)

@router.delete("/data_reset")
def delete_data():
    data_folder_list = ['db/', 'notes/']
    for data_folder in data_folder_list:
        clear_json_files(data_folder)

    return JSONResponse(content={"result": "data reset"}, status_code=200)

@api_catch_error
@router.post("/rag_generate")
def generate(data: data_format) -> JSONResponse:
    global CHOSEN_TAGS_PROMPT
    hackmd_api_token = data.HackMD_API_TOKEN
    groq_api_token = data.GROQ_API_TOKEN
    question = data.question
    model_id = data.model_id

    hackmd_api_instance = API(hackmd_api_token)
    groq_llm_instance = ChatGroq(
                            temperature= 0.8,
                            model=model_id,
                            api_key=groq_api_token
                        )
    
    note_content_list: str | Errors = get_content(hackmd_api_instance, groq_llm_instance, question)

    if isinstance(note_content_list, Errors):
        return note_content_list

    response = answer_question(groq_llm_instance, question, note_content_list)

    return JSONResponse(content=response, status_code=200)




# method
@catch_error
def get_content(hackmd_api_instance, groq_llm_instance, question) -> list | Errors:
    # 1. get notes list
    note_list_data: list = get_notes_list(hackmd_api_instance)

    if len(note_list_data) == 0:
        return Errors.NOTES_NOT_EXIST_ERROR

    question_xml = f'<User_Question>{question}</User_Question>'

    tags_list = []
    for note in note_list_data:
        tags_list.extend(note['tags'])
    tags_list = list(set(tags_list))

    tags_list_xml = ''
    for tag in tags_list:
        tags_list_xml += f'<Tag>{tag}</Tag>\n'
    tags_list_xml = f'<Tags_List>{tags_list_xml}</Tags_List>'


    # 2. LLM chosen tags
    prompt = CHOSEN_TAGS_PROMPT.format(User_Question=question_xml, Tags_List=tags_list_xml)
    messages = [("human", prompt)]
    tag_response = groq_llm_instance.invoke(messages)


    # 3. get notes content by tag
    tag_result = get_json_result(tag_response.content)['tag_result']
    notes_content_list: list = get_notes_content_by_tag(hackmd_api_instance, note_list_data, tag_result)

    if notes_content_list == None or len(notes_content_list) == 0:
        return Errors.NOTES_NOT_EXIST_ERROR
        
    return notes_content_list


@catch_error
def answer_question(groq_llm_instance: str, question: str, note_content_list: list[dict]) -> str:
    def get_text_chunks_langchain(text):
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            model_name="gpt-4",
            chunk_size=600,
            chunk_overlap=100,
        )
        return [ Document(page_content=x) for x in text_splitter.split_text(text) ]

    # 1. Split texts into chunks
    chunk_list = []
    for note_content in note_content_list:
        page_content = note_content['title'] + '\n' + note_content['content']
        chunk_list.extend(get_text_chunks_langchain(page_content))


    # 2. Create FAISS index
    embedding_path = 'GanymedeNil/text2vec-large-chinese'
    embeddings = HuggingFaceEmbeddings(model_name=embedding_path)
    docsearch = FAISS.from_documents(chunk_list, embeddings)
    retriever = docsearch.as_retriever()


    # 3. Create chain and invoke
    prompt_template = ChatPromptTemplate.from_messages(
        [("system", RAG_SYSTEM_PROMPT), ("human", RAG_USER_PROMPT)]
    )
    # 用 | 分割不同步驟，將前面步驟的輸出作為後面步驟的輸入
    chain = (
        {"Reference_Data": retriever | format_docs | (lambda x: convert_str_to_xml(x, "Reference_Data")), "User_Question": RunnablePassthrough() | (lambda x: convert_str_to_xml(x, "User_Question")) } |
        prompt_template |
        groq_llm_instance | 
        StrOutputParser()
    )

    response = chain.invoke(question)

    result = get_json_result(response)
    return result