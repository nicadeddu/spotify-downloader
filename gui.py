__version__ = "1.0.3"
__author__ = "Cha @github.com/invzfnc"

import os
import sys
import threading
import tkinter as tk
from tkinter import filedialog, ttk, scrolledtext
from tkinter.font import Font
import io
from contextlib import redirect_stdout

from main import main

class TextRedirector:
    """Reindirizza stdout a un widget tkinter"""

    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.buffer = io.StringIO()

    def write(self, string):
        self.buffer.write(string)
        self.text_widget.insert(tk.END, string)
        self.text_widget.see(tk.END)

    def flush(self):
        pass


class SpotifyDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Spotify Playlist Downloader")
        self.root.geometry("650x500")
        self.root.resizable(True, True)

        try:
            if sys.platform == "win32" and os.path.exists("assets/icon.ico"):
                self.root.iconbitmap("assets/icon.ico")
            # Per macOS l'icona si imposta durante la compilazione
        except Exception:
            pass  # Ignora qualsiasi errore relativo all'icona

        self.create_widgets()
        self.center_window()

    def center_window(self):
        """Centra la finestra sullo schermo"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def create_widgets(self):
        """Crea tutti i widget dell'interfaccia"""
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Titolo
        title_font = Font(family="Helvetica", size=16, weight="bold")
        title_label = ttk.Label(main_frame, text="Spotify Playlist Downloader", font=title_font)
        title_label.pack(pady=(0, 20))

        # URL della playlist
        url_frame = ttk.Frame(main_frame)
        url_frame.pack(fill=tk.X, pady=5)

        url_label = ttk.Label(url_frame, text="URL Playlist Spotify:")
        url_label.pack(side=tk.LEFT, padx=(0, 10))

        self.url_entry = ttk.Entry(url_frame)
        self.url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Directory di output
        dir_frame = ttk.Frame(main_frame)
        dir_frame.pack(fill=tk.X, pady=5)

        dir_label = ttk.Label(dir_frame, text="Directory di output:")
        dir_label.pack(side=tk.LEFT, padx=(0, 10))

        self.dir_entry = ttk.Entry(dir_frame)
        self.dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.dir_entry.insert(0, os.path.abspath("./downloads/"))

        browse_button = ttk.Button(dir_frame, text="Sfoglia", command=self.browse_directory)
        browse_button.pack(side=tk.LEFT, padx=(10, 0))

        # Pulsanti
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X, pady=10)

        self.download_button = ttk.Button(
            buttons_frame,
            text="Scarica Playlist",
            command=self.start_download
        )
        self.download_button.pack(side=tk.LEFT, padx=(0, 10))

        self.cancel_button = ttk.Button(
            buttons_frame,
            text="Annulla",
            command=self.cancel_download,
            state=tk.DISABLED
        )
        self.cancel_button.pack(side=tk.LEFT)

        # Area di log
        log_label = ttk.Label(main_frame, text="Log:")
        log_label.pack(anchor=tk.W, pady=(10, 5))

        self.log_text = scrolledtext.ScrolledText(main_frame, height=15, wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        self.log_text.config(state=tk.DISABLED)

        # Barra di stato
        self.status_var = tk.StringVar()
        self.status_var.set("Pronto")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Variabili per il thread di download
        self.download_thread = None
        self.is_downloading = False

    def browse_directory(self):
        """Apre la finestra di dialogo per selezionare la directory di output"""
        directory = filedialog.askdirectory(
            initialdir=self.dir_entry.get(),
            title="Seleziona la directory di output"
        )
        if directory:
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, directory)

    def enable_log_writing(self):
        """Abilita la scrittura nel widget di log"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)

    def disable_log_writing(self):
        """Disabilita la scrittura nel widget di log"""
        self.log_text.config(state=tk.DISABLED)

    def start_download(self):
        """Avvia il download in un thread separato"""
        playlist_url = self.url_entry.get().strip()
        output_dir = self.dir_entry.get().strip()

        if not playlist_url:
            self.show_error("Inserisci un URL della playlist Spotify valido")
            return

        if not output_dir:
            self.show_error("Seleziona una directory di output valida")
            return

        # Crea la directory se non esiste
        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
            except Exception as e:
                self.show_error(f"Impossibile creare la directory: {str(e)}")
                return

        # Aggiorna l'interfaccia
        self.download_button.config(state=tk.DISABLED)
        self.cancel_button.config(state=tk.NORMAL)
        self.status_var.set("Download in corso...")
        self.is_downloading = True

        # Abilita la scrittura nel log
        self.enable_log_writing()

        # Reindirizza stdout al widget di testo
        self.stdout_redirector = TextRedirector(self.log_text)

        # Avvia il download in un thread separato
        self.download_thread = threading.Thread(
            target=self.download_task,
            args=(playlist_url, output_dir)
        )
        self.download_thread.daemon = True
        self.download_thread.start()

        # Controlla lo stato del thread
        self.root.after(100, self.check_download_status)

    def download_task(self, playlist_url, output_dir):
        """Esegue il download (questa funzione viene eseguita in un thread separato)"""
        try:
            # Reindirizza stdout al widget di log
            with redirect_stdout(self.stdout_redirector):
                main(playlist_url, output_dir)
        except Exception as e:
            print(f"\nErrore durante il download: {str(e)}")

    def check_download_status(self):
        """Controlla lo stato del thread di download"""
        if self.is_downloading and not self.download_thread.is_alive():
            # Il download è terminato
            self.download_complete()
        elif self.is_downloading:
            # Il download è ancora in corso
            self.root.after(100, self.check_download_status)

    def download_complete(self):
        """Gestisce il completamento del download"""
        self.is_downloading = False
        self.download_button.config(state=tk.NORMAL)
        self.cancel_button.config(state=tk.DISABLED)
        self.status_var.set("Download completato")
        self.disable_log_writing()

    def cancel_download(self):
        """Annulla il download in corso"""
        if self.is_downloading:
            # Non possiamo davvero interrompere il thread in modo sicuro
            # Imposteremo solo i flag per l'interfaccia utente
            self.status_var.set("Download annullato")
            self.is_downloading = False
            self.download_button.config(state=tk.NORMAL)
            self.cancel_button.config(state=tk.DISABLED)
            print("\nDownload annullato dall'utente.")

    def show_error(self, message):
        """Mostra un messaggio di errore"""
        from tkinter import messagebox
        messagebox.showerror("Errore", message)


def main_gui():
    root = tk.Tk()
    app = SpotifyDownloaderApp(root)
    root.mainloop()


if __name__ == "__main__":
    main_gui()