import gradio as gr
import modules.shared as shared
from duckduckgo_search import DDGS

import urllib
import html2text

search_access = True

def search_results(query):
    html = ""
    with DDGS() as ddgs:
        for r in ddgs.text(query, safesearch='off', timelimit='y', max_results=10):
            html = html + str(r) + "\n"
    return html

    driver = webdriver.Chrome(service=service,options=options)
    driver.set_page_load_timeout(3)
    html = ""
    output = ""
    h = html2text.HTML2Text()
    
    try:
        driver.get(url)
    except TimeoutException:
        driver.execute_script("window.stop();")
        try:
            h.ignore_links = True
            main_element = driver.find_element(By.CSS_SELECTOR, "[id~='content']")
            html += h.handle(main_element.get_attribute('innerHTML')) if main_element.text else ""
        except NoSuchElementException:
            try:
                content_element = driver.find_element(By.CSS_SELECTOR, "[class~='content']")
                html += h.handle(content_element.get_attribute('innerHTML')) if content_element.text else ""
            except NoSuchElementException:
                try:
                   content_element = driver.find_element(By.TAG_NAME, "main")
                   html += h.handle(content_element.get_attribute('innerHTML')) if content_element.text else ""
                except NoSuchElementException:
                    pass
    except NoSuchElementException as e:
        pass
    
    output = html
    driver.quit()
    return output

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
        search_query = re.search(r'search\s+"([^"]+)"', user_input, re.IGNORECASE)

        if search_query:
            query = search_query.group(1)
        elif user_input.lower().startswith("search"):
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
