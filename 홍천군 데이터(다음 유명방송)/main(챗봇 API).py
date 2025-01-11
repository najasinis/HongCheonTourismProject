import openai
import sys
import io

# 표준 출력 인코딩 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

openai.api_key = "자신의 api key"

messages = []
while True:
    user_content = input("user: ")
    messages.append({"role": "user", "content": user_content})

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", 
            messages=messages
        )

        assistant_content = completion.choices[0].message["content"].strip()
        messages.append({"role": "assistant", "content": assistant_content})

        print(f"GPT: {assistant_content}")

    except Exception as e:
        print(f"오류 발생: {str(e)}")