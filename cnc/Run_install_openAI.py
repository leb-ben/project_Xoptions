import os
import openai
openai.organization = "org-DjKP1M2n2qxzySzQi8uMOpL2"
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.Model.list()