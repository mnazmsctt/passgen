#!/usr/bin/env python3
"""
passgen-pro - Password Generator CLI yang Keren
"""

import typer
import random
import string
import pyperclip
from rich.console import Console
from rich.panel import Panel
from rich.progress import track
from typing import Optional

console = Console()
app = typer.Typer(help="🔐 passgen-pro - Password Generator Keren")

def generate_password(
    length: int = 16,
    uppercase: bool = True,
    lowercase: bool = True,
    digits: bool = True,
    symbols: bool = True,
    passphrase: bool = False
) -> str:
    if passphrase:
        # Simple word list untuk passphrase
        words = ["apple", "banana", "mountain", "river", "sunset", "guitar", "thunder", "ocean", "forest", "dragon"]
        return "-".join(random.choice(words) for _ in range(4))
    
    characters = ""
    if uppercase: characters += string.ascii_uppercase
    if lowercase: characters += string.ascii_lowercase
    if digits: characters += string.digits
    if symbols: characters += "!@#$%^&*()_+-=[]{}|;:,.<>/?"

    return ''.join(random.choice(characters) for _ in range(length))


def password_strength(password: str) -> tuple[str, str]:
    score = 0
    if len(password) >= 16: score += 3
    elif len(password) >= 12: score += 2
    if any(c.isupper() for c in password): score += 1
    if any(c.islower() for c in password): score += 1
    if any(c.isdigit() for c in password): score += 1
    if any(c in "!@#$%^&*" for c in password): score += 1

    if score >= 6:  return "🟢 SANGAT KUAT", "green"
    elif score >= 4: return "🟡 KUAT", "yellow"
    else:            return "🔴 LEMAH", "red"


@app.command()
def gen(
    length: int = typer.Option(16, "--length", "-l", help="Panjang password"),
    amount: int = typer.Option(1, "--amount", "-a", help="Jumlah password"),
    no_upper: bool = typer.Option(False, "--no-upper"),
    no_lower: bool = typer.Option(False, "--no-lower"),
    no_digit: bool = typer.Option(False, "--no-digit"),
    no_symbol: bool = typer.Option(False, "--no-symbol"),
    passphrase: bool = typer.Option(False, "--passphrase", "-p", help="Generate passphrase (kata-kata)"),
    copy: bool = typer.Option(True, "--copy/--no-copy"),
):
    """Generate password keren"""
    
    console.print(Panel.fit("[bold cyan]🔐 PASSGEN PRO[/bold cyan]", border_style="cyan"))

    for i in range(amount):
        password = generate_password(
            length=length,
            uppercase=not no_upper,
            lowercase=not no_lower,
            digits=not no_digit,
            symbols=not no_symbol,
            passphrase=passphrase
        )

        strength_text, color = password_strength(password)

        console.print(f"🔑 [bold]{password}[/bold]")
        console.print(f"   {strength_text}  •  {len(password)} karakter", style=color)
        
        if copy and i == 0 and amount == 1:
            try:
                pyperclip.copy(password)
                console.print("   📋 Password sudah dicopy ke clipboard!", style="yellow")
            except:
                console.print("   ⚠️  Clipboard tidak tersedia", style="yellow")

        if amount > 1:
            console.print("")


@app.command()
def strength(password: str = typer.Argument(..., help="Password yang mau dicek")):
    """Cek kekuatan password"""
    strength_text, color = password_strength(password)
    console.print(Panel(f"[bold]{password}[/bold]\n\nKekuatan: [{color}]{strength_text}[/{color}]"))


if __name__ == "__main__":
    app()