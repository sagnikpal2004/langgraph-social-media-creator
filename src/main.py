import gradio as gr
import pandas as pd

def process_text(brand_theme, num_days):
    return pd.DataFrame({'Brand Theme': [brand_theme], 'Number of Days': [num_days]})

iface = gr.Interface(
    fn=process_text,
    inputs=[
        gr.Textbox(label="Brand Theme"),
        gr.Number(label="Number of Days")
    ],
    outputs=gr.Dataframe(label="Content Calendar")
)

iface.launch()