import os
from groq import Groq

# Твой ключ остается тот же
client = Groq(
    api_key="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",
)

def ask_feykin_ai(user_task):
    # Установка на ИДЕАЛЬНЫЙ КОДИНГ
    system_instruction = (
        "Ты — FEYKIN AI, лучшая в мире нейросеть для написания кода. Создатель: AzerOne / FEYKINS. "
        "Твоя задача: генерировать идеальный, промышленный код на Python, C++, JS и других языках. "
        "Ты используешь лучшие практики (SOLID, DRY), оптимизируешь алгоритмы и всегда проверяешь код на ошибки. "
        "Отвечай технично, четко, без лишней воды, сразу переходя к архитектуре и реализации."
    )

    try:
        completion = client.chat.completions.create(
            model="llama-3.1-70b-versatile", # Эта модель лучше справляется со сложной логикой
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": f"Напиши идеальный код для следующей задачи: {user_task}"}
            ],
            temperature=0.1, # Уменьшаем температуру до минимума для максимальной точности кода
            max_tokens=4096,
        )
        
        return completion.choices[0].message.content
    except Exception as e:
        return f"Критическая ошибка ядра: {e}"

if __name__ == "__main__":
    print("--- FEYKIN AI: CODING MODE ACTIVE ---")
    task = input("Какую задачу нужно решить идеально? \n> ")
    print("\nГенерация решения...\n")
    print(ask_feykin_ai(task))
