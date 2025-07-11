import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv
import threading
import os
from PIL import Image, ImageTk

TOTAL_LOOPS = 200
WAIT_TIME = 3
SCROLL_TIMES = 2


# SPLASH SCREEN FIRST
class SplashScreen(tk.Toplevel):
    def __init__(self, root, on_close_callback):
        super().__init__(root)
        self.title("Loading XFollowingViews...")
        self.geometry("400x300")
        self.overrideredirect(True)
        self.config(bg="white")
        self.after(3000, on_close_callback)  # Show for 3 seconds

        try:
            image = Image.open("logo.png")
            image = image.resize((150, 150), Image.ANTIALIAS)
            self.logo = ImageTk.PhotoImage(image)
            tk.Label(self, image=self.logo, bg="white").pack(pady=20)
        except Exception as e:
            print("Splash image not found or failed to load.")

        tk.Label(self, text="XFollowingViews", font=("Arial", 18, "bold"), bg="white", fg="#1DA1F2").pack()
        tk.Label(self, text="Loading, please wait...", font=("Arial", 12), bg="white").pack(pady=10)


class TwitterScraperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("XFollowingViews - Twitter Following Scraper")
        self.root.geometry("400x250")
        self.root.resizable(False, False)

        tk.Label(root, text="Twitter Username (without @):").pack(pady=10)
        self.username_entry = tk.Entry(root, width=30)
        self.username_entry.pack()

        self.start_btn = tk.Button(root, text="Start Scraping", command=self.run_scraper)
        self.start_btn.pack(pady=15)

        self.status_label = tk.Label(root, text="", fg="blue")
        self.status_label.pack()

        self.quit_btn = tk.Button(root, text="Exit", command=root.quit)
        self.quit_btn.pack(pady=10)

    def run_scraper(self):
        username = self.username_entry.get().strip()
        if not username:
            messagebox.showerror("Error", "Please enter a Twitter username.")
            return

        self.status_label.config(text="Launching browser...")

        thread = threading.Thread(target=self.scrape, args=(username,))
        thread.start()

    def scrape(self, username):
        try:
            from selenium.webdriver.chrome.service import Service
            driver = webdriver.Chrome(service=Service("chromedriver.exe"))
            driver.maximize_window()

            self.status_label.config(text="Waiting for manual login...")

            driver.get("https://twitter.com/login")
            messagebox.showinfo("Manual Login", "Please log in to Twitter manually.\nThen click OK to continue.")

            unique_handles = set()

            for i in range(TOTAL_LOOPS):
                self.status_label.config(text=f"Round {i+1}/{TOTAL_LOOPS}")
                driver.get(f"https://twitter.com/{username}/following")
                time.sleep(WAIT_TIME + 2)

                for _ in range(SCROLL_TIMES):
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(WAIT_TIME)

                elements = driver.find_elements(By.XPATH, '//span[starts-with(text(), "@")]')
                round_handles = [el.text.strip() for el in elements if el.text.startswith("@")]
                new_handles = [h for h in round_handles if h not in unique_handles]
                unique_handles.update(new_handles)

                if len(unique_handles) >= 5000:
                    break

            filename = f"{username}_following_handles.csv"
            with open(filename, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Handle"])
                for h in sorted(unique_handles):
                    writer.writerow([h])

            self.status_label.config(text=f"✅ Done! Saved {len(unique_handles)} handles.")
            messagebox.showinfo("Done", f"Saved to {filename}")
            driver.quit()

        except Exception as e:
            messagebox.showerror("Error", f"Something went wrong:\n{str(e)}")


# MAIN STARTUP
def launch_main_window():
    splash.destroy()
    app_window = tk.Tk()
    TwitterScraperApp(app_window)
    app_window.mainloop()


# Start app with splash
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the root while splash shows
    splash = SplashScreen(root, on_close_callback=launch_main_window)
    splash.mainloop()
