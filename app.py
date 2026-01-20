import os
import customtkinter as ctk
from groq import Groq
import threading

# --- ЯДРО FEYKIN AI (ТВОИ ДАННЫЕ) ---
API_KEY = "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"
CREATOR = "AzerOne / FEYKINS"

class FeykinCore:
    def __init__(self):
        self.client = Groq(api_key=API_KEY)
        self.model = "llama-3.3-70b-versatile" # Самая мощная для кодинга

    def generate_code(self, prompt):
        system_msg = (
            f"Ты — FEYKIN AI, лучшая нейросеть для кодинга. Создатель: {CREATOR}. "
            "Пиши только идеальный, оптимизированный код. Используй SOLID и DRY. "
            "Минимум воды, максимум архитектуры и комментариев."
        )
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": f"Напиши идеальный код: {prompt}"}
                ],
                temperature=0.1, # Точность на максимум
                max_tokens=4096
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"Критическая ошибка: {str(e)}"

# --- ИНТЕРФЕЙС ПРИЛОЖЕНИЯ ---
class FeykinApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.ai = FeykinCore()

        # Настройка окна
        self.title(f"FEYKIN AI v1.0 - {CREATOR}")
        self.geometry("900x700")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Сетка
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Заголовок
        self.header = ctk.CTkLabel(self, text="FEYKIN AI", font=("Consolas", 32, "bold"), text_color="#ff003c")
        self.header.grid(row=0, column=0, pady=20)

        # Поле вывода кода (с поддержкой скролла)
        self.code_display = ctk.CTkTextbox(self, font=("Consolas", 14), fg_color="#1a1a1a", border_color="#333", border_width=2)
        self.code_display.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        # Фрейм ввода
        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.grid(row=2, column=0, padx=20, pady=20, sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.user_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Опиши алгоритм или задачу...", height=45, font=("Arial", 14))
        self.user_entry.grid(row=0, column=0, padx=(0, 10), sticky="ew")

        self.gen_button = ctk.CTkButton(self.input_frame, text="СГЕНЕРИРОВАТЬ КОД", command=self.start_gen_thread, 
                                        fg_color="#ff003c", hover_color="#aa0028", width=150, height=45, font=("Arial", 13, "bold"))
        self.gen_button.grid(row=0, column=1)

        # Футер
        self.footer = ctk.CTkLabel(self, text=f"Build by {CREATOR} | Powered by Groq LPU", font=("Arial", 10), text_color="#555")
        self.footer.grid(row=3, column=0, pady=5)

    def start_gen_thread(self):
        # Запускаем в отдельном потоке, чтобы интерфейс не зависал
        task = self.user_entry.get()
        if not task: return
        
        self.gen_button.configure(state="disabled", text="ДУМАЮ...")
        self.code_display.insert("end", f"\n\n>>> ЗАПРОС: {task}\n" + "-"*50 + "\n")
        
        thread = threading.Thread(target=self.run_ai, args=(task,))
        thread.start()

    def run_ai(self, task):
        response = self.ai.generate_code(task)
        # Возвращаемся в основной поток для обновления UI
        self.after(0, lambda: self.update_ui(response))

    def update_ui(self, response):
        self.code_display.insert("end", response)
        self.code_display.see("end")
        self.gen_button.configure(state="normal", text="СГЕНЕРИРОВАТЬ КОД")
        self.user_entry.delete(0, 'end')

if __name__ == "__main__":
    app = FeykinApp()
    app.mainloop()
