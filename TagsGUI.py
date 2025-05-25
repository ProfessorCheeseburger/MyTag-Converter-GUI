import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import json
import os
import sys
import subprocess
import threading

class MusicTagsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MyTag Extractor and Converter")
        self.root.geometry("600x250")  # Shrink the window size
        
        if getattr(sys, 'frozen', False):
            application_path = sys._MEIPASS
        elif __file__:
            application_path = os.path.dirname(__file__)
        
        self.root.iconbitmap(default=os.path.join(application_path, 'images/rekordbox.ico'))

        self.config_file = 'config.json'  # Default config file

        # Load config data
        self.load_config()

        # Create widgets
        self.create_widgets()

    def load_config(self):
        """Load the configuration from the JSON file."""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        else:
            self.config = {
                "use_rekordbox_xml": False,
                "rekordbox_db_path": "/path/to/exported/rekordbox.xml",
                "music_directory": "/path/to/your/music/directory",
                "mytag_db_file": "MyTags.xml",
                "tag_delimiter": " / "
            }
            self.add_default_categories()
            
def add_default_categories(self):
    """Add the default categories if none exist."""
    default_categories = {
        "Genre": {
            "tags": ["House", "Trap", "Dubstep", "Disco", "Drum and Bass"],
            "rekordbox_field": "Genre",
            "mp3_metadata_field": "GENRE",
            "flac_metadata_field": "GENRE"
        },
        "Components": {
            "tags": ["Synth", "Piano", "Kick", "Hi Hat"],
            "rekordbox_field": "Composer",
            "mp3_metadata_field": "COMPOSER",
            "flac_metadata_field": "COMPOSER"
        },
        "Situation": {
            "tags": ["Warm Up", "Building", "Peak Time", "After Hours", "Lounge", "House Party"],
            "rekordbox_field": "Label",
            "mp3_metadata_field": "LABEL",
            "flac_metadata_field": "LABEL"
        },
        "Mood": {
            "tags": ["Happy", "Melancholy", "Emotional", "Hype", "Angry"],
            "rekordbox_field": "Comments",
            "mp3_metadata_field": "COMMENT",
            "flac_metadata_field": "COMMENT"
        }
    }
    
    self.config["categories"] = default_categories
    self.save_config()

    def save_config(self):
        """Save the current configuration to the JSON file."""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=4)

    def create_widgets(self):
        """Create the GUI widgets."""
        self.create_file_selectors()
        self.create_buttons()

    def create_file_selectors(self):
        """Create the file selectors for Rekordbox XML, music directory, and output XML."""
        
        # Rekordbox XML Path
        self.rekordbox_label = tk.Label(self.root, text="Rekordbox XML Path:")
        self.rekordbox_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.rekordbox_path = tk.Entry(self.root, width=50)
        self.rekordbox_path.insert(0, self.config.get("rekordbox_db_path", ""))
        self.rekordbox_path.grid(row=0, column=1, padx=10, pady=5)
        self.rekordbox_path.bind("<KeyRelease>", self.on_file_path_change)

        self.rekordbox_browse = tk.Button(self.root, text="Browse", command=self.browse_rekordbox)
        self.rekordbox_browse.grid(row=0, column=2, padx=10, pady=5)

        # Music Directory Path
        self.music_dir_label = tk.Label(self.root, text="Music Directory Path:")
        self.music_dir_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.music_dir_path = tk.Entry(self.root, width=50)
        self.music_dir_path.insert(0, self.config.get("music_directory", ""))
        self.music_dir_path.grid(row=1, column=1, padx=10, pady=5)
        self.music_dir_path.bind("<KeyRelease>", self.on_file_path_change)

        self.music_dir_browse = tk.Button(self.root, text="Browse", command=self.browse_music_dir)
        self.music_dir_browse.grid(row=1, column=2, padx=10, pady=5)

        # Output XML Path
        self.output_xml_label = tk.Label(self.root, text="MyTags Database XML Path:")
        self.output_xml_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.output_xml_path = tk.Entry(self.root, width=50)
        self.output_xml_path.insert(0, self.config.get("mytag_db_file", ""))
        self.output_xml_path.grid(row=2, column=1, padx=10, pady=5)
        self.output_xml_path.bind("<KeyRelease>", self.on_file_path_change)

        self.output_xml_browse = tk.Button(self.root, text="Browse", command=self.browse_output_xml)
        self.output_xml_browse.grid(row=2, column=2, padx=10, pady=5)
        
        # Tag Delimiter
        self.tag_delimiter_label = tk.Label(self.root, text="Tag Delimiter:")
        self.tag_delimiter_label.grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.tag_delimiter = tk.Entry(self.root, width=5)
        self.tag_delimiter.insert(0, self.config.get("tag_delimiter", ""))
        self.tag_delimiter.grid(row=3, column=1, sticky='w', padx=10, pady=5)
        self.tag_delimiter.bind("<KeyRelease>", self.on_file_path_change)

        # Use Rekordbox XML Checkbox
        self.use_rekordbox_var = tk.BooleanVar(value=self.config.get("use_rekordbox_xml", False))
        self.use_rekordbox_checkbox = tk.Checkbutton(self.root, text="Use Rekordbox XML", variable=self.use_rekordbox_var, command=self.on_use_rekordbox_change)
        self.use_rekordbox_checkbox.grid(row=4, column=0, columnspan=3, padx=10, pady=5)

    def on_file_path_change(self, event):
        """Update the corresponding value in config when a file path is modified."""
        self.config["rekordbox_db_path"] = self.rekordbox_path.get()
        self.config["music_directory"] = self.music_dir_path.get()
        self.config["mytag_db_file"] = self.output_xml_path.get()
        self.config["tag_delimiter"] = self.tag_delimiter.get()
        self.save_config()

    def on_use_rekordbox_change(self):
        """Update the 'use_rekordbox_xml' value in the config when the checkbox is toggled."""
        self.config["use_rekordbox_xml"] = self.use_rekordbox_var.get()
        self.save_config()

    def create_buttons(self):
        """Create the 'MyTags' and 'Run Script' buttons side by side."""
        button_frame = tk.Frame(self.root)
        button_frame.grid(row=5, column=0, columnspan=3, pady=20)

        # MyTags Button
        self.mytags_button = tk.Button(button_frame, text="MyTags", command=self.open_mytags_window)
        self.mytags_button.grid(row=0, column=0, padx=10, pady=5)

        # Run Script Button
        self.run_button = tk.Button(button_frame, text="Run Script", command=self.run_script)
        self.run_button.grid(row=0, column=1, padx=10, pady=5)

    def browse_rekordbox(self):
        """Browse for the Rekordbox XML file."""
        file_path = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
        if file_path:
            self.rekordbox_path.delete(0, tk.END)
            self.rekordbox_path.insert(0, file_path)
            self.on_file_path_change(None)  # Trigger config update

    def browse_music_dir(self):
        """Browse for the music directory."""
        dir_path = filedialog.askdirectory()
        if dir_path:
            self.music_dir_path.delete(0, tk.END)
            self.music_dir_path.insert(0, dir_path)
            self.on_file_path_change(None)  # Trigger config update

    def browse_output_xml(self):
        """Browse for the output XML file."""
        file_path = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("XML files", "*.xml")])
        if file_path:
            self.output_xml_path.delete(0, tk.END)
            self.output_xml_path.insert(0, file_path)
            self.on_file_path_change(None)  # Trigger config update

    def open_mytags_window(self):
        """Open the MyTags window to modify categories."""
        prefs_window = tk.Toplevel(self.root)
        prefs_window.title("MyTags")
        prefs_window.geometry("600x400")

        notebook = ttk.Notebook(prefs_window)
        notebook.pack(fill=tk.BOTH, expand=True)

        # Add default categories if none exist
        if not self.config["categories"]:
            self.add_default_categories()

        # Create tabs for each category
        for category in list(self.config["categories"].keys()):
            tab = ttk.Frame(notebook)
            notebook.add(tab, text=category)

            self.create_category_tab(tab, category)

        prefs_window.mainloop()

