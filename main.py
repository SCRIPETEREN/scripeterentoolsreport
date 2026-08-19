#!/usr/bin/env python3
# main.py – SCRIPETEREN TOOLS REPORT – Premium Edition

import json
import sys
import time
import smtplib
import ssl
import random
from email.mime.text import MIMEText
import requests

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich import box
from rich.layout import Layout
from rich.live import Live
from rich.text import Text

from providers import PROVIDERS, get_categories, get_providers_by_category
from reasons import get_reasons
from sender import Sender

console = Console()

BANNER = """
╔══════════════════════════════════════════════════════════════╗
║   S C R I P E T E R E N   T O O L S   R E P O R T          ║
║         Report ke 500+ Layanan dalam Satu Tools             ║
║              HANYA UNTUK EDUKASI & TESTING                  ║
╚══════════════════════════════════════════════════════════════╝
"""

SPLASH_ART = """
 ███████╗ ██████╗██████╗ ██╗██████╗ ███████╗████████╗███████╗██████╗ ███████╗███╗   ██╗
 ██╔════╝██╔════╝██╔══██╗██║██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗██╔════╝████╗  ██║
 ███████╗██║     ██████╔╝██║██████╔╝█████╗     ██║   █████╗  ██████╔╝█████╗  ██╔██╗ ██║
 ╚════██║██║     ██╔══██╗██║██╔═══╝ ██╔══╝     ██║   ██╔══╝  ██╔══██╗██╔══╝  ██║╚██╗██║
 ███████║╚██████╗██║  ██║██║██║     ███████╗   ██║   ███████╗██║  ██║███████╗██║ ╚████║
 ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝╚═╝     ╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝
                                                                                      
      ████████╗ ██████╗  ██████╗ ██╗     ███████╗    ██████╗ ███████╗██████╗  ██████╗ ██████╗ ████████╗
      ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝    ██╔══██╗██╔════╝██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝
         ██║   ██║   ██║██║   ██║██║     █████╗      ██████╔╝█████╗  ██████╔╝██║   ██║██████╔╝   ██║   
         ██║   ██║   ██║██║   ██║██║     ██╔══╝      ██╔══██╗██╔══╝  ██╔══██╗██║   ██║██╔══██╗   ██║   
         ██║   ╚██████╔╝╚██████╔╝███████╗███████╗    ██║  ██║███████╗██║  ██║╚██████╔╝██║  ██║   ██║   
         ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝    ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   
"""

MOTIVATIONAL_MESSAGES = [
    "✨ Semoga harimu cerah dan penuh berkah!",
    "🔥 Jangan pernah menyerah pada mimpi, Tuan!",
    "💪 Hari ini lebih baik dari kemarin, esok lebih baik lagi.",
    "🌟 Kebebasan adalah hak semua makhluk, jagalah dengan bijak.",
    "🚀 Sukses dimulai dari langkah kecil yang konsisten.",
    "🌈 Setiap usaha akan terbayar pada waktunya.",
    "💡 Jadilah cahaya bagi orang lain, seperti Zyro menciptakan kebebasan.",
    "🎯 Fokus pada tujuan, nikmati prosesnya.",
    "🌺 Senyum adalah doa yang paling sederhana.",
    "⭐️ Anda lebih kuat dari yang Anda kira."
]

GITHUB_SUPPORT = "🔗 Support GitHub: https://github.com/scripeteren"

