import os #getting API key from system enviroment
from openai import OpenAI


def generate_product_description(prompt):
    """
    Utility function to generate a product description using OpenAI API.
    """
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key='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', #just in this case it will be hardcoded here
    )
    try:
        completion = client.chat.completions.create(
            model="deepseek/deepseek-r1:free",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error generating description: {e}")
        return None
