import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

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

def update_background(event):
    new_width = root.winfo_width()
    new_height = root.winfo_height()
    resized_image = background_image.resize((new_width, new_height), Image.ANTIALIAS)
    new_background_photo = ImageTk.PhotoImage(resized_image)
    background_label.config(image=new_background_photo)
    background_label.image = new_background_photo

# Initialize the main window
root = tk.Tk()
root.title("VIT_ADAS")
root.geometry("600x400")
root.state("zoomed")  # Start maximized

# Load the background image
background_image = Image.open("assets/background2.jpg")
background_photo = ImageTk.PhotoImage(background_image)

background_label = tk.Label(root, image=background_photo)
background_label.place(relwidth=1, relheight=1)  # Cover the entire window

# Bind the resizing event to update the background
root.bind("<Configure>", update_background)

# Load icons
start_icon = ImageTk.PhotoImage(Image.open("assets/start_icon.png").resize((100, 100)))
emergency_icon = ImageTk.PhotoImage(Image.open("assets/emergency_icon.png").resize((100, 100)))
recordings_icon = ImageTk.PhotoImage(Image.open("assets/recordings_icon.png").resize((100, 100)))
face_icon = ImageTk.PhotoImage(Image.open("assets/face_icon.png").resize((100, 100)))
music_icon = ImageTk.PhotoImage(Image.open("assets/music_icon.png").resize((100, 100)))
volume_icon = ImageTk.PhotoImage(Image.open("assets/volume_icon2.png").resize((100, 100)))
# Place buttons with icons
left_frame = tk.Frame(root, bg="white", bd=0)
right_frame = tk.Frame(root, bg="white", bd=0)

left_frame.place(relx=0.15, rely=0.5, anchor="center")
right_frame.place(relx=0.85, rely=0.5, anchor="center")

# Left Column
tk.Button(left_frame, image=start_icon, command=start_driving, bd=0).pack(pady=10)
tk.Button(left_frame, image=emergency_icon, command=emergency_services, bd=0).pack(pady=10)
tk.Button(left_frame, image=recordings_icon, command=view_recordings, bd=0).pack(pady=10)

# Right Column
tk.Button(right_frame, image=face_icon, command=face_recognition, bd=0).pack(pady=10)
tk.Button(right_frame, image=music_icon, command=mood_music_player, bd=0).pack(pady=10)
tk.Button(right_frame, image=volume_icon, command=volume_control, bd=0).pack(pady=10)

# Run the app
root.mainloop()