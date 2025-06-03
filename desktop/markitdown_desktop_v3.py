#!/usr/bin/env python3
"""
MarkItDown Desktop App - Multi-File Version with ZIP Export
Batch processing, multi-file upload, ZIP download of markdown files

INSTALLATION & START:
1. Save this file as 'markitdown_desktop.py'
2. Open terminal and run: python markitdown_desktop.py
3. Start converting - MarkItDown is already installed!

NEW FEATURES:
- Multi-file selection and processing
- Batch conversion with progress tracking
- ZIP download with all markdown files
- Individual file management
- Folder structure preservation

SUPPORTED FORMATS:
- Office: Word, Excel, PowerPoint
- PDF: All PDF documents  
- Images: JPG, PNG, GIF (with OCR)
- Audio: MP3, WAV (with transcription)
- Web: HTML, CSV, JSON, XML
- Archives: ZIP files
- E-Books: EPUB

Version: 3.0 (Multi-File Support)
Developer: Rudolf Wagner
Kindergarten Project: https://www.paypal.com/donate/?hosted_button_id=PAGH54TWEXP54
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import sys
import subprocess
import threading
import tempfile
import webbrowser
import platform
import zipfile
from datetime import datetime
import json

# App Constants
APP_NAME = "MarkItDown Desktop"
APP_VERSION = "3.0"

def check_and_install_dependencies():
    """Check and install dependencies before GUI start"""
    print("Checking MarkItDown installation...")
    
    try:
        from markitdown import MarkItDown
        print("✅ MarkItDown is already installed!")
        return True
    except ImportError:
        print("❌ MarkItDown not found.")
        
        # Ask user in terminal
        response = input("\nShould MarkItDown be installed automatically? (y/n): ").lower().strip()
        
        if response in ['y', 'yes', 'j', 'ja', '']:
            print("\nInstalling MarkItDown...")
            try:
                # Installation with visible output
                cmd = [sys.executable, "-m", "pip", "install", "--upgrade", "markitdown[all]"]
                print(f"Running: {' '.join(cmd)}")
                
                result = subprocess.run(cmd, check=True, text=True)
                
                print("✅ Installation completed!")
                print("Testing installation...")
                
                # Test import
                from markitdown import MarkItDown
                print("✅ MarkItDown successfully installed and tested!")
                return True
                
            except subprocess.CalledProcessError as e:
                print(f"❌ Installation failed: {e}")
                print("Try manually: pip install 'markitdown[all]'")
                return False
            except ImportError:
                print("❌ Installation was successful, but import fails.")
                print("Please restart the application.")
                return False
        else:
            print("❌ Installation cancelled.")
            print("The app cannot function without MarkItDown.")
            print("   Install it manually with: pip install 'markitdown[all]'")
            return False

class FileItem:
    """Represents a file in the processing queue"""
    def __init__(self, filepath):
        self.filepath = filepath
        self.filename = os.path.basename(filepath)
        self.status = "Pending"  # Pending, Processing, Completed, Error
        self.markdown_content = ""
        self.error_message = ""
        self.filesize = os.path.getsize(filepath) if os.path.exists(filepath) else 0

class MarkItDownApp:
    """Main application with multi-file support"""
    
    def __init__(self, root):
        self.root = root
        self.file_queue = []  # List of FileItem objects
        self.processing = False
        self.current_processing_index = 0
        
        # Initialize MarkItDown
        try:
            from markitdown import MarkItDown
            self.markitdown = MarkItDown()
            self.markitdown_available = True
        except ImportError:
            self.markitdown = None
            self.markitdown_available = False
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup user interface"""
        # Window configuration
        self.root.title(f"{APP_NAME} v{APP_VERSION} - Multi-File")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f0f0f0')
        
        # Styles
        style = ttk.Style()
        if 'clam' in style.theme_names():
            style.theme_use('clam')
        
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ttk.Label(header_frame, text="MarkItDown Desktop - Multi-File", 
                               font=('Arial', 18, 'bold'))
        title_label.pack(side=tk.LEFT)
        
        # Version and Author
        info_frame = ttk.Frame(header_frame)
        info_frame.pack(side=tk.RIGHT)
        
        version_label = ttk.Label(info_frame, text=f"v{APP_VERSION}", 
                                 font=('Arial', 10))
        version_label.pack()
        
        author_label = ttk.Label(info_frame, text="by Rudolf Wagner", 
                                font=('Arial', 9), 
                                foreground='#1976d2', cursor='hand2')
        author_label.pack()
        author_label.bind('<Button-1>', self.open_linkedin)
        
        donate_label = ttk.Label(info_frame, text="Support Kindergarten Project", 
                                font=('Arial', 8), 
                                foreground='#e74c3c', cursor='hand2')
        donate_label.pack(pady=(2, 0))
        donate_label.bind('<Button-1>', self.open_donation)
        
        subtitle_label = ttk.Label(header_frame, 
                                  text="Batch convert multiple files to Markdown",
                                  font=('Arial', 11))
        subtitle_label.pack(side=tk.LEFT, padx=(20, 0))
        
        # Content area with 3 columns
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        content_frame.columnconfigure(0, weight=1)  # File queue
        content_frame.columnconfigure(1, weight=1)  # Controls
        content_frame.columnconfigure(2, weight=2)  # Preview
        content_frame.rowconfigure(0, weight=1)
        
        # Left panel - File Queue
        self.create_file_queue_panel(content_frame)
        
        # Middle panel - Controls
        self.create_controls_panel(content_frame)
        
        # Right panel - Preview
        self.create_preview_panel(content_frame)
        
        # Status bar
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.status_bar = ttk.Label(status_frame, text="Ready for multi-file processing", relief='sunken')
        self.status_bar.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Overall progress
        self.overall_progress = ttk.Progressbar(status_frame, mode='determinate', length=200)
        self.overall_progress.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Check if MarkItDown is available
        if not self.markitdown_available:
            self.show_error_message()
    
    def create_file_queue_panel(self, parent):
        """Left panel for file queue management"""
        queue_frame = ttk.LabelFrame(parent, text="File Queue", padding="15")
        queue_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        queue_frame.columnconfigure(0, weight=1)
        queue_frame.rowconfigure(1, weight=1)
        
        # Queue controls
        queue_controls = ttk.Frame(queue_frame)
        queue_controls.pack(fill=tk.X, pady=(0, 10))
        queue_controls.columnconfigure(1, weight=1)
        
        add_files_btn = ttk.Button(queue_controls, text="Add Files", 
                                  command=self.add_files)
        add_files_btn.grid(row=0, column=0, padx=(0, 5))
        
        add_folder_btn = ttk.Button(queue_controls, text="Add Folder", 
                                   command=self.add_folder)
        add_folder_btn.grid(row=0, column=1, padx=(0, 5))
        
        clear_btn = ttk.Button(queue_controls, text="Clear All", 
                              command=self.clear_queue)
        clear_btn.grid(row=0, column=2, padx=(0, 5))
        
        remove_btn = ttk.Button(queue_controls, text="Remove Selected", 
                               command=self.remove_selected)
        remove_btn.grid(row=0, column=3)
        
        # File list with scrollbar
        list_frame = ttk.Frame(queue_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Treeview for file list
        columns = ('File', 'Status', 'Size')
        self.file_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        # Column headers
        self.file_tree.heading('File', text='Filename')
        self.file_tree.heading('Status', text='Status')
        self.file_tree.heading('Size', text='Size')
        
        # Column widths
        self.file_tree.column('File', width=200)
        self.file_tree.column('Status', width=80)
        self.file_tree.column('Size', width=80)
        
        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.file_tree.yview)
        self.file_tree.configure(yscrollcommand=scrollbar.set)
        
        self.file_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Bind selection event
        self.file_tree.bind('<<TreeviewSelect>>', self.on_file_select)
        
        # Queue statistics
        self.queue_stats = ttk.Label(queue_frame, text="Files: 0 | Completed: 0 | Errors: 0", 
                                    font=('Arial', 9))
        self.queue_stats.pack(pady=(10, 0))
    
    def create_controls_panel(self, parent):
        """Middle panel for processing controls"""
        controls_frame = ttk.LabelFrame(parent, text="Processing Controls", padding="15")
        controls_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        
        # Processing options
        options_frame = ttk.LabelFrame(controls_frame, text="Options", padding="10")
        options_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.preserve_structure = tk.BooleanVar(value=True)
        preserve_check = ttk.Checkbutton(options_frame, text="Preserve folder structure", 
                                        variable=self.preserve_structure)
        preserve_check.pack(anchor=tk.W)
        
        self.skip_errors = tk.BooleanVar(value=True)
        skip_check = ttk.Checkbutton(options_frame, text="Skip files with errors", 
                                    variable=self.skip_errors)
        skip_check.pack(anchor=tk.W)
        
        self.create_index = tk.BooleanVar(value=True)
        index_check = ttk.Checkbutton(options_frame, text="Create index file", 
                                     variable=self.create_index)
        index_check.pack(anchor=tk.W)
        
        # Processing buttons
        process_frame = ttk.Frame(controls_frame)
        process_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.start_btn = ttk.Button(process_frame, text="Start Batch Processing", 
                                   command=self.start_batch_processing, state='disabled')
        self.start_btn.pack(fill=tk.X, pady=(0, 5))
        
        self.stop_btn = ttk.Button(process_frame, text="Stop Processing", 
                                  command=self.stop_processing, state='disabled')
        self.stop_btn.pack(fill=tk.X, pady=(0, 5))
        
        # Export buttons
        export_frame = ttk.LabelFrame(controls_frame, text="Export Results", padding="10")
        export_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.export_zip_btn = ttk.Button(export_frame, text="Download ZIP", 
                                        command=self.export_zip, state='disabled')
        self.export_zip_btn.pack(fill=tk.X, pady=(0, 5))
        
        self.export_folder_btn = ttk.Button(export_frame, text="Save to Folder", 
                                           command=self.export_folder, state='disabled')
        self.export_folder_btn.pack(fill=tk.X, pady=(0, 5))
        
        # Current processing info
        current_frame = ttk.LabelFrame(controls_frame, text="Current Processing", padding="10")
        current_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.current_file_label = ttk.Label(current_frame, text="No file processing", 
                                           font=('Arial', 9), wraplength=200)
        self.current_file_label.pack(anchor=tk.W)
        
        self.current_progress = ttk.Progressbar(current_frame, mode='indeterminate')
        self.current_progress.pack(fill=tk.X, pady=(5, 0))
        
        # Supported formats (compact)
        formats_frame = ttk.LabelFrame(controls_frame, text="Supported Formats", padding="10")
        formats_frame.pack(fill=tk.X)
        
        formats_text = "Office, PDF, Images, Audio, Web, Archives, E-Books"
        formats_label = ttk.Label(formats_frame, text=formats_text, 
                                 font=('Arial', 9), wraplength=200)
        formats_label.pack()
        
        # Help and donate buttons
        help_frame = ttk.Frame(controls_frame)
        help_frame.pack(fill=tk.X, pady=(15, 0))
        help_frame.columnconfigure(0, weight=1)
        help_frame.columnconfigure(1, weight=1)
        
        help_btn = ttk.Button(help_frame, text="Help", command=self.show_help)
        help_btn.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 2))
        
        donate_btn = ttk.Button(help_frame, text="Donate", command=self.open_donation)
        donate_btn.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(2, 0))
    
    def create_preview_panel(self, parent):
        """Right panel for markdown preview"""
        preview_frame = ttk.LabelFrame(parent, text="Markdown Preview", padding="15")
        preview_frame.grid(row=0, column=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.rowconfigure(1, weight=1)
        
        # Preview toolbar
        toolbar_frame = ttk.Frame(preview_frame)
        toolbar_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        toolbar_frame.columnconfigure(3, weight=1)
        
        self.copy_btn = ttk.Button(toolbar_frame, text="Copy", 
                                  command=self.copy_current, state='disabled')
        self.copy_btn.grid(row=0, column=0, padx=(0, 5))
        
        self.save_btn = ttk.Button(toolbar_frame, text="Save", 
                                  command=self.save_current, state='disabled')
        self.save_btn.grid(row=0, column=1, padx=(0, 5))
        
        self.preview_btn = ttk.Button(toolbar_frame, text="HTML Preview", 
                                     command=self.preview_current, state='disabled')
        self.preview_btn.grid(row=0, column=2, padx=(0, 5))
        
        # File selector for preview
        self.preview_selector = ttk.Combobox(toolbar_frame, state='readonly', width=20)
        self.preview_selector.grid(row=0, column=4, padx=(5, 0))
        self.preview_selector.bind('<<ComboboxSelected>>', self.on_preview_select)
        
        # Preview text area
        self.preview_text = scrolledtext.ScrolledText(preview_frame, 
                                                     wrap=tk.WORD, 
                                                     font=('Monaco', 10) if platform.system() == 'Darwin' else ('Consolas', 9),
                                                     state='disabled',
                                                     bg='white',
                                                     fg='#333333')
        self.preview_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Preview stats
        self.preview_stats = ttk.Label(preview_frame, text="Select a file to preview", 
                                      font=('Arial', 9))
        self.preview_stats.grid(row=2, column=0, sticky=tk.W, pady=(10, 0))
    
    def add_files(self):
        """Add multiple files to queue"""
        if not self.markitdown_available:
            messagebox.showerror("Error", "MarkItDown is not available!")
            return
        
        filetypes = [
            ('All Files', '*.*'),
            ('PDF Documents', '*.pdf'),
            ('Office Documents', '*.docx;*.doc;*.xlsx;*.xls;*.pptx;*.ppt'),
            ('Images', '*.jpg;*.jpeg;*.png;*.gif'),
            ('Audio', '*.mp3;*.wav'),
            ('Web Files', '*.html;*.csv;*.json;*.xml'),
            ('Archives', '*.zip'),
            ('E-Books', '*.epub')
        ]
        
        try:
            filenames = filedialog.askopenfilenames(
                title="Select files for batch conversion",
                filetypes=filetypes
            )
            
            if filenames:
                added_count = 0
                for filename in filenames:
                    if not any(item.filepath == filename for item in self.file_queue):
                        file_item = FileItem(filename)
                        self.file_queue.append(file_item)
                        added_count += 1
                
                self.update_file_tree()
                self.update_queue_stats()
                self.update_buttons()
                self.update_status(f"Added {added_count} files to queue")
                
        except Exception as e:
            messagebox.showerror("Error", f"Could not add files: {str(e)}")
    
    def add_folder(self):
        """Add all supported files from a folder"""
        if not self.markitdown_available:
            messagebox.showerror("Error", "MarkItDown is not available!")
            return
        
        folder = filedialog.askdirectory(title="Select folder to add files from")
        
        if folder:
            supported_extensions = {
                '.pdf', '.docx', '.doc', '.xlsx', '.xls', '.pptx', '.ppt',
                '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff',
                '.mp3', '.wav', '.m4a', '.flac',
                '.html', '.htm', '.csv', '.json', '.xml',
                '.zip', '.epub', '.txt'
            }
            
            added_count = 0
            for root, dirs, files in os.walk(folder):
                for file in files:
                    if os.path.splitext(file)[1].lower() in supported_extensions:
                        filepath = os.path.join(root, file)
                        if not any(item.filepath == filepath for item in self.file_queue):
                            file_item = FileItem(filepath)
                            self.file_queue.append(file_item)
                            added_count += 1
            
            self.update_file_tree()
            self.update_queue_stats()
            self.update_buttons()
            self.update_status(f"Added {added_count} files from folder")
    
    def clear_queue(self):
        """Clear all files from queue"""
        if self.processing:
            messagebox.showwarning("Warning", "Cannot clear queue while processing!")
            return
        
        if self.file_queue:
            result = messagebox.askyesno("Confirm", "Clear all files from queue?")
            if result:
                self.file_queue.clear()
                self.update_file_tree()
                self.update_queue_stats()
                self.update_buttons()
                self.update_preview_selector()
                self.clear_preview()
                self.update_status("Queue cleared")
    
    def remove_selected(self):
        """Remove selected files from queue"""
        if self.processing:
            messagebox.showwarning("Warning", "Cannot remove files while processing!")
            return
        
        selected_items = self.file_tree.selection()
        if not selected_items:
            messagebox.showinfo("Info", "No files selected!")
            return
        
        # Get indices of selected items
        indices_to_remove = []
        for item in selected_items:
            index = self.file_tree.index(item)
            indices_to_remove.append(index)
        
        # Remove in reverse order to maintain indices
        for index in sorted(indices_to_remove, reverse=True):
            if 0 <= index < len(self.file_queue):
                del self.file_queue[index]
        
        self.update_file_tree()
        self.update_queue_stats()
        self.update_buttons()
        self.update_preview_selector()
        self.update_status(f"Removed {len(indices_to_remove)} files")
    
    def update_file_tree(self):
        """Update the file tree display"""
        # Clear existing items
        for item in self.file_tree.get_children():
            self.file_tree.delete(item)
        
        # Add current queue items
        for file_item in self.file_queue:
            self.file_tree.insert('', 'end', values=(
                file_item.filename,
                file_item.status,
                self.format_filesize(file_item.filesize)
            ))
    
    def update_queue_stats(self):
        """Update queue statistics display"""
        total = len(self.file_queue)
        completed = sum(1 for item in self.file_queue if item.status == "Completed")
        errors = sum(1 for item in self.file_queue if item.status == "Error")
        
        self.queue_stats.config(text=f"Files: {total} | Completed: {completed} | Errors: {errors}")
        
        # Update overall progress
        if total > 0:
            progress = (completed + errors) / total * 100
            self.overall_progress.config(value=progress)
        else:
            self.overall_progress.config(value=0)
    
    def update_buttons(self):
        """Update button states based on current state"""
        has_files = len(self.file_queue) > 0
        has_completed = any(item.status == "Completed" for item in self.file_queue)
        
        if self.processing:
            self.start_btn.config(state='disabled')
            self.stop_btn.config(state='normal')
        else:
            self.start_btn.config(state='normal' if has_files else 'disabled')
            self.stop_btn.config(state='disabled')
        
        # Export buttons
        self.export_zip_btn.config(state='normal' if has_completed else 'disabled')
        self.export_folder_btn.config(state='normal' if has_completed else 'disabled')
    
    def start_batch_processing(self):
        """Start batch processing of all files in queue"""
        if not self.file_queue:
            messagebox.showinfo("Info", "No files in queue!")
            return
        
        if self.processing:
            return
        
        self.processing = True
        self.current_processing_index = 0
        self.update_buttons()
        
        # Reset all files to pending
        for item in self.file_queue:
            if item.status != "Completed":
                item.status = "Pending"
        
        self.update_file_tree()
        self.update_status("Starting batch processing...")
        
        # Start processing in thread
        thread = threading.Thread(target=self.process_queue_thread, daemon=True)
        thread.start()
    
    def process_queue_thread(self):
        """Process all files in queue (runs in separate thread)"""
        for i, file_item in enumerate(self.file_queue):
            if not self.processing:  # Check if stopped
                break
            
            if file_item.status == "Completed":
                continue  # Skip already completed files
            
            self.current_processing_index = i
            
            # Update UI in main thread
            self.root.after(0, lambda: self.update_current_processing(file_item))
            
            try:
                # Update status
                file_item.status = "Processing"
                self.root.after(0, self.update_file_tree)
                
                # Convert file
                print(f"Converting: {file_item.filepath}")
                result = self.markitdown.convert(file_item.filepath)
                markdown_content = result.text_content
                
                if not markdown_content:
                    raise Exception("No content extracted")
                
                file_item.markdown_content = markdown_content
                file_item.status = "Completed"
                print(f"Completed: {file_item.filename}")
                
            except Exception as e:
                file_item.status = "Error"
                file_item.error_message = str(e)
                print(f"Error processing {file_item.filename}: {e}")
                
                if not self.skip_errors.get():
                    # Ask user what to do
                    response = messagebox.askyesnocancel(
                        "Processing Error", 
                        f"Error processing {file_item.filename}:\n{str(e)}\n\nContinue with next file?"
                    )
                    if response is None:  # Cancel
                        self.processing = False
                        break
                    elif not response:  # No
                        self.processing = False
                        break
            
            # Update UI
            self.root.after(0, self.update_file_tree)
            self.root.after(0, self.update_queue_stats)
        
        # Processing finished
        self.root.after(0, self.processing_finished)
    
    def update_current_processing(self, file_item):
        """Update current processing display"""
        self.current_file_label.config(text=f"Processing: {file_item.filename}")
        self.current_progress.start()
    
    def processing_finished(self):
        """Called when batch processing is finished"""
        self.processing = False
        self.current_progress.stop()
        self.current_file_label.config(text="Processing completed")
        self.update_buttons()
        self.update_preview_selector()
        
        # Show summary
        completed = sum(1 for item in self.file_queue if item.status == "Completed")
        errors = sum(1 for item in self.file_queue if item.status == "Error")
        
        self.update_status(f"Batch processing completed: {completed} successful, {errors} errors")
        
        messagebox.showinfo("Processing Complete", 
                           f"Batch processing finished!\n\n"
                           f"Successfully converted: {completed} files\n"
                           f"Errors: {errors} files\n\n"
                           f"You can now export the results as ZIP or to a folder.")
    
    def stop_processing(self):
        """Stop batch processing"""
        if self.processing:
            result = messagebox.askyesno("Confirm", "Stop batch processing?")
            if result:
                self.processing = False
                self.update_status("Processing stopped by user")
    
    def export_zip(self):
        """Export all completed markdown files as ZIP"""
        completed_files = [item for item in self.file_queue if item.status == "Completed"]
        
        if not completed_files:
            messagebox.showinfo("Info", "No completed files to export!")
            return
        
        # Choose save location
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_name = f"markitdown_export_{timestamp}.zip"
        
        zip_path = filedialog.asksaveasfilename(
            title="Save ZIP file",
            defaultextension=".zip",
            initialvalue=default_name,
            filetypes=[('ZIP files', '*.zip'), ('All files', '*.*')]
        )
        
        if not zip_path:
            return
        
        try:
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Add individual markdown files
                for file_item in completed_files:
                    # Create markdown filename
                    base_name = os.path.splitext(file_item.filename)[0]
                    md_filename = f"{base_name}.md"
                    
                    # Preserve folder structure if enabled
                    if self.preserve_structure.get():
                        # Try to preserve relative path structure
                        try:
                            common_path = os.path.commonpath([item.filepath for item in self.file_queue])
                            relative_path = os.path.relpath(file_item.filepath, common_path)
                            relative_dir = os.path.dirname(relative_path)
                            if relative_dir:
                                md_filename = os.path.join(relative_dir, f"{base_name}.md")
                        except:
                            pass  # Use simple filename if path calculation fails
                    
                    # Add markdown content to ZIP
                    zipf.writestr(md_filename, file_item.markdown_content)
                
                # Create index file if enabled
                if self.create_index.get():
                    index_content = self.create_index_content(completed_files)
                    zipf.writestr("README.md", index_content)
                
                # Add conversion summary
                summary_content = self.create_summary_content()
                zipf.writestr("conversion_summary.json", summary_content)
            
            self.update_status(f"ZIP exported: {os.path.basename(zip_path)}")
            messagebox.showinfo("Export Complete", 
                               f"Successfully exported {len(completed_files)} files to ZIP!\n\n"
                               f"Saved as: {os.path.basename(zip_path)}")
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Could not create ZIP file: {str(e)}")
    
    def export_folder(self):
        """Export all completed markdown files to a folder"""
        completed_files = [item for item in self.file_queue if item.status == "Completed"]
        
        if not completed_files:
            messagebox.showinfo("Info", "No completed files to export!")
            return
        
        # Choose folder
        folder_path = filedialog.askdirectory(title="Select export folder")
        
        if not folder_path:
            return
        
        try:
            # Create export subfolder with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            export_folder = os.path.join(folder_path, f"markitdown_export_{timestamp}")
            os.makedirs(export_folder, exist_ok=True)
            
            # Save individual markdown files
            for file_item in completed_files:
                base_name = os.path.splitext(file_item.filename)[0]
                md_filename = f"{base_name}.md"
                
                # Preserve folder structure if enabled
                if self.preserve_structure.get():
                    try:
                        common_path = os.path.commonpath([item.filepath for item in self.file_queue])
                        relative_path = os.path.relpath(file_item.filepath, common_path)
                        relative_dir = os.path.dirname(relative_path)
                        if relative_dir:
                            target_dir = os.path.join(export_folder, relative_dir)
                            os.makedirs(target_dir, exist_ok=True)
                            md_filepath = os.path.join(target_dir, f"{base_name}.md")
                        else:
                            md_filepath = os.path.join(export_folder, md_filename)
                    except:
                        md_filepath = os.path.join(export_folder, md_filename)
                else:
                    md_filepath = os.path.join(export_folder, md_filename)
                
                # Write markdown file
                with open(md_filepath, 'w', encoding='utf-8') as f:
                    f.write(file_item.markdown_content)
            
            # Create index file if enabled
            if self.create_index.get():
                index_content = self.create_index_content(completed_files)
                with open(os.path.join(export_folder, "README.md"), 'w', encoding='utf-8') as f:
                    f.write(index_content)
            
            # Create summary file
            summary_content = self.create_summary_content()
            with open(os.path.join(export_folder, "conversion_summary.json"), 'w', encoding='utf-8') as f:
                f.write(summary_content)
            
            self.update_status(f"Files exported to: {export_folder}")
            messagebox.showinfo("Export Complete", 
                               f"Successfully exported {len(completed_files)} files!\n\n"
                               f"Location: {export_folder}")
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Could not export files: {str(e)}")
    
    def create_index_content(self, completed_files):
        """Create index/README content for export"""
        content = f"""# MarkItDown Conversion Results

Generated by MarkItDown Desktop v{APP_VERSION}
Conversion Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Converted Files

"""
        
        for file_item in completed_files:
            base_name = os.path.splitext(file_item.filename)[0]
            md_filename = f"{base_name}.md"
            file_size = self.format_filesize(file_item.filesize)
            
            content += f"- [{file_item.filename}]({md_filename}) ({file_size})\n"
        
        content += f"""

## Statistics

- Total files processed: {len(completed_files)}
- Total original size: {self.format_filesize(sum(item.filesize for item in completed_files))}
- Processing tool: Microsoft MarkItDown
- Desktop GUI: MarkItDown Desktop by Rudolf Wagner

## Support the Project

This conversion was made possible by MarkItDown Desktop, created to support a meaningful kindergarten project.

🎁 **Support the Kindergarten Project**: [Donate via PayPal](https://www.paypal.com/donate/?hosted_button_id=PAGH54TWEXP54)

👨‍💻 **Developer**: [Rudolf Wagner on LinkedIn](https://www.linkedin.com/in/rudolfwagner)

---

*Generated with ❤️ by MarkItDown Desktop*
"""
        
        return content
    
    def create_summary_content(self):
        """Create JSON summary of conversion process"""
        summary = {
            "conversion_info": {
                "tool": f"MarkItDown Desktop v{APP_VERSION}",
                "timestamp": datetime.now().isoformat(),
                "total_files": len(self.file_queue),
                "completed_files": len([item for item in self.file_queue if item.status == "Completed"]),
                "error_files": len([item for item in self.file_queue if item.status == "Error"])
            },
            "files": []
        }
        
        for file_item in self.file_queue:
            file_info = {
                "original_filename": file_item.filename,
                "original_filepath": file_item.filepath,
                "original_size": file_item.filesize,
                "status": file_item.status,
                "markdown_size": len(file_item.markdown_content) if file_item.markdown_content else 0
            }
            
            if file_item.status == "Error":
                file_info["error_message"] = file_item.error_message
            
            summary["files"].append(file_info)
        
        return json.dumps(summary, indent=2)
    
    def on_file_select(self, event):
        """Handle file selection in tree"""
        selected_items = self.file_tree.selection()
        if selected_items:
            index = self.file_tree.index(selected_items[0])
            if 0 <= index < len(self.file_queue):
                file_item = self.file_queue[index]
                if file_item.status == "Completed":
                    self.show_preview(file_item)
                else:
                    self.clear_preview()
    
    def update_preview_selector(self):
        """Update the preview file selector"""
        completed_files = [item for item in self.file_queue if item.status == "Completed"]
        filenames = [item.filename for item in completed_files]
        
        self.preview_selector['values'] = filenames
        if filenames:
            self.preview_selector.set(filenames[0])
            self.on_preview_select(None)
        else:
            self.preview_selector.set('')
            self.clear_preview()
    
    def on_preview_select(self, event):
        """Handle preview file selection"""
        selected_filename = self.preview_selector.get()
        if selected_filename:
            file_item = next((item for item in self.file_queue 
                            if item.filename == selected_filename and item.status == "Completed"), None)
            if file_item:
                self.show_preview(file_item)
    
    def show_preview(self, file_item):
        """Show markdown preview for a file"""
        self.preview_text.config(state='normal')
        self.preview_text.delete(1.0, tk.END)
        self.preview_text.insert(1.0, file_item.markdown_content)
        self.preview_text.config(state='disabled')
        
        # Update stats
        lines = len(file_item.markdown_content.split('\n'))
        words = len(file_item.markdown_content.split())
        chars = len(file_item.markdown_content)
        
        self.preview_stats.config(text=f"{file_item.filename}: {lines} lines, {words} words, {chars} characters")
        
        # Enable preview buttons
        self.copy_btn.config(state='normal')
        self.save_btn.config(state='normal')
        self.preview_btn.config(state='normal')
    
    def clear_preview(self):
        """Clear preview area"""
        self.preview_text.config(state='normal')
        self.preview_text.delete(1.0, tk.END)
        self.preview_text.config(state='disabled')
        
        self.preview_stats.config(text="Select a completed file to preview")
        
        # Disable preview buttons
        self.copy_btn.config(state='disabled')
        self.save_btn.config(state='disabled')
        self.preview_btn.config(state='disabled')
    
    def copy_current(self):
        """Copy current preview to clipboard"""
        selected_filename = self.preview_selector.get()
        if selected_filename:
            file_item = next((item for item in self.file_queue 
                            if item.filename == selected_filename and item.status == "Completed"), None)
            if file_item:
                self.root.clipboard_clear()
                self.root.clipboard_append(file_item.markdown_content)
                self.update_status(f"Copied {file_item.filename} to clipboard")
    
    def save_current(self):
        """Save current preview as file"""
        selected_filename = self.preview_selector.get()
        if selected_filename:
            file_item = next((item for item in self.file_queue 
                            if item.filename == selected_filename and item.status == "Completed"), None)
            if file_item:
                base_name = os.path.splitext(file_item.filename)[0]
                default_name = f"{base_name}.md"
                
                filename = filedialog.asksaveasfilename(
                    title="Save Markdown File",
                    defaultextension=".md",
                    initialvalue=default_name,
                    filetypes=[('Markdown Files', '*.md'), ('Text Files', '*.txt'), ('All Files', '*.*')]
                )
                
                if filename:
                    try:
                        with open(filename, 'w', encoding='utf-8') as f:
                            f.write(file_item.markdown_content)
                        self.update_status(f"Saved {os.path.basename(filename)}")
                    except Exception as e:
                        messagebox.showerror("Save Error", f"Could not save file: {str(e)}")
    
    def preview_current(self):
        """Open HTML preview of current file"""
        selected_filename = self.preview_selector.get()
        if selected_filename:
            file_item = next((item for item in self.file_queue 
                            if item.filename == selected_filename and item.status == "Completed"), None)
            if file_item:
                self.open_html_preview(file_item.markdown_content, file_item.filename)
    
    def open_html_preview(self, markdown_content, filename):
        """Open HTML preview in browser"""
        try:
            import markdown
            html_content = markdown.markdown(markdown_content, extensions=['tables', 'fenced_code', 'codehilite'])
        except ImportError:
            html_content = self.basic_markdown_to_html(markdown_content)
        
        full_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Preview: {filename}</title>
    <style>
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; 
            max-width: 900px; 
            margin: 0 auto; 
            padding: 40px 20px; 
            line-height: 1.6; 
            color: #333;
        }}
        h1, h2, h3, h4, h5, h6 {{ color: #2c3e50; margin-top: 2em; }}
        pre {{ background: #f8f9fa; padding: 1em; border-radius: 8px; overflow-x: auto; }}
        code {{ background: #f1f2f6; padding: 0.2em 0.4em; border-radius: 4px; }}
        table {{ border-collapse: collapse; width: 100%; margin: 1.5em 0; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        th {{ background-color: #3498db; color: white; }}
    </style>
</head>
<body>
    <div style="text-align: center; margin-bottom: 2em; border-bottom: 2px solid #ecf0f1; padding-bottom: 1em;">
        <h1>📄 {filename}</h1>
        <p>Generated by MarkItDown Desktop v{APP_VERSION}</p>
    </div>
    
    {html_content}
    
    <div style="text-align: center; margin-top: 3em; padding-top: 1em; border-top: 1px solid #ecf0f1; color: #95a5a6;">
        <p>Converted with MarkItDown Desktop by Rudolf Wagner</p>
        <p>🎁 <a href="https://www.paypal.com/donate/?hosted_button_id=PAGH54TWEXP54">Support the Kindergarten Project</a></p>
    </div>
</body>
</html>
"""
        
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
                f.write(full_html)
                temp_file = f.name
            
            webbrowser.open(f'file://{temp_file}')
            self.update_status("HTML preview opened")
        except Exception as e:
            messagebox.showerror("Preview Error", f"Could not open preview: {str(e)}")
    
    def basic_markdown_to_html(self, markdown_text):
        """Basic markdown to HTML conversion fallback"""
        import re
        html = markdown_text
        html = re.sub(r'^# (.*$)', r'<h1>\1</h1>', html, flags=re.MULTILINE)
        html = re.sub(r'^## (.*$)', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^### (.*$)', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)
        html = re.sub(r'```(.*?)```', r'<pre><code>\1</code></pre>', html, flags=re.DOTALL)
        html = re.sub(r'`(.*?)`', r'<code>\1</code>', html)
        html = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', html)
        html = html.replace('\n\n', '</p><p>')
        html = html.replace('\n', '<br>')
        return '<p>' + html + '</p>'
    
    def show_error_message(self):
        """Show error message if MarkItDown is missing"""
        error_msg = """
MarkItDown is not available!

The application cannot function without MarkItDown.

Install it with:
pip install "markitdown[all]"

Or restart the app for automatic installation.
"""
        messagebox.showerror("MarkItDown Missing", error_msg)
        self.update_status("MarkItDown not available")
    
    def open_linkedin(self, event=None):
        """Open LinkedIn profile"""
        try:
            webbrowser.open("https://www.linkedin.com/in/rudolfwagner")
            self.update_status("LinkedIn profile opened")
        except Exception as e:
            print(f"Error opening link: {e}")
    
    def open_donation(self, event=None):
        """Open PayPal donation link for kindergarten project"""
        try:
            webbrowser.open("https://www.paypal.com/donate/?hosted_button_id=PAGH54TWEXP54")
            self.update_status("Thank you for supporting the kindergarten project!")
        except Exception as e:
            print(f"Error opening donation link: {e}")
    
    def show_help(self):
        """Show help dialog"""
        help_text = f"""
{APP_NAME} v{APP_VERSION} - Multi-File Batch Processing

USAGE:
1. Add Files: Click "Add Files" or "Add Folder" to build your conversion queue
2. Configure Options: Set processing preferences (folder structure, error handling)
3. Start Processing: Click "Start Batch Processing" to convert all files
4. Export Results: Download as ZIP or save to folder

NEW FEATURES:
• Multi-file selection and batch processing
• Folder structure preservation option
• ZIP export with all markdown files
• Individual file preview and management
• Progress tracking for large batches
• Error handling and recovery options

SUPPORTED FORMATS:
• Office: Word, Excel, PowerPoint (.docx, .xlsx, .pptx, etc.)
• PDF: All PDF documents
• Images: JPG, PNG, GIF (with OCR)
• Audio: MP3, WAV (with transcription)
• Web: HTML, CSV, JSON, XML
• Archives: ZIP files
• E-Books: EPUB

EXPORT OPTIONS:
• ZIP Download: All markdown files in one archive
• Folder Export: Save to organized folder structure
• Individual Files: Copy, save, or preview any converted file
• Index Generation: Automatic README with file listing
• Conversion Summary: JSON report with processing details

PROCESSING OPTIONS:
• Preserve Folder Structure: Maintain original directory layout
• Skip Errors: Continue processing even if some files fail
• Create Index: Generate README.md with file listing

DEVELOPED BY:
Rudolf Wagner
LinkedIn: https://www.linkedin.com/in/rudolfwagner

SUPPORTING A GREAT CAUSE:
The developer is founding a kindergarten!
Support this meaningful project:
PayPal: https://www.paypal.com/donate/?hosted_button_id=PAGH54TWEXP54

Every donation helps create a nurturing environment
for children's early education and development.

SUPPORT:
For technical issues visit:
github.com/microsoft/markitdown

© 2024 - Based on Microsoft MarkItDown
"""
        
        # Create help window
        help_window = tk.Toplevel(self.root)
        help_window.title("Help - Multi-File Processing")
        help_window.geometry("600x700")
        help_window.configure(bg='white')
        
        # Center window
        help_window.transient(self.root)
        help_window.grab_set()
        
        # Help content
        help_frame = ttk.Frame(help_window, padding="20")
        help_frame.pack(fill=tk.BOTH, expand=True)
        
        help_text_widget = scrolledtext.ScrolledText(help_frame, wrap=tk.WORD, 
                                                    font=('Arial', 10),
                                                    bg='white', fg='#333')
        help_text_widget.pack(fill=tk.BOTH, expand=True)
        help_text_widget.insert(1.0, help_text)
        help_text_widget.config(state='disabled')
        
        # Close button
        close_btn = ttk.Button(help_frame, text="Close", 
                              command=help_window.destroy)
        close_btn.pack(pady=(10, 0))
    
    def update_status(self, message):
        """Update status bar"""
        self.status_bar.config(text=message)
    
    def format_filesize(self, size_bytes):
        """Format file size in human readable format"""
        if size_bytes == 0:
            return "0 B"
        size_names = ["B", "KB", "MB", "GB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names)-1:
            size_bytes /= 1024
            i += 1
        return f"{size_bytes:.1f} {size_names[i]}"


def main():
    """Main function"""
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                {APP_NAME} v{APP_VERSION} - Multi-File           ║
║            Complete with Kindergarten Support               ║
╚══════════════════════════════════════════════════════════════╝
""")
    
    # Python version check
    if sys.version_info < (3, 7):
        print("❌ Python 3.7+ required!")
        print(f"   Current version: {sys.version}")
        sys.exit(1)
    
    print(f"✅ Python {sys.version.split()[0]} found")
    
    # Dependencies check and installation BEFORE GUI start
    if not check_and_install_dependencies():
        print("\n❌ Cannot continue without MarkItDown.")
        print("💡 Install it manually and restart.")
        sys.exit(1)
    
    print("\n🚀 Starting Multi-File GUI application...")
    
    try:
        # Create GUI
        root = tk.Tk()
        app = MarkItDownApp(root)
        
        # Window centering
        root.update_idletasks()
        width = root.winfo_width()
        height = root.winfo_height()
        x = (root.winfo_screenwidth() // 2) - (width // 2)
        y = (root.winfo_screenheight() // 2) - (height // 2)
        root.geometry(f'{width}x{height}+{x}+{y}')
        
        print("✅ Multi-File GUI started successfully!")
        print("📋 You can now add multiple files for batch conversion.")
        print("🎁 Don't forget to check out the kindergarten donation option!")
        print("\n💡 NEW: Add entire folders, batch process, and export as ZIP!")
        
        # Start main loop
        root.mainloop()
        
    except KeyboardInterrupt:
        print("\n👋 Application terminated")
    except Exception as e:
        print(f"❌ GUI error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n👋 Goodbye!")


if __name__ == "__main__":
    main()
