import os
#from openai import OpenAI
#import openai
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from metadata_extractor import extract_metadata
import configparser

# Config file for persisting API key
CONFIG_PATH = os.path.expanduser('~/.search_buddy_config')
CONFIG_SECTION = 'openai'

class SearchBuddyGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Search Buddy GUI")
        self.geometry("800x600")
        self.config = configparser.ConfigParser()
        self.api_key = ''
        self.pdf_folder = ''
        self.load_api_key()
        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="OpenAI API Key:").grid(row=0, column=0, sticky=tk.W)
        self.api_entry = ttk.Entry(frame, width=50)
        self.api_entry.grid(row=0, column=1, sticky=tk.W)
        self.api_entry.insert(0, self.api_key)

        self.save_button = ttk.Button(frame, text="Save Key", command=self.save_api_key)
        self.save_button.grid(row=0, column=2, sticky=tk.W)

        ttk.Button(frame, text="Select PDFs Folder", command=self.select_folder).grid(row=1, column=0, pady=5)
        self.folder_label = ttk.Label(frame, text="No folder selected")
        self.folder_label.grid(row=1, column=1, sticky=tk.W)

        ttk.Button(frame, text="Run Extraction", command=self.run_extraction).grid(row=2, column=0, pady=5)

        self.status = ttk.Label(frame, text="Ready")
        self.status.grid(row=3, column=0, columnspan=3, sticky=tk.W)

        cols = ["Filename","Author","Score","Tests","Statement"]
        self.tree = ttk.Treeview(frame, columns=cols, show='headings')
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=150)
        self.tree.grid(row=4, column=0, columnspan=3, sticky='nsew')
        frame.rowconfigure(4, weight=1)
        frame.columnconfigure(1, weight=1)

    def load_api_key(self):
        if os.path.exists(CONFIG_PATH):
            self.config.read(CONFIG_PATH)
            self.api_key = self.config.get(CONFIG_SECTION, 'api_key', fallback='')

    def save_api_key(self):
        key = self.api_entry.get().strip()
        if not key:
            messagebox.showerror("Error","API key cannot be empty")
            return
        if CONFIG_SECTION not in self.config:
            self.config[CONFIG_SECTION] = {}
        self.config[CONFIG_SECTION]['api_key'] = key
        with open(CONFIG_PATH, 'w') as cf:
            self.config.write(cf)
        self.api_key = key
        messagebox.showinfo("Success","API key saved")
        self.status.config(text="API key saved")

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.pdf_folder = folder
            self.folder_label.config(text=folder)

    def run_extraction(self):
        if not self.api_key:
            messagebox.showerror("Error","Enter and save an API key first")
            return

        # instantiate OpenAI client and set env var
        client = OpenAI(api_key=self.api_key)
        os.environ["OPENAI_API_KEY"] = self.api_key
        openai.api_key = self.api_key

        self.tree.delete(*self.tree.get_children())
        self.status.config(text="Extracting...")

        for fname in os.listdir(self.pdf_folder):
            if not fname.lower().endswith('.pdf'): continue
            path = os.path.join(self.pdf_folder, fname)
            meta = extract_metadata(path)
            tests = meta.get('positionality_tests', [])
            snippets = meta.get('positionality_snippets', {}) or {}

            # pick snippet priority
            if 'gpt_full_text' in snippets:
                summary = snippets['gpt_full_text']
            elif 'header' in snippets:
                summary = snippets['header']
            elif 'tail' in snippets:
                summary = snippets.get('tail','')
            else:
                summary = ''

            score = meta.get('positionality_score', 0.0)
            rows = (fname,
                    meta.get('author'),
                    round(score, 2),
                    ', '.join(tests),
                    summary)
            self.tree.insert('', tk.END, values=rows)

        self.status.config(text="Done.")

if __name__ == '__main__':
    app = SearchBuddyGUI()
    app.mainloop()
