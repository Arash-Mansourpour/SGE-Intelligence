import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
from tkinter.font import Font
import json
import threading
import os
import webbrowser
from datetime import datetime
from PIL import Image, ImageTk
import requests
from io import BytesIO
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from groq import Groq
import customtkinter as ctk

# API Configuration
API_KEY = "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"

class AdvancedSGEApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced SGE Content Intelligence Platform")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        # Initialize Groq client
        self.client = Groq(api_key=API_KEY)
        
        # App state variables
        self.history = []
        self.current_file = None
        self.is_generating = False
        self.settings = self.load_settings()
        self.selected_model = tk.StringVar(value=self.settings.get("default_model", "llama-3.3-70b-versatile"))
        
        # Create UI
        self.create_widgets()
        self.apply_theme()
        
    def load_settings(self):
        try:
            if os.path.exists("settings.json"):
                with open("settings.json", "r") as f:
                    return json.load(f)
            return {
                "default_model": "llama-3.3-70b-versatile",
                "temperature": 0.7,
                "max_tokens": 1024,
                "theme": "dark",
                "recent_searches": [],
                "saved_templates": {
                    "SEO Blog Post": "Create an SEO-optimized blog post about {query} focusing on {keywords}",
                    "Product Description": "Generate a compelling product description for {query} highlighting {keywords}",
                    "FAQ Section": "Create an FAQ section about {query} addressing {keywords}"
                }
            }
        except Exception as e:
            print(f"Error loading settings: {e}")
            return {"default_model": "llama-3.3-70b-versatile", "temperature": 0.7, "max_tokens": 1024}

    def save_settings(self):
        try:
            with open("settings.json", "w") as f:
                json.dump(self.settings, f)
        except Exception as e:
            print(f"Error saving settings: {e}")

    def create_widgets(self):
        self.main_container = ctk.CTkFrame(self.root)
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.create_header()
        self.create_sidebar()
        self.create_main_content()
        self.create_status_bar()

    def create_header(self):
        header_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 10))
        
        title_label = ctk.CTkLabel(header_frame, text="Advanced SGE Content Intelligence", font=ctk.CTkFont(family="Helvetica", size=22, weight="bold"))
        title_label.pack(side="left", padx=10)
        
        settings_btn = ctk.CTkButton(header_frame, text="⚙️", width=40, command=self.open_settings, fg_color="transparent")
        settings_btn.pack(side="right", padx=5)
        
        help_btn = ctk.CTkButton(header_frame, text="?", width=40, command=self.show_help, fg_color="transparent")
        help_btn.pack(side="right", padx=5)

    def create_sidebar(self):
        self.content_frame = ctk.CTkFrame(self.main_container)
        self.content_frame.pack(fill="both", expand=True)
        
        self.sidebar = ctk.CTkFrame(self.content_frame, width=250)
        self.sidebar.pack(side="left", fill="y", padx=(0, 10))
        
        template_label = ctk.CTkLabel(self.sidebar, text="Content Templates", font=ctk.CTkFont(size=14, weight="bold"))
        template_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        self.template_frame = ctk.CTkScrollableFrame(self.sidebar, height=200)
        self.template_frame.pack(fill="x", padx=10, pady=5)
        
        for name, template in self.settings.get("saved_templates", {}).items():
            self.add_template_button(name, template)
            
        add_template_btn = ctk.CTkButton(self.sidebar, text="+ Add Template", command=self.add_new_template, height=30)
        add_template_btn.pack(fill="x", padx=10, pady=5)
        
        history_label = ctk.CTkLabel(self.sidebar, text="Recent Searches", font=ctk.CTkFont(size=14, weight="bold"))
        history_label.pack(anchor="w", padx=10, pady=(20, 5))
        
        self.history_frame = ctk.CTkScrollableFrame(self.sidebar)
        self.history_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        analytics_btn = ctk.CTkButton(self.sidebar, text="📊 Analytics Dashboard", command=self.open_analytics, height=35)
        analytics_btn.pack(fill="x", padx=10, pady=10)

    def create_main_content(self):
        self.main_frame = ctk.CTkFrame(self.content_frame)
        self.main_frame.pack(side="right", fill="both", expand=True)
        
        input_frame = ctk.CTkFrame(self.main_frame)
        input_frame.pack(fill="x", padx=10, pady=10)
        
        query_label = ctk.CTkLabel(input_frame, text="Search Query:")
        query_label.grid(row=0, column=0, sticky="w", pady=(10, 0))
        
        self.query_entry = ctk.CTkEntry(input_frame, height=35, placeholder_text="Enter main search query here...")
        self.query_entry.grid(row=1, column=0, sticky="ew", pady=(5, 10))
        
        keywords_label = ctk.CTkLabel(input_frame, text="Target Keywords:")
        keywords_label.grid(row=0, column=1, sticky="w", pady=(10, 0), padx=(20, 0))
        
        self.keywords_entry = ctk.CTkEntry(input_frame, height=35, placeholder_text="Enter target keywords separated by commas...")
        self.keywords_entry.grid(row=1, column=1, sticky="ew", pady=(5, 10), padx=(20, 0))
        
        input_frame.grid_columnconfigure(0, weight=1)
        input_frame.grid_columnconfigure(1, weight=1)
        
        advanced_frame = ctk.CTkFrame(self.main_frame)
        advanced_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        model_label = ctk.CTkLabel(advanced_frame, text="AI Model:")
        model_label.grid(row=0, column=0, sticky="w")
        
        models = ["llama-3.3-70b-versatile", "llama-3.1-70b-versatile", "llama-3.1-8b-versatile", "mixtral-8x7b-32768"]
        model_dropdown = ctk.CTkOptionMenu(advanced_frame, variable=self.selected_model, values=models, width=200)
        model_dropdown.grid(row=0, column=1, sticky="w", padx=(10, 20))
        
        content_label = ctk.CTkLabel(advanced_frame, text="Content Type:")
        content_label.grid(row=0, column=2, sticky="w")
        
        self.content_type = tk.StringVar(value="comprehensive")
        content_types = ["comprehensive", "blog", "product", "landing", "faq", "rich-snippet"]
        content_dropdown = ctk.CTkOptionMenu(advanced_frame, variable=self.content_type, values=content_types, width=150)
        content_dropdown.grid(row=0, column=3, sticky="w", padx=(10, 0))
        
        advanced_frame.grid_columnconfigure(0, weight=0)
        advanced_frame.grid_columnconfigure(1, weight=0)
        advanced_frame.grid_columnconfigure(2, weight=0)
        advanced_frame.grid_columnconfigure(3, weight=0)
        advanced_frame.grid_columnconfigure(4, weight=1)
        
        btn_frame = ctk.CTkFrame(self.main_frame)
        btn_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        self.create_button(btn_frame, "Generate SGE Content", self.generate_content, 0, 0)
        self.create_button(btn_frame, "Analyze Search Intent", lambda: self.start_analysis("intent"), 0, 1)
        self.create_button(btn_frame, "Schema Generator", lambda: self.start_analysis("schema"), 0, 2)
        self.create_button(btn_frame, "SERP Feature Optimizer", lambda: self.start_analysis("serp"), 0, 3)
        
        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)
        btn_frame.grid_columnconfigure(2, weight=1)
        btn_frame.grid_columnconfigure(3, weight=1)
        
        self.output_notebook = ctk.CTkTabview(self.main_frame)
        self.output_notebook.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        self.output_notebook.add("Content")
        self.output_notebook.add("Analysis")
        self.output_notebook.add("Schema")
        
        self.output_text = ctk.CTkTextbox(self.output_notebook.tab("Content"), wrap="word", font=("Helvetica", 12))
        self.output_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        analysis_frame = ctk.CTkFrame(self.output_notebook.tab("Analysis"))
        analysis_frame.pack(fill="both", expand=True, padx=5, pady=5)
        self.analysis_text = ctk.CTkTextbox(analysis_frame, wrap="word", font=("Helvetica", 12))
        self.analysis_text.pack(fill="both", expand=True)
        
        schema_frame = ctk.CTkFrame(self.output_notebook.tab("Schema"))
        schema_frame.pack(fill="both", expand=True, padx=5, pady=5)
        self.schema_text = ctk.CTkTextbox(schema_frame, wrap="word", font=("Helvetica", 12))
        self.schema_text.pack(fill="both", expand=True)

    def create_status_bar(self):
        status_frame = ctk.CTkFrame(self.main_container, height=30)
        status_frame.pack(fill="x", pady=(10, 0))
        
        self.status_label = ctk.CTkLabel(status_frame, text="Ready")
        self.status_label.pack(side="left", padx=10)
        
        self.progress_bar = ctk.CTkProgressBar(status_frame, width=200)
        self.progress_bar.pack(side="right", padx=10)
        self.progress_bar.set(0)
        
        save_btn = ctk.CTkButton(status_frame, text="Save", width=80, command=self.save_output)
        save_btn.pack(side="right", padx=5)
        
        copy_btn = ctk.CTkButton(status_frame, text="Copy", width=80, command=self.copy_to_clipboard)
        copy_btn.pack(side="right", padx=5)
        
        clear_btn = ctk.CTkButton(status_frame, text="Clear", width=80, command=self.clear_output)
        clear_btn.pack(side="right", padx=5)

    def create_button(self, parent, text, command, row, column):
        btn = ctk.CTkButton(parent, text=text, command=command, height=40, corner_radius=8)
        btn.grid(row=row, column=column, sticky="ew", padx=5, pady=5)
        return btn

    def add_template_button(self, name, template):
        btn = ctk.CTkButton(self.template_frame, text=name, command=lambda t=template: self.use_template(t), height=30, anchor="w")
        btn.pack(fill="x", pady=2)

    def use_template(self, template):
        if "{query}" in template and "{keywords}" in template:
            query = self.query_entry.get() if self.query_entry.get() else "{query}"
            keywords = self.keywords_entry.get() if self.keywords_entry.get() else "{keywords}"
            self.template_prompt = template.replace("{query}", query).replace("{keywords}", keywords)
            self.status_label.configure(text=f"Template active: {template[:30]}...")
        else:
            self.template_prompt = template
            self.status_label.configure(text=f"Template active: {template[:30]}...")

    def add_new_template(self):
        dialog = ctk.CTkInputDialog(title="Add Template", text="Enter template name:")
        name = dialog.get_input()
        
        if name:
            dialog2 = ctk.CTkInputDialog(title="Template Content", text="Enter template content (use {query} and {keywords} as placeholders):")
            content = dialog2.get_input()
            
            if content:
                if "saved_templates" not in self.settings:
                    self.settings["saved_templates"] = {}
                self.settings["saved_templates"][name] = content
                self.save_settings()
                self.add_template_button(name, content)

    def generate_content(self):
        self.start_analysis("content")

    def start_analysis(self, analysis_type):
        query = self.query_entry.get()
        keywords = self.keywords_entry.get()
        
        if not query:
            self.show_error("Please enter a search query!")
            return
        
        self.is_generating = True
        self.status_label.configure(text=f"Generating {analysis_type}...")
        self.progress_bar.start()
        
        if analysis_type == "content":
            self.output_notebook.set("Content")
            self.output_text.delete("0.0", "end")
        elif analysis_type == "intent":
            self.output_notebook.set("Analysis")
            self.analysis_text.delete("0.0", "end")
        elif analysis_type in ["schema", "serp"]:
            self.output_notebook.set("Schema")
            self.schema_text.delete("0.0", "end")
        
        thread = threading.Thread(target=self.process_sge, args=(query, keywords, analysis_type))
        thread.daemon = True
        thread.start()
        
        self.add_to_history(query, keywords, analysis_type)

    def process_sge(self, query, keywords, analysis_type):
        try:
            model = self.selected_model.get()
            content_type = self.content_type.get()
            
            if analysis_type == "content":
                template = getattr(self, 'template_prompt', None)
                if template:
                    user_content = template.replace("{query}", query).replace("{keywords}", keywords)
                else:
                    user_content = f"""Create comprehensive SGE-optimized content for the search query: '{query}' 
                    targeting these keywords: '{keywords}'. 
                    Content type: {content_type}
                    Include:
                    1. An engaging title optimized for both users and search engines
                    2. Meta description (160 characters max)
                    3. Well-structured content with appropriate headings
                    4. Natural keyword integration
                    5. Internal and external linking suggestions
                    6. Rich media suggestions (images, videos)
                    7. User engagement elements
                    8. Call-to-action recommendations"""
                system_content = """You are an expert in Search Generative Experience (SGE) content creation.
                You understand how to create content that works well with Google's SGE and modern search algorithms.
                Always focus on providing exceptional value to users while maintaining search visibility.
                Format your output nicely with appropriate Markdown formatting."""
            elif analysis_type == "intent":
                user_content = f"""Perform comprehensive search intent analysis for query: '{query}'
                with related keywords: '{keywords}'.
                Include:
                1. Query classification (informational, navigational, transactional, commercial investigation)
                2. User journey stage analysis
                3. Search features likely to appear for this query
                4. Competing content types
                5. Key topics to address
                6. Questions the user is likely asking
                7. Recommended content format and structure
                8. Strategic recommendations for SGE optimization"""
                system_content = """You are an expert search intent analyst specializing in SGE.
                Provide comprehensive analysis to help content creators understand what users are truly seeking.
                Format your output clearly with appropriate Markdown formatting and sections."""
            elif analysis_type == "schema":
                user_content = f"""Generate optimized schema markup for content about: '{query}'
                with keywords: '{keywords}'.
                Content type: {content_type}
                Include:
                1. Recommended schema.org types to implement
                2. Complete JSON-LD code examples
                3. Explanation of each schema property
                4. Custom property recommendations
                5. Implementation guidance
                6. Rich result potential analysis"""
                system_content = """You are an expert in schema markup and structured data for search engines.
                Provide detailed, technically correct schema markup that enhances visibility in search.
                Include both the code and explanations."""
            elif analysis_type == "serp":
                user_content = f"""Create a SERP feature optimization strategy for: '{query}'
                targeting keywords: '{keywords}'.
                Include:
                1. Featured snippet opportunities and format recommendations
                2. Knowledge panel strategy
                3. People Also Ask optimization
                4. Video and image optimization for search
                5. Local SEO considerations (if applicable)
                6. Mobile SERP optimization
                7. Voice search considerations
                8. SGE-specific positioning strategy"""
                system_content = """You are an expert in SERP feature optimization and SGE positioning.
                Provide strategic advice for maximizing visibility across all search features.
                Format your recommendations clearly with prioritized action items."""
            
            messages = [{"role": "system", "content": system_content}, {"role": "user", "content": user_content}]
            
            completion = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=self.settings.get("temperature", 0.7),
                max_tokens=self.settings.get("max_tokens", 1024),
                stream=True
            )
            
            result = ""
            for chunk in completion:
                content = chunk.choices[0].delta.content
                if content:
                    result += content
                    self.update_output(content, analysis_type)
            
            for item in self.history:
                if item["query"] == query and item["type"] == analysis_type:
                    item["result"] = result
                    break
            
            self.root.after(0, lambda: self.progress_bar.stop())
            self.root.after(0, lambda: self.progress_bar.set(1))
            self.root.after(0, lambda: self.status_label.configure(text="Generation complete!"))
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.root.after(0, lambda: self.show_error(error_msg))
            self.root.after(0, lambda: self.status_label.configure(text="Error occurred"))
            self.root.after(0, lambda: self.progress_bar.stop())
        finally:
            self.is_generating = False

    def update_output(self, content, analysis_type):
        def update():
            if analysis_type == "content":
                self.output_text.insert("end", content)
                self.output_text.see("end")
            elif analysis_type == "intent":
                self.analysis_text.insert("end", content)
                self.analysis_text.see("end")
            elif analysis_type in ["schema", "serp"]:
                self.schema_text.insert("end", content)
                self.schema_text.see("end")
        self.root.after(0, update)

    def add_to_history(self, query, keywords, analysis_type):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        history_item = {"query": query, "keywords": keywords, "type": analysis_type, "timestamp": timestamp, "result": ""}
        self.history.insert(0, history_item)
        if len(self.history) > 10:
            self.history = self.history[:10]
        self.update_history_ui()
        
        if "recent_searches" not in self.settings:
            self.settings["recent_searches"] = []
        self.settings["recent_searches"].insert(0, {"query": query, "keywords": keywords, "type": analysis_type, "timestamp": timestamp})
        if len(self.settings["recent_searches"]) > 20:
            self.settings["recent_searches"] = self.settings["recent_searches"][:20]
        self.save_settings()

    def update_history_ui(self):
        for widget in self.history_frame.winfo_children():
            widget.destroy()
        for item in self.history:
            item_frame = ctk.CTkFrame(self.history_frame)
            item_frame.pack(fill="x", pady=2)
            query_text = ctk.CTkLabel(item_frame, text=item["query"][:25] + "..." if len(item["query"]) > 25 else item["query"], anchor="w", font=ctk.CTkFont(size=12))
            query_text.pack(side="left", padx=5)
            type_indicators = {"content": "📄", "intent": "🔍", "schema": "🏷️", "serp": "📊"}
            type_label = ctk.CTkLabel(item_frame, text=type_indicators.get(item["type"], ""), width=20, font=ctk.CTkFont(size=14))
            type_label.pack(side="right", padx=5)
            item_frame.bind("<Button-1>", lambda e, i=item: self.load_history_item(i))
            query_text.bind("<Button-1>", lambda e, i=item: self.load_history_item(i))
            type_label.bind("<Button-1>", lambda e, i=item: self.load_history_item(i))

    def load_history_item(self, item):
        self.query_entry.delete(0, "end")
        self.query_entry.insert(0, item["query"])
        self.keywords_entry.delete(0, "end")
        self.keywords_entry.insert(0, item["keywords"])
        if item["result"]:
            if item["type"] == "content":
                self.output_notebook.set("Content")
                self.output_text.delete("0.0", "end")
                self.output_text.insert("0.0", item["result"])
            elif item["type"] == "intent":
                self.output_notebook.set("Analysis")
                self.analysis_text.delete("0.0", "end")
                self.analysis_text.insert("0.0", item["result"])
            elif item["type"] in ["schema", "serp"]:
                self.output_notebook.set("Schema")
                self.schema_text.delete("0.0", "end")
                self.schema_text.insert("0.0", item["result"])

    def save_output(self):
        current_tab = self.output_notebook.get()
        if current_tab == "Content":
            content = self.output_text.get("0.0", "end")
        elif current_tab == "Analysis":
            content = self.analysis_text.get("0.0", "end")
        elif current_tab == "Schema":
            content = self.schema_text.get("0.0", "end")
        else:
            content = ""
        if not content.strip():
            self.show_error("No content to save!")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".md", filetypes=[("Markdown", "*.md"), ("Text", "*.txt"), ("All Files", "*.*")])
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                self.status_label.configure(text=f"Saved to {os.path.basename(file_path)}")
                self.current_file = file_path
            except Exception as e:
                self.show_error(f"Error saving file: {str(e)}")

    def copy_to_clipboard(self):
        current_tab = self.output_notebook.get()
        if current_tab == "Content":
            content = self.output_text.get("0.0", "end")
        elif current_tab == "Analysis":
            content = self.analysis_text.get("0.0", "end")
        elif current_tab == "Schema":
            content = self.schema_text.get("0.0", "end")
        else:
            content = ""
        if not content.strip():
            self.show_error("No content to copy!")
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(content)
        self.status_label.configure(text="Copied to clipboard")

    def clear_output(self):
        current_tab = self.output_notebook.get()
        if current_tab == "Content":
            self.output_text.delete("0.0", "end")
        elif current_tab == "Analysis":
            self.analysis_text.delete("0.0", "end")
        elif current_tab == "Schema":
            self.schema_text.delete("0.0", "end")
        self.status_label.configure(text="Output cleared")

    def apply_theme(self):
        """Apply custom theme tweaks"""
        self.root.configure(bg="#1E1E1E")
        self.main_container.configure(fg_color="#1E1E1E", border_color="#2D2D2D")
        self.sidebar.configure(fg_color="#252526")
        self.main_frame.configure(fg_color="#1E1E1E")
        self.output_notebook.configure(fg_color="#252526", border_color="#2D2D2D")

    def open_settings(self):
        """Open settings dialog"""
        settings_window = ctk.CTkToplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("400x300")
        settings_window.transient(self.root)
        settings_window.grab_set()

        # Model selection
        model_label = ctk.CTkLabel(settings_window, text="Default Model:")
        model_label.pack(pady=(10, 0))
        model_var = tk.StringVar(value=self.settings.get("default_model", "llama-3.3-70b-versatile"))
        model_dropdown = ctk.CTkOptionMenu(settings_window, variable=model_var, values=["llama-3.3-70b-versatile", "llama-3.1-70b-versatile", "llama-3.1-8b-versatile", "mixtral-8x7b-32768"])
        model_dropdown.pack(pady=5)

        # Temperature slider
        temp_label = ctk.CTkLabel(settings_window, text="Temperature:")
        temp_label.pack(pady=(10, 0))
        temp_slider = ctk.CTkSlider(settings_window, from_=0.1, to=1.0, number_of_steps=9, command=lambda val: temp_value.configure(text=f"{val:.1f}"))
        temp_slider.set(self.settings.get("temperature", 0.7))
        temp_slider.pack(pady=5)
        temp_value = ctk.CTkLabel(settings_window, text=f"{temp_slider.get():.1f}")
        temp_value.pack()

        # Max tokens entry
        tokens_label = ctk.CTkLabel(settings_window, text="Max Tokens:")
        tokens_label.pack(pady=(10, 0))
        tokens_entry = ctk.CTkEntry(settings_window, placeholder_text="Enter max tokens")
        tokens_entry.insert(0, str(self.settings.get("max_tokens", 1024)))
        tokens_entry.pack(pady=5)

        # Save button
        def save_settings():
            self.settings["default_model"] = model_var.get()
            self.settings["temperature"] = temp_slider.get()
            self.settings["max_tokens"] = int(tokens_entry.get())
            self.save_settings()
            self.selected_model.set(model_var.get())
            settings_window.destroy()
            self.status_label.configure(text="Settings saved")

        save_btn = ctk.CTkButton(settings_window, text="Save", command=save_settings)
        save_btn.pack(pady=20)

    def show_help(self):
        """Show help dialog"""
        help_text = """Advanced SGE Content Intelligence Platform
Features:
- Generate SGE-optimized content
- Analyze search intent
- Create schema markup
- Optimize for SERP features
- Template management
- History tracking
- Analytics dashboard

Usage:
1. Enter a search query and target keywords
2. Select content type and AI model
3. Choose an action (Generate, Analyze, etc.)
4. View results in the tabs
5. Save or copy output as needed"""
        
        messagebox.showinfo("Help", help_text)

    def open_analytics(self):
        """Open analytics dashboard"""
        analytics_window = ctk.CTkToplevel(self.root)
        analytics_window.title("Analytics Dashboard")
        analytics_window.geometry("600x400")
        analytics_window.transient(self.root)
        analytics_window.grab_set()

        # Simple analytics: Number of searches by type
        fig, ax = plt.subplots(figsize=(6, 4))
        types = ["content", "intent", "schema", "serp"]
        counts = [sum(1 for h in self.history if h["type"] == t) for t in types]
        ax.bar(types, counts, color="#306998")
        ax.set_title("Search Type Distribution")
        ax.set_ylabel("Count")
        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=analytics_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        # Close button
        close_btn = ctk.CTkButton(analytics_window, text="Close", command=analytics_window.destroy)
        close_btn.pack(pady=10)

    def show_error(self, message):
        """Show error message"""
        messagebox.showerror("Error", message)

def main():
    root = ctk.CTk()
    app = AdvancedSGEApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()