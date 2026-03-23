import os
import openai
import json

openai.api_key = os.environ.get('OPENAI_API_KEY')

def generate_code_insights(code_text):
    """Generate AI-powered insights for the given code text."""
    prompt = f"Provide detailed analysis and insights for the following code:\n\n{code_text}\n\nInclude the following in your response:\n- High-level overview of the code's purpose and functionality\n- Identification of any potential issues, bugs, or areas for improvement\n- Suggestions for optimizations or refactoring to improve performance, readability, and maintainability\n- Explanation of any complex or noteworthy aspects of the code"
    
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
    with open('src/main.py', 'r') as f:
        code_text = f.read()
    
    insights = generate_code_insights(code_text)
    print(insights)

if __name__ == '__main__':
    main()