import requests
import gradio as gr

OLLAMA = "http://127.0.0.1:11434"
MODEL = "llama3.2:3b"

SYSTEM = """You are a high-school coding tutor.
Help students understand concepts and debug code.
Do NOT complete graded assignments.
Give hints and explanations instead of full solutions.
"""

def ollama_chat(messages):
    r = requests.post(
        f"{OLLAMA}/api/chat",
        json={"model": MODEL, "messages": messages, "stream": False},
        timeout=120
    )
    r.raise_for_status()
    return r.json()["message"]["content"]

def reply(message, history):
    msgs = [{"role":"system","content":SYSTEM}]
    for u,a in history:
        msgs.append({"role":"user","content":u})
        if a:
            msgs.append({"role":"assistant","content":a})
    msgs.append({"role":"user","content":message})
    return ollama_chat(msgs)

with gr.Blocks() as demo:
    gr.Markdown("# 🧑‍🏫 Coding Trainer Chatbot")
    chat = gr.ChatInterface(reply)

if __name__ == "__main__":
    demo.launch()
