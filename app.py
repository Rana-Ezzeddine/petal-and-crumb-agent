"""Gradio interface; demo evidence is isolated to the current conversation turn."""
import gradio as gr
from core_bot import chatbot_with_trace

try:
    import spaces
except ImportError:
    class _LocalSpaces:
        @staticmethod
        def GPU(function):
            return function
    spaces = _LocalSpaces()


@spaces.GPU
def serve(message, history):
    """Honor the existing Space's ZeroGPU runtime; inference uses Gemini."""
    return chatbot_with_trace(message, history)

THEME = gr.themes.Soft(primary_hue="rose", secondary_hue="orange", neutral_hue="stone")
CSS = ".gradio-container { max-width: 1000px !important; } h1 { font-family: Georgia, serif !important; }"

with gr.Blocks() as demo:
    gr.Markdown(
        "# Flora | Petal & Crumb Atelier\n"
        "*A botanical concierge for pastries, flowers, workshops, and private celebrations.*\n\n"
        "Fictional coursework business. Use fictional contact details for demonstrations."
    )
    with gr.Accordion("Coursework demo: router, tools, and reflection", open=False):
        gr.Markdown("Shows only the current turn from your conversation. A recorded lead is an enquiry, not a confirmed reservation.")
        trace = gr.JSON(label="Current turn evidence")
    gr.ChatInterface(fn=serve, additional_outputs=[trace], api_name="chat",
        examples=["What is included in Glaze & Sip?",
                  "I would like to reserve a floral workshop for four people.",
                  "Can you guarantee a nut-free pastry?",
                  "Feedback: I would love a candle-making workshop."])

if __name__ == "__main__":
    demo.launch(theme=THEME, css=CSS)
