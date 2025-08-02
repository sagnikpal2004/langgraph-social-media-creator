import gradio as gr

import agent

iface = gr.Interface(
    fn=agent.run_agent,
    inputs=[
        gr.Textbox(label="Brand Theme"),
        gr.Number(label="Number of Days", value=30)
    ],
    outputs=[
        gr.Dataframe(label="Content Calendar"),
        gr.DownloadButton(label="Download CSV")
    ],
    title="Content Calendar Generator",
)

iface.launch()