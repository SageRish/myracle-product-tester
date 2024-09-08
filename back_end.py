from openai import OpenAI
import json
import os
import base64
from dotenv import load_dotenv

load_dotenv()

OPENAI_API = os.getenv("OPENAI_API_KEY") # Get the OpenAI API key from the environment variables

client = OpenAI()


extract_context = """ You are a assistant which extracts a list of functionalities from the screenshot of an app and returns them as the following JSON format:
                      {
                        "functionalities": ["list of functionalities"]
                      }"""

generator_context = """ You will be given a functionality, optional context and screenshot of an app page and asked to generate testing instructions based on the screenshots. 
                        The testing instructions should include the following components:
                        1. Description: What the test case is about.
                        2. Pre-conditions: What needs to be set up or ensured before testing.
                        3. Testing Steps: Clear, step-by-step instructions on how to perform the test.
                        4. Expected Result: What should happen if the feature works correctly."""

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    
# Function to call the OpenAI API
def api_call(system_context, user_context, image_path, tokens):
    # Encode the image
    image_data = encode_image(image_path)

    # Call the OpenAI API to generate testing instructions
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_context},
            {
                "role": "user",
                "content": [
                    {
                        "type": "text", "text": user_context
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_data}",
                            "detail": "high"
                        },
                    },
                ],
            }
        ],
        max_tokens=tokens,
    )
    
    # Extract the testing instructions from the response
    output = response.choices[0].message.content
    
    # Return the testing instructions
    return output

def extract_functionalities(optional_context, image_path):
    # Create user context
    user_context = optional_context if optional_context else "Extract the functionalities from this image"
    
    # Extract the functionalities from the response
    functionalities = api_call(extract_context, user_context, image_path, 200)

    # Store output in text file
    with open('output.txt', 'w') as f:
        f.write(functionalities)

    functionalities = functionalities.replace('json', '') # Remove the 'json' string from the response
    functionalities = functionalities.replace('```', '') # Replace single quotes with double quotes

    # Convert functionalities to dictionary
    functionalities = json.loads(functionalities)
    
    # Return the functionalities
    return functionalities

def generate_testing_instructions(functionality, image_path):
    # Create user context
    user_context = f"Generate testing instructions for the following functionality based on the given image: {functionality}"
    
    # Extract the testing instructions from the response
    instructions = api_call(generator_context, user_context, image_path, 600)
    
    # Return the testing instructions
    return instructions