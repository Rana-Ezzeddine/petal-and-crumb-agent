"""Gradio entry point for the Petal & Crumb Atelier assistant."""

import gradio as gr

from core_bot import chatbot


demo = gr.ChatInterface(
    fn=chatbot,
    title="Flora - Petal & Crumb Atelier",
    description=(
        "Explore pastries, flowers, creative workshops, and private celebrations. "
        "This is a fictional course project; do not enter sensitive information."
    ),
    examples=[
        "What is included in Glaze & Sip?",
        "I would like to reserve a floral workshop for four people.",
        "Can you guarantee a nut-free pastry?",
        "Feedback: I would love a candle-making workshop.",
    ],
)


if __name__ == "__main__":
    demo.launch()
