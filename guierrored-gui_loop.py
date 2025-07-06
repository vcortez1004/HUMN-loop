import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import os, sys
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.compositing.CompositeVideoClip import concatenate_videoclips

class VideoLooperApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("HUMN Video Looper")
        self.geometry("480x340")
        self.resizable(False, False)

        # Where is the logo?
        if getattr(sys, 'frozen', False):
            base_dir = sys._MEIPASS
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))

        logo_path = os.path.join(base_dir, "humn_logo.png")
        try:
            logo_img = tk.PhotoImage(file=logo_path)
            logo_lbl = tk.Label(self, image=logo_img)
            logo_lbl.image = logo_img  # keep a reference!
            logo_lbl.pack(pady=(14, 6))
        except Exception as e:
            print(f"Logo not loaded from {logo_path}: {e}")

        frm = ttk.Frame(self)
        frm.pack(fill="both", expand=True, padx=30, pady=8)

        # Variables
        self.file_var = tk.StringVar()
        self.hours_var = tk.IntVar(value=12)
        self.minutes_var = tk.IntVar(value=0)
        self.output_var = tk.StringVar()
        self.speed_var = tk.StringVar(value="medium")
        self.status_var = tk.StringVar(value="Ready.")

        # Row 1: File
        ttk.Label(frm, text="Video File:").grid(row=0, column=0, sticky="w")
        ttk.Entry(frm, textvariable=self.file_var, width=26).grid(row=0, column=1, padx=3)
        ttk.Button(frm, text="Browse", command=self.browse_file).grid(row=0, column=2)

        # Row 2: Hours & Minutes
        ttk.Label(frm, text="Hours:").grid(row=1, column=0, sticky="e", pady=4)
        ttk.Spinbox(frm, from_=0, to=99, width=5, textvariable=self.hours_var).grid(row=1, column=1, sticky="w")
        ttk.Label(frm, text="Minutes:").grid(row=1, column=1, sticky="e", padx=(50,0))
        ttk.Spinbox(frm, from_=0, to=59, width=5, textvariable=self.minutes_var).grid(row=1, column=2, sticky="w")

        # Row 3: Encoding Speed
        ttk.Label(frm, text="Encoding Speed:").grid(row=2, column=0, sticky="e")
        speed_choices = ["ultrafast", "superfast", "fast", "medium", "slow", "veryslow"]
        ttk.Combobox(frm, textvariable=self.speed_var, values=speed_choices, width=10, state="readonly").grid(row=2, column=1, sticky="w", pady=2)

        # Row 4: Output
        ttk.Label(frm, text="Output Name:").grid(row=3, column=0, sticky="w")
        ttk.Entry(frm, textvariable=self.output_var, width=26).grid(row=3, column=1, padx=3)
        ttk.Label(frm, text=".mp4").grid(row=3, column=2, sticky="w")

        # Row 5: Go Button & Status
        ttk.Button(frm, text="Create Loop", command=self.start_loop).grid(row=4, column=1, pady=8, sticky="we")
        ttk.Label(frm, textvariable=self.status_var, foreground="#333").grid(row=5, column=0, columnspan=3, pady=7)

        # Remove ALL theme/color overrides: use OS default
        style = ttk.Style(self)
        style.theme_use("default")
        # Optionally tweak font size only
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
        speed = self.speed_var.get()
        out = out + ".mp4"
        if not src:
            messagebox.showwarning("Missing File", "Select a video file.")
            return
        total_secs = hours*3600 + mins*60
        if total_secs <= 0:
            messagebox.showwarning("Invalid Duration", "Set hours or minutes above zero.")
            return
        self.status_var.set("Processing…")
        self.update()
        def task():
            try:
                clip = VideoFileClip(src)
                loops = int(total_secs // clip.duration) + 1
                final_clip = final_clip.subclip(0, desired_duration)
                final.write_videofile(out, codec="libx264", audio_codec="aac", threads=4, preset=speed)
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
