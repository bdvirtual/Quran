import sqlite3
import json
from pathlib import Path

DB_PATH = Path("quran_primary.db")
OUT_DIR = Path("exported_quran")
SURAH_DIR = OUT_DIR / "surahs"

OUT_DIR.mkdir(exist_ok=True)
SURAH_DIR.mkdir(exist_ok=True)

SURAH_NAMES = {
    1: ("الفاتحة", "আল-ফাতিহা", "Al-Fatihah"),
    2: ("البقرة", "আল-বাকারা", "Al-Baqarah"),
    3: ("آل عمران", "আলে ইমরান", "Ali 'Imran"),
    4: ("النساء", "আন-নিসা", "An-Nisa"),
    5: ("المائدة", "আল-মায়িদাহ", "Al-Ma'idah"),
    6: ("الأنعام", "আল-আনআম", "Al-An'am"),
    7: ("الأعراف", "আল-আরাফ", "Al-A'raf"),
    8: ("الأنفال", "আল-আনফাল", "Al-Anfal"),
    9: ("التوبة", "আত-তাওবা", "At-Tawbah"),
    10: ("يونس", "ইউনুস", "Yunus"),
    11: ("هود", "হুদ", "Hud"),
    12: ("يوسف", "ইউসুফ", "Yusuf"),
    13: ("الرعد", "আর-রাদ", "Ar-Ra'd"),
    14: ("إبراهيم", "ইবরাহীম", "Ibrahim"),
    15: ("الحجر", "আল-হিজর", "Al-Hijr"),
    16: ("النحل", "আন-নাহল", "An-Nahl"),
    17: ("الإسراء", "আল-ইসরা", "Al-Isra"),
    18: ("الكهف", "আল-কাহফ", "Al-Kahf"),
    19: ("مريم", "মারইয়াম", "Maryam"),
    20: ("طه", "ত্বা-হা", "Ta-Ha"),
    21: ("الأنبياء", "আল-আম্বিয়া", "Al-Anbya"),
    22: ("الحج", "আল-হাজ্জ", "Al-Hajj"),
    23: ("المؤمنون", "আল-মুমিনূন", "Al-Mu'minun"),
    24: ("النور", "আন-নূর", "An-Nur"),
    25: ("الفرقان", "আল-ফুরকান", "Al-Furqan"),
    26: ("الشعراء", "আশ-শুআরা", "Ash-Shu'ara"),
    27: ("النمل", "আন-নামল", "An-Naml"),
    28: ("القصص", "আল-কাসাস", "Al-Qasas"),
    29: ("العنكبوت", "আল-আনকাবূত", "Al-'Ankabut"),
    30: ("الروم", "আর-রূম", "Ar-Rum"),
    31: ("لقمان", "লোকমান", "Luqman"),
    32: ("السجدة", "আস-সাজদাহ", "As-Sajdah"),
    33: ("الأحزاب", "আল-আহযাব", "Al-Ahzab"),
    34: ("سبإ", "সাবা", "Saba"),
    35: ("فاطر", "ফাতির", "Fatir"),
    36: ("يس", "ইয়াসীন", "Ya-Sin"),
    37: ("الصافات", "আস-সাফফাত", "As-Saffat"),
    38: ("ص", "সাদ", "Sad"),
    39: ("الزمر", "আয-যুমার", "Az-Zumar"),
    40: ("غافر", "গাফির", "Ghafir"),
    41: ("فصلت", "ফুসসিলাত", "Fussilat"),
    42: ("الشورى", "আশ-শূরা", "Ash-Shura"),
    43: ("الزخرف", "আয-যুখরুফ", "Az-Zukhruf"),
    44: ("الدخان", "আদ-দুখান", "Ad-Dukhan"),
    45: ("الجاثية", "আল-জাসিয়াহ", "Al-Jathiyah"),
    46: ("الأحقاف", "আল-আহকাফ", "Al-Ahqaf"),
    47: ("محمد", "মুহাম্মাদ", "Muhammad"),
    48: ("الفتح", "আল-ফাতহ", "Al-Fath"),
    49: ("الحجرات", "আল-হুজুরাত", "Al-Hujurat"),
    50: ("ق", "ক্বাফ", "Qaf"),
    51: ("الذاريات", "আয-যারিয়াত", "Adh-Dhariyat"),
    52: ("الطور", "আত-তূর", "At-Tur"),
    53: ("النجم", "আন-নাজম", "An-Najm"),
    54: ("القمر", "আল-কামার", "Al-Qamar"),
    55: ("الرحمن", "আর-রহমান", "Ar-Rahman"),
    56: ("الواقعة", "আল-ওয়াকিয়াহ", "Al-Waqi'ah"),
    57: ("الحديد", "আল-হাদীদ", "Al-Hadid"),
    58: ("المجادلة", "আল-মুজাদালাহ", "Al-Mujadila"),
    59: ("الحشر", "আল-হাশর", "Al-Hashr"),
    60: ("الممتحنة", "আল-মুমতাহিনা", "Al-Mumtahanah"),
    61: ("الصف", "আস-সফ", "As-Saff"),
    62: ("الجمعة", "আল-জুমুআহ", "Al-Jumu'ah"),
    63: ("المنافقون", "আল-মুনাফিকূন", "Al-Munafiqun"),
    64: ("التغابن", "আত-তাগাবুন", "At-Taghabun"),
    65: ("الطلاق", "আত-তালাক", "At-Talaq"),
    66: ("التحريم", "আত-তাহরীম", "At-Tahrim"),
    67: ("الملك", "আল-মুলক", "Al-Mulk"),
    68: ("القلم", "আল-কলম", "Al-Qalam"),
    69: ("الحاقة", "আল-হাক্কাহ", "Al-Haqqah"),
    70: ("المعارج", "আল-মাআরিজ", "Al-Ma'arij"),
    71: ("نوح", "নূহ", "Nuh"),
    72: ("الجن", "আল-জিন", "Al-Jinn"),
    73: ("المزمل", "আল-মুযযাম্মিল", "Al-Muzzammil"),
    74: ("المدثر", "আল-মুদ্দাসসির", "Al-Muddaththir"),
    75: ("القيامة", "আল-কিয়ামাহ", "Al-Qiyamah"),
    76: ("الإنسان", "আল-ইনসান", "Al-Insan"),
    77: ("المرسلات", "আল-মুরসালাত", "Al-Mursalat"),
    78: ("النبإ", "আন-নাবা", "An-Naba"),
    79: ("النازعات", "আন-নাযিআত", "An-Nazi'at"),
    80: ("عبس", "আবাসা", "'Abasa"),
    81: ("التكوير", "আত-তাকভীর", "At-Takwir"),
    82: ("الإنفطار", "আল-ইনফিতার", "Al-Infitar"),
    83: ("المطففين", "আল-মুতাফফিফীন", "Al-Mutaffifin"),
    84: ("الإنشقاق", "আল-ইনশিকাক", "Al-Inshiqaq"),
    85: ("البروج", "আল-বুরূজ", "Al-Buruj"),
    86: ("الطارق", "আত-তারিক", "At-Tariq"),
    87: ("الأعلى", "আল-আলা", "Al-A'la"),
    88: ("الغاشية", "আল-গাশিয়াহ", "Al-Ghashiyah"),
    89: ("الفجر", "আল-ফাজর", "Al-Fajr"),
    90: ("البلد", "আল-বালাদ", "Al-Balad"),
    91: ("الشمس", "আশ-শামস", "Ash-Shams"),
    92: ("الليل", "আল-লাইল", "Al-Layl"),
    93: ("الضحى", "আদ-দুহা", "Ad-Duha"),
    94: ("الشرح", "আশ-শারহ", "Ash-Sharh"),
    95: ("التين", "আত-তীন", "At-Tin"),
    96: ("العلق", "আল-আলাক", "Al-'Alaq"),
    97: ("القدر", "আল-কদর", "Al-Qadr"),
    98: ("البينة", "আল-বাইয়িনাহ", "Al-Bayyinah"),
    99: ("الزلزلة", "আয-যালযালাহ", "Az-Zalzalah"),
    100: ("العاديات", "আল-আদিয়াত", "Al-'Adiyat"),
    101: ("القارعة", "আল-কারিআহ", "Al-Qari'ah"),
    102: ("التكاثر", "আত-তাকাসুর", "At-Takathur"),
    103: ("العصر", "আল-আসর", "Al-'Asr"),
    104: ("الهمزة", "আল-হুমাযাহ", "Al-Humazah"),
    105: ("الفيل", "আল-ফীল", "Al-Fil"),
    106: ("قريش", "কুরাইশ", "Quraysh"),
    107: ("الماعون", "আল-মাউন", "Al-Ma'un"),
    108: ("الكوثر", "আল-কাওসার", "Al-Kawthar"),
    109: ("الكافرون", "আল-কাফিরুন", "Al-Kafirun"),
    110: ("النصر", "আন-নাসর", "An-Nasr"),
    111: ("المسد", "আল-মাসাদ", "Al-Masad"),
    112: ("الإخلاص", "আল-ইখলাস", "Al-Ikhlas"),
    113: ("الفلق", "আল-ফালাক", "Al-Falaq"),
    114: ("الناس", "আন-নাস", "An-Nas"),
}

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

