#!/usr/bin/env python3
"""
MarkItDown Desktop App - Complete Version with Donation Support
Crash-safe, proper markdown output, and kindergarten project donation

INSTALLATION & START:
1. Save this file as 'markitdown_desktop.py'
2. Open terminal and run: python markitdown_desktop.py
3. Start converting - MarkItDown is already installed!

SUPPORTED FORMATS:
- Office: Word, Excel, PowerPoint
- PDF: All PDF documents  
- Images: JPG, PNG, GIF (with OCR)
- Audio: MP3, WAV (with transcription)
- Web: HTML, CSV, JSON, XML
- Archives: ZIP files
- E-Books: EPUB

Version: 2.5 (Clean - No Emoji Issues)
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

# App Constants
APP_NAME = "MarkItDown Desktop"
APP_VERSION = "2.5"

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

class MarkItDownApp:
    """Main application"""
    
    def __init__(self, root):
        self.root = root
        self.current_file = None
        self.current_markdown = ""
        self.processing = False
        
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
        self.root.title(f"{APP_NAME} v{APP_VERSION}")
        self.root.geometry("1200x800")
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
        
        title_label = ttk.Label(header_frame, text="MarkItDown Desktop", 
                               font=('Arial', 18, 'bold'))
        title_label.pack(side=tk.LEFT)
        
        # Version and Author in consistent styling
        info_frame = ttk.Frame(header_frame)
        info_frame.pack(side=tk.RIGHT)
        
        version_label = ttk.Label(info_frame, text=f"v{APP_VERSION}", 
                                 font=('Arial', 10))
        version_label.pack()
        
        # Author link with same styling as subtitle
        author_label = ttk.Label(info_frame, text="by Rudolf Wagner", 
                                font=('Arial', 9), 
                                foreground='#1976d2', cursor='hand2')
        author_label.pack()
        author_label.bind('<Button-1>', self.open_linkedin)
        
        # Donation link for kindergarten project
        donate_label = ttk.Label(info_frame, text="Support Kindergarten Project", 
                                font=('Arial', 8), 
                                foreground='#e74c3c', cursor='hand2')
        donate_label.pack(pady=(2, 0))
        donate_label.bind('<Button-1>', self.open_donation)
        
        subtitle_label = ttk.Label(header_frame, 
                                  text="Convert any files to Markdown",
                                  font=('Arial', 11))
        subtitle_label.pack(side=tk.LEFT, padx=(20, 0))
        
        # Content area
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        content_frame.columnconfigure(0, weight=1)
        content_frame.columnconfigure(1, weight=2)
        content_frame.rowconfigure(0, weight=1)
        
        # Left panel
        self.create_left_panel(content_frame)
        
        # Right panel  
        self.create_right_panel(content_frame)
        
        # Status bar
        self.status_bar = ttk.Label(main_frame, text="Ready", relief='sunken')
        self.status_bar.pack(fill=tk.X, pady=(10, 0))
        
        # Check if MarkItDown is available
        if not self.markitdown_available:
            self.show_error_message()
    
    def create_left_panel(self, parent):
        """Left panel for file upload"""
        left_frame = ttk.LabelFrame(parent, text="File Upload", padding="15")
        left_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        left_frame.columnconfigure(0, weight=1)
        
        # Drop zone - macOS compatible
        drop_outer = ttk.Frame(left_frame, relief='ridge', borderwidth=2)
        drop_outer.pack(fill=tk.X, pady=(0, 15))
        
        drop_frame = tk.Frame(drop_outer, bg='#e3f2fd', height=150, cursor='hand2')
        drop_frame.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)
        drop_frame.pack_propagate(False)
        
        # Drop zone content - NO EMOJIS
        drop_content = tk.Frame(drop_frame, bg='#e3f2fd')
        drop_content.place(relx=0.5, rely=0.5, anchor='center')
        
        icon_label = tk.Label(drop_content, text="[FILE]", font=('Arial', 24, 'bold'), 
                             bg='#e3f2fd', fg='#1976d2')
        icon_label.pack()
        
        text_label = tk.Label(drop_content, text="Click here to\nselect file", 
                             font=('Arial', 12, 'bold'), bg='#e3f2fd', fg='#1976d2')
        text_label.pack(pady=(5, 0))
        
        hint_label = tk.Label(drop_content, text="PDF, Office, Images, Audio & more", 
                             font=('Arial', 9), bg='#e3f2fd', fg='#666666')
        hint_label.pack()
        
        # Bind click events
        for widget in [drop_frame, drop_content, icon_label, text_label, hint_label]:
            widget.bind('<Button-1>', self.select_file)
        
        # File info
        self.file_info = ttk.Label(left_frame, text="No file selected", 
                                  font=('Arial', 10), wraplength=250)
        self.file_info.pack(anchor=tk.W, pady=(0, 15))
        
        # Buttons
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(fill=tk.X, pady=(0, 15))
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        
        self.select_btn = ttk.Button(button_frame, text="Select File", 
                                    command=self.select_file)
        self.select_btn.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        self.convert_btn = ttk.Button(button_frame, text="Convert", 
                                     command=self.convert_file, state='disabled')
        self.convert_btn.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        
        # Progress
        self.progress = ttk.Progressbar(left_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=(0, 15))
        
        # Auto-convert option
        self.auto_convert = tk.BooleanVar(value=True)
        auto_check = ttk.Checkbutton(left_frame, text="Auto-Convert", 
                                    variable=self.auto_convert)
        auto_check.pack(anchor=tk.W, pady=(0, 15))
        
        # CLEAN supported formats - NO EMOJIS
        formats_title = ttk.Label(left_frame, text="Supported Formats:", 
                                 font=('Arial', 10, 'bold'))
        formats_title.pack(anchor=tk.W, pady=(10, 5))
        
        # Simple text list
        formats_list = [
            "• Office: Word, Excel, PowerPoint",
            "• PDF: All PDF documents", 
            "• Images: JPG, PNG, GIF (with OCR)",
            "• Audio: MP3, WAV (transcription)",
            "• Web: HTML, CSV, JSON, XML",
            "• Archives: ZIP files",
            "• E-Books: EPUB"
        ]
        
        for format_text in formats_list:
            format_label = ttk.Label(left_frame, text=format_text, 
                                   font=('Arial', 9))
            format_label.pack(anchor=tk.W)
    
    def create_right_panel(self, parent):
        """Right panel for output"""
        right_frame = ttk.LabelFrame(parent, text="Markdown Output", padding="15")
        right_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(1, weight=1)
        
        # Toolbar
        toolbar_frame = ttk.Frame(right_frame)
        toolbar_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        toolbar_frame.columnconfigure(5, weight=1)
        
        self.copy_btn = ttk.Button(toolbar_frame, text="Copy", 
                                  command=self.copy_markdown, state='disabled')
        self.copy_btn.grid(row=0, column=0, padx=(0, 5))
        
        self.save_btn = ttk.Button(toolbar_frame, text="Save", 
                                  command=self.save_markdown, state='disabled')
        self.save_btn.grid(row=0, column=1, padx=(0, 5))
        
        self.preview_btn = ttk.Button(toolbar_frame, text="Preview", 
                                     command=self.preview_markdown, state='disabled')
        self.preview_btn.grid(row=0, column=2, padx=(0, 5))
        
        self.clear_btn = ttk.Button(toolbar_frame, text="Clear", 
                                   command=self.clear_output, state='disabled')
        self.clear_btn.grid(row=0, column=3, padx=(0, 5))
        
        # Help button
        help_btn = ttk.Button(toolbar_frame, text="Help", 
                             command=self.show_help)
        help_btn.grid(row=0, column=6)
        
        # Donation button
        donate_btn = ttk.Button(toolbar_frame, text="Donate", 
                               command=self.open_donation)
        donate_btn.grid(row=0, column=7, padx=(5, 0))
        
        # Output area
        self.output_text = scrolledtext.ScrolledText(right_frame, 
                                                    wrap=tk.WORD, 
                                                    font=('Monaco', 11) if platform.system() == 'Darwin' else ('Consolas', 10),
                                                    state='disabled',
                                                    bg='white',
                                                    fg='#333333',
                                                    insertbackground='#333333',
                                                    selectbackground='#e3f2fd',
                                                    selectforeground='#1976d2',
                                                    relief='sunken',
                                                    borderwidth=1)
        self.output_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Stats
        self.stats_label = ttk.Label(right_frame, text="Statistics: -", 
                                     font=('Arial', 9))
        self.stats_label.grid(row=2, column=0, sticky=tk.W, pady=(10, 0))
    
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
    
    def select_file(self, event=None):
        """Select file - macOS-safe"""
        if not self.markitdown_available:
            messagebox.showerror("Error", "MarkItDown is not available!")
            return
        
        try:
            # Simplified filetypes for macOS compatibility
            filetypes = [
                ('All Files', '*.*'),
                ('PDF Documents', '*.pdf'),
                ('Word Documents', '*.docx'),
                ('Word Legacy', '*.doc'), 
                ('Excel Files', '*.xlsx'),
                ('Excel Legacy', '*.xls'),
                ('PowerPoint', '*.pptx'),
                ('PowerPoint Legacy', '*.ppt'),
                ('Images', '*.jpg'),
                ('PNG Images', '*.png'),
                ('GIF Images', '*.gif'),
                ('Audio MP3', '*.mp3'),
                ('Audio WAV', '*.wav'),
                ('HTML Files', '*.html'),
                ('CSV Files', '*.csv'),
                ('JSON Files', '*.json'),
                ('XML Files', '*.xml'),
                ('ZIP Archives', '*.zip'),
                ('EPUB E-Books', '*.epub'),
                ('Text Files', '*.txt')
            ]
            
            filename = filedialog.askopenfilename(
                title="Select file for conversion",
                filetypes=filetypes
            )
            
            if filename:
                self.process_file(filename)
                
        except Exception as e:
            print(f"File dialog error: {e}")
            # Fallback: Simple dialog without filetypes
            try:
                filename = filedialog.askopenfilename(
                    title="Select file (all formats)"
                )
                if filename:
                    self.process_file(filename)
            except Exception as e2:
                messagebox.showerror("Dialog Error", 
                                   f"File dialog not working: {str(e2)}\n\n"
                                   f"Please try restarting the application.")
    
    def process_file(self, filepath):
        """Process selected file"""
        if not os.path.exists(filepath):
            messagebox.showerror("Error", "File does not exist!")
            return
        
        # Check if file extension is supported
        supported_extensions = [
            '.pdf', '.docx', '.doc', '.xlsx', '.xls', '.pptx', '.ppt',
            '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff',
            '.mp3', '.wav', '.m4a', '.flac',
            '.html', '.htm', '.mhtml', 
            '.csv', '.json', '.xml', '.yaml',
            '.zip', '.rar', '.7z',
            '.epub', '.txt'
        ]
        
        file_ext = os.path.splitext(filepath)[1].lower()
        if file_ext not in supported_extensions:
            messagebox.showwarning("Warning", 
                                 f"File extension '{file_ext}' might not be supported.\n\n"
                                 f"Supported formats: {', '.join(supported_extensions)}\n\n"
                                 f"Trying to convert anyway...")
        
        self.current_file = filepath
        filename = os.path.basename(filepath)
        filesize = self.format_filesize(os.path.getsize(filepath))
        
        self.file_info.config(text=f"{filename}\nSize: {filesize}")
        self.convert_btn.config(state='normal')
        self.update_status(f"File loaded: {filename}")
        
        # Auto-convert
        if self.auto_convert.get():
            self.root.after(500, self.convert_file)
    
    def convert_file(self):
        """Convert file"""
        if not self.current_file or not self.markitdown_available or self.processing:
            return
        
        self.processing = True
        self.progress.start()
        self.convert_btn.config(state='disabled')
        self.update_status("Converting...")
        
        # Threading for conversion
        def convert_thread():
            try:
                print(f"Converting: {self.current_file}")
                result = self.markitdown.convert(self.current_file)
                markdown_content = result.text_content
                
                if not markdown_content:
                    raise Exception("No content extracted")
                
                print(f"Conversion successful: {len(markdown_content)} characters")
                self.current_markdown = markdown_content
                
                # UI update in main thread
                self.root.after(0, lambda: self.display_result(markdown_content))
                
            except Exception as e:
                print(f"Conversion failed: {e}")
                error_msg = f"Conversion failed: {str(e)}"
                self.root.after(0, lambda: self.show_conversion_error(error_msg))
            
            finally:
                self.root.after(0, self.conversion_finished)
        
        thread = threading.Thread(target=convert_thread, daemon=True)
        thread.start()
    
    def display_result(self, content):
        """Show conversion result"""
        self.output_text.config(state='normal')
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(1.0, content)
        self.output_text.config(state='disabled')
        
        # Enable buttons
        self.copy_btn.config(state='normal')
        self.save_btn.config(state='normal')
        self.preview_btn.config(state='normal')
        self.clear_btn.config(state='normal')
        
        # Update stats
        lines = len(content.split('\n'))
        words = len(content.split())
        chars = len(content)
        self.stats_label.config(text=f"Statistics: {lines} lines, {words} words, {chars} characters")
        
        self.update_status("Conversion successful!")
    
    def show_conversion_error(self, error_msg):
        """Show conversion error"""
        messagebox.showerror("Conversion Error", error_msg)
        self.update_status(f"Error: {error_msg}")
    
    def conversion_finished(self):
        """Cleanup after conversion"""
        self.processing = False
        self.progress.stop()
        self.convert_btn.config(state='normal')
    
    def copy_markdown(self):
        """Copy to clipboard"""
        if self.current_markdown:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.current_markdown)
            self.update_status("Copied to clipboard!")
    
    def save_markdown(self):
        """Save as file"""
        if not self.current_markdown:
            return
        
        default_name = "output.md"
        if self.current_file:
            base_name = os.path.splitext(os.path.basename(self.current_file))[0]
            default_name = f"{base_name}.md"
        
        try:
            filename = filedialog.asksaveasfilename(
                title="Save Markdown",
                defaultextension=".md",
                initialvalue=default_name,
                filetypes=[
                    ('Markdown Files', '*.md'),
                    ('Text Files', '*.txt'),
                    ('All Files', '*.*')
                ]
            )
            
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.current_markdown)
                self.update_status(f"Saved: {os.path.basename(filename)}")
                
        except Exception as e:
            print(f"Save error: {e}")
            messagebox.showerror("Save Error", f"Error: {str(e)}")
    
    def preview_markdown(self):
        """HTML preview"""
        if not self.current_markdown:
            return
        
        # Try to use markdown library for proper rendering
        try:
            import markdown
            html_content = markdown.markdown(self.current_markdown, extensions=['tables', 'fenced_code', 'codehilite'])
        except ImportError:
            # Fallback: basic HTML conversion
            html_content = self.basic_markdown_to_html(self.current_markdown)
        
        # Complete HTML document
        full_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Markdown Preview</title>
    <style>
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; 
            max-width: 900px; 
            margin: 0 auto; 
            padding: 40px 20px; 
            line-height: 1.6; 
            color: #333;
            background: #fff;
        }}
        h1, h2, h3, h4, h5, h6 {{ 
            color: #2c3e50; 
            margin-top: 2em;
            margin-bottom: 0.5em;
            font-weight: 600;
        }}
        h1 {{ 
            font-size: 2.5em; 
            border-bottom: 3px solid #3498db;
            padding-bottom: 0.3em;
        }}
        h2 {{ 
            font-size: 2em; 
            border-bottom: 2px solid #ecf0f1;
            padding-bottom: 0.3em;
        }}
        pre {{ 
            background: #f8f9fa; 
            padding: 1em; 
            border-radius: 8px; 
            overflow-x: auto; 
            border-left: 4px solid #3498db;
            margin: 1.5em 0;
        }}
        code {{ 
            background: #f1f2f6; 
            padding: 0.2em 0.4em; 
            border-radius: 4px; 
            font-family: 'Monaco', 'Menlo', 'Courier New', monospace;
            font-size: 0.9em;
            color: #e74c3c;
        }}
        table {{ 
            border-collapse: collapse; 
            width: 100%; 
            margin: 1.5em 0;
        }}
        th, td {{ 
            border: 1px solid #ddd; 
            padding: 12px 15px; 
            text-align: left; 
        }}
        th {{ 
            background-color: #3498db; 
            color: white;
        }}
    </style>
</head>
<body>
    <div style="text-align: center; margin-bottom: 2em; padding-bottom: 1em; border-bottom: 2px solid #ecf0f1;">
        <h1>Markdown Preview</h1>
        <p>Generated by MarkItDown Desktop</p>
    </div>
    
    {html_content}
    
    <div style="text-align: center; margin-top: 3em; padding-top: 1em; border-top: 1px solid #ecf0f1; color: #95a5a6; font-size: 0.9em;">
        <p>Converted with MarkItDown Desktop by Rudolf Wagner</p>
        <p><a href="https://www.paypal.com/donate/?hosted_button_id=PAGH54TWEXP54">Support the Kindergarten Project</a></p>
    </div>
</body>
</html>
"""
        
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
                f.write(full_html)
                temp_file = f.name
            
            webbrowser.open(f'file://{temp_file}')
            self.update_status("Preview opened")
        except Exception as e:
            messagebox.showerror("Preview Error", f"Could not open preview: {str(e)}")
    
    def basic_markdown_to_html(self, markdown_text):
        """Basic markdown to HTML conversion fallback"""
        import re
        
        html = markdown_text
        
        # Headers
        html = re.sub(r'^# (.*$)', r'<h1>\1</h1>', html, flags=re.MULTILINE)
        html = re.sub(r'^## (.*$)', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^### (.*$)', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        
        # Bold and Italic
        html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)
        
        # Code blocks
        html = re.sub(r'```(.*?)```', r'<pre><code>\1</code></pre>', html, flags=re.DOTALL)
        html = re.sub(r'`(.*?)`', r'<code>\1</code>', html)
        
        # Links
        html = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', html)
        
        # Line breaks
        html = html.replace('\n\n', '</p><p>')
        html = html.replace('\n', '<br>')
        html = '<p>' + html + '</p>'
        
        return html
    
    def clear_output(self):
        """Clear output"""
        self.output_text.config(state='normal')
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state='disabled')
        
        self.current_markdown = ""
        self.current_file = None
        
        # Reset UI
        self.copy_btn.config(state='disabled')
        self.save_btn.config(state='disabled')
        self.preview_btn.config(state='disabled')
        self.clear_btn.config(state='disabled')
        self.convert_btn.config(state='disabled')
        
        self.file_info.config(text="No file selected")
        self.stats_label.config(text="Statistics: -")
        self.update_status("Ready")
    
    def show_help(self):
        """Show help"""
        help_text = f"""
{APP_NAME} v{APP_VERSION} - by Rudolf Wagner

USAGE:
1. Select file (click blue area or button)
2. Conversion starts automatically
3. Markdown is displayed on the right
4. Copy, Save or Preview

SUPPORTED FORMATS:
• Office: Word, Excel, PowerPoint
• PDF: All PDF documents
• Images: JPG, PNG, GIF (with OCR)
• Audio: MP3, WAV (with transcription)
• Web: HTML, CSV, JSON, XML
• Archives: ZIP files
• E-Books: EPUB

FEATURES:
• Auto-conversion enabled
• Preview shows formatted HTML
• Statistics about content
• Clipboard integration

TROUBLESHOOTING:
• Internet connection needed for audio
• Large files take more time
• OCR works only on clear images

macOS NOTES:
• If dialog problems: use 'Select File' button
• Restart app if conversion fails

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
        help_window.title("Help")
        help_window.geometry("500x700")
        help_window.configure(bg='white')
        
        # Center window
        help_window.transient(self.root)
        help_window.grab_set()
        
        # Help content
        help_frame = ttk.Frame(help_window, padding="20")
        help_frame.pack(fill=tk.BOTH, expand=True)
        
        help_text_widget = scrolledtext.ScrolledText(help_frame, wrap=tk.WORD, 
                                                    font=('Arial', 11),
                                                    bg='white', fg='#333')
        help_text_widget.pack(fill=tk.BOTH, expand=True)
        help_text_widget.insert(1.0, help_text)
        help_text_widget.config(state='disabled')
        
        # Close button
        close_btn = ttk.Button(help_frame, text="Close", 
                              command=help_window.destroy)
        close_btn.pack(pady=(10, 0))
    
    def update_status(self, message):
        """Update status"""
        self.status_bar.config(text=message)
    
    def format_filesize(self, size_bytes):
        """Format file size"""
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
║                    {APP_NAME} v{APP_VERSION}                     ║
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
    
    print("\n🚀 Starting GUI application...")
    
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
        
        print("✅ GUI started successfully!")
        print("📋 You can now convert files.")
        print("🎁 Don't forget to check out the kindergarten donation option!")
        print("\n💡 TIP: If file dialog has problems, use the 'Select File' button!")
        
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
