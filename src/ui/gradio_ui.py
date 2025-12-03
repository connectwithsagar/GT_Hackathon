import gradio as gr
from src.app_logic import chat

def gradio_chat(username, message):
    return chat(username, message)

with gr.Blocks(theme="gradio/soft") as ui:
    gr.Markdown("# 🛍️ Context Retail AI Assistant\nSmarter Recommendations Based on Preferences + Memory")

    with gr.Row():
        with gr.Column(scale=1):
            username = gr.Textbox(
                label="Customer Name",
                placeholder="e.g., Aditya, Aditi, Sai, Aarav...",
                scale=1
            )

            message = gr.Textbox(
                label="Message",
                placeholder="Type something like: 'It's cold today' or 'I prefer latte'",
                lines=3,
                scale=1
            )

            submit = gr.Button("Submit", variant="primary")

        with gr.Column(scale=2):
            output = gr.Textbox(
                label="💬 Assistant Response",
                lines=8,
                interactive=False,
                show_copy_button=True,
                scale=2
            )

    submit.click(fn=gradio_chat, inputs=[username, message], outputs=output)

if __name__ == "__main__":
    ui.launch()
