import gradio as gr
import modules.shared as shared
from duckduckgo_search import DDGS

import urllib

search_access = True

def search_results(query):
    html = ""
    with DDGS() as ddgs:
        for r in ddgs.text(query, safesearch='off', timelimit='y', max_results=10):
            html = html + str(r) + "\n"
    return html


def ui():
    global search_access
    checkbox = gr.Checkbox(value=search_access, label="Enable DuckDuckGo Search")
    checkbox.change(fn=update_search_access, inputs=checkbox)
    return checkbox, search_access


def update_search_access(checkbox_value):
    global search_access
    search_access = checkbox_value  # assign the value of the checkbox to the variable
    return search_access, checkbox_value


def input_modifier(user_input, state):
    global search_access
    if search_access:
        if user_input.lower().startswith("search"):
            shared.processing_message = "*Searching online...*"
            query = user_input.replace("search", "").strip()
            state["context"] = state["context"] + "Relevant search results are in the DuckDuckGo search results. Use this info in the response."
            search_data = search_results(query)
            user_prompt = f"User question: {user_input}\nDuckDuckGo search results: {search_data}"
            return str(user_prompt)               
    shared.processing_message = "*Typing...*"
    return user_input


def output_modifier(output):
    return output


def bot_prefix_modifier(prefix):
    return prefix
