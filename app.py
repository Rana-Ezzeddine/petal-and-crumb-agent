"""Gradio entry point for the Petal & Crumb Atelier assistant."""

import gradio as gr

from core_bot import chatbot


THEME = gr.themes.Soft(primary_hue="rose", secondary_hue="orange", neutral_hue="stone")
CSS = """
    .gradio-container { max-width: 1000px !important; }
    h1 { font-family: Georgia, serif !important; letter-spacing: 0.02em; }
    footer { display: none !important; }
"""


with gr.Blocks() as demo:
    gr.Markdown(
        "# Flora | Petal & Crumb Atelier\n"
        "*A botanical concierge for pastries, flowers, creative workshops, and private celebrations.*\n\n"
        "This is a fictional course project; please do not enter sensitive information."
    )
    gr.ChatInterface(
        fn=chatbot,
        examples=[
            "What is included in Glaze & Sip?",
            "I would like to reserve a floral workshop for four people.",
            "Can you guarantee a nut-free pastry?",
            "Feedback: I would love a candle-making workshop.",
        ],
    )


if __name__ == "__main__":
    demo.launch(theme=THEME, css=CSS)
