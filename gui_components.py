import customtkinter as ctk

class SetupWindow(ctk.CTkFrame):
    def __init__(self, parent, on_submit):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)
        self.on_submit = on_submit
        
        self.lbl = ctk.CTkLabel(self, text="Set Master Password", font=ctk.CTkFont(family="SF Pro Display", size=24, weight="bold"), text_color="white")
        self.lbl.pack(pady=(150, 20))
        
        self.pwd = ctk.CTkEntry(self, show="•", placeholder_text="Password", width=300, height=45, corner_radius=12,
                                     fg_color="#2a2d2e", border_color="#3f4345",
                                     text_color="white")
        self.pwd.pack(pady=10)
        self.pwd.bind("<Return>", lambda e: self.submit())
        
        self.btn = ctk.CTkButton(self, text="Create Vault", command=self.submit, width=300, height=45, corner_radius=15, fg_color="#007AFF", hover_color="#005BBF")
        self.btn.pack(pady=20)
        
    def submit(self):
        self.on_submit(self.pwd.get())


class LoginWindow(ctk.CTkFrame):
    def __init__(self, parent, on_submit):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)
        self.on_submit = on_submit
        
        self.lbl = ctk.CTkLabel(self, text="Unlock Vault", font=ctk.CTkFont(family="SF Pro Display", size=24, weight="bold"), text_color="white")
        self.lbl.pack(pady=(150, 20))
        
        self.pwd = ctk.CTkEntry(self, show="•", placeholder_text="Master Password", width=300, height=45, corner_radius=12,
                                     fg_color="#2a2d2e", border_color="#3f4345",
                                     text_color="white")
        self.pwd.pack(pady=10)
        self.pwd.bind("<Return>", lambda e: self.submit())
        
        self.btn = ctk.CTkButton(self, text="Unlock", command=self.submit, width=300, height=45, corner_radius=15, fg_color="#007AFF", hover_color="#005BBF")
        self.btn.pack(pady=20)
        
    def submit(self):
        self.on_submit(self.pwd.get())


