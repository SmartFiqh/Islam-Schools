import csv
import json
import random
from datetime import datetime

# =====================================================================
# 1) قوائم البيانات الأساسية (للتوليد العشوائي)
# =====================================================================

# الموضوعات (Topics)
TOPICS = ["ibadat", "muamalat", "family", "other"]

# المذاهب (لـ rulings_by_madhab)
MADHHABS = ["maliki", "shafii", "hanafi", "hanbali", "zahiri", "jafari", "zaidi", "ibadi"]

# عناوين المسائل (بالعربية) – 100 عنوان مختلف، سيتم تكرارها مع تغييرات
TITLES_AR = [
    "صلاة الجماعة", "صلاة الفجر", "صلاة الظهر", "صلاة العصر", "صلاة المغرب", "صلاة العشاء",
    "صلاة الوتر", "صلاة الضحى", "صلاة الاستخارة", "صلاة التوبة", "صلاة الجنازة", "صلاة العيد",
    "صلاة الكسوف", "صلاة الخوف", "صلاة المسافر", "صلاة المريض", "صلاة الجمعة", "صلاة التراويح",
    "الزكاة", "زكاة الفطر", "زكاة المال", "زكاة الأسهم", "زكاة الذهب", "زكاة الفضة", "زكاة التجارة",
    "الصيام", "صيام رمضان", "صيام التطوع", "صيام يوم عرفة", "صيام عاشوراء", "صيام الست من شوال",
    "الحج", "العمرة", "الطواف", "السعي", "الوقوف بعرفة", "رمي الجمرات",
    "الوضوء", "الغسل", "التيمم", "الطهارة", "النجاسة", "الحيض", "النفاس",
    "البيع", "الشراء", "الإجارة", "الرهن", "الضمان", "الوكالة", "الشركة", "المضاربة",
    "الربا", "الفوائد البنكية", "التأمين", "الأسهم", "السندات", "العملات الرقمية",
    "النكاح", "الطلاق", "الخلع", "العدة", "النفقة", "الحضانة", "الميراث", "الوصية",
    "الأضحية", "العقيقة", "الهدي", "الكفارات", "النذور", "الأيمان",
    "اللباس", "الزينة", "الطعام", "الذبح", "الصيد", "الذبائح",
    "القضاء", "الشهادة", "الدعوى", "الحدود", "القصاص", "الديات",
    "الجهاد", "البيعة", "الإمارة", "الخراج", "الجزية",
    "الرقى", "التمائم", "الكهانة", "السحر", "العرافة",
]

# الأحكام (العربية) – لمستويات الإجابة الثلاثة
RULINGS_VS_AR = ["فرض", "واجب", "سنة مؤكدة", "سنة", "مستحب", "مباح", "مكروه", "حرام"]
RULINGS_S_AR = [
    "فرض عين على كل مكلف",
    "واجب مؤكد عند الجمهور",
    "سنة مؤكدة فعلها النبي ﷺ",
    "سنة غير مؤكدة",
    "مستحب يثاب فاعله",
    "مباح لا إثم فيه",
    "مكروه تركه أولى",
    "حرام قطعاً",
]
RULINGS_F_AR = [
    "هذا الحكم ثابت بالكتاب والسنة، وهو فرض عين على كل مكلف.",
    "هذا الحكم واجب عند جمهور الفقهاء، وتركه مكروه.",
    "هذه سنة مؤكدة واظب عليها النبي ﷺ في الغالب.",
    "هذه سنة غير مؤكدة، وتركها لا إثم فيه.",
    "هذا مستحب ويثاب فاعله، ولا يعاقب تاركه.",
    "هذا مباح، للمكلف الخيار بين الفعل والترك.",
    "هذا مكروه، وتركه أفضل من فعله.",
    "هذا حرام بنص قطعي، وفاعله آثم.",
]

# =====================================================================
# 2) دوال مساعدة لإنشاء البيانات
# =====================================================================

def random_choice(lst):
    return random.choice(lst)

