RAG_SYSTEM_PROMPT = "You are a professional chatbot who can respond to questions from different fields in \"Traditional Chinese\". Each time you answer a question, please provide relevant references or sources to ensure your answer is both accurate and supported. Your response should be clear, concise, and relevant to the user's needs."

RAG_USER_PROMPT = """
# Reference_Data #
{Reference_Data}

# Question #
{User_Question}

# Instruction #
Refer to <Reference_Data> information to help you answer <User_Question> about citations on different topics. If the reference is not available or there is an uncertain answer, please reply "Sorry, your question is not in the provided data".

# Output Format #
Output the answer with JSON format. the keys of the JSON should be "Result" and "Reference_Data". The value of "Result" should be the answer to the user's question. The value of "Reference_Data" should be the title of the reference material in your response. 
"""

CHOSEN_TAGS_PROMPT = """
{User_Question}

{Tags_List}

# Instruction #
Read and analyze <User_Question> carefully and determine which <Tag> in <Tags_List> the problem may belong to. 
Do not answer the question in <User_Question>.

# Output Format #
Output the result in JSON format with keys \"tag_result\". The value of \"tag_result\" should be the tag that the problem belongs to. If the problem does not belong to any tag, please output \"None\" for \"tag_result\".
"""