import os
import openai
import json

openai.api_key = os.environ.get('OPENAI_API_KEY')

def advanced_prompt_engineering(prompt, max_tokens=2048, temperature=0.7, top_p=0.9, frequency_penalty=0.0, presence_penalty=0.0):
    """Generates text using the OpenAI GPT-3 language model with advanced prompt engineering."""
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=temperature,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty
    )

    return response.choices[0].text.strip()

def main():
    prompt = "Provide a detailed and engaging product description for a new AI-powered writing assistant."
    result = advanced_prompt_engineering(prompt)
    print(result)

if __name__ == "__main__":
    main()