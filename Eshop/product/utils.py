import os #getting API key from system enviroment
from openai import OpenAI




def generate_product_description(prompt):
    """
    Utility function to generate a product description using OpenAI API.
    """
    client = OpenAI(
        base_url="https://api.deepseek.com/v1",
        api_key='sk-4bd5549b441e4719b82c46013ca9ccf1', #just in this case it will be hardcoded here
    )
    try:
        completion = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error generating description: {e}")
        return None