class Dashboard(ctk.CTkFrame):
    def __init__(self, parent, vm, password):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)
        self.vm = vm
        self.password = password
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ── Sidebar (Glass Side) ──────────────────────────────────────────
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color="transparent")
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=10)

        self.logo = ctk.CTkLabel(self.sidebar, text="VAULT", font=ctk.CTkFont(family="SF Pro Display", size=24, weight="bold"), text_color="#FFFFFF")
        self.logo.pack(pady=(40, 30))

        self.nav_btn = ctk.CTkButton(self.sidebar, text="🔑  Passwords", fg_color="#007AFF", text_color="white", hover_color="#005BBF", corner_radius=15, height=40)
        self.nav_btn.pack(fill="x", padx=15, pady=5)

        self.add_btn = ctk.CTkButton(self.sidebar, text="➕  Add Password", command=self.add_new_secret, fg_color="#2a2d2e", text_color="white", hover_color="#3f4345", corner_radius=15, height=40)
        self.add_btn.pack(fill="x", padx=15, pady=5)

        self.add_note_btn = ctk.CTkButton(self.sidebar, text="📝  Add Note", command=self.add_new_note, fg_color="#2a2d2e", text_color="white", hover_color="#3f4345", corner_radius=15, height=40)
        self.add_note_btn.pack(fill="x", padx=15, pady=5)

        # ── Main Content (Blurred Workspace) ──────────────────────────────
        self.content = ctk.CTkFrame(self, fg_color="transparent")
        self.content.grid(row=0, column=1, sticky="nsew", padx=30, pady=30)

        # Title with Glow
        self.header = ctk.CTkLabel(self.content, text="Secure Passwords", font=ctk.CTkFont(family="SF Pro Display", size=32, weight="bold"), text_color="#FFFFFF")
        self.header.pack(anchor="w", pady=(0, 20))

        # Floating Glass Search Bar
        self.search = ctk.CTkEntry(self.content, placeholder_text="Search Vault...", height=45, corner_radius=12, fg_color="#2a2d2e", border_width=1, border_color="#3f4345", text_color="white")
        self.search.pack(fill="x", pady=(0, 20))

        # List Area
        self.list_frame = ctk.CTkScrollableFrame(self.content, fg_color="transparent")
        self.list_frame.pack(fill="both", expand=True)

        self.refresh_list()

    def refresh_list(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        data = self.vm.get_entries()
        if not data:
            lbl = ctk.CTkLabel(self.list_frame, text="No items in vault.", text_color="#AAAAAA")
            lbl.pack(pady=20)
            return

        for idx, secret_data in enumerate(data):
            entry_type = secret_data.get("type", "password")
            if entry_type == "note":
                title = secret_data.get("title", "Untitled Note")
                self.add_glass_item("📝 " + title, "Secure Note", idx)
            else:
                app_name = secret_data.get("app_name", "Unknown")
                username = secret_data.get("username", "")
                self.add_glass_item("🔑 " + app_name, username, idx)

    def add_glass_item(self, title, subtitle, idx):
        card = ctk.CTkFrame(self.list_frame, fg_color="#1e1e1e", height=70, corner_radius=15, border_width=1, border_color="#3f4345")
        card.pack(fill="x", pady=8)
        card.pack_propagate(False)

        lbl_title = ctk.CTkLabel(card, text=title, text_color="white", font=ctk.CTkFont(family="SF Pro Text", size=15, weight="bold"))
        lbl_title.place(x=20, y=12)

        lbl_sub = ctk.CTkLabel(card, text=subtitle, text_color="#AAAAAA", font=ctk.CTkFont(family="SF Pro Text", size=12))
        lbl_sub.place(x=20, y=38)

        go_btn = ctk.CTkButton(card, text=">", width=30, height=30, fg_color="#2a2d2e", hover_color="#3f4345", corner_radius=10, command=lambda i=idx: self.view_secret(i))
        go_btn.place(relx=0.95, rely=0.5, anchor="center")
        
    def add_new_secret(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Add New Secret")
        dialog.geometry("350x450")
        dialog.attributes("-topmost", True)
        dialog.configure(fg_color="#1e1e1e")

        ctk.CTkLabel(dialog, text="Title / Website", font=ctk.CTkFont(weight="bold")).pack(pady=(20, 5))
        app_entry = ctk.CTkEntry(dialog, width=250)
        app_entry.pack(pady=5)

        ctk.CTkLabel(dialog, text="Username", font=ctk.CTkFont(weight="bold")).pack(pady=(15, 5))
        user_entry = ctk.CTkEntry(dialog, width=250)
        user_entry.pack(pady=5)

        ctk.CTkLabel(dialog, text="Password", font=ctk.CTkFont(weight="bold")).pack(pady=(15, 5))
        
        pwd_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        pwd_frame.pack(pady=5)
        
        pwd_entry = ctk.CTkEntry(pwd_frame, show="•", width=190)
        pwd_entry.pack(side="left", padx=(0, 10))
        
        def generate_pwd():
            import string
            import secrets
            characters = string.ascii_letters + string.digits + string.punctuation
            pwd = ''.join(secrets.choice(characters) for i in range(16))
            pwd_entry.delete(0, 'end')
            pwd_entry.insert(0, pwd)
            pwd_entry.configure(show="")

        gen_btn = ctk.CTkButton(pwd_frame, text="Generate", width=50, command=generate_pwd, fg_color="#2a2d2e", hover_color="#3f4345")
        gen_btn.pack(side="left")

        def save():
            app = app_entry.get().strip()
            user = user_entry.get().strip()
            pwd = pwd_entry.get()
            if app and pwd:
                self.vm.add_entry({"type": "password", "app_name": app, "username": user, "password": pwd})
                self.vm.save_vault(self.password)
                self.refresh_list()
                dialog.destroy()
            else:
                from tkinter import messagebox
                messagebox.showerror("Error", "Title and Password are required.", parent=dialog)

        save_btn = ctk.CTkButton(dialog, text="Save", command=save, width=250, corner_radius=10)
        save_btn.pack(pady=25)

    def add_new_note(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Add Secure Note")
        dialog.geometry("450x500")
        dialog.attributes("-topmost", True)
        dialog.configure(fg_color="#1e1e1e")

        ctk.CTkLabel(dialog, text="Note Title", font=ctk.CTkFont(weight="bold")).pack(pady=(20, 5))
        title_entry = ctk.CTkEntry(dialog, width=350)
        title_entry.pack(pady=5)

        ctk.CTkLabel(dialog, text="Secure Note Content", font=ctk.CTkFont(weight="bold")).pack(pady=(15, 5))
        content_text = ctk.CTkTextbox(dialog, width=350, height=200, corner_radius=10)
        content_text.pack(pady=5)

        def save():
            title = title_entry.get().strip()
            content = content_text.get("1.0", "end-1c").strip()
            if title and content:
                self.vm.add_entry({"type": "note", "title": title, "content": content})
                self.vm.save_vault(self.password)
                self.refresh_list()
                dialog.destroy()
            else:
                from tkinter import messagebox
                messagebox.showerror("Error", "Title and Content are required.", parent=dialog)

        save_btn = ctk.CTkButton(dialog, text="Save Note", command=save, width=250, corner_radius=10)
        save_btn.pack(pady=25)

    def view_secret(self, idx):
        data = self.vm.get_entries()
        if idx >= len(data): return
        secret = data[idx]
        
        entry_type = secret.get("type", "password")
        
        if entry_type == "note":
            self.view_note(secret, idx)
        else:
            self.view_password(secret, idx)
            
    def view_note(self, secret, idx):
        title = secret.get("title", "Untitled Note")
        content = secret.get("content", "")

        dialog = ctk.CTkToplevel(self)
        dialog.title(f"Note: {title}")
        dialog.geometry("450x500")
        dialog.attributes("-topmost", True)
        dialog.configure(fg_color="#1e1e1e")
            
        ctk.CTkLabel(dialog, text=f"📝 {title}", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(20, 10))
        
        content_box = ctk.CTkTextbox(dialog, width=380, height=250, corner_radius=10)
        content_box.insert("1.0", content)
        content_box.configure(state="disabled") # Make read-only
        content_box.pack(pady=10)
        
        def copy_content():
            self.clipboard_clear()
            self.clipboard_append(content)
            self.update()
            copy_btn.configure(text="Copied!")
            dialog.after(2000, lambda: copy_btn.configure(text="Copy Note"))
            
        def delete_secret():
            self.vm.delete_entry(idx)
            self.vm.save_vault(self.password)
            self.refresh_list()
            dialog.destroy()

        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(pady=15)
        
        copy_btn = ctk.CTkButton(btn_frame, text="Copy Note", command=copy_content, width=120)
        copy_btn.pack(side="left", padx=5)
        
        del_btn = ctk.CTkButton(btn_frame, text="Delete", command=delete_secret, width=80, fg_color="#D32F2F", hover_color="#B71C1C")
        del_btn.pack(side="left", padx=5)

    def view_password(self, secret, idx):
        app_name = secret.get("app_name", "Unknown")

        dialog = ctk.CTkToplevel(self)
        dialog.title(f"Secret: {app_name}")
        dialog.geometry("350x300")
        dialog.attributes("-topmost", True)
        dialog.configure(fg_color="#1e1e1e")
            
        ctk.CTkLabel(dialog, text=f"{app_name}", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(20, 10))
        
        username = secret.get("username", "N/A")
        ctk.CTkLabel(dialog, text=f"Username: {username}", font=ctk.CTkFont(size=14)).pack(pady=5)
        
        pwd = secret.get("password", "")
        # Add a fixed width for the password label to prevent shifting
        pwd_label = ctk.CTkLabel(dialog, text=f"Password: {'•' * 8}", font=ctk.CTkFont(size=14))
        pwd_label.pack(pady=5)

        def toggle_pwd():
            current_text = pwd_label.cget("text")
            if current_text == f"Password: {pwd}":
                pwd_label.configure(text=f"Password: {'•' * 8}")
                toggle_btn.configure(text="Show Password")
            else:
                pwd_label.configure(text=f"Password: {pwd}")
                toggle_btn.configure(text="Hide Password")

        def copy_pwd():
            self.clipboard_clear()
            self.clipboard_append(pwd)
            self.update()
            copy_btn.configure(text="Copied!")
            dialog.after(2000, lambda: copy_btn.configure(text="Copy Password"))
            
        def delete_secret():
            self.vm.delete_entry(idx)
            self.vm.save_vault(self.password)
            self.refresh_list()
            dialog.destroy()

        toggle_btn = ctk.CTkButton(dialog, text="Show Password", command=toggle_pwd, width=150)
        toggle_btn.pack(pady=(20, 5))
        
        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(pady=5)
        
        copy_btn = ctk.CTkButton(btn_frame, text="Copy Password", command=copy_pwd, width=120)
        copy_btn.pack(side="left", padx=5)
        
        del_btn = ctk.CTkButton(btn_frame, text="Delete", command=delete_secret, width=80, fg_color="#D32F2F", hover_color="#B71C1C")
        del_btn.pack(side="left", padx=5)