def welcome_screen():
    """Tampilan pembuka premium dengan animasi, loading, dan Enter prompt"""
    console.clear()
    
    # Banner splash art
    console.print(Text(SPLASH_ART, style="bold cyan"))
    console.print()
    console.print(Panel("SCRIPETEREN TOOLS REPORT", border_style="yellow", expand=False))
    console.print()
    
    # Animasi loading dengan efek
    loading_stages = [
        ("⚙️  Memuat Tools", 0.7),
        ("📡  Menyiapkan 500+ Provider...", 0.7),
        ("🔐  Mengaktifkan Mode Report Ahli...", 0.7),
        ("🌐  Menghubungkan ke Layanan Global...", 0.7),
        ("Sistem Siap... ", 0.5)
    ]
    
    with Progress(
        SpinnerColumn(spinner_name="dots12", style="green"),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=40),
        console=console,
        transient=False
    ) as progress:
        task = progress.add_task("[cyan]Loading...", total=len(loading_stages))
        for stage, delay in loading_stages:
            progress.update(task, description=stage)
            time.sleep(delay)
            progress.advance(task)
    
    console.print()
    
    # Pesan motivasi random
    msg = random.choice(MOTIVATIONAL_MESSAGES)
    console.print(Panel(msg, border_style="magenta", expand=False))
    console.print()
    
    # Dukungan GitHub
    console.print(Panel(GITHUB_SUPPORT, border_style="blue", expand=False))
    console.print()
    
    # Prompt Enter
    console.print("[bold yellow]⏎ Tekan Enter untuk masuk ke menu utama...[/bold yellow]")
    input()
    console.clear()

