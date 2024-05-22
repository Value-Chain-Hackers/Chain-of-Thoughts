import panel as pn
import ollama
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain_community.llms.ollama import Ollama
from langchain_community.llms import OpenAIChat
from langchain_core.output_parsers.string import StrOutputParser
from langchain_core.output_parsers.json import JsonOutputParser
import pandas as pd
import json
from IPython.display import display, Markdown

pn.config.theme = 'dark'

def generate_response(contents: str, user: str, chat_interface: pn.chat.ChatInterface):
    chat_history = chat_interface.serialize(format="transformers",)
    response = ollama.chat(model='llama2', stream=True, messages=chat_history)
    message = ""
    for partial_resp in response:
        token = partial_resp["message"]["content"]
        message += token
        yield message

chat_interface = pn.chat.ChatInterface(callback=generate_response)
chat_interface.send("Hi! How can i help you?", user="System", avatar="🤖", respond=False)

chatbot = pn.Column(
    pn.pane.Markdown("# Llama2 🐪 Chatbot"),
    chat_interface,
    styles={"padding": "15px", 'border': '1px solid white',}
)



def load_graph(file):
    with open(file) as f:
        data = json.load(f)

    text = "```mermaid\ngraph LR\n"
    for item in data["links"]:
        text += f'\t{item["source"]} -- {item["value"]} --> {item["target"]}\n'
    text += "```"
    return text
text = load_graph("miserables_1.json")

graph_length = len(text)

print(f"Graph length: {graph_length}")

chatbot.servable()

# pip install panel watchfiles