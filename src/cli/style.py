from questionary import Style
from rich.console import Console
from rich.theme import Theme

THEME = Theme({
    "success": "bold #3B6D11",
    "error":   "bold #A32D2D",
    "muted":   "#888780",
    "accent":  "#534AB7",
    "info":    "#185FA5",
    "warn":    "#854F0B",
})

console = Console(theme=THEME)

Q_STYLE = Style([
    ("qmark",       "fg:#534AB7 bold"),
    ("question",    "bold"),
    ("answer",      "fg:#3B6D11 bold"),
    ("pointer",     "fg:#534AB7 bold"),
    ("highlighted", "fg:#534AB7 bold"),
    ("selected",    "fg:#3B6D11"),
    ("separator",   "fg:#888780"),
    ("instruction", "fg:#888780 italic"),
])