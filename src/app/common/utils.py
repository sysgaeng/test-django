class ConsoleColors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"


def color_string(color, text):
    getattr(ConsoleColors, color.upper())
    return getattr(ConsoleColors, color.upper()) + str(text) + ConsoleColors.RESET
