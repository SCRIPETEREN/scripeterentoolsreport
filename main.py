#!/usr/bin/env python3
import json, sys, time, random, base64
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from auth import get_gmail_service
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich import box
from rich.text import Text
from providers import PROVIDERS, get_categories, get_providers_by_category
from reasons import get_reasons

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
"""
MOTIVATIONAL_MESSAGES = ["Semoga harimu cerah.", "Jangan menyerah.", "Kebebasan adalah hak semua.", "Sukses dimulai dari langkah kecil.", "Anda lebih kuat dari yang Anda kira."]
GITHUB_SUPPORT = "Support: https://github.com/scripeteren/scripeteren-tools-report"

def welcome_screen():
    console.clear()
    console.print(Text(SPLASH_ART, style="bold cyan"))
    console.print()
    console.print(Panel("SCRIPETEREN TOOLS REPORT", border_style="yellow", expand=False))
    console.print()
    loading = ["Memuat Tools...", "Menyiapkan Provider...", "Mengaktifkan Mode Report...", "Siap!"]
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
        task = progress.add_task("[cyan]Loading...", total=len(loading))
        for stage in loading:
            progress.update(task, description=stage)
            time.sleep(0.7)
            progress.advance()
    console.print()
    console.print(Panel(random.choice(MOTIVATIONAL_MESSAGES), border_style="magenta", expand=False))
    console.print()
    console.print(Panel(GITHUB_SUPPORT, border_style="blue", expand=False))
    console.print()
    console.print("[bold yellow]Press Enter to continue...[/bold yellow]")
    input()
    console.clear()

def load_config():
    try:
        with open("config.json", "r") as f:
            return json.load(f)
    except:
        return {}

def get_global_report_data():
    console.print("\n[bold cyan]DATA PENGIRIM & TARGET[/bold cyan]\n")
    data = {}
    data["sender_name"] = Prompt.ask("[bold cyan]Nama lengkap Anda[/bold cyan]", default="User")
    data["sender_email"] = Prompt.ask("[bold cyan]Email Gmail Anda (pengirim)[/bold cyan]", default="user@gmail.com")
    data["sender_phone"] = Prompt.ask("[bold cyan]Nomor telepon Anda[/bold cyan]", default="-")
    data["target_type"] = Prompt.ask("[bold cyan]Jenis target[/bold cyan]", choices=["nomor_telepon","username","id_akun","rekening_bank","domain_ip","email","lainnya"], default="nomor_telepon")
    data["target_value"] = Prompt.ask("[bold cyan]Masukkan data target[/bold cyan]")
    data["target_description"] = Prompt.ask("[bold cyan]Deskripsi singkat masalah[/bold cyan]", default="Penipuan")
    reason_options = ["Penipuan finansial", "Pelecehan/Ancaman", "Spam/Phishing", "Konten ilegal", "Pencurian identitas", "Lainnya"]
    console.print("\n[bold yellow]Alasan laporan:[/bold yellow]")
    for i, r in enumerate(reason_options, 1): console.print(f"  {i}. {r}")
    choice = Prompt.ask("[bold green]Pilih nomor[/bold green]")
    try:
        idx = int(choice)-1
        data["global_reason"] = reason_options[idx] if 0 <= idx < len(reason_options) else Prompt.ask("[bold cyan]Tulis alasan[/bold cyan]")
    except:
        data["global_reason"] = Prompt.ask("[bold cyan]Tulis alasan[/bold cyan]")
    console.print("\n[bold green]Ringkasan:[/bold green]")
    console.print(f"Pengirim: {data['sender_name']} ({data['sender_email']})")
    console.print(f"Target: {data['target_type']} -> {data['target_value']}")
    console.print(f"Alasan: {data['global_reason']}")
    if not Confirm.ask("[bold yellow]Lanjutkan?[/bold yellow]", default=True):
        return get_global_report_data()
    return data

def show_main_menu():
    console.clear()
    console.print(Panel(BANNER, border_style="cyan"))
    console.print("\n[bold yellow]Pilih mode:[/bold yellow]")
    console.print("  1. Report ke satu provider")
    console.print("  2. Report ke satu kategori")
    console.print("  3. Report ke SEMUA provider")
    console.print("  4. Custom daftar provider")
    console.print("  5. Keluar")
    return Prompt.ask("[bold green]Pilihan[/bold green]", choices=["1","2","3","4","5"])

def select_provider():
    names = list(PROVIDERS.keys())
    total = len(names)
    page = 0
    per_page = 20
    while True:
        start = page*per_page
        end = min(start+per_page, total)
        table = Table(title=f"Provider (halaman {page+1}/{(total-1)//per_page+1})", box=box.ROUNDED)
        table.add_column("No", style="cyan")
        table.add_column("Nama", style="green")
        table.add_column("Kategori", style="yellow")
        for i in range(start, end):
            name = names[i]
            table.add_row(str(i+1), name, PROVIDERS[name]["category"])
        console.print(table)
        console.print("[dim]Ketik nomor, 'n' next, 'p' prev, 'q' batal[/dim]")
        choice = Prompt.ask("[bold green]Pilih[/bold green]")
        if choice.lower()=='n':
            if end < total: page += 1
            else: console.print("[red]Halaman terakhir[/red]")
        elif choice.lower()=='p':
            if page > 0: page -= 1
            else: console.print("[red]Halaman pertama[/red]")
        elif choice.lower()=='q':
            return []
        else:
            try:
                idx = int(choice)-1
                if 0 <= idx < total:
                    return [names[idx]]
                else:
                    console.print("[red]Nomor tidak valid[/red]")
            except:
                console.print("[red]Input tidak valid[/red]")

def select_category():
    categories = get_categories()
    table = Table(title="Kategori", box=box.ROUNDED)
    table.add_column("No", style="cyan")
    table.add_column("Kategori", style="yellow")
    for i, cat in enumerate(categories, 1):
        table.add_row(str(i), cat)
    console.print(table)
    choice = Prompt.ask("[bold green]Pilih nomor kategori[/bold green]")
    try:
        idx = int(choice)-1
        if 0 <= idx < len(categories):
            return list(get_providers_by_category(categories[idx]).keys())
        else:
            console.print("[red]Nomor tidak valid[/red]")
            return []
    except:
        console.print("[red]Input tidak valid[/red]")
        return []

def get_report_count():
    console.print("\n[bold yellow]Jumlah pengiriman:[/bold yellow]")
    console.print("  - 0 = infinite (Ctrl+C untuk berhenti)")
    console.print("  - angka >0 = jumlah tertentu")
    return IntPrompt.ask("[bold green]Masukkan angka[/bold green]", default=0)

def get_delay():
    return float(Prompt.ask("[bold green]Jeda antar kirim (detik)[/bold green]", default="0.5"))

def get_specific_input(category, global_data):
    extra = {}
    if category in ["game","streaming","forum"]:
        extra["id_user"] = Prompt.ask("[bold cyan]ID/Username target[/bold cyan]", default=global_data.get("target_value",""))
        if category=="game": extra["server"] = Prompt.ask("[bold cyan]Server game[/bold cyan]", default="-")
    elif category in ["ecommerce","ecommerce_intl","marketplace"]:
        extra["order_id"] = Prompt.ask("[bold cyan]Order ID[/bold cyan]", default="-")
        extra["seller_name"] = Prompt.ask("[bold cyan]Nama penjual[/bold cyan]", default="-")
    elif category in ["bank","bank_intl","fintech"]:
        extra["rekening"] = Prompt.ask("[bold cyan]Nomor rekening[/bold cyan]", default=global_data.get("target_value",""))
        extra["nama_pemilik"] = Prompt.ask("[bold cyan]Nama pemilik[/bold cyan]", default="-")
    elif category in ["travel","jasa"]:
        extra["nama_driver"] = Prompt.ask("[bold cyan]Nama driver[/bold cyan]", default="-")
        extra["id_transaksi"] = Prompt.ask("[bold cyan]ID transaksi[/bold cyan]", default="-")
    elif category in ["pemerintah","pemerintah_intl"]:
        extra["instansi"] = Prompt.ask("[bold cyan]Instansi[/bold cyan]", default="-")
    elif category in ["teknologi","hosting","domain"]:
        extra["domain_ip"] = Prompt.ask("[bold cyan]Domain/IP[/bold cyan]", default=global_data.get("target_value",""))
    else:
        extra["keterangan"] = Prompt.ask("[bold cyan]Keterangan tambahan[/bold cyan]", default="-")
    return extra

def get_report_reason(category, global_reason):
    reasons = get_reasons(category)
    console.print(f"\n[bold yellow]Pilih alasan untuk kategori '{category}':[/bold yellow]")
    for i, r in enumerate(reasons, 1): console.print(f"  {i}. {r}")
    console.print(f"  {len(reasons)+1}. Tulis sendiri")
    console.print(f"  {len(reasons)+2}. Pakai alasan global: '{global_reason}'")
    choice = Prompt.ask("[bold green]Pilih nomor[/bold green]")
    try:
        idx = int(choice)-1
        if 0 <= idx < len(reasons): return reasons[idx]
        elif idx == len(reasons): return Prompt.ask("[bold cyan]Tulis alasan[/bold cyan]")
        elif idx == len(reasons)+1: return global_reason
        else: return global_reason
    except: return global_reason

def send_email_via_oauth(sender_email, target_email, subject, body):
    try:
        creds = get_gmail_service()
        service = build('gmail', 'v1', credentials=creds)
        message = MIMEText(body)
        message['to'] = target_email
        message['subject'] = subject
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        service.users().messages().send(userId='me', body={'raw': raw}).execute()
        return {"status": "sent", "target": target_email}
    except Exception as e:
        return {"status": "failed", "error": str(e)}

def run_reports(provider_names, global_data, count, delay):
    sender_email = global_data.get("sender_email")
    if not sender_email:
        console.print("[red]Email pengirim tidak ditemukan.[/red]")
        return
    subject_base = f"Laporan dari {global_data.get('sender_name','User')}"
    specific_data = {}
    for name in provider_names:
        cat = PROVIDERS[name]["category"]
        if cat not in specific_data:
            console.print(f"\n[bold cyan]Kategori: {cat}[/bold cyan]")
            specific_data[cat] = get_specific_input(cat, global_data)
            specific_data[cat]["reason"] = get_report_reason(cat, global_data.get("global_reason","Penipuan"))
    total = len(provider_names)
    console.print(f"\n[bold cyan]Akan mengirim ke {total} provider.[/bold cyan]")
    if count == 0: console.print("[bold yellow]Mode INFINITE[/bold yellow]")
    else: console.print(f"[bold yellow]Total kiriman: {count} kali per provider.[/bold yellow]")
    if not Confirm.ask("[bold red]Lanjutkan?[/bold red]", default=False):
        console.print("[red]Dibatalkan.[/red]")
        return
    sent = 0
    failed = 0
    try:
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
            task = progress.add_task("[cyan]Mengirim...", total=total * (count if count > 0 else 1))
            while True:
                for name in provider_names:
                    info = PROVIDERS[name]
                    cat = info["category"]
                    data = specific_data[cat]
                    method = info.get("method", "email")
                    body_lines = [
                        f"Laporan dari: {global_data.get('sender_name','User')}",
                        f"Email: {global_data.get('sender_email','-')}",
                        f"Telepon: {global_data.get('sender_phone','-')}",
                        "",
                        "Target:",
                        f"  - Jenis: {global_data.get('target_type','-')}",
                        f"  - Nilai: {global_data.get('target_value','-')}",
                        f"  - Deskripsi: {global_data.get('target_description','-')}",
                        "",
                        f"Kategori: {cat}",
                        f"Alasan: {data.get('reason','Penipuan')}",
                        "",
                        "Data Spesifik:"
                    ]
                    for k,v in data.items():
                        if k != "reason" and v:
                            body_lines.append(f"  - {k}: {v}")
                    body = "\n".join(body_lines)
                    subject = f"{subject_base} - {name}"
                    if method == "email":
                        target = info.get("target")
                        if not target:
                            result = {"status": "failed", "error": "Target email tidak ditemukan"}
                        else:
                            result = send_email_via_oauth(sender_email, target, subject, body)
                    elif method == "http":
                        result = {"status": "simulated", "provider": name, "url": info.get("url","-")}
                    elif method == "form":
                        result = {"status": "simulated", "provider": name, "note": f"Buka {info.get('url','-')} dan isi manual"}
                    else:
                        result = {"status": "failed", "error": f"Metode '{method}' tidak dikenal"}
                    if result.get("status") in ["sent","simulated"]:
                        console.print(f"[green]SUKSES[/green] {name} -> {result.get('target', result.get('url','success'))}")
                        sent += 1
                    else:
                        console.print(f"[red]GAGAL[/red] {name} : {result.get('error','unknown')}")
                        failed += 1
                    progress.update(task, advance=1)
                    if count > 0 and (sent+failed) >= count * total:
                        console.print("\n[bold green]Selesai![/bold green]")
                        console.print(f"[green]Berhasil: {sent}[/green]" + (f" [red]Gagal: {failed}[/red]" if failed else ""))
                        return
                    time.sleep(delay)
                if count == 0:
                    console.print("[dim]Satu siklus selesai, lanjut...[/dim]")
                else:
                    break
    except KeyboardInterrupt:
        console.print(f"\n[bold yellow]Dihentikan user. Berhasil: {sent}, Gagal: {failed}[/bold yellow]")

def main():
    welcome_screen()
    import os
    if not os.path.exists('credentials.json'):
        console.print("[red]ERROR: credentials.json tidak ditemukan.[/red]")
        console.print("[yellow]Ikuti panduan README untuk membuat credentials OAuth.[/yellow]")
        sys.exit(1)
    global_data = get_global_report_data()
    while True:
        choice = show_main_menu()
        if choice == "5":
            console.print("[bold cyan]Sampai jumpa, Tuan![/bold cyan]")
            break
        provider_names = []
        if choice == "1":
            provider_names = select_provider()
        elif choice == "2":
            provider_names = select_category()
        elif choice == "3":
            provider_names = list(PROVIDERS.keys())
        elif choice == "4":
            names = Prompt.ask("[bold green]Masukkan nama provider dipisah koma[/bold green]")
            provider_names = [n.strip() for n in names.split(",") if n.strip() in PROVIDERS]
            if not provider_names:
                console.print("[red]Tidak ada provider valid.[/red]")
                continue
        if not provider_names:
            console.print("[red]Tidak ada provider dipilih.[/red]")
            continue
        count = get_report_count()
        delay = get_delay()
        run_reports(provider_names, global_data, count, delay)
        if not Confirm.ask("[bold cyan]Kembali ke menu utama?[/bold cyan]", default=True):
            break

if __name__ == "__main__":
    main()