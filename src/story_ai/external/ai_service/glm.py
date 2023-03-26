import os
from typing import List

import openai


class GLM:
    def __init__(self):
        pass

    def text_to_embedding(self, text: str) -> List:
        raise NotImplementedError


class OpenAIGLM(GLM):
    def __init__(self):
        GLM.__init__(self)
        openai.api_key = os.environ.get("OPENAI_API_KEY")
        self.embedding_model = "text-embedding-ada-002"

    def text_to_embedding(self, text: str) -> List:
        result = openai.Embedding.create(model=self.embedding_model, input=text)
        return result["data"][0]["embedding"]

    def text_completion(self, prompt: str):
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.9,
            max_tokens=600,
            best_of=3,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop=[" Human:", " AI:"],
        )
        return response.choices[0].text
