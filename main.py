import customtkinter as ctk
import pywinstyles
from tkinter import messagebox

from src.vault_manager import VaultManager
from src.gui_components import LoginWindow, SetupWindow, Dashboard

try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

class SecureVaultApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Secure Vault")
        self.geometry("900x600")

        self.configure(fg_color="#111111")
        try:
            pywinstyles.apply_style(self, "acrylic")
            pywinstyles.set_opacity(self, color="#111111", value=0.8)
        except Exception:
            pass

        self.vm = VaultManager()
        self.password = None

        if not self.vm.vault_exists():
            self.show_setup()
        else:
            self.show_login()

    def show_setup(self):
        self._clear()
        SetupWindow(self, self.handle_setup)

    def handle_setup(self, password):
        try:
            self.vm.initialize_vault(password)
            self.password = password
        except Exception as e:
            messagebox.showerror("Setup Error", f"Could not initialize vault:\n{e}", parent=self)
            return
        self.show_dashboard()

    def show_login(self):
        self._clear()
        LoginWindow(self, self.handle_login)

    def handle_login(self, password):
        try:
            self.vm.load_vault(password)
            self.password = password
        except Exception:
            messagebox.showerror("Login Error", "Incorrect master password or corrupted vault.", parent=self)
            return
        self.show_dashboard()

    def show_dashboard(self):
        self._clear()
        Dashboard(self, self.vm, self.password)

    def _clear(self):
        for widget in self.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = SecureVaultApp()
    app.mainloop()
