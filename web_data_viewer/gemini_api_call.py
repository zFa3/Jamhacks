#!/usr/bin/env python3

# Author: Jayden W
# Date: May 2025
# File: gemini_interface.py
# Version: 1.2

# Description
#
#   This file creates a class that handles the communciation between
#   the program and google's AI API. Very succinct class, includes the essentials
#   that are required to prompt a response from an LLM

# pip install -q -U google-genai
# OR
# pip install google-genai
from google.genai import types, errors
from google import genai
from time import sleep
import os

class Interface:

    # the initializer, uses the flash-lite as the defualt model
    def __init__(self, model: str = "gemini-2.0-flash-lite", temperature = 1) -> None:
        
        # attempt to load the API
        env = os.environ
        self.API_KEY = env.get("GEMINI_KEY")

        # If you don't have a paid Google AI studio account
        # use this "gemini-2.5-pro-exp-03-25" as opposed to the paid version "gemini-2.5-pro-preview-03-25"

        # this file is to create a nice and easy way to access the Gemini API
        # acts as the interface between the program and the request calls

        self.MODELS = {
            # smallest, fastest model
            "gemini-2.0-flash-lite",
            
            # A smaller, faster model
            "gemini-2.0-flash",

            # A larger, better reasoning model but also slower to respond
            # Excels in more complex tasks involving Science, Mathematics and CS
            "gemini-2.5-pro-exp-03-25",
        }

        self.model = model

        self.attempts = 5

        self.temperature = temperature

    def generate(self, prompt: str) -> str:
        
        client = genai.Client(
            api_key = self.API_KEY,
        )

        contents = [
            types.Content(
                role = "user",
                parts = [
                    types.Part.from_text(text = prompt),
                ],
            ),
        ]

        generate_content_config = types.GenerateContentConfig(
            response_mime_type="text/plain",
            temperature=self.temperature,
        )


        safety_settings = [
            # versus threshold = "OFF"
            types.SafetySetting(category='HARM_CATEGORY_UNSPECIFIED', threshold="BLOCK_NONE"),
            types.SafetySetting(category='HARM_CATEGORY_HATE_SPEECH', threshold="BLOCK_NONE"),
            types.SafetySetting(category='HARM_CATEGORY_DANGEROUS_CONTENT', threshold="BLOCK_NONE"),
            types.SafetySetting(category='HARM_CATEGORY_HARASSMENT', threshold="BLOCK_NONE"),
            types.SafetySetting(category='HARM_CATEGORY_SEXUALLY_EXPLICIT', threshold="BLOCK_NONE"),
            types.SafetySetting(category='HARM_CATEGORY_CIVIC_INTEGRITY', threshold="BLOCK_NONE"),
        ]

        response = ""
        for chunk in client.models.generate_content_stream(
            model = self.model,
            contents = contents,
            config = generate_content_config,
        ):
            response += chunk.text
        return response
    
    def safe_generate(self, prompt: str) -> str:
        # generate the response wrappen in try except,
        # to prevent rate limits from crashing the program
        for _ in range(self.attempts):
            try:
                response = self.generate(prompt)
                return response
            except errors.APIError as error:
                print(f"Error - code: {error.code}")
                print(f"Retrying in 15s...")
            sleep(15)

    def set_api_key(self, key: str) -> None:
        # reset the API key to the provided string
        self.API_KEY = key
    
    def set_model(self, model: str) -> None:
        # change the model
        self.model = model

    def set_temperature(self, temp: float) -> None:
        # change the model temperature, from 0 - 2
        temp = min(2, max(0, temp))
        self.temperature = temp


# this is just a test and will only run if you run this file directly
if __name__  ==  "__main__":
    # for testing purposes
    intf = Interface("gemini-2.0-flash")
    # https://peps.python.org/pep-0572/
    while (a := input(">>> ").lower()) != "q":
        print(intf.generate(a))