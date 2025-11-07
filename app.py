# ✅ Chef AI - working with new OpenAI SDK
from openai import OpenAI
import gradio as gr
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Function that creates a response from AI
def chef_ai(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a master chef AI assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# Gradio UI
demo = gr.Interface(
    fn=chef_ai,
    inputs=gr.Textbox(label="Enter ingredients or ask a recipe"),
    outputs="text",
    title="👨‍🍳 Chef AI",
    description="Ask Chef AI for recipes, cooking tips, or meal ideas!"
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=10000)