def create_category_tab(self, parent, category):
    """Create the input fields for a specific category."""
    category_info = self.config["categories"].get(category, {})

    # Category Name
    tk.Label(parent, text="Category:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
    category_name_entry = tk.Entry(parent, width=30)
    category_name_entry.insert(0, category)
    category_name_entry.grid(row=0, column=1, padx=10, pady=5)

    # Tags
    tk.Label(parent, text="Tags (comma separated):").grid(row=1, column=0, sticky="w", padx=10, pady=5)
    tags_entry = tk.Entry(parent, width=30)
    tags_entry.insert(0, ", ".join(category_info.get("tags", [])))
    tags_entry.grid(row=1, column=1, padx=10, pady=5)

    # Rekordbox Field (Dropdown)
    rekordbox_field_options = ["Genre", "Composer", "Label", "Comments"]  # Predefined list for Rekordbox fields
    tk.Label(parent, text="Rekordbox Field:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
    rekordbox_field_combobox = ttk.Combobox(parent, values=rekordbox_field_options, width=30)
    rekordbox_field_combobox.set(category_info.get("rekordbox_field", ""))
    rekordbox_field_combobox.grid(row=2, column=1, padx=10, pady=5)

    # MP3 Metadata Field (Dropdown)
    mp3_metadata_field_options = ["album", "bpm", "compilation", "composer", "copyright", "encodedby", "lyricist", "length", "media", "mood", "grouping", "title", "version", "artist", "albumartist", "conductor", "arranger", "discnumber", "organization", "tracknumber", "author", "albumartistsort", "albumsort", "composersort", "artistsort", "titlesort", "isrc", "discsubtitle", "language", "genre", "date", "originaldate", "performer", "website", "releasecountry", "asin", "barcode", "catalognumber"]  # Predefined list for MP3 fields
    tk.Label(parent, text="MP3 Metadata Field:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
    mp3_metadata_field_combobox = ttk.Combobox(parent, values=mp3_metadata_field_options, width=30)
    mp3_metadata_field_combobox.set(category_info.get("mp3_metadata_field", ""))
    mp3_metadata_field_combobox.grid(row=3, column=1, padx=10, pady=5)

    # FLAC Metadata Field (Dropdown)
    flac_metadata_field_options = ["GENRE", "COMPOSER", "LABEL", "COMMENT"]  # Predefined list for FLAC fields
    tk.Label(parent, text="FLAC Metadata Field:").grid(row=4, column=0, sticky="w", padx=10, pady=5)
    flac_metadata_field_combobox = ttk.Combobox(parent, values=flac_metadata_field_options, width=30)
    flac_metadata_field_combobox.set(category_info.get("flac_metadata_field", ""))
    flac_metadata_field_combobox.grid(row=4, column=1, padx=10, pady=5)

    # Save Button
    def save_category():
        # Save the new category data
        self.config["categories"][category_name_entry.get()] = {
            "tags": [tag.strip() for tag in tags_entry.get().split(",")],
            "rekordbox_field": rekordbox_field_combobox.get(),
            "mp3_metadata_field": mp3_metadata_field_combobox.get(),
            "flac_metadata_field": flac_metadata_field_combobox.get()
        }
        self.save_config()

        # Update the tab name
        notebook.tab(notebook.index(tab), text=category_name_entry.get())

    save_button = tk.Button(parent, text="Save", command=save_category)
    save_button.grid(row=5, column=0, columnspan=2, pady=10)


    def run_script(self):
        """Run the script in a separate thread."""
        self.update_config()  # Update config with current values

        # Run the script in a background thread
        def thread_func():
            try:
                self.root.title("Running... Please Wait") # Change window title to indicate script is running
                result = subprocess.run(['python', 'script/mytag_converter.py'], capture_output=True, text=True)
                output = result.stdout + "\n" + result.stderr
                self.root.title("MyTag Extractor and Converter")
                self.show_popup(output)
            except Exception as e:
                self.show_popup(f"Error: {str(e)}")

        thread = threading.Thread(target=thread_func)
        thread.start()

    def update_config(self):
        """Update the configuration with the current GUI values."""
        self.config["rekordbox_db_path"] = self.rekordbox_path.get()
        self.config["music_directory"] = self.music_dir_path.get()
        self.config["mytag_db_file"] = self.output_xml_path.get()
        self.config["use_rekordbox_xml"] = self.use_rekordbox_var.get()
        self.config["tag_delimiter"] = self.tag_delimiter.get()

    def show_popup(self, message):
        """Show a popup window with the output or error."""
        # Update GUI safely by scheduling it to the main thread
        self.root.after(0, self._show_popup, message)

    def _show_popup(self, message):
        """Create the popup window in the main thread."""
        popup = tk.Toplevel(self.root)
        popup.title("Script Output")
        popup.geometry("400x300")
        output_text = tk.Text(popup, wrap=tk.WORD)
        output_text.insert(tk.END, message)
        output_text.config(state=tk.DISABLED)
        output_text.pack(padx=10, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicTagsApp(root)
    root.mainloop()