def generate_issue(index):
    """توليد مسألة واحدة مع جميع الحقول المطلوبة"""
    topic = random_choice(TOPICS)
    title_ar = random_choice(TITLES_AR) + " " + str(random.randint(1, 100))
    # توليد كلمات مفتاحية عربية
    keywords_ar = ",".join(random.sample(["فقه", "عبادة", "معاملة", "طهارة", "صلاة", "زكاة", "صوم", "حج", "نكاح", "طلاق", "بيع", "ربا", "إجارة", "رهن", "ضمان", "وكالة", "شركة", "مضاربة", "جهاد", "حدود", "قصاص", "ديات", "شهادة", "قضاء", "وصية", "وقف", "نذر", "كفارة", "أضحية", "عقيقة", "هدي"], k=random.randint(3, 6)))
    ruling_vs_ar = random_choice(RULINGS_VS_AR)
    ruling_s_ar = random_choice(RULINGS_S_AR)
    ruling_f_ar = random_choice(RULINGS_F_AR)
    
    # إنشاء ترجمات مبسطة (نفس النص مع إضافة لغة)
    # نستخدم نفس النص مع تغيير طفيف للغات الأخرى (لتوفير الوقت)
    title_en = f"Issue about {title_ar}"
    title_fr = f"Question sur {title_ar}"
    title_fa = f"مسئله درباره {title_ar}"
    title_ms = f"Isu tentang {title_ar}"
    title_ur = f"{title_ar} کے بارے میں مسئلہ"
    keywords_en = ",".join(["fiqh", "islam", "ruling"] + random.sample(["prayer", "zakat", "fasting", "hajj", "marriage", "divorce", "trade", "interest", "inheritance", "witness", "judgment"], k=random.randint(2, 4)))
    keywords_fr = ",".join(["fiqh", "islam"] + random.sample(["prière", "zakat", "jeûne", "pèlerinage", "mariage", "divorce", "commerce", "intérêt", "héritage", "témoignage", "jugement"], k=random.randint(2, 4)))
    keywords_fa = ",".join(["فقه", "اسلام"] + random.sample(["نماز", "زکات", "روزه", "حج", "ازدواج", "طلاق", "تجارت", "ربا", "ارث", "شهادت", "قضاوت"], k=random.randint(2, 4)))
    keywords_ms = ",".join(["fiqh", "islam"] + random.sample(["solat", "zakat", "puasa", "haji", "nikah", "cerai", "perniagaan", "riba", "pusaka", "saksi", "penghakiman"], k=random.randint(2, 4)))
    keywords_ur = ",".join(["فقہ", "اسلام"] + random.sample(["نماز", "زکات", "روزہ", "حج", "نکاح", "طلاق", "تجارت", "سود", "وراثت", "گواہی", "فیصلہ"], k=random.randint(2, 4)))
    
    # إنشاء آراء المذاهب (JSON) – نستخدم نفس الأحكام مع اختلافات بسيطة
    rulings_by_madhab = {}
    for m in MADHHABS:
        # نعطي كل مذهب نفس الحكم مع اختلاف طفيف في الصياغة
        rulings_by_madhab[m] = {
            "very_short": random_choice(RULINGS_VS_AR),
            "short": random_choice(RULINGS_S_AR),
            "full": random_choice(RULINGS_F_AR) + " (رأي المذهب " + m + ")"
        }
    rulings_by_madhab_ar = json.dumps(rulings_by_madhab, ensure_ascii=False)
    rulings_by_madhab_en = json.dumps({m: {"very_short": "Obligatory", "short": "It is obligatory", "full": "It is an obligation according to " + m} for m in MADHHABS}, ensure_ascii=False)
    rulings_by_madhab_fr = json.dumps({m: {"very_short": "Obligatoire", "short": "C'est obligatoire", "full": "C'est une obligation selon " + m} for m in MADHHABS}, ensure_ascii=False)
    rulings_by_madhab_fa = json.dumps({m: {"very_short": "واجب", "short": "واجب است", "full": "به عقیده " + m + " واجب است"} for m in MADHHABS}, ensure_ascii=False)
    rulings_by_madhab_ms = json.dumps({m: {"very_short": "Wajib", "short": "Ia wajib", "full": "Ia wajib menurut " + m} for m in MADHHABS}, ensure_ascii=False)
    rulings_by_madhab_ur = json.dumps({m: {"very_short": "واجب", "short": "یہ واجب ہے", "full": "کے مطابق یہ واجب ہے " + m} for m in MADHHABS}, ensure_ascii=False)
    
    # ترجمات الأحكام (نستخدم نفس النص مع إضافة لغة)
    ruling_vs_en = ruling_vs_ar
    ruling_s_en = ruling_s_ar
    ruling_f_en = ruling_f_ar
    ruling_vs_fr = ruling_vs_ar
    ruling_s_fr = ruling_s_ar
    ruling_f_fr = ruling_f_ar
    ruling_vs_fa = ruling_vs_ar
    ruling_s_fa = ruling_s_ar
    ruling_f_fa = ruling_f_ar
    ruling_vs_ms = ruling_vs_ar
    ruling_s_ms = ruling_s_ar
    ruling_f_ms = ruling_f_ar
    ruling_vs_ur = ruling_vs_ar
    ruling_s_ur = ruling_s_ar
    ruling_f_ur = ruling_f_ar

    return {
        "topic": topic,
        "title_ar": title_ar, "title_en": title_en, "title_fr": title_fr, "title_fa": title_fa, "title_ms": title_ms, "title_ur": title_ur,
        "keywords_ar": keywords_ar, "keywords_en": keywords_en, "keywords_fr": keywords_fr, "keywords_fa": keywords_fa, "keywords_ms": keywords_ms, "keywords_ur": keywords_ur,
        "ruling_vs_ar": ruling_vs_ar, "ruling_s_ar": ruling_s_ar, "ruling_f_ar": ruling_f_ar,
        "ruling_vs_en": ruling_vs_en, "ruling_s_en": ruling_s_en, "ruling_f_en": ruling_f_en,
        "ruling_vs_fr": ruling_vs_fr, "ruling_s_fr": ruling_s_fr, "ruling_f_fr": ruling_f_fr,
        "ruling_vs_fa": ruling_vs_fa, "ruling_s_fa": ruling_s_fa, "ruling_f_fa": ruling_f_fa,
        "ruling_vs_ms": ruling_vs_ms, "ruling_s_ms": ruling_s_ms, "ruling_f_ms": ruling_f_ms,
        "ruling_vs_ur": ruling_vs_ur, "ruling_s_ur": ruling_s_ur, "ruling_f_ur": ruling_f_ur,
        "rulings_by_madhab_ar": rulings_by_madhab_ar,
        "rulings_by_madhab_en": rulings_by_madhab_en,
        "rulings_by_madhab_fr": rulings_by_madhab_fr,
        "rulings_by_madhab_fa": rulings_by_madhab_fa,
        "rulings_by_madhab_ms": rulings_by_madhab_ms,
        "rulings_by_madhab_ur": rulings_by_madhab_ur,
    }

