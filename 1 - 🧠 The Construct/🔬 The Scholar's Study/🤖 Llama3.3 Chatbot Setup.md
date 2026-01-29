# 🤖 Llama3.3 Chatbot Setup
> *Protocol for deploying the DavidAU/Llama3.3-8B-Instruct-Thinking-Claude-4.5-Opus-High-Reasoning model via Colab/Gradio.*

---

## 📋 The Protocol

This script sets up a local or cloud-based server for the **Llama3.3-8B** model, utilizing **Gradio** for the interface and **Ngrok** for public access.

> [!warning] Dependencies
> Requires a GPU environment (e.g., Google Colab T4).

### 🛠️ Python Implementation

```python
# 1. Install necessary libraries
!pip install -q torch gradio transformers accelerate huggingface_hub pyngrok

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import gradio as gr
from pyngrok import ngrok

# 2. Configuration
# Model: DavidAU/Llama3.3-8B-Instruct-Thinking-Claude-4.5-Opus-High-Reasoning
model_id = 'DavidAU/Llama3.3-8B-Instruct-Thinking-Claude-4.5-Opus-High-Reasoning'
ngrok_token = "2fqsHp5dfyGOlPwj0EZCZcNj9r9_6vpw6GDD2TGCveJSutcpM" # Replace if needed

# 3. Load Model & Tokenizer (Approx 5-10 mins)
print("⏳ Loading Model...")
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.float16, # Reduces memory usage
    device_map="auto",
    low_cpu_mem_usage=True
)
pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)

# 4. Response Generation Logic
def generate_response(message, history):
    # Format prompt for the model
    prompt = f"USER: {message}\nASSISTANT: "
    
    # Generate output
    outputs = pipe(
        prompt, 
        max_new_tokens=256, 
        do_sample=True, 
        temperature=0.7, 
        top_p=0.95
    )
    
    generated_text = outputs[0]['generated_text']
    # Extract response
    response = generated_text.split("ASSISTANT: ")[-1]
    return response

# 5. Gradio Interface
demo = gr.ChatInterface(
    fn=generate_response,
    title="🤖 Llama3.3 High-Reasoning Chatbot",
    description="Running DavidAU/Llama3.3-8B-Instruct-Thinking-Claude-4.5-Opus-High-Reasoning",
    theme="soft"
)

# 6. Launch Server
print("🚀 Starting server...")
ngrok.set_auth_token(ngrok_token)
public_url = ngrok.connect(7860)
print(f"✅ Public URL: {public_url.public_url}")

demo.launch(share=False, server_name="0.0.0.0", server_port=7860)
```

---
#ai #llm #python #colab #automation
