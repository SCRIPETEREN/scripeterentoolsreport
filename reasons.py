# reasons.py – Template alasan per kategori untuk SCRIPETEREN TOOLS REPORT

REASON_TEMPLATES = {
    "sosial_media": [
        "Akun ini mengirim spam ke inbox saya setiap hari.",
        "Akun ini menyebarkan konten yang menghina dan ujaran kebencian.",
        "Akun ini mencuri foto profil dan berpura-pura menjadi saya.",
        "Akun ini melakukan penipuan dengan mengatasnamakan teman saya.",
        "Akun ini meminta data pribadi melalui pesan langsung."
    ],
    "ecommerce": [
        "Toko ini menjual barang palsu dan tidak mengirim pesanan.",
        "Penjual ini meminta pembayaran di luar aplikasi dan tidak mengirim barang.",
        "Produk yang diterima berbeda jauh dari deskripsi.",
        "Penjual ini mengirim link phishing melalui chat.",
        "Penjual ini tidak memberikan garansi yang dijanjikan."
    ],
    "ecommerce_intl": [
        "This seller never shipped the item after payment.",
        "The product received is counterfeit.",
        "The seller asked for payment outside the platform.",
        "This account sent phishing links via chat.",
        "The seller provided fake tracking number."
    ],
    "bank": [
        "Rekening ini digunakan untuk menampung dana hasil penipuan.",
        "Saya menerima transfer mencurigakan dari rekening ini.",
        "Rekening ini meminta saya mentransfer uang untuk investasi palsu.",
        "Rekening ini terlibat dalam skema money mule.",
        "Saya menjadi korban penipuan melalui rekening ini."
    ],
    "bank_intl": [
        "This account is involved in fraud and money laundering.",
        "I received a suspicious transfer from this account.",
        "This account asked me to send money for fake investment.",
        "This account is linked to a scam syndicate.",
        "This account is used for money muling."
    ],
    "pemerintah": [
        "Nomor ini digunakan untuk menyebarkan hoax dan berita palsu.",
        "Saya menerima ancaman melalui nomor ini.",
        "Nomor ini meminta data pribadi dengan mengaku petugas pajak.",
        "Nomor ini melakukan penipuan mengatasnamakan lembaga pemerintah.",
        "Saya menerima pesan mengaku dari instansi resmi namun mencurigakan."
    ],
    "pemerintah_intl": [
        "This number is used for international scam calls.",
        "I received a phishing attempt from this number.",
        "This number impersonates a government official.",
        "This number is involved in cross-border fraud.",
        "This number claims to be from a foreign embassy."
    ],
    "teknologi": [
        "Domain ini digunakan untuk hosting situs phishing.",
        "IP ini melakukan serangan DDoS ke server saya.",
        "Akun ini menyebarkan malware melalui link.",
        "Layanan ini digunakan untuk mengirim email spam.",
        "Aplikasi ini meminta izin berlebihan tanpa alasan."
    ],
    "hosting": [
        "Server ini digunakan untuk hosting situs ilegal.",
        "Domain ini menyebarkan konten berbahaya.",
        "Hosting ini digunakan untuk phishing campaign.",
        "Server ini menjadi sumber serangan siber.",
        "Server ini digunakan untuk botnet."
    ],
    "domain": [
        "Domain ini digunakan untuk situs penipuan.",
        "Domain ini meniru situs resmi untuk mencuri data.",
        "Domain ini menyebarkan malware.",
        "Domain ini digunakan untuk spam massal.",
        "Domain ini terlibat dalam kegiatan ilegal."
    ],
    "forum": [
        "User ini menyebarkan konten ilegal di forum.",
        "User ini melakukan doxxing terhadap anggota lain.",
        "User ini mengirim spam dan link berbahaya.",
        "User ini melakukan pelecehan di ruang diskusi.",
        "User ini mempromosikan situs judi ilegal."
    ],
    "media": [
        "Berita ini tidak benar dan menyesatkan publik.",
        "Artikel ini memicu kebencian antar kelompok.",
        "Media ini menyebarkan informasi palsu.",
        "Komentar di bawah artikel ini penuh dengan ujaran kebencian.",
        "Media ini melakukan clickbait berbahaya."
    ],
    "media_intl": [
        "This news article contains false information.",
        "This media outlet is spreading hate speech.",
        "This article is misleading the public.",
        "The comments section is full of toxic content.",
        "This outlet is known for fake news."
    ],
    "fintech": [
        "Saya menerima transfer mencurigakan dari aplikasi ini.",
        "Aplikasi ini meminta akses berlebihan ke data pribadi.",
        "Saya menjadi korban phishing melalui aplikasi ini.",
        "Transaksi di aplikasi ini tidak sesuai dengan riwayat saya.",
        "Aplikasi ini gagal memproses penarikan dana saya."
    ],
    "travel": [
        "Driver ini tidak mengkonfirmasi pesanan dan meminta bayaran di luar aplikasi.",
        "Penginapan ini tidak sesuai dengan foto dan deskripsi.",
        "Saya menerima ancaman dari driver ini.",
        "Pesanan tiket saya dibatalkan tanpa pemberitahuan.",
        "Driver ini meminta uang tambahan secara paksa."
    ],
    "game": [
        "Player ini menggunakan cheat dan merusak permainan.",
        "Player ini melakukan toxic behavior di chat.",
        "Player ini melakukan penipuan dalam transaksi item game.",
        "Player ini mengirim link phishing melalui DM game.",
        "Player ini melakukan exploit terhadap bug game."
    ],
    "streaming": [
        "Konten ini melanggar hak cipta.",
        "Konten ini mengandung unsur kekerasan berlebihan.",
        "Komentar di bawah konten ini penuh dengan spam.",
        "Akun ini mempromosikan situs ilegal di chat.",
        "Streamer ini melakukan tindakan tidak pantas."
    ],
    "pendidikan": [
        "Kursus ini menipu dengan materi yang tidak sesuai.",
        "Platform ini tidak memberikan sertifikat setelah pembayaran.",
        "Instruktur ini melakukan plagiarisme.",
        "Saya menerima spam dari platform ini setiap hari.",
        "Platform ini tidak memberikan akses setelah pembayaran."
    ],
    "jasa": [
        "Freelancer ini tidak menyelesaikan pekerjaan sesuai kontrak.",
        "Saya ditipu oleh freelancer ini.",
        "Freelancer ini meminta pembayaran tambahan di luar platform.",
        "Pekerjaan yang diberikan tidak sesuai dengan kesepakatan.",
        "Freelancer ini menghilang setelah menerima pembayaran."
    ],
    "crypto": [
        "Exchange ini membekukan aset saya tanpa alasan.",
        "Saya menerima email phishing mengatasnamakan exchange ini.",
        "Exchange ini diduga terlibat dalam skema ponzi.",
        "Saya tidak bisa menarik aset saya dari exchange ini.",
        "Exchange ini tidak memberikan bukti transaksi yang valid."
    ],
    "marketplace": [
        "Penjual ini tidak mengirim barang setelah pembayaran.",
        "Barang yang diterima adalah palsu.",
        "Penjual ini meminta pembayaran di luar platform.",
        "Saya menerima ancaman dari penjual ini.",
        "Penjual ini menghapus listing setelah saya membayar."
    ],
    "keuangan": [
        "Agen asuransi ini menjanjikan klaim palsu.",
        "Saya menerima spam investasi dari nomor ini.",
        "Produk asuransi ini tidak sesuai dengan polis.",
        "Agen ini meminta data pribadi berlebihan.",
        "Saya ditipu oleh agen investasi ilegal."
    ]
}

def get_reasons(category):
    """Kembalikan daftar alasan untuk kategori tertentu, atau default jika tidak ada."""
    return REASON_TEMPLATES.get(category, [
        "Saya melaporkan aktivitas mencurigakan ini untuk keamanan bersama.",
        "Saya menjadi korban penipuan dari entitas ini.",
        "Saya menerima ancaman dan perilaku tidak pantas.",
        "Saya menemukan indikasi penipuan pada akun/layanan ini."
    ])