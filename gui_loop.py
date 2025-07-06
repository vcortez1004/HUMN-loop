#!/usr/bin/env python3
import os
import sys
import threading
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

COPYRIGHT = "Made with \u2665 by HUMN.audio 2025"

class VideoLooperApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("HUMN Video Looper")
        self.geometry("500x520")
        self.resizable(False, False)

        # Load Logo (required)
        if getattr(sys, 'frozen', False):
            base_dir = sys._MEIPASS
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(base_dir, "humn_logo.png")
        try:
            logo_img = tk.PhotoImage(file=logo_path)
            logo_lbl = tk.Label(self, image=logo_img)
            logo_lbl.image = logo_img
            logo_lbl.pack(pady=(20, 6))
        except Exception as e:
            tk.Label(self, text="[Logo missing]", font=("Segoe UI", 14, "bold")).pack(pady=(20, 6))
            print(f"Logo not loaded from {logo_path}: {e}")

        # Main frame (input controls)
        frm = ttk.Frame(self)
        frm.pack(fill="x", expand=False, padx=30, pady=(8, 0))

        self.file_var = tk.StringVar()
        self.hours_var = tk.IntVar(value=0)
        self.minutes_var = tk.IntVar(value=0)
        self.output_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Ready.")
        self.progress_var = tk.DoubleVar(value=0)

        # File input row
        ttk.Label(frm, text="Video File:").grid(row=0, column=0, sticky="w")
        ttk.Entry(frm, textvariable=self.file_var, width=26).grid(row=0, column=1, padx=3)
        ttk.Button(frm, text="Browse", command=self.browse_file).grid(row=0, column=2)

        # Duration row
        ttk.Label(frm, text="Hours:").grid(row=1, column=0, sticky="e", pady=4)
        ttk.Spinbox(frm, from_=0, to=99, width=5, textvariable=self.hours_var).grid(row=1, column=1, sticky="w")
        ttk.Label(frm, text="Minutes:").grid(row=1, column=1, sticky="e", padx=(50,0))
        ttk.Spinbox(frm, from_=0, to=59, width=5, textvariable=self.minutes_var).grid(row=1, column=2, sticky="w")

        # Output name
        ttk.Label(frm, text="Output Name:").grid(row=2, column=0, sticky="w", pady=4)
        ttk.Entry(frm, textvariable=self.output_var, width=26).grid(row=2, column=1, padx=3)
        ttk.Label(frm, text=".mp4").grid(row=2, column=2, sticky="w")

        # Go button and status
        ttk.Button(frm, text="Create Loop", command=self.start_loop).grid(row=3, column=1, pady=8, sticky="we")
        ttk.Label(frm, textvariable=self.status_var, foreground="#333").grid(row=4, column=0, columnspan=3, pady=7)

        # Progress bar
        self.progress = ttk.Progressbar(self, length=340, mode="determinate", variable=self.progress_var, maximum=100)
        self.progress.pack(pady=(10, 2))
        self.percent_label = ttk.Label(self, text="0%")
        self.percent_label.pack()

        # Footer
        footer = tk.Frame(self)
        footer.pack(side="bottom", fill="x", pady=(8, 16))
        ttk.Separator(footer, orient="horizontal").pack(fill="x", pady=(0,4))
        tk.Label(
            footer,
            text=COPYRIGHT,
            font=("Segoe UI", 10, "italic"),
            fg="#888",
            anchor="center"
        ).pack(fill="x", pady=(0,0))

        # Default system theme
        style = ttk.Style(self)
        style.theme_use("default")
        style.configure(".", font=("Segoe UI", 11))

    def browse_file(self):
        path = filedialog.askopenfilename(
            title="Select video",
            filetypes=[("MP4 files","*.mp4"),("All files","*.*")]
        )
        if path:
            self.file_var.set(path)
            base = os.path.splitext(os.path.basename(path))[0]
            h, m = self.hours_var.get(), self.minutes_var.get()
            self.output_var.set(f"{base}_looped_{h}h{m}m")

    def start_loop(self):
        src = self.file_var.get()
        hours = self.hours_var.get()
        mins = self.minutes_var.get()
        out = self.output_var.get().strip() or "output"
        out += ".mp4"
        if not src:
            messagebox.showwarning("Missing File", "Select a video file.")
            return
        total_secs = hours * 3600 + mins * 60
        if total_secs <= 0:
            messagebox.showwarning("Invalid Duration", "Set hours or minutes above zero.")
            return
        self.status_var.set("Processing…")
        self.progress_var.set(0)
        self.percent_label.config(text="0%")
        self.update()

        def task():
            try:
                # Use FFmpeg for fast looping
                cmd = [
                    "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                    "-stream_loop", "-1", "-i", src,
                    "-c", "copy", "-t", str(total_secs), out
                ]
                self.progress.config(mode="indeterminate")
                self.progress.start(10)
                proc = subprocess.Popen(cmd, stderr=subprocess.PIPE)
                proc.wait()
                self.progress.stop()
                self.progress.config(mode="determinate", variable=self.progress_var)
                if proc.returncode != 0:
                    raise RuntimeError(f"FFmpeg exited with code {proc.returncode}")
                self.progress_var.set(100)
                self.percent_label.config(text="100%")
                self.status_var.set("Done! Output: "+out)
                messagebox.showinfo("Done!", f"Created {out}")
            except Exception as e:
                self.status_var.set("Error.")
                messagebox.showerror("Error", str(e))
            finally:
                self.status_var.set("Ready.")

        threading.Thread(target=task, daemon=True).start()

if __name__ == "__main__":
    VideoLooperApp().mainloop()
