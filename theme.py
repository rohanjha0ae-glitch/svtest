"""
theme.py — Centralized design tokens and styling helpers for Secure Vault.
"""
import tkinter as tk
from tkinter import ttk

# ──────────────────────────────────────────────
#  Color Palette
# ──────────────────────────────────────────────
BG          = "#0f1117"   # Main window background
SURFACE     = "#1a1d27"   # Card / panel surface
SURFACE2    = "#22263a"   # Slightly lighter surface (sidebar, row hover)
BORDER      = "#2e3250"   # Subtle border / divider
ACCENT      = "#7c6af7"   # Primary accent — blue-violet
ACCENT_DARK = "#5b4fd4"   # Darker accent (button hover)
ACCENT_GLOW = "#9d8fff"   # Lighter accent (highlights)
TEXT        = "#e8eaf6"   # Primary text
TEXT_MUTED  = "#8b8fa8"   # Secondary / placeholder text
TEXT_FAINT  = "#4a4f6a"   # Very dim text
SUCCESS     = "#4caf7d"   # Green (strength bar / match)
WARNING     = "#f5a623"   # Amber
DANGER      = "#e05c5c"   # Red (errors / mismatch)
ENTRY_BG    = "#12141e"   # Input field background
SCROLLBAR   = "#2a2d45"   # Scrollbar trough / thumb

# ──────────────────────────────────────────────
#  Fonts  (Segoe UI preferred on Windows)
# ──────────────────────────────────────────────
FONT_FAMILY  = "Segoe UI"
FONT_TITLE   = (FONT_FAMILY, 22, "bold")
FONT_HEADING = (FONT_FAMILY, 13, "bold")
FONT_LABEL   = (FONT_FAMILY, 10)
FONT_LABEL_B = (FONT_FAMILY, 10, "bold")
FONT_SMALL   = (FONT_FAMILY, 8)
FONT_MONO    = ("Consolas", 10)

# ──────────────────────────────────────────────
#  Dimensions
# ──────────────────────────────────────────────
PAD         = 16
PAD_SM      = 8
RADIUS      = 8    # Used for pseudo-round-corner frames
BTN_PAD_X   = 18
BTN_PAD_Y   = 9

# ──────────────────────────────────────────────
#  Root / Window helpers
# ──────────────────────────────────────────────

def apply_theme(root: tk.Tk):
    """Apply global dark theme to the root Tk window and ttk style."""
    root.configure(bg=BG)
    root.option_add("*Font", FONT_LABEL)

    style = ttk.Style(root)
    # Try a neutral base theme available on Windows
    try:
        style.theme_use("clam")
    except Exception:
        pass

    # ── Treeview ──────────────────────────────
    style.configure("Vault.Treeview",
                    background=SURFACE,
                    foreground=TEXT,
                    fieldbackground=SURFACE,
                    borderwidth=0,
                    rowheight=36,
                    font=FONT_LABEL)
    style.configure("Vault.Treeview.Heading",
                    background=SURFACE2,
                    foreground=TEXT_MUTED,
                    font=FONT_LABEL_B,
                    relief="flat",
                    borderwidth=0)
    style.map("Vault.Treeview",
              background=[("selected", ACCENT_DARK)],
              foreground=[("selected", TEXT)])
    style.map("Vault.Treeview.Heading",
              background=[("active", BORDER)])

    # ── Scrollbar ─────────────────────────────
    style.configure("Vault.Vertical.TScrollbar",
                    background=SCROLLBAR,
                    troughcolor=SURFACE,
                    borderwidth=0,
                    arrowcolor=TEXT_MUTED,
                    width=8)
    style.map("Vault.Vertical.TScrollbar",
              background=[("active", ACCENT)])

    # ── Separator ─────────────────────────────
    style.configure("Vault.TSeparator", background=BORDER)


def center_window(win: tk.Tk | tk.Toplevel, w: int, h: int):
    """Center a window on the screen."""
    win.update_idletasks()
    sw = win.winfo_screenwidth()
    sh = win.winfo_screenheight()
    x = (sw - w) // 2
    y = (sh - h) // 2
    win.geometry(f"{w}x{h}+{x}+{y}")


# ──────────────────────────────────────────────
#  Reusable Styled Widgets
# ──────────────────────────────────────────────

