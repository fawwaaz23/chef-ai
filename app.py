# app.py
import os
import time
from typing import Optional
from dotenv import load_dotenv
import openai
import gradio as gr

load_dotenv()
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("Set OPENAI_API_KEY in your environment or .env file")
openai.api_key = OPENAI_API_KEY

# === Helper: system prompt that makes the assistant a helpful Chef AI ===
SYSTEM_PROMPT = """
You are Chef AI — a friendly, concise, and practical cooking assistant.
When given ingredients or a cooking question, return:
1) A short recipe title.
2) Ingredients list (quantities if possible).
3) Step-by-step instructions numbered.
4) Preparation + cook time estimate.
5) Serving size.
6) 2 quick tips or substitutions.
Be clear and concise. If the user gives dietary constraints (vegan, gluten-free), obey them.
If the user doesn't give ingredients but asks for ideas, propose 3 quick recipe options, each 1-2 sentences.
"""

def build_messages(user_text: str, context: Optional[list] = None):
    messages = [{"role":"system", "content": SYSTEM_PROMPT}]
    if context:
        messages.extend(context)
    messages.append({"role":"user", "content": user_text})
    return messages

def call_openai_chat(prompt_text: str, temperature: float = 0.6, max_tokens: int = 600):
    messages = build_messages(prompt_text)
    # You can change model to whichever chat model you have access to.
    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",   # replace with a model you have access to, e.g., "gpt-4o" or "gpt-4o-mini"
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
        n=1,
    )
    content = resp["choices"][0]["message"]["content"]
    return content

# === Gradio UI functions ===
def chef_chat(user_input, temperature):
    # Keep conversation simple: single-turn for now
    try:
        start = time.time()
        reply = call_openai_chat(user_input, temperature=float(temperature))
        took = time.time() - start
        return f"{reply}\n\n---\n(Generated in {took:.1f}s)"
    except Exception as e:
        return f"Error: {e}"

# === Optional: example prompts to show in UI ===
EXAMPLES = [
    "I have chicken breast, tomatoes, rice and spinach. Give me a 30-minute dinner recipe for two.",
    "I'm vegetarian and only have potatoes, onions, and chickpeas. Suggest 3 meal ideas.",
    "How do I make a quick tomato chutney to go with dosas?",
]

# === Build Gradio interface ===
with gr.Blocks(title="Chef AI — Recipe & Cooking Assistant") as demo:
    gr.Markdown("# 🍽️ Chef AI\nAsk for recipes, substitutions, or cooking tips. Example: \"What can I cook with chicken and rice?\"")
    with gr.Row():
        user_input = gr.Textbox(lines=4, placeholder="Type ingredients or ask a cooking question...", label="Your question")
        temperature = gr.Slider(minimum=0.0, maximum=1.0, value=0.6, label="Creativity (temperature)")
    with gr.Row():
        submit = gr.Button("Ask Chef AI")
    output = gr.Textbox(label="Chef AI response", lines=20)
    submit.click(chef_chat, inputs=[user_input, temperature], outputs=output)
    gr.Examples(EXAMPLES, inputs=user_input)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
