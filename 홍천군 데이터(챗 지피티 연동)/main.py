import openai
import os

# OpenAI API 키 설정
openai.api_key = 'sk-proj--bG1dOLMfJG7BFHy2sH2QvzdlhUPszNzlnel5aLcK0k24A'  # 여기서 YOUR_API_KEY를 실제 API 키로 변경하세요.

def chat_with_gpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # 사용하고자 하는 모델
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content']

def main():
    print("ChatGPT에 대화해보세요! 'exit'를 입력하면 종료됩니다.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
        response = chat_with_gpt(user_input)
        print(f"ChatGPT: {response}")

if __name__ == "__main__":
    main()