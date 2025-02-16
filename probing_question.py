# This code block is for static questions.

# def generate_probing_questions():
#     """Returns probing questions to refine user requests."""
#     return [
#         "Which specific metrics are you interested in?",
#         "What time frame should the report cover?",
#         "Is this for a specific department/team?",
#         "Do you need a high-level summary or a detailed breakdown?"
#     ]

# This code block is generating questions with the help of LLM.

import requests
import ast
from config import LLM_API_KEY, LLM_API_URL

LLM_API_URL =  LLM_API_URL
LLM_API_KEY = LLM_API_KEY

def generate_probing_questions(user_query):
    """Generates contextual probing questions using LLM based on user's report request."""
    
    prompt = f"""
    [INST]You are an intelligent analytics assistant. Given a user request for a report: "{user_query}",\ngenerate 4 contextually relevant probing questions to refine the request.\nThe questions should help clarify:\n- Specific metrics required\n- Time frame\n- Department or team focus\n- Level of detail (high-level summary or detailed breakdown)\n\nReturn the questions as a Python list.[INST]
    """
    
    headers = {
        "Authorization": f"Bearer {LLM_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
    "model": "Qwen/Qwen2.5-72B-Instruct",
    "messages": [
		{
            "role":"user",
			"content":prompt
		}
	],
    "return_full_text":False,
    "temperature":0.9,
    "max_new_tokens":2048,
    "top_p": 0.9,
    "do_sample": True,
    "stream": False
   }
    
    response = requests.post(LLM_API_URL, json=data, headers=headers)
    response_json = response.json()
    message_content = response_json.get("choices", [{}])[0].get("message", {}).get("content", "")

    # Removing Python code block delimiters
    if message_content.startswith("```python"):
        message_content = message_content[9:]  # Remove starting ```python
    if message_content.endswith("```"):
        message_content = message_content[:-3]  # Remove ending ```

    try:
        # Converting the string into a Python list safely
        probing_questions = ast.literal_eval(message_content.strip())
        return probing_questions if isinstance(probing_questions, list) else []
    except (SyntaxError, ValueError):
        return ["Failed to generate valid questions. Please refine your query."]