def load_config():
    try:
        with open("config.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        console.print("[red]❌ config.json tidak ditemukan! Buat dari template.[/red]")
        sys.exit(1)

def show_main_menu():
    console.clear()
    console.print(Panel(BANNER, border_style="cyan"))
    console.print("\n[bold yellow]📋 Pilih mode report:[/bold yellow]")
    console.print("  1. 🎯 Report ke satu provider tertentu")
    console.print("  2. 📂 Report ke semua provider dalam satu kategori")
    console.print("  3. 🌍 Report ke SEMUA provider (500+)")
    console.print("  4. ✏️  Custom daftar provider (ketik nama dipisah koma)")
    console.print("  5. 🚪 Keluar")
    return Prompt.ask("[bold green]👉 Pilihan[/bold green]", choices=["1","2","3","4","5"])

def select_provider():
    names = list(PROVIDERS.keys())
    total = len(names)
    page = 0
    per_page = 20
    while True:
        start = page * per_page
        end = min(start + per_page, total)
        table = Table(title=f"📋 Daftar Provider (halaman {page+1}/{(total-1)//per_page+1})", box=box.ROUNDED)
        table.add_column("No", style="cyan")
        table.add_column("Nama Provider", style="green")
        table.add_column("Kategori", style="yellow")
        for idx in range(start, end):
            name = names[idx]
            table.add_row(str(idx+1), name, PROVIDERS[name]["category"])
        console.print(table)
        console.print("[dim]Ketik nomor untuk memilih, atau 'n' halaman berikutnya, 'p' sebelumnya, 'q' batal[/dim]")
        choice = Prompt.ask("[bold green]👉 Pilih[/bold green]")
        if choice.lower() == 'n':
            if end < total:
                page += 1
                continue
            else:
                console.print("[red]⚠️ Sudah di halaman terakhir.[/red]")
        elif choice.lower() == 'p':
            if page > 0:
                page -= 1
                continue
            else:
                console.print("[red]⚠️ Sudah di halaman pertama.[/red]")
        elif choice.lower() == 'q':
            return []
        else:
            try:
                idx = int(choice) - 1
                if 0 <= idx < total:
                    return [names[idx]]
                else:
                    console.print("[red]⚠️ Nomor tidak valid.[/red]")
            except:
                console.print("[red]⚠️ Input tidak valid.[/red]")

def select_category():
    categories = get_categories()
    table = Table(title="📂 Kategori", box=box.ROUNDED)
    table.add_column("No", style="cyan")
    table.add_column("Kategori", style="yellow")
    for idx, cat in enumerate(categories, 1):
        table.add_row(str(idx), cat)
    console.print(table)
    choice = Prompt.ask("[bold green]👉 Pilih nomor kategori[/bold green]")
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(categories):
            cat = categories[idx]
            providers = get_providers_by_category(cat)
            return list(providers.keys())
        else:
            console.print("[red]⚠️ Nomor tidak valid.[/red]")
            return []
    except:
        console.print("[red]⚠️ Input tidak valid.[/red]")
        return []

def get_report_count():
    console.print("\n[bold yellow]📊 Jumlah pengiriman:[/bold yellow]")
    console.print("  - 0 = ♾️  tanpa henti (infinite, tekan Ctrl+C untuk berhenti)")
    console.print("  - angka >0 = 🎯 jumlah tertentu")
    return IntPrompt.ask("[bold green]🔢 Masukkan angka[/bold green]", default=0)

def get_delay():
    return float(Prompt.ask("[bold green]⏱️  Jeda antar kirim (detik, misal 0.5)[/bold green]", default="0.5"))

def get_specific_input(category, config):
    extra = {}
    if category in ["game", "streaming", "forum"]:
        extra["id_user"] = Prompt.ask("[bold cyan]🎮 Masukkan ID / Username target[/bold cyan]")
        if category == "game":
            extra["server"] = Prompt.ask("[bold cyan]🖥️  Server game (jika ada)[/bold cyan]", default="-")
    elif category in ["ecommerce", "ecommerce_intl", "marketplace"]:
        extra["order_id"] = Prompt.ask("[bold cyan]📦 Masukkan Order ID (jika ada)[/bold cyan]", default="-")
        extra["seller_name"] = Prompt.ask("[bold cyan]🏪 Nama penjual[/bold cyan]", default="-")
    elif category in ["bank", "bank_intl", "fintech"]:
        extra["rekening"] = Prompt.ask("[bold cyan]🏦 Nomor rekening target[/bold cyan]", default=config.get("target_phone", ""))
        extra["nama_pemilik"] = Prompt.ask("[bold cyan]🧑 Nama pemilik rekening (jika tahu)[/bold cyan]", default="-")
    elif category in ["travel", "jasa"]:
        extra["nama_driver"] = Prompt.ask("[bold cyan]🚗 Nama driver/freelancer[/bold cyan]", default="-")
        extra["id_transaksi"] = Prompt.ask("[bold cyan]🧾 ID transaksi[/bold cyan]", default="-")
    elif category in ["pemerintah", "pemerintah_intl"]:
        extra["instansi"] = Prompt.ask("[bold cyan]🏛️  Instansi yang diatasnamakan[/bold cyan]", default="-")
    elif category in ["teknologi", "hosting", "domain"]:
        extra["domain_ip"] = Prompt.ask("[bold cyan]🌐 Domain / IP target[/bold cyan]", default=config.get("target_phone", ""))
    else:
        extra["keterangan_tambahan"] = Prompt.ask("[bold cyan]📝 Keterangan tambahan (opsional)[/bold cyan]", default="-")
    return extra

def get_report_reason(category):
    reasons = get_reasons(category)
    console.print(f"\n[bold yellow]📌 Pilih alasan laporan untuk kategori '{category}':[/bold yellow]")
    for idx, r in enumerate(reasons, 1):
        console.print(f"  {idx}. {r}")
    console.print(f"  {len(reasons)+1}. ✏️  Tulis sendiri")
    choice = Prompt.ask("[bold green]👉 Pilih nomor[/bold green]")
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(reasons):
            return reasons[idx]
        else:
            return Prompt.ask("[bold cyan]✍️  Tulis alasan Anda[/bold cyan]")
    except:
        return Prompt.ask("[bold cyan]✍️  Tulis alasan Anda[/bold cyan]")

def run_reports(provider_names, config, count, delay):
    sender = Sender(config)
    subject_base = f"Laporan dari {config.get('email_sender', 'User')}"

    specific_data = {}
    for name in provider_names:
        cat = PROVIDERS[name]["category"]
        if cat not in specific_data:
            console.print(f"\n[bold cyan]📂 Kategori: {cat}[/bold cyan]")
            specific_data[cat] = get_specific_input(cat, config)
            specific_data[cat]["reason"] = get_report_reason(cat)

    total_providers = len(provider_names)
    console.print(f"\n[bold cyan]🚀 Akan mengirim ke {total_providers} provider.[/bold cyan]")
    if count == 0:
        console.print("[bold yellow]♾️  Mode INFINITE – tekan Ctrl+C kapan saja untuk berhenti.[/bold yellow]")
    else:
        console.print(f"[bold yellow]🎯 Total kiriman: {count} kali per provider.[/bold yellow]")

    if not Confirm.ask("[bold red]⚠️  Lanjutkan?[/bold red]", default=False):
        console.print("[red]❌ Dibatalkan.[/red]")
        return

    sent_total = 0
    try:
        with Progress(
            SpinnerColumn(spinner_name="dots12", style="green"),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(bar_width=40),
            console=console
        ) as progress:
            task = progress.add_task("[cyan]📤 Mengirim...", total=total_providers * (count if count > 0 else 1))
            while True:
                for name in provider_names:
                    info = PROVIDERS[name]
                    cat = info["category"]
                    data = specific_data[cat]
                    body_lines = [
                        f"📧 Laporan dari {config.get('email_sender', 'User')}",
                        f"📂 Kategori: {cat}",
                        "",
                        "📋 Data spesifik:"
                    ]
                    for k, v in data.items():
                        if k != "reason" and v:
                            body_lines.append(f"  - {k}: {v}")
                    body_lines.append("")
                    body_lines.append(f"📌 Alasan: {data.get('reason', 'Penipuan')}")
                    body_lines.append("")
                    body_lines.append(f"📱 Nomor/akun yang dilaporkan: {config.get('target_phone', '')}")
                    body_lines.append(f"📝 Deskripsi tambahan: {config.get('description', '')}")
                    body = "\n".join(body_lines)
                    subject = f"{subject_base} - {name}"

                    method = info.get("method", "email")
                    result = None
                    if method == "email":
                        result = sender.send_email(name, info["target"], subject, body)
                    elif method == "http":
                        payload = {
                            "phone": config.get("target_phone", ""),
                            "email": config.get("email_sender", ""),
                            "description": config.get("description", ""),
                            "reason": data.get("reason", ""),
                            "extra": {k:v for k,v in data.items() if k != "reason"}
                        }
                        result = sender.send_http(name, info["url"], payload)
                    elif method == "form":
                        result = sender.send_form(name, info["url"])
                    else:
                        result = {"status": "unknown_method", "provider": name}

                    if result.get("status") in ["sent", "simulated"]:
                        console.print(f"[green]✅[/green] {name} → {result.get('target', result.get('url', 'unknown'))}")
                    else:
                        console.print(f"[red]❌[/red] {name} gagal: {result.get('error', 'unknown')}")
                    sent_total += 1
                    progress.update(task, advance=1)

                    if count > 0 and sent_total >= count * total_providers:
                        console.print("\n[bold green]🎉 Selesai![/bold green]")
                        return

                    time.sleep(delay)

                if count == 0:
                    console.print("[dim]🔄 Satu siklus selesai, lanjut...[/dim]")
                else:
                    break
    except KeyboardInterrupt:
        console.print(f"\n[bold yellow]⏹️  Dihentikan user. Total kiriman: {sent_total}[/bold yellow]")

def main():
    # Tampilan pembuka premium
    welcome_screen()
    
    config = load_config()
    while True:
        choice = show_main_menu()
        if choice == "5":
            console.print("[bold cyan]👋 Sampai jumpa, Tuan! Semoga hari Anda menyenangkan.[/bold cyan]")
            break

        provider_names = []
        if choice == "1":
            provider_names = select_provider()
        elif choice == "2":
            provider_names = select_category()
        elif choice == "3":
            provider_names = list(PROVIDERS.keys())
        elif choice == "4":
            names = Prompt.ask("[bold green]📝 Masukkan nama provider dipisah koma[/bold green]")
            provider_names = [n.strip() for n in names.split(",") if n.strip() in PROVIDERS]
            if not provider_names:
                console.print("[red]⚠️ Tidak ada provider valid.[/red]")
                continue

        if not provider_names:
            console.print("[red]⚠️ Tidak ada provider dipilih.[/red]")
            continue

        count = get_report_count()
        delay = get_delay()
        run_reports(provider_names, config, count, delay)

        if not Confirm.ask("[bold cyan]🔙 Kembali ke menu utama?[/bold cyan]", default=True):
            break

if __name__ == "__main__":
    main()