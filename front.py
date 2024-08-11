import tkinter as tk
import customtkinter as ctk
import queue
import time
import os

from tkinter import filedialog, messagebox
from threading import Thread
from moviepy.editor import VideoFileClip

class VideoCutterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fatiador de Vídeos")
        self.root.geometry("815x550")  # Ajuste o tamanho para acomodar novas opções

        # Create a queue to handle console output
        self.queue = queue.Queue()

        # Time tracking variables
        self.start_time = None

        # Create and place widgets using customtkinter
        self.create_widgets()

        # Start the update loop for the queue
        self.update_queue()

    def create_widgets(self):
        # Path inputs
        self.input_path_label = ctk.CTkLabel(self.root, text="Caminho do vídeo:")
        self.input_path_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.input_path_entry = ctk.CTkEntry(self.root, width=300)
        self.input_path_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        self.browse_input_button = ctk.CTkButton(self.root, text="Buscar", command=self.browse_input)
        self.browse_input_button.grid(row=0, column=2, padx=10, pady=10)

        self.output_path_label = ctk.CTkLabel(self.root, text="Caminho de saída:")
        self.output_path_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.output_path_entry = ctk.CTkEntry(self.root, width=300)
        self.output_path_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        self.browse_output_button = ctk.CTkButton(self.root, text="Buscar", command=self.browse_output)
        self.browse_output_button.grid(row=1, column=2, padx=10, pady=10)

        # Duration options
        self.duration_label = ctk.CTkLabel(self.root, text="Duração:")
        self.duration_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.duration_entry = ctk.CTkEntry(self.root, width=50)
        self.duration_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        self.duration_unit_var = tk.StringVar(value="s")
        self.seconds_radio = ctk.CTkRadioButton(self.root, text="Segundos", variable=self.duration_unit_var, value="s")
        self.seconds_radio.grid(row=2, column=2, padx=5, pady=10, sticky="w")

        self.minutes_radio = ctk.CTkRadioButton(self.root, text="Minutos", variable=self.duration_unit_var, value="m")
        self.minutes_radio.grid(row=2, column=3, padx=5, pady=10, sticky="w")

        # Format and Quality options
        self.format_label = ctk.CTkLabel(self.root, text="Formato:")
        self.format_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        self.format_var = tk.StringVar(value="mp4")
        self.format_menu = ctk.CTkOptionMenu(self.root, variable=self.format_var, values=["mp4", "avi", "mov", "mkv", "webm"])
        self.format_menu.grid(row=3, column=1, padx=10, pady=10)

        self.quality_label = ctk.CTkLabel(self.root, text="Qualidade:")
        self.quality_label.grid(row=3, column=2, padx=10, pady=10, sticky="w")

        self.quality_var = tk.StringVar(value="medium")
        self.quality_menu = ctk.CTkOptionMenu(self.root, variable=self.quality_var, values=["low", "medium", "high"])
        self.quality_menu.grid(row=3, column=3, padx=10, pady=10)

        # Start Button
        self.start_button = ctk.CTkButton(self.root, text="Iniciar Corte", command=self.start_cutting)
        self.start_button.grid(row=4, column=0, columnspan=4, padx=10, pady=10)

        # Progress Bar
        self.progress_bar = ctk.CTkProgressBar(self.root, mode="indeterminate")
        self.progress_bar.grid(row=5, column=0, columnspan=4, padx=10, pady=10, sticky="ew")

        # Status Label
        self.status_label = ctk.CTkLabel(self.root, text="")
        self.status_label.grid(row=6, column=0, columnspan=4, padx=10, pady=10, sticky="ew")

        # Total Cuts Label
        self.total_cuts_label = ctk.CTkLabel(self.root, text="Número Total de Cortes: N/A")
        self.total_cuts_label.grid(row=7, column=0, columnspan=4, padx=10, pady=10, sticky="ew")

    def browse_input(self):
        file_path = filedialog.askopenfilename(filetypes=[("Vídeo", "*.mp4;*.avi;*.mov;*.mkv;*.webm")])
        if file_path:
            self.input_path_entry.delete(0, tk.END)
            self.input_path_entry.insert(0, file_path)

    def browse_output(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.output_path_entry.delete(0, tk.END)
            self.output_path_entry.insert(0, folder_path)

    def validate_inputs(self):
        video_path = self.input_path_entry.get()
        output_dir = self.output_path_entry.get()
        duration = self.duration_entry.get()

        # Check if input and output paths are provided
        if not video_path or not output_dir:
            messagebox.showerror("Erro", "Por favor, insira os caminhos de entrada e saída.")
            return False

        # Check if the video file exists
        if not os.path.isfile(video_path):
            messagebox.showerror("Erro", "O arquivo de vídeo especificado não existe.")
            return False

        # Check if the output directory exists
        if not os.path.isdir(output_dir):
            messagebox.showerror("Erro", "O diretório de saída especificado não existe.")
            return False

        # Check if duration is a valid number
        try:
            duration = int(duration)
            if duration <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "A duração deve ser um número inteiro positivo.")
            return False

        return True

    def start_cutting(self):
        if not self.validate_inputs():
            return

        video_path = self.input_path_entry.get()
        output_dir = self.output_path_entry.get()
        duration = self.duration_entry.get()
        format_choice = self.format_var.get()
        quality_choice = self.quality_var.get()
        duration_unit = self.duration_unit_var.get()

        try:
            duration = int(duration)
            if duration_unit == "m":
                duration *= 60
        except ValueError:
            duration = 60  # Default to 60 seconds if input is invalid

        # Define bitrate based on quality choice
        bitrate_options = {
            "low": "500k",
            "medium": "1000k",
            "high": "2000k"
        }
        bitrate = bitrate_options.get(quality_choice, "1000k")

        # Calculate the number of cuts
        video_clip = VideoFileClip(video_path)
        total_duration = int(video_clip.duration)
        num_chunks = total_duration // duration + (1 if total_duration % duration else 0)
        self.total_cuts_label.configure(text=f"@wellfulstack Telegram: https://t.me/wellfulstack\n\nSera feito um Total de: {num_chunks} Cortes")

        self.progress_bar.start()
        self.status_label.configure(text="Processando...")

        # Start the timer
        self.start_time = time.time()

        # Start processing in a separate thread
        thread = Thread(target=self.process_video, args=(video_path, output_dir, duration, format_choice, bitrate, num_chunks))
        thread.start()

    def process_video(self, video_path, output_dir, duration, format_choice, bitrate, num_chunks):
        try:
            video_clip = VideoFileClip(video_path)
            for i in range(num_chunks):
                start_time = i * duration
                end_time = min((i + 1) * duration, int(video_clip.duration))

                # Define the output file path
                output_file = os.path.join(output_dir, f"video_part_{i + 1}.{format_choice}")

                # Cut the video
                trimmed_clip = video_clip.subclip(start_time, end_time)
                trimmed_clip.write_videofile(output_file, codec="libx264", audio_codec="aac", bitrate=bitrate)

                # Put a message in the queue
                self.queue.put(f"Corte {i + 1}/{num_chunks} concluído: {output_file}")

            # Final message
            self.queue.put("Processamento concluído.")
        except Exception as e:
            self.queue.put(f"Erro: {str(e)}")
        finally:
            self.progress_bar.stop()
            self.status_label.configure(text="Pronto")

    def update_queue(self):
        try:
            while True:
                message = self.queue.get_nowait()
                self.status_label.configure(text=message)
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self.update_queue)

if __name__ == "__main__":
    root = ctk.CTk()
    app = VideoCutterApp(root)
    root.mainloop()

