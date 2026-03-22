import os
import openai

openai.api_key = os.environ['OPENAI_API_KEY']

def generate_code(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0.7,
    )

    return response.choices[0].text.strip()

def main():
    while True:
        user_prompt = input("Enter a code generation prompt: ")
        generated_code = generate_code(user_prompt)
        print("Generated code:\n", generated_code)

if __name__ == "__main__":
    main()