def make_card(parent, **kwargs) -> tk.Frame:
    """A SURFACE-colored rounded-look frame."""
    defaults = dict(bg=SURFACE, padx=PAD, pady=PAD)
    defaults.update(kwargs)
    return tk.Frame(parent, **defaults)


def make_label(parent, text="", bold=False, muted=False, size=None, **kwargs) -> tk.Label:
    font_size = size or 10
    weight = "bold" if bold else "normal"
    color = TEXT_MUTED if muted else TEXT
    return tk.Label(parent, text=text, bg=kwargs.pop("bg", BG),
                    fg=color, font=(FONT_FAMILY, font_size, weight), **kwargs)


def make_entry(parent, show=None, **kwargs) -> tk.Entry:
    """A styled dark-mode entry widget."""
    e = tk.Entry(parent,
                 bg=ENTRY_BG,
                 fg=TEXT,
                 insertbackground=ACCENT_GLOW,
                 relief="flat",
                 font=FONT_LABEL,
                 bd=0,
                 highlightthickness=1,
                 highlightbackground=BORDER,
                 highlightcolor=ACCENT,
                 **({} if show is None else {"show": show}),
                 **kwargs)
    return e


class StyledButton(tk.Frame):
    """A rounded-looking button built from a Frame + Label."""

    def __init__(self, parent, text, command=None,
                 bg=None, fg=TEXT, font=None,
                 padx=BTN_PAD_X, pady=BTN_PAD_Y,
                 danger=False, secondary=False, **kwargs):
        if bg is None:
            if danger:
                bg = DANGER
            elif secondary:
                bg = SURFACE2
            else:
                bg = ACCENT
        self._bg = bg
        self._hover = self._darken(bg)
        super().__init__(parent, bg=bg, cursor="hand2", **kwargs)
        self._label = tk.Label(self, text=text,
                               bg=bg, fg=fg,
                               font=font or FONT_LABEL_B,
                               padx=padx, pady=pady)
        self._label.pack(fill="both", expand=True)
        if command:
            self.bind("<Button-1>", lambda e: command())
            self._label.bind("<Button-1>", lambda e: command())
        self.bind("<Enter>", self._on_enter)
        self._label.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self._label.bind("<Leave>", self._on_leave)

    def _darken(self, hex_color: str) -> str:
        r = max(0, int(hex_color[1:3], 16) - 24)
        g = max(0, int(hex_color[3:5], 16) - 24)
        b = max(0, int(hex_color[5:7], 16) - 24)
        return f"#{r:02x}{g:02x}{b:02x}"

    def _on_enter(self, _=None):
        self.configure(bg=self._hover)
        self._label.configure(bg=self._hover)

    def _on_leave(self, _=None):
        self.configure(bg=self._bg)
        self._label.configure(bg=self._bg)

    def configure_text(self, text: str):
        self._label.configure(text=text)


class LabeledEntry(tk.Frame):
    """Label + Entry pair in a vertical stack, with optional password toggle."""

    def __init__(self, parent, label, secret=False, bg=BG, **kwargs):
        super().__init__(parent, bg=bg, **kwargs)
        self._secret = secret
        self._showing = False

        tk.Label(self, text=label, bg=bg, fg=TEXT_MUTED,
                 font=FONT_SMALL, anchor="w").pack(fill="x")

        row = tk.Frame(self, bg=bg)
        row.pack(fill="x", pady=(2, 0))

        self.entry = make_entry(row, show="•" if secret else None)
        self.entry.pack(side="left", fill="x", expand=True, ipady=6)

        if secret:
            self._toggle_btn = tk.Label(row, text="👁", bg=ENTRY_BG,
                                        fg=TEXT_MUTED, cursor="hand2",
                                        font=(FONT_FAMILY, 11),
                                        padx=6)
            self._toggle_btn.pack(side="right", fill="y")
            self._toggle_btn.bind("<Button-1>", self._toggle)

    def _toggle(self, _=None):
        self._showing = not self._showing
        self.entry.configure(show="" if self._showing else "•")

    def get(self) -> str:
        return self.entry.get()

    def set(self, value: str):
        self.entry.delete(0, "end")
        self.entry.insert(0, value)

    def focus(self):
        self.entry.focus()
