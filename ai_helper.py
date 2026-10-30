import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

client = Anthropic(
    base_url=os.getenv("ANTHRPIC_BASE_URL"),
    api_key=os.getenv("ANTHROPIC_API_KEY")
)


def ask_ai(prompt, image_data=None, image_type="image/jpeg"):
    content = []

    # 이미지가 있으면 먼저 추가
    if image_data:
        content.append({
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": image_type,
                "data": image_data
            }
        })

    # 텍스트 프롬프트 추가
    content.append({
        "type": "text",
        "text": prompt
    })

    res = client.messages.create(
        model="claude-haiku", max_tokens=1024,
        messages=[{"role": "user", "content": content}]
    )
    return res.content[0].text