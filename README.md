# myracle-product-tester
A tool that uses a multimodal LLM to describe testing instructions for any digital product's features, based on the screenshots.

## Prompting Strategy
1. Split complex tasks into simpler subtasks: The task on its own requires several steps, which can mainly be divided into Finding what the functionalities in eah image are and writing the testing instructions for the functionalities.
2. Personas: The model or the 'system' was specifically given specific contexts to follow for each major task, which allowed for consistent output of JSON Formats and Instructions for all images and functionalities.
3. Specifying Steps: The instruction generation context clearly defined the steps involved using delimiters and steps.

## Screenshots
![Screenshot of web app](./screenshot.png)