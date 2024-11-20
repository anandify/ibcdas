import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess
# Functionality for buttons
def start_driving():
    try:
        subprocess.Popen(['python', 'traffic-sign-recognition.py'], shell=True)
        messagebox.showinfo("Start Driving", "Traffic sign recognition started.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to start traffic sign recognition: {e}")

def emergency_services():
    # Create a new full-screen window for emergency services
    emergency_window = tk.Toplevel(root)
    
    # Get screen dimensions
    screen_width = emergency_window.winfo_screenwidth()
    screen_height = emergency_window.winfo_screenheight()
    
    # Calculate window size (90% of screen size)
    window_width = int(screen_width * 0.9)
    window_height = int(screen_height * 0.9)
    
    # Calculate position to center the window
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2
    
    # Set window geometry
    emergency_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    
    # Load the SOS image
    sos_image = Image.open("assets/sos.png")
    
    # Resize image to fit the window while maintaining aspect ratio
    sos_photo = ImageTk.PhotoImage(sos_image.resize((window_width, window_height), Image.LANCZOS))
    
    # Create a label to display the image
    sos_label = tk.Label(emergency_window, image=sos_photo)
    sos_label.image = sos_photo  # Keep a reference to prevent garbage collection
    sos_label.pack(fill=tk.BOTH, expand=True)
    
    # Add a way to close the emergency window
    def close_emergency():
        emergency_window.destroy()
    
    # Bind the Escape key to close the window
    emergency_window.bind('<Escape>', lambda e: close_emergency())
    
    # Optional: Add a close button
    close_button = tk.Button(emergency_window, text="Close Emergency Screen", command=close_emergency)
    close_button.pack(side=tk.BOTTOM, pady=20)

def view_recordings():
    messagebox.showinfo("Uploaded Recordings", "Displaying uploaded recordings...")

def face_recognition():
    messagebox.showinfo("Face Recognition", "Launching face recognition/authentication...")

def mood_music_player():
    messagebox.showinfo("Mood-Based Music Player", "Opening mood-based music player...")

def volume_control():
    try:
        subprocess.Popen(['python', 'Volume_Control.py'], shell=True)
        messagebox.showinfo("Volume Control", "Launching volume and gesture-based services...")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to do volume control: {e}")


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
volume_icon = ImageTk.PhotoImage(Image.open("assets/volume_icon.png").resize((100, 100)))
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
