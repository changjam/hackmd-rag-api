# hackmd-rag-api
> Connected with hackMD API, a simple chat bot for hackMD.


## Setup
* [Get Your HackMD token](https://hackmd.io/@hackmd-api/developer-portal/https%3A%2F%2Fhackmd.io%2F%40hackmd-api%2FrkoVeBXkq)
* [Get Your Groq token](https://console.groq.com/keys)
* Please obtain your tokens first, and then you can pass the token in request body.


### HackMD Setting
* Custom "tag" for your every note.
* Add "Private" tag to the notes if you want to hide it from client.


### Run
```bash
pip install -r requirements.txt
cd src/
python api.py
```

### Request
#### CURL
```bash
# healthy check
curl -X 'GET' \
  'http://localhost:8000/api/v1/ping' \
  -H 'accept: application/json'

# data_reset
curl -X 'DELETE' \
  'http://127.0.0.1:8000/api/v1/data_reset' \
  -H 'accept: application/json'

# rag_generate
curl -X 'POST' \
  'http://localhost:8000/api/v1/rag_generate' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "HackMD_API_TOKEN": "",
    "GROQ_API_TOKEN": "",
    "question": "",
    "model_id": "llama3-70b-8192"
    }'
```

### Response
```python
# ping
{
  "result": "alive"
}

# data_reset
{
  "result": "data reset"
}

# rag_generate
{
  "Result": "str",
  "Reference_Data": "str"
}
```
### Errors Response

#### NOTES_NOT_EXIST_ERROR
```python
JSONResponse({'result': 'NOTES_NOT_EXIST_ERROR'}, 400)
```
#### NO_RESULT_ERROR
```python
JSONResponse({'result': 'NO_RESULT_ERROR'}, 400)
```
#### INTERNAL_ERROR
```python
JSONResponse({'result': 'INTERNAL_ERROR'}, 500)
```
