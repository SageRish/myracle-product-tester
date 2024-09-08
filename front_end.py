import gradio as gr
import tempfile
import os
from PIL import Image
import matplotlib.pyplot as plt
from back_end import extract_functionalities, generate_testing_instructions

def get_instructions(context, images):
    if not images:
        return "Error: Please upload at least one screenshot."
    
    num_images = len(images)
    instructions = f"Testing instructions based on {num_images} screenshot(s):\n\n"
    
    if context:
        instructions += f"Context: {context}\n\n"
    
    i = 1

    for image in images:
        
        image = Image.open(image)
        plt.imshow(image)
        plt.axis('off')  
        plt.show()
        image.save(f"output_image_{i}.png")
        image_path = f"output_image_{i}.png"
        i += 1
        
        # Add the image path to the instructions
        functionalities = extract_functionalities(context, image_path)

        function_list = functionalities["functionalities"]

        for function in function_list:
            testing_instructions = generate_testing_instructions(function, image_path)
            instructions += f"Test ID: {function}\n\n"
            instructions += f"Testing Instructions: {testing_instructions}\n\n"
        
    return instructions

# Gradio UI components
iface = gr.Interface(
    fn= get_instructions,
    inputs=[
        gr.Textbox(label="Optional Context", placeholder="Enter any additional context here..."),
        gr.File(label="Screenshots", file_count="multiple", file_types=["image"])
    ],
    outputs=gr.Textbox(label="Testing Instructions"),
    title="Testing Instruction Generator",
    description="Upload screenshots and optionally provide context to generate testing instructions.",
    theme="default",
    allow_flagging="never",
    submit_btn="Describe Testing Instructions"
)

# Launch the interface
iface.launch()