cur.execute("""
    SELECT surah_no, ayah_count
    FROM surah
    ORDER BY surah_no
""")
surah_rows = cur.fetchall()

meta = {"surahs": []}

for row in surah_rows:
    surah_no = row["surah_no"]
    ar_name, bn_name, en_name = SURAH_NAMES[surah_no]

    meta["surahs"].append({
        "surah_no": surah_no,
        "ar_name": ar_name,
        "bn_name": bn_name,
        "en_name": en_name,
        "ayah_count": row["ayah_count"]
    })

    cur.execute("""
        SELECT
            a.ayat_no,
            a.ayat_arabic AS arabic,
            t.text AS bn
        FROM ayah a
        LEFT JOIN translation t
          ON t.surah_no = a.surah_no
         AND t.ayat_no = a.ayat_no
         AND t.lang = 'bn'
         AND t.version = 'db_bn_v1'
        WHERE a.surah_no = ?
        ORDER BY a.ayat_no
    """, (surah_no,))
    ayah_rows = cur.fetchall()

    surah_json = {
        "surah_no": surah_no,
        "ar_name": ar_name,
        "bn_name": bn_name,
        "en_name": en_name,
        "ayahs": []
    }

    for ayah in ayah_rows:
        surah_json["ayahs"].append({
            "ayah_no": ayah["ayat_no"],
            "arabic": ayah["arabic"] or "",
            "bn": ayah["bn"] or "",
            "words": []
        })

    out_file = SURAH_DIR / f"{surah_no}.json"
    out_file.write_text(
        json.dumps(surah_json, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

conn.close()

print("Done.")
print(f"Created: {meta_file}")
print(f"Created surah files in: {SURAH_DIR}")