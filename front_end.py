import gradio as gr

def generate_testing_instructions(context, images):
    if not images:
        return "Error: Please upload at least one screenshot."
    
    num_images = len(images)
    instructions = f"Testing instructions based on {num_images} screenshot(s):\n\n"
    
    if context:
        instructions += f"Context: {context}\n\n"
    
    instructions += "1. Verify the UI elements in the screenshots.\n"
    instructions += "2. Test the functionality shown in the images.\n"
    instructions += "3. Ensure all interactive elements are working as expected.\n"
    
    return instructions

# Gradio UI components
iface = gr.Interface(
    fn=generate_testing_instructions,
    inputs=[
        gr.Textbox(label="Optional Context", placeholder="Enter any additional context here..."),
        gr.File(label="Screenshots", file_count="multiple", file_types=["image"])
    ],
    outputs=gr.Textbox(label="Testing Instructions"),
    title="Testing Instruction Generator",
    description="Upload screenshots and optionally provide context to generate testing instructions.",
    theme="default",
    allow_flagging="never"
)

# Launch the interface
iface.launch()