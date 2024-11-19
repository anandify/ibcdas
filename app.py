import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # For handling images

# Functionality for buttons
def start_driving():
    messagebox.showinfo("Start Driving", "Starting driving mode...")

def emergency_services():
    messagebox.showinfo("Emergency Services", "Contacting emergency services...")

def view_recordings():
    messagebox.showinfo("Uploaded Recordings", "Displaying uploaded recordings...")

def face_recognition():
    messagebox.showinfo("Face Recognition", "Launching face recognition/authentication...")

def mood_music_player():
    messagebox.showinfo("Mood-Based Music Player", "Opening mood-based music player...")

def volume_control():
    messagebox.showinfo("Volume Control", "Launching volume and gesture-based services...")

# Initialize the main window
root = tk.Tk()
root.title("VIT_ADAS")
root.geometry("600x400")
root.resizable(False, False)

# Load the background image
background_image = Image.open("assets/background.jpg")
background_photo = ImageTk.PhotoImage(background_image)

background_label = tk.Label(root, image=background_photo)
background_label.place(relwidth=1, relheight=1)  # Cover the entire window

# Load icons
start_icon = ImageTk.PhotoImage(Image.open("assets/start_icon.png").resize((50, 50)))
emergency_icon = ImageTk.PhotoImage(Image.open("assets/emergency_icon.png").resize((50, 50)))
recordings_icon = ImageTk.PhotoImage(Image.open("assets/recordings_icon.png").resize((50, 50)))
face_icon = ImageTk.PhotoImage(Image.open("assets/face_icon.png").resize((50, 50)))
music_icon = ImageTk.PhotoImage(Image.open("assets/music_icon.png").resize((50, 50)))
volume_icon = ImageTk.PhotoImage(Image.open("assets/volume_icon.png").resize((50, 50)))

# Place buttons with icons
button_frame = tk.Frame(root, bg="white", bd=0)  # Transparent frame for buttons
button_frame.place(relx=0.5, rely=0.5, anchor="center")

# Left Column
tk.Button(button_frame, image=start_icon, command=start_driving, bd=0).grid(row=0, column=0, padx=20, pady=10)
tk.Button(button_frame, image=emergency_icon, command=emergency_services, bd=0).grid(row=1, column=0, padx=20, pady=10)
tk.Button(button_frame, image=recordings_icon, command=view_recordings, bd=0).grid(row=2, column=0, padx=20, pady=10)

# Right Column
tk.Button(button_frame, image=face_icon, command=face_recognition, bd=0).grid(row=0, column=1, padx=20, pady=10)
tk.Button(button_frame, image=music_icon, command=mood_music_player, bd=0).grid(row=1, column=1, padx=20, pady=10)
tk.Button(button_frame, image=volume_icon, command=volume_control, bd=0).grid(row=2, column=1, padx=20, pady=10)

# Run the app
root.mainloop()
