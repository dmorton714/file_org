import os
import shutil
from datetime import datetime
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox


def organize_photos_by_date(source_folder, destination_folder, photo_file_extensions):
    photos_by_date = {}

    # Iterate through all files in the source folder
    for filename in os.listdir(source_folder):
        file_path = os.path.join(source_folder, filename)
        
        # Check if the current path is a file and has a photo extension
        if os.path.isfile(file_path) and filename.lower().endswith(photo_file_extensions):
            # Get the modification time and convert it to a readable date format
            creation_time = os.path.getmtime(file_path)
            creation_date = datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d')

            # Add the file to the corresponding date in the dictionary
            if creation_date not in photos_by_date:
                photos_by_date[creation_date] = []
            photos_by_date[creation_date].append(file_path)

    # Create folders for each date and move files
    for creation_date, files in photos_by_date.items():
        date_folder_path = os.path.join(destination_folder, creation_date)
        os.makedirs(date_folder_path, exist_ok=True)
        
        for file_path in files:
            filename = os.path.basename(file_path)
            destination_path = os.path.join(date_folder_path, filename)
            
            # If a file with the same name already exists, append a counter to the filename
            if os.path.exists(destination_path):
                base, extension = os.path.splitext(filename)
                counter = 1
                while os.path.exists(destination_path):
                    new_filename = f"{base}_{counter}{extension}"
                    destination_path = os.path.join(date_folder_path, new_filename)
                    counter += 1

            # Move the file to the destination path
            shutil.move(file_path, destination_path)
            print(f"Moved: {file_path} to {destination_path}")


def select_source_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        source_folder_var.set(folder_selected)


def select_destination_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        destination_folder_var.set(folder_selected)


def run_organize_photos():
    source_folder = source_folder_var.get()
    destination_folder = destination_folder_var.get()
    photo_file_extensions = (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", 
                              ".tif", ".webp", ".cr2", ".cr3", ".nrw", ".arw", 
                              ".srf", ".sr2", ".orf", ".rw2", ".raf", ".dng",
                              ".pef", ".ptx", ".x3f", ".r3d", ".3fr", ".fff", 
                              ".mef", ".mos", ".iiq", ".kc2", ".rwz", ".crw", 
                              ".bay")
    organize_photos_by_date(source_folder, destination_folder, photo_file_extensions)
    messagebox.showinfo("Success", "Photos have been organized successfully!")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Photo.Sort")

    source_folder_var = tk.StringVar()
    destination_folder_var = tk.StringVar()

    tk.Label(root, text="Source Folder:").grid(row=0, column=0, padx=10, pady=5)
    tk.Entry(root, textvariable=source_folder_var, width=50).grid(row=0, column=1, padx=10, pady=5)
    tk.Button(root, text="Browse", command=select_source_folder).grid(row=0, column=2, padx=10, pady=5)

    tk.Label(root, text="Destination Folder:").grid(row=1, column=0, padx=10, pady=5)
    tk.Entry(root, textvariable=destination_folder_var, width=50).grid(row=1, column=1, padx=10, pady=5)
    tk.Button(root, text="Browse", command=select_destination_folder).grid(row=1, column=2, padx=10, pady=5)

    tk.Button(root, text="Organize Photos", command=run_organize_photos).grid(row=2, column=0, columnspan=3, pady=20)

    root.mainloop()