# =====================================================================
# 3) إنشاء ملف CSV
# =====================================================================

def generate_csv(num_issues=1000, filename="issues_1000.csv"):
    """توليد ملف CSV يحتوي على عدد محدد من المسائل"""
    # الأعمدة المطلوبة (ترتيبها حسب قاعدة البيانات)
    fieldnames = [
        "topic",
        "title_ar", "title_en", "title_fr", "title_fa", "title_ms", "title_ur",
        "keywords_ar", "keywords_en", "keywords_fr", "keywords_fa", "keywords_ms", "keywords_ur",
        "ruling_vs_ar", "ruling_s_ar", "ruling_f_ar",
        "ruling_vs_en", "ruling_s_en", "ruling_f_en",
        "ruling_vs_fr", "ruling_s_fr", "ruling_f_fr",
        "ruling_vs_fa", "ruling_s_fa", "ruling_f_fa",
        "ruling_vs_ms", "ruling_s_ms", "ruling_f_ms",
        "ruling_vs_ur", "ruling_s_ur", "ruling_f_ur",
        "rulings_by_madhab_ar", "rulings_by_madhab_en", "rulings_by_madhab_fr",
        "rulings_by_madhab_fa", "rulings_by_madhab_ms", "rulings_by_madhab_ur"
    ]

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(num_issues):
            issue = generate_issue(i)
            writer.writerow(issue)
    print(f"✅ تم إنشاء {num_issues} مسألة في ملف '{filename}'")

if __name__ == "__main__":
    # نضع بذرة عشوائية ثابتة للتكرار
    random.seed(42)
    generate_csv(1000, "issues_1000.csv")
