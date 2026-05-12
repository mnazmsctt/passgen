#!/usr/bin/env python3
"""
passgen - Simple & Strong Password Generator
"""

import typer
import random
import string
import pyperclip
from typing import Optional

app = typer.Typer(help="🔐 passgen - Password Generator CLI")

def generate_password(
    length: int = 16,
    uppercase: bool = True,
    lowercase: bool = True,
    digits: bool = True,
    symbols: bool = True
) -> str:
    characters = ""
    if uppercase: characters += string.ascii_uppercase
    if lowercase: characters += string.ascii_lowercase
    if digits: characters += string.digits
    if symbols: characters += "!@#$%^&*()_+-=[]{}|;:,.<>/?"

    if not characters:
        characters = string.ascii_letters + string.digits

    password = ''.join(random.choice(characters) for _ in range(length))
    return password

@app.command()
def gen(
    length: int = typer.Option(16, "--length", "-l", help="Panjang password"),
    no_upper: bool = typer.Option(False, "--no-upper", help="Tanpa huruf besar"),
    no_lower: bool = typer.Option(False, "--no-lower", help="Tanpa huruf kecil"),
    no_digit: bool = typer.Option(False, "--no-digit", help="Tanpa angka"),
    no_symbol: bool = typer.Option(False, "--no-symbol", help="Tanpa simbol"),
    amount: int = typer.Option(1, "--amount", "-a", help="Jumlah password"),
    copy: bool = typer.Option(True, "--copy/--no-copy", help="Copy ke clipboard"),
):
    """Generate password acak"""
    
    for i in range(amount):
        password = generate_password(
            length=length,
            uppercase=not no_upper,
            lowercase=not no_lower,
            digits=not no_digit,
            symbols=not no_symbol
        )
        
        typer.secho(f"🔑 {password}", fg=typer.colors.BRIGHT_GREEN)
        
        if copy and i == 0 and amount == 1:
            pyperclip.copy(password)
            typer.secho("📋 Password sudah dicopy ke clipboard!", fg=typer.colors.YELLOW)

@app.command()
def strength(password: str = typer.Argument(..., help="Password yang mau dicek kekuatannya")):
    """Cek kekuatan password"""
    score = 0
    if len(password) >= 12: score += 2
    if any(c.isupper() for c in password): score += 1
    if any(c.islower() for c in password): score += 1
    if any(c.isdigit() for c in password): score += 1
    if any(c in "!@#$%^&*()_+" for c in password): score += 1

    if score >= 5:
        typer.secho("🟢 Sangat Kuat", fg=typer.colors.GREEN)
    elif score >= 3:
        typer.secho("🟡 Cukup Kuat", fg=typer.colors.YELLOW)
    else:
        typer.secho("🔴 Lemah", fg=typer.colors.RED)

if __name__ == "__main__":
    app()