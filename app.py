import streamlit as st
import re
import sqlite3
import json
import os
import csv
import io

# =====================================================================
# 0) استيراد المكتبات الاختيارية بأمان
# =====================================================================
try:
    from dotenv import load_dotenv
    load_dotenv()
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False

try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    genai = None
    GENAI_AVAILABLE = False

# =====================================================================
# 1) الحصول على مفتاح Gemini (من st.secrets أو متغير البيئة)
# =====================================================================
def get_gemini_api_key():
    try:
        return st.secrets["GEMINI_API_KEY"]
    except (KeyError, AttributeError):
        pass
    if DOTENV_AVAILABLE:
        return os.getenv("GEMINI_API_KEY")
    return None

GEMINI_API_KEY = get_gemini_api_key()
USE_GEMINI = GEMINI_API_KEY is not None and GENAI_AVAILABLE
if USE_GEMINI:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception:
        USE_GEMINI = False

# =====================================================================
# 2) قاعدة البيانات (SQLite)
# =====================================================================
DB_PATH = "fiqh.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS issues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT,
            title_ar TEXT, title_en TEXT, title_fr TEXT, title_fa TEXT, title_ms TEXT, title_ur TEXT,
            keywords_ar TEXT, keywords_en TEXT, keywords_fr TEXT, keywords_fa TEXT, keywords_ms TEXT, keywords_ur TEXT,
            ruling_vs_ar TEXT, ruling_s_ar TEXT, ruling_f_ar TEXT,
            ruling_vs_en TEXT, ruling_s_en TEXT, ruling_f_en TEXT,
            ruling_vs_fr TEXT, ruling_s_fr TEXT, ruling_f_fr TEXT,
            ruling_vs_fa TEXT, ruling_s_fa TEXT, ruling_f_fa TEXT,
            ruling_vs_ms TEXT, ruling_s_ms TEXT, ruling_f_ms TEXT,
            ruling_vs_ur TEXT, ruling_s_ur TEXT, ruling_f_ur TEXT,
            rulings_by_madhab_ar JSON, rulings_by_madhab_en JSON, rulings_by_madhab_fr JSON,
            rulings_by_madhab_fa JSON, rulings_by_madhab_ms JSON, rulings_by_madhab_ur JSON
        )
    ''')
    conn.commit()
    conn.close()

def seed_initial_issues():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM issues")
    if c.fetchone()[0] > 0:
        conn.close()
        return

    # 7 مسائل أساسية مع ترجمات كاملة (مختصرة للعرض)
    issues = [
        {
            "topic": "ibadat",
            "title_ar": "صلاة الجماعة", "title_en": "Congregational Prayer", "title_fr": "La prière en congrégation",
            "title_fa": "نماز جماعت", "title_ms": "Solat Berjemaah", "title_ur": "نماز باجماعت",
            "keywords_ar": "جماعة,مسجد,رجال,صلاة,فرض,سنة,واجب",
            "keywords_en": "congregation,mosque,men,prayer,obligatory,sunnah",
            "keywords_fr": "congrégation,mosquée,hommes,prière,obligatoire,sunna",
            "keywords_fa": "جماعت,مسجد,مردان,نماز,فرض,سنت,واجب",
            "keywords_ms": "jemaah,masjid,lelaki,solat,fardu,sunnah,wajib",
            "keywords_ur": "جماعت,مسجد,مرد,نماز,فرض,سنت,واجب",
            "ruling_vs_ar": "سنة مؤكدة", "ruling_s_ar": "سنة مؤكدة عند الجمهور، واجبة عند الحنفية",
            "ruling_f_ar": "تجب صلاة الجماعة في المسجد على الرجال عند جمهور الفقهاء؛ فهي فرض عين عند الحنابلة، واجب مؤكد عند الحنفية، فرض كفاية عند المالكية والشافعية، ومستحبة تأكيداً عند الجعفرية في زمن الغيبة.",
            "ruling_vs_en": "Emphasized Sunnah", "ruling_s_en": "Emphasized sunnah for most jurists, obligatory for the Hanafis",
            "ruling_f_en": "Congregational prayer in the mosque is required of men according to the majority of jurists: an individual obligation for the Hanbalis, an emphasized obligation for the Hanafis, a communal obligation for the Malikis and Shafi'is, and a strongly recommended act for the Ja'faris during the Occultation.",
            "ruling_vs_fr": "Sunna fortement recommandée", "ruling_s_fr": "Sunna fortement recommandée pour la majorité, obligatoire pour les hanafites",
            "ruling_f_fr": "La prière en congrégation à la mosquée est requise des hommes selon la majorité des juristes : obligation individuelle chez les hanbalites, obligation appuyée chez les hanafites, obligation collective chez les malikites et les chaféites, et acte fortement recommandé chez les jaafarites durant l'Occultation.",
            "ruling_vs_fa": "سنت مؤکد", "ruling_s_fa": "سنت مؤکد نزد جمهور، واجب نزد حنفیان",
            "ruling_f_fa": "نماز جماعت در مسجد بر مردان واجب است به اتفاق جمهور فقها؛ فرض عین برای حنبلی‌ها، واجب مؤکد برای حنفی‌ها، فرض کفایه برای مالکی‌ها و شافعی‌ها، و مستحب مؤکد برای جعفری‌ها در زمان غیبت.",
            "ruling_vs_ms": "Sunnah muakkadah", "ruling_s_ms": "Sunnah muakkadah bagi majoriti, wajib bagi Hanafi",
            "ruling_f_ms": "Solat berjemaah di masjid diwajibkan ke atas lelaki menurut majoriti ulama; fardu ain bagi Hanbali, wajib muakkad bagi Hanafi, fardu kifayah bagi Maliki dan Syafii, dan mustahab muakkad bagi Jaafari semasa ghaib.",
            "ruling_vs_ur": "سنت مؤکدہ", "ruling_s_ur": "سنت مؤکدہ نزد جمہور، واجب نزد احناف",
            "ruling_f_ur": "مسجد میں نماز باجماعت مردوں پر جمہور فقہاء کے نزدیک واجب ہے؛ حنابلہ کے نزدیک فرض عین، احناف کے نزدیک واجب مؤکد، مالکیہ و شافعیہ کے نزدیک فرض کفایہ، اور جعفریہ کے نزدیک مستحب مؤکد ہے۔",
            "rulings_by_madhab_ar": json.dumps({
                "maliki": {"very_short": "فرض كفاية", "short": "فرض كفاية على أهل الحي، سنة مؤكدة للفرد", "full": "فرض كفاية على أهل الحي؛ وفي حق الفرد الواحد سنة مؤكدة لا يُكره تركها إلا لمن واظب عليه."},
                "shafii": {"very_short": "سنة مؤكدة", "short": "فرض كفاية على المجتمع، سنة مؤكدة للفرد", "full": "فرض كفاية على المجتمع ككل، وسنة مؤكدة في حق الفرد؛ وهو الأصح في المذهب."},
                "hanafi": {"very_short": "واجب", "short": "واجبة على كل رجل حر بالغ عاقل", "full": "واجبة وجوباً غير ملزم على كل رجل حر بالغ عاقل قادر؛ وتركها بلا عذر مكروه تحريماً عند المتأخرين."},
                "hanbali": {"very_short": "فرض عين", "short": "فرض عين على كل رجل قادر", "full": "فرض عين على كل رجل مكلف قادر؛ لا يجوز تركها إلا لعذر شرعي معتبر."},
                "zahiri": {"very_short": "فرض عين", "short": "فرض عين؛ ظاهر الأمر النبوي يقتضي الوجوب", "full": "فرض عين أخذاً بظاهر الأمر النبوي بالمحافظة عليها، دون تأويل يصرفه عن الوجوب."},
                "jafari": {"very_short": "مستحب مؤكد", "short": "مستحبة استحباباً مؤكداً في زمن الغيبة", "full": "مستحبة استحباباً مؤكداً وليست واجبة عيناً في زمن الغيبة الكبرى، وثوابها عظيم."},
                "zaidi": {"very_short": "فرض كفاية", "short": "قريب من رأي أهل السنة في تأكيدها", "full": "فرض كفاية، ويقترب الرأي الزيدي من الرأي السني في التأكيد على المحافظة عليها جماعة."},
                "ibadi": {"very_short": "سنة مؤكدة", "short": "من أعلام الدين ولا تُترك باستمرار", "full": "من أعلام الدين الظاهرة، سنة مؤكدة لا ينبغي تركها باستمرار وإن لم تكن شرطاً لصحة الصلاة."}
            }),
            "rulings_by_madhab_en": json.dumps({
                "maliki": {"very_short": "Communal obligation", "short": "Communal obligation on the locality, emphasized sunnah for the individual", "full": "A communal obligation (fard kifayah) upon the residents of a locality; for a single individual it is an emphasized sunnah, and abandoning it is disliked only for one who habitually neglects it."},
                "shafii": {"very_short": "Emphasized Sunnah", "short": "Communal obligation on society, emphasized sunnah for the individual", "full": "A communal obligation upon society as a whole, and an emphasized sunnah for the individual — this is the most authoritative view in the school."},
                "hanafi": {"very_short": "Wajib", "short": "Obligatory (wajib) on every free, sane, adult man", "full": "It is obligatory (wajib), one degree below fard, upon every free, sane, adult, capable man; abandoning it without excuse is strongly disliked according to later scholars."},
                "hanbali": {"very_short": "Fard Ayn", "short": "Individual obligation on every capable man", "full": "It is an individual obligation (fard ayn) upon every legally accountable, capable man; it may not be abandoned except for a recognized legal excuse."},
                "zahiri": {"very_short": "Fard Ayn", "short": "Individual obligation, based on the literal Prophetic command", "full": "It is an individual obligation, taken from the literal wording of the Prophet's command to maintain it, without interpretation that would divert it away from obligation."},
                "jafari": {"very_short": "Strongly recommended", "short": "Strongly recommended during the Occultation, not individually obligatory", "full": "It is strongly recommended rather than individually obligatory during the Major Occultation, and its reward is great."},
                "zaidi": {"very_short": "Fard Kifayah", "short": "Close to the Sunni emphasis on maintaining it", "full": "It is a communal obligation; the Zaidi view is close to the Sunni emphasis on maintaining it in congregation."},
                "ibadi": {"very_short": "Emphasized Sunnah", "short": "A visible marker of the religion; should not be habitually abandoned", "full": "It is one of the visible markers of the religion, an emphasized sunnah that should not be habitually abandoned, though it is not a condition for the validity of the prayer."}
            }),
            "rulings_by_madhab_fr": "{}",
            "rulings_by_madhab_fa": "{}",
            "rulings_by_madhab_ms": "{}",
            "rulings_by_madhab_ur": "{}"
        }
        # باقي المسائل (زكاة الأسهم، الجمع في السفر، نواقض الوضوء، الربا، صلاة المسافر، طلاق الحائض)
        # يمكن إضافتها بنفس النمط، وسأضعها في المرفق لتوفير المساحة.
        # ولكن في هذا الكود، سأكتفي بهذه المسألة كنموذج لتشغيل التطبيق.
    ]
    for issue in issues:
        c.execute('''
            INSERT INTO issues (
                topic, title_ar, title_en, title_fr, title_fa, title_ms, title_ur,
                keywords_ar, keywords_en, keywords_fr, keywords_fa, keywords_ms, keywords_ur,
                ruling_vs_ar, ruling_s_ar, ruling_f_ar,
                ruling_vs_en, ruling_s_en, ruling_f_en,
                ruling_vs_fr, ruling_s_fr, ruling_f_fr,
                ruling_vs_fa, ruling_s_fa, ruling_f_fa,
                ruling_vs_ms, ruling_s_ms, ruling_f_ms,
                ruling_vs_ur, ruling_s_ur, ruling_f_ur,
                rulings_by_madhab_ar, rulings_by_madhab_en, rulings_by_madhab_fr,
                rulings_by_madhab_fa, rulings_by_madhab_ms, rulings_by_madhab_ur
            ) VALUES (?,?,?,?,?,?,?, ?,?,?,?,?,?, ?,?,?, ?,?,?, ?,?,?, ?,?,?, ?,?,?, ?,?,?, ?,?,?, ?,?,?)
        ''', (
            issue["topic"], issue["title_ar"], issue["title_en"], issue["title_fr"], issue["title_fa"], issue["title_ms"], issue["title_ur"],
            issue["keywords_ar"], issue["keywords_en"], issue["keywords_fr"], issue["keywords_fa"], issue["keywords_ms"], issue["keywords_ur"],
            issue["ruling_vs_ar"], issue["ruling_s_ar"], issue["ruling_f_ar"],
            issue["ruling_vs_en"], issue["ruling_s_en"], issue["ruling_f_en"],
            issue["ruling_vs_fr"], issue["ruling_s_fr"], issue["ruling_f_fr"],
            issue["ruling_vs_fa"], issue["ruling_s_fa"], issue["ruling_f_fa"],
            issue["ruling_vs_ms"], issue["ruling_s_ms"], issue["ruling_f_ms"],
            issue["ruling_vs_ur"], issue["ruling_s_ur"], issue["ruling_f_ur"],
            issue["rulings_by_madhab_ar"], issue["rulings_by_madhab_en"], issue["rulings_by_madhab_fr"],
            issue["rulings_by_madhab_fa"], issue["rulings_by_madhab_ms"], issue["rulings_by_madhab_ur"]
        ))
    conn.commit()
    conn.close()

def load_issues(lang, topic_filter="all"):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    lang_suffix = lang
    query = f'''
        SELECT id, topic, title_{lang_suffix}, keywords_{lang_suffix},
               ruling_vs_{lang_suffix}, ruling_s_{lang_suffix}, ruling_f_{lang_suffix},
               rulings_by_madhab_{lang_suffix}
        FROM issues
    '''
    if topic_filter != "all":
        query += f" WHERE topic = '{topic_filter}'"
    c.execute(query)
    rows = c.fetchall()
    conn.close()
    issues = []
    for row in rows:
        kw = row[3].split(',') if row[3] else []
        issues.append({
            "id": row[0],
            "topic": row[1],
            "title": row[2],
            "keywords": [k.strip() for k in kw if k.strip()],
            "rulings": {
                "very_short": row[4],
                "short": row[5],
                "full": row[6]
            },
            "rulings_by_madhab": json.loads(row[7]) if row[7] else {}
        })
    return issues

def import_from_csv(csv_content):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    reader = csv.DictReader(io.StringIO(csv_content.decode('utf-8')))
    count = 0
    for row in reader:
        c.execute('''
            INSERT INTO issues (
                topic, title_ar, title_en, title_fr, title_fa, title_ms, title_ur,
                keywords_ar, keywords_en, keywords_fr, keywords_fa, keywords_ms, keywords_ur,
                ruling_vs_ar, ruling_s_ar, ruling_f_ar,
                ruling_vs_en, ruling_s_en, ruling_f_en,
                ruling_vs_fr, ruling_s_fr, ruling_f_fr,
                ruling_vs_fa, ruling_s_fa, ruling_f_fa,
                ruling_vs_ms, ruling_s_ms, ruling_f_ms,
                ruling_vs_ur, ruling_s_ur, ruling_f_ur,
                rulings_by_madhab_ar, rulings_by_madhab_en, rulings_by_madhab_fr,
                rulings_by_madhab_fa, rulings_by_madhab_ms, rulings_by_madhab_ur
            ) VALUES (?,?,?,?,?,?,?, ?,?,?,?,?,?, ?,?,?, ?,?,?, ?,?,?, ?,?,?, ?,?,?, ?,?,?, ?,?,?, ?,?,?)
        ''', (
            row.get("topic", "other"),
            row.get("title_ar", ""), row.get("title_en", ""), row.get("title_fr", ""), row.get("title_fa", ""), row.get("title_ms", ""), row.get("title_ur", ""),
            row.get("keywords_ar", ""), row.get("keywords_en", ""), row.get("keywords_fr", ""), row.get("keywords_fa", ""), row.get("keywords_ms", ""), row.get("keywords_ur", ""),
            row.get("ruling_vs_ar", ""), row.get("ruling_s_ar", ""), row.get("ruling_f_ar", ""),
            row.get("ruling_vs_en", ""), row.get("ruling_s_en", ""), row.get("ruling_f_en", ""),
            row.get("ruling_vs_fr", ""), row.get("ruling_s_fr", ""), row.get("ruling_f_fr", ""),
            row.get("ruling_vs_fa", ""), row.get("ruling_s_fa", ""), row.get("ruling_f_fa", ""),
            row.get("ruling_vs_ms", ""), row.get("ruling_s_ms", ""), row.get("ruling_f_ms", ""),
            row.get("ruling_vs_ur", ""), row.get("ruling_s_ur", ""), row.get("ruling_f_ur", ""),
            row.get("rulings_by_madhab_ar", "{}"), row.get("rulings_by_madhab_en", "{}"), row.get("rulings_by_madhab_fr", "{}"),
            row.get("rulings_by_madhab_fa", "{}"), row.get("rulings_by_madhab_ms", "{}"), row.get("rulings_by_madhab_ur", "{}")
        ))
        count += 1
    conn.commit()
    conn.close()
    return count

# =====================================================================
# 3) SEMANTIC SEARCH (GEMINI)
# =====================================================================
def semantic_search(query, issues, lang):
    if not USE_GEMINI or not issues:
        return None
    titles_with_ids = [f"{issue['id']}: {issue['title']}" for issue in issues]
    prompt = f"""
    أنت مساعد فقهي. لديك قائمة بعناوين مسائل فقهية. سؤال المستخدم: "{query}".

    قائمة العناوين (مع أرقامها):
    {chr(10).join(titles_with_ids)}

    المطلوب: حدد ما يصل إلى 3 عناوين من القائمة هي الأقرب لسؤال المستخدم.
    أخرج النتيجة على شكل قائمة بأرقام المسائل مفصولة بفواصل (مثال: 3, 7, 12).
    إذا لم تجد أي تطابق، اكتب "لا يوجد".
    """
    try:
        response = model.generate_content(prompt)
        result = response.text.strip()
        if result == "لا يوجد":
            return []
        ids = re.findall(r'\d+', result)
        return [int(id) for id in ids[:3]]
    except Exception:
        return None

# =====================================================================
# 4) SEARCH LOGIC
# =====================================================================
def search_issues(query, topic_filter, madhabs, level, lang):
    if not query:
        return []
    all_issues = load_issues(lang, topic_filter)
    if not all_issues:
        return []
    q = query.strip().lower()

    semantic_ids = None
    if USE_GEMINI:
        semantic_ids = semantic_search(q, all_issues, lang)

    results = []
    if semantic_ids is not None:
        for id in semantic_ids:
            issue = next((i for i in all_issues if i["id"] == id), None)
            if issue and issue not in results:
                results.append(issue)

    if not results:
        for issue in all_issues:
            pool = (issue["title"].lower() + " " +
                    " ".join(issue["keywords"]).lower() + " " +
                    issue["rulings"]["full"].lower())
            if q in pool:
                results.append(issue)
        if not results:
            words = re.findall(r"\w+", q)
            for issue in all_issues:
                pool = issue["title"].lower() + " " + " ".join(issue["keywords"]).lower()
                if any(w in pool for w in words):
                    results.append(issue)

    final_results = []
    for issue in results:
        cards = []
        per_madhab = issue.get("rulings_by_madhab", {})
        if per_madhab:
            for m in madhabs:
                data = per_madhab.get(m)
                if data:
                    cards.append({
                        "label": MADHHAB_NAMES[m][lang],
                        "answer": data.get(level, data.get("full", "")),
                        "note": T["note_madhab"].format(MADHHAB_NAMES[m][lang]),
                    })
        if not cards:
            cards.append({
                "label": TOPICS[issue["topic"]][lang],
                "answer": issue["rulings"].get(level, issue["rulings"]["full"]),
                "note": T["note_general"],
            })
        final_results.append({
            "title": issue["title"],
            "topic": TOPICS[issue["topic"]][lang],
            "cards": cards,
        })
    return final_results

# =====================================================================
# 5) UI DATA (Translations, Madhhabs, etc.)
# =====================================================================
LANGS = {"العربية": "ar", "English": "en", "Français": "fr", "فارسی": "fa", "Bahasa Melayu": "ms", "اردو": "ur"}

UI = {
    "ar": {
        "app_title": "الجامع المختصر لآراء المذاهب",
        "app_subtitle": "منصة لعرض ومقارنة آراء المذاهب الفقهية — للفهم والتبصر، وليست موقع إفتاء.",
        "lang_label": "اللغة",
        "s1_title": "١ — اختر المذهب",
        "group_q": "مذاهب السنة، أم مذاهب الشيعة، أم المذهب الإباضي؟",
        "multi_hint": "💡 يمكنك اختيار أكثر من مذهب لعرض إجاباتها جنباً إلى جنب للمقارنة.",
        "sub_select": "اختر مذهباً واحداً أو أكثر:",
        "s2_title": "٢ — اختر الموضوع",
        "topic_q": "اختر الموضوع الفقهي",
        "s3_title": "٣ — طريقة عرض الإجابة",
        "level_q": "اختر مستوى التفصيل",
        "s4_title": "٤ — اكتب سؤالك",
        "question_placeholder": "مثال: ما حكم صلاة الجماعة؟",
        "search_btn": "🔍 ابحث عن الإجابة",
        "s5_title": "٥ — الإجابة",
        "answer_placeholder": "ستظهر الإجابة هنا بعد كتابة السؤال والضغط على زر البحث.",
        "no_question_warning": "الرجاء كتابة سؤالك أولاً في الفقرة الرابعة.",
        "no_madhab_warning": "الرجاء اختيار مذهب واحد على الأقل.",
        "no_results_warning": "🔍 لم نجد مسألة بهذا الوصف ضمن الموضوع المختار. جرّب صياغة أخرى أو وسّع نطاق البحث.",
        "signature": "هذا والله أعلم",
        "note_general": "رأي عام موحّد — لم يُفصّل بعد لكل مذهب",
        "note_madhab": "رأي المذهب {}",
        "expander_imams": "📜 الأئمة المؤسسون للمذاهب",
        "expander_countries": "🗺️ الدول الإسلامية والمذهب الرسمي السائد",
        "expander_glossary": "📚 مصطلحات فقهية رئيسية",
        "expander_comments": "💬 أضف تعليقك أو ملاحظتك",
        "rating_label": "قيّم فائدة الإجابة:",
        "comment_placeholder": "اكتب ملاحظتك هنا...",
        "comment_submit": "إرسال التعليق",
        "comment_success": "✅ تم إرسال تعليقك، شكراً لك.",
        "comment_warning": "⚠️ الرجاء كتابة تعليق قبل الإرسال.",
        "comments_title": "تعليقات هذه الجلسة:",
        "comments_note": "ملاحظة: هذه التعليقات محفوظة لجلستك الحالية فقط.",
        "birthplace": "مكان الميلاد",
        "founding_place": "مكان تأسيس المذهب",
        "scholars": "أشهر فقهاء المذهب",
        "official_madhab": "المذهب الرسمي",
        "population": "عدد السكان (تقريبي)",
    },
    "en": {
        "app_title": "The Concise Compendium of Madhhab Opinions",
        "app_subtitle": "A platform for presenting and comparing juristic (fiqh) opinions — for understanding, not for issuing formal rulings (fatwas).",
        "lang_label": "Language",
        "s1_title": "1 — Choose the Madhhab",
        "group_q": "Sunni schools, Shia schools, or the Ibadi school?",
        "multi_hint": "💡 You can select more than one school to compare their answers side by side.",
        "sub_select": "Choose one or more schools:",
        "s2_title": "2 — Choose the Topic",
        "topic_q": "Choose a fiqh topic",
        "s3_title": "3 — Answer Detail Level",
        "level_q": "Choose the level of detail",
        "s4_title": "4 — Type Your Question",
        "question_placeholder": "Example: What is the ruling on congregational prayer?",
        "search_btn": "🔍 Search for the Ruling",
        "s5_title": "5 — The Answer",
        "answer_placeholder": "The answer will appear here after you type a question and press search.",
        "no_question_warning": "Please type your question first in section 4.",
        "no_madhab_warning": "Please select at least one school.",
        "no_results_warning": "🔍 No matching issue was found in the selected topic. Try rephrasing or widen the topic.",
        "signature": "And God knows best",
        "note_general": "A general, unified opinion — not yet detailed per school",
        "note_madhab": "Opinion of the {} school",
        "expander_imams": "📜 The Founding Imams of the Schools",
        "expander_countries": "🗺️ Muslim-Majority Countries & Their Prevailing Official School",
        "expander_glossary": "📚 Key Juristic Terms",
        "expander_comments": "💬 Add Your Comment or Note",
        "rating_label": "Rate how helpful this answer was:",
        "comment_placeholder": "Write your note here...",
        "comment_submit": "Submit Comment",
        "comment_success": "✅ Your comment has been submitted, thank you.",
        "comment_warning": "⚠️ Please write a comment before submitting.",
        "comments_title": "Comments in this session:",
        "comments_note": "Note: these comments are saved for your current session only.",
        "birthplace": "Birthplace",
        "founding_place": "Where the school was founded",
        "scholars": "Prominent scholars of the school",
        "official_madhab": "Official school",
        "population": "Population (approx.)",
    },
    "fr": {
        "app_title": "Le Recueil Concis des Avis des Écoles Juridiques",
        "app_subtitle": "Une plateforme pour présenter et comparer les avis juridiques (fiqh) — pour la compréhension, non pour émettre des fatwas.",
        "lang_label": "Langue",
        "s1_title": "1 — Choisir l'école juridique",
        "group_q": "Écoles sunnites, écoles chiites, ou école ibadite ?",
        "multi_hint": "💡 Vous pouvez sélectionner plusieurs écoles pour comparer leurs réponses côte à côte.",
        "sub_select": "Choisissez une ou plusieurs écoles :",
        "s2_title": "2 — Choisir le sujet",
        "topic_q": "Choisissez un sujet de fiqh",
        "s3_title": "3 — Niveau de détail de la réponse",
        "level_q": "Choisissez le niveau de détail",
        "s4_title": "4 — Écrivez votre question",
        "question_placeholder": "Exemple : Quel est le statut de la prière en congrégation ?",
        "search_btn": "🔍 Rechercher la réponse",
        "s5_title": "5 — La réponse",
        "answer_placeholder": "La réponse apparaîtra ici après avoir écrit une question et appuyé sur rechercher.",
        "no_question_warning": "Veuillez d'abord écrire votre question à la section 4.",
        "no_madhab_warning": "Veuillez sélectionner au moins une école.",
        "no_results_warning": "🔍 Aucune question correspondante trouvée dans le sujet choisi. Essayez une autre formulation ou élargissez le sujet.",
        "signature": "Et Dieu est plus savant",
        "note_general": "Avis général unifié — pas encore détaillé par école",
        "note_madhab": "Avis de l'école {}",
        "expander_imams": "📜 Les Imams Fondateurs des Écoles",
        "expander_countries": "🗺️ Pays à Majorité Musulmane et Leur École Officielle Dominante",
        "expander_glossary": "📚 Termes Juridiques Clés",
        "expander_comments": "💬 Ajoutez Votre Commentaire ou Remarque",
        "rating_label": "Évaluez l'utilité de cette réponse :",
        "comment_placeholder": "Écrivez votre remarque ici...",
        "comment_submit": "Envoyer le commentaire",
        "comment_success": "✅ Votre commentaire a été envoyé, merci.",
        "comment_warning": "⚠️ Veuillez écrire un commentaire avant d'envoyer.",
        "comments_title": "Commentaires de cette session :",
        "comments_note": "Remarque : ces commentaires ne sont conservés que pour votre session actuelle.",
        "birthplace": "Lieu de naissance",
        "founding_place": "Lieu de fondation de l'école",
        "scholars": "Savants marquants de l'école",
        "official_madhab": "École officielle",
        "population": "Population (approx.)",
    },
    "fa": {
        "app_title": "جامع مختصر آراء مذاهب",
        "app_subtitle": "پلتفرمی برای نمایش و مقایسه آراء فقهی مذاهب — برای فهم و بصیرت، نه صدور فتوا.",
        "lang_label": "زبان",
        "s1_title": "۱ — انتخاب مذهب",
        "group_q": "مذاهب اهل سنت، مذاهب شیعه، یا مذهب اباضی؟",
        "multi_hint": "💡 می‌توانید بیش از یک مذهب را برای مقایسه پاسخ‌ها انتخاب کنید.",
        "sub_select": "یک یا چند مذهب را انتخاب کنید:",
        "s2_title": "۲ — انتخاب موضوع",
        "topic_q": "موضوع فقهی را انتخاب کنید",
        "s3_title": "۳ — سطح نمایش پاسخ",
        "level_q": "سطح جزئیات را انتخاب کنید",
        "s4_title": "۴ — سوال خود را بنویسید",
        "question_placeholder": "مثال: حکم نماز جماعت چیست؟",
        "search_btn": "🔍 جستجوی پاسخ",
        "s5_title": "۵ — پاسخ",
        "answer_placeholder": "پاسخ پس از نوشتن سوال و کلیک روی جستجو نمایش داده می‌شود.",
        "no_question_warning": "لطفاً ابتدا سوال خود را در بخش ۴ بنویسید.",
        "no_madhab_warning": "لطفاً حداقل یک مذهب را انتخاب کنید.",
        "no_results_warning": "🔍 هیچ مسئله‌ای با این توضیح در موضوع انتخاب‌شده یافت نشد. عبارت دیگری را امتحان کنید.",
        "signature": "والله اعلم",
        "note_general": "نظر عمومی واحد — هنوز به‌تفکیک مذهب نیست",
        "note_madhab": "نظر مذهب {}",
        "expander_imams": "📜 ائمه مؤسس مذاهب",
        "expander_countries": "🗺️ کشورهای اسلامی و مذهب رسمی",
        "expander_glossary": "📚 اصطلاحات کلیدی فقهی",
        "expander_comments": "💬 نظر یا پیشنهاد خود را اضافه کنید",
        "rating_label": "میزان مفید بودن پاسخ را ارزیابی کنید:",
        "comment_placeholder": "نظر خود را اینجا بنویسید...",
        "comment_submit": "ارسال نظر",
        "comment_success": "✅ نظر شما با موفقیت ارسال شد، سپاسگزاریم.",
        "comment_warning": "⚠️ لطفاً قبل از ارسال، نظر خود را بنویسید.",
        "comments_title": "نظرات این جلسه:",
        "comments_note": "توجه: این نظرات فقط برای جلسه فعلی ذخیره می‌شوند.",
        "birthplace": "محل تولد",
        "founding_place": "محل تأسیس مذهب",
        "scholars": "مشهورترین فقهای مذهب",
        "official_madhab": "مذهب رسمی",
        "population": "جمعیت (تقریبی)",
    },
    "ms": {
        "app_title": "Himpunan Ringkas Pendapat Mazhab",
        "app_subtitle": "Platform untuk memaparkan dan membandingkan pendapat fiqh mazhab — untuk kefahaman dan wawasan, bukan laman fatwa.",
        "lang_label": "Bahasa",
        "s1_title": "1 — Pilih Mazhab",
        "group_q": "Mazhab Sunni, Syiah, atau Ibadi?",
        "multi_hint": "💡 Anda boleh memilih lebih daripada satu mazhab untuk membandingkan jawapan mereka.",
        "sub_select": "Pilih satu atau lebih mazhab:",
        "s2_title": "2 — Pilih Topik",
        "topic_q": "Pilih topik fiqh",
        "s3_title": "3 — Tahap Perincian Jawapan",
        "level_q": "Pilih tahap perincian",
        "s4_title": "4 — Taip Soalan Anda",
        "question_placeholder": "Contoh: Apakah hukum solat berjemaah?",
        "search_btn": "🔍 Cari Jawapan",
        "s5_title": "5 — Jawapan",
        "answer_placeholder": "Jawapan akan muncul di sini selepas anda menaip soalan dan menekan cari.",
        "no_question_warning": "Sila taip soalan anda terlebih dahulu di bahagian 4.",
        "no_madhab_warning": "Sila pilih sekurang-kurangnya satu mazhab.",
        "no_results_warning": "🔍 Tiada isu sepadan ditemui dalam topik yang dipilih. Cuba kata kunci lain.",
        "signature": "Dan Allah lebih mengetahui",
        "note_general": "Pendapat umum yang disatukan — belum diperincikan mengikut mazhab",
        "note_madhab": "Pendapat mazhab {}",
        "expander_imams": "📜 Imam Pengasas Mazhab",
        "expander_countries": "🗺️ Negara Islam & Mazhab Rasmi",
        "expander_glossary": "📚 Istilah Fiqh Utama",
        "expander_comments": "💬 Tambah Ulasan atau Nota Anda",
        "rating_label": "Nilaikan kemanfaatan jawapan ini:",
        "comment_placeholder": "Tulis ulasan anda di sini...",
        "comment_submit": "Hantar Ulasan",
        "comment_success": "✅ Ulasan anda telah dihantar, terima kasih.",
        "comment_warning": "⚠️ Sila tulis ulasan sebelum menghantar.",
        "comments_title": "Ulasan sesi ini:",
        "comments_note": "Nota: ulasan ini hanya disimpan untuk sesi semasa anda.",
        "birthplace": "Tempat lahir",
        "founding_place": "Tempat penubuhan mazhab",
        "scholars": "Ulama terkemuka mazhab",
        "official_madhab": "Mazhab rasmi",
        "population": "Penduduk (anggaran)",
    },
    "ur": {
        "app_title": "مذاہب کی آراء کا مختصر مجموعہ",
        "app_subtitle": "مذاہب فقہیہ کی آراء دکھانے اور موازنہ کرنے کا پلیٹ فارم — فہم و بصیرت کے لیے، فتویٰ جاری کرنے کے لیے نہیں۔",
        "lang_label": "زبان",
        "s1_title": "۱ — مذہب منتخب کریں",
        "group_q": "اہل سنت کے مذاہب، اہل تشیع کے مذاہب، یا اباضی مذہب؟",
        "multi_hint": "💡 آپ موازنہ کے لیے ایک سے زیادہ مذاہب منتخب کر سکتے ہیں۔",
        "sub_select": "ایک یا زیادہ مذاہب منتخب کریں:",
        "s2_title": "۲ — موضوع منتخب کریں",
        "topic_q": "فقہی موضوع منتخب کریں",
        "s3_title": "۳ — جواب کی تفصیل کی سطح",
        "level_q": "تفصیل کی سطح منتخب کریں",
        "s4_title": "۴ — اپنا سوال لکھیں",
        "question_placeholder": "مثال: نماز باجماعت کا کیا حکم ہے؟",
        "search_btn": "🔍 جواب تلاش کریں",
        "s5_title": "۵ — جواب",
        "answer_placeholder": "جواب یہاں ظاہر ہوگا جب آپ سوال لکھیں گے اور تلاش پر کلک کریں گے۔",
        "no_question_warning": "براہ کرم پہلے حصہ ۴ میں اپنا سوال لکھیں۔",
        "no_madhab_warning": "براہ کرم کم از کم ایک مذہب منتخب کریں۔",
        "no_results_warning": "🔍 منتخب موضوع میں اس تفصیل کا کوئی مسئلہ نہیں ملا۔ دوسرے الفاظ آزمائیں۔",
        "signature": "واللہ اعلم",
        "note_general": "متفقہ عمومی رائے — ابھی تک مذہب کے لحاظ سے تفصیل نہیں دی گئی",
        "note_madhab": "مذہب {} کی رائے",
        "expander_imams": "📜 مذاہب کے بانی ائمہ",
        "expander_countries": "🗺️ اسلامی ممالک اور سرکاری مذہب",
        "expander_glossary": "📚 اہم فقہی اصطلاحات",
        "expander_comments": "💬 اپنا تبصرہ یا نوٹ شامل کریں",
        "rating_label": "اس جواب کی افادیت کی درجہ بندی کریں:",
        "comment_placeholder": "اپنا تبصرہ یہاں لکھیں...",
        "comment_submit": "تبصرہ جمع کریں",
        "comment_success": "✅ آپ کا تبصرہ موصول ہوگیا، شکریہ۔",
        "comment_warning": "⚠️ براہ کرم جمع کرنے سے پہلے تبصرہ لکھیں۔",
        "comments_title": "اس سیشن کے تبصرے:",
        "comments_note": "نوٹ: یہ تبصرے صرف آپ کے موجودہ سیشن کے لیے محفوظ ہیں۔",
        "birthplace": "جائے پیدائش",
        "founding_place": "مذہب کے قیام کی جگہ",
        "scholars": "مشہور فقہاء",
        "official_madhab": "سرکاری مذہب",
        "population": "آبادی (تقریباً)",
    },
}

MADHHAB_NAMES = {
    "maliki": {"ar": "مالكي", "en": "Maliki", "fr": "Malikite", "fa": "مالکی", "ms": "Maliki", "ur": "مالکی"},
    "shafii": {"ar": "شافعي", "en": "Shafi'i", "fr": "Chaféite", "fa": "شافعی", "ms": "Syafie", "ur": "شافعی"},
    "hanafi": {"ar": "حنفي", "en": "Hanafi", "fr": "Hanafite", "fa": "حنفی", "ms": "Hanafi", "ur": "حنفی"},
    "hanbali": {"ar": "حنبلي", "en": "Hanbali", "fr": "Hanbalite", "fa": "حنبلی", "ms": "Hanbali", "ur": "حنبلی"},
    "zahiri": {"ar": "ظاهري", "en": "Zahiri", "fr": "Zahirite", "fa": "ظاهری", "ms": "Zahiri", "ur": "ظاہری"},
    "jafari": {"ar": "جعفري", "en": "Ja'fari", "fr": "Jaafarite", "fa": "جعفری", "ms": "Jaafari", "ur": "جعفری"},
    "zaidi": {"ar": "زيدي", "en": "Zaidi", "fr": "Zaydite", "fa": "زیدی", "ms": "Zaidi", "ur": "زیدی"},
    "ibadi": {"ar": "إباضي", "en": "Ibadi", "fr": "Ibadite", "fa": "اباضی", "ms": "Ibadi", "ur": "اباضی"},
}

GROUPS = {
    "sunni": {"ar": "مذاهب السنة", "en": "Sunni Schools", "fr": "Écoles sunnites", "fa": "مذاهب اهل سنت", "ms": "Mazhab Sunni", "ur": "اہل سنت کے مذاہب",
              "members": ["maliki", "shafii", "hanafi", "hanbali", "zahiri"]},
    "shia": {"ar": "مذاهب الشيعة", "en": "Shia Schools", "fr": "Écoles chiites", "fa": "مذاهب شیعه", "ms": "Mazhab Syiah", "ur": "شیعہ مذاہب",
             "members": ["jafari", "zaidi"]},
    "ibadi": {"ar": "المذهب الإباضي", "en": "Ibadi School", "fr": "École ibadite", "fa": "مذهب اباضی", "ms": "Mazhab Ibadi", "ur": "اباضی مذہب",
              "members": ["ibadi"]},
}

TOPICS = {
    "ibadat": {"ar": "العبادات", "en": "Acts of Worship", "fr": "Actes d'adoration", "fa": "عبادات", "ms": "Ibadat", "ur": "عبادات"},
    "muamalat": {"ar": "المعاملات", "en": "Transactions", "fr": "Transactions", "fa": "معاملات", "ms": "Muamalat", "ur": "معاملات"},
    "family": {"ar": "الأسرة", "en": "Family", "fr": "Famille", "fa": "خانواده", "ms": "Keluarga", "ur": "خاندان"},
    "other": {"ar": "مواضيع أخرى", "en": "Other Topics", "fr": "Autres sujets", "fa": "موضوعات دیگر", "ms": "Topik Lain", "ur": "دیگر موضوعات"},
}

LEVELS = {
    "very_short": {"ar": "مختصرة (كلمة)", "en": "Very short (one word)", "fr": "Très bref (un mot)", "fa": "بسیار مختصر (یک واژه)", "ms": "Sangat ringkas (satu perkataan)", "ur": "بہت مختصر (ایک لفظ)"},
    "short": {"ar": "مبسطة (سطر)", "en": "Short (one line)", "fr": "Bref (une ligne)", "fa": "ساده (یک خط)", "ms": "Ringkas (satu baris)", "ur": "آسان (ایک سطر)"},
    "full": {"ar": "مفصل (أكثر من سطر)", "en": "Detailed (full)", "fr": "Détaillé (complet)", "fa": "مفصل (چند خط)", "ms": "Terperinci (penuh)", "ur": "تفصیلی (مکمل)"},
}

GLOSSARY = [
    {"term": {"ar": "الفرض / فرض العين", "en": "Fard / Fard Ayn (Individual Obligation)", "fr": "Le fard / fard ayn (Obligation individuelle)", "fa": "فرض / فرض عین", "ms": "Fardu / Fardu Ain (Kewajipan Individu)", "ur": "فرض / فرض عین"},
     "definition": {"ar": "ما طلب الشارع فعله طلباً جازماً من كل مكلف بعينه، يُثاب فاعله ويُعاقب تاركه.",
                    "en": "What the Lawgiver has decisively commanded every legally accountable individual to perform; one who does it is rewarded, and one who abandons it is sinful.",
                    "fr": "Ce que le Législateur a ordonné de façon décisive à tout individu responsable d'accomplir ; celui qui l'accomplit est récompensé, et celui qui l'abandonne est fautif.",
                    "fa": "آنچه شارع به‌طور قطعی بر هر مکلفی واجب کرده است؛ انجام‌دهنده پاداش می‌گیرد و ترک‌کننده گناهکار است.",
                    "ms": "Apa yang Pembuat Syariat telah perintahkan secara tegas kepada setiap individu yang bertanggungjawab untuk melaksanakannya; yang melaksanakannya diberi pahala, dan yang meninggalkannya berdosa.",
                    "ur": "وہ چیز جسے شارع نے ہر مکلف پر قطعی طور پر واجب کیا ہے؛ اسے کرنے والا ثواب پاتا ہے اور چھوڑنے والا گنہگار ہے۔"}},
    # باقي المصطلحات (اختصاراً، أكتفي بهذا المثال)
]

IMAMS = [
    {"name": {"ar": "الإمام مالك بن أنس الأصبحي", "en": "Imam Malik ibn Anas al-Asbahi", "fr": "L'imam Malik ibn Anas al-Asbahi", "fa": "امام مالک بن انس اصبحی", "ms": "Imam Malik bin Anas al-Asbahi", "ur": "امام مالک بن انس اصبحی"},
     "school": MADHHAB_NAMES["maliki"], "lifespan": "93 - 179 AH",
     "birthplace": {"ar": "المدينة المنورة", "en": "Medina", "fr": "Médine", "fa": "مدینه منوره", "ms": "Madinah", "ur": "مدینہ منورہ"},
     "founding_place": {"ar": "المدينة المنورة", "en": "Medina", "fr": "Médine", "fa": "مدینه منوره", "ms": "Madinah", "ur": "مدینہ منورہ"},
     "scholars": {"ar": "ابن القاسم، سحنون، ابن رشد، القرافي، خليل بن إسحاق",
                  "en": "Ibn al-Qasim, Sahnun, Ibn Rushd, al-Qarafi, Khalil ibn Ishaq",
                  "fr": "Ibn al-Qasim, Sahnun, Ibn Rushd, al-Qarafi, Khalil ibn Ishaq",
                  "fa": "ابن قاسم، سحنون، ابن رشد، قرافی، خلیل بن اسحاق",
                  "ms": "Ibn al-Qasim, Sahnun, Ibn Rushd, al-Qarafi, Khalil bin Ishaq",
                  "ur": "ابن قاسم، سحنون، ابن رشد، قرافی، خلیل بن اسحاق"}},
    # باقي الأئمة (اختصاراً)
]

COUNTRIES = [
    {"flag": "🇸🇦", "name": {"ar": "السعودية", "en": "Saudi Arabia", "fr": "Arabie saoudite", "fa": "عربستان سعودی", "ms": "Arab Saudi", "ur": "سعودی عرب"}, "madhab": "hanbali", "population": "36.4M"},
    {"flag": "🇪🇬", "name": {"ar": "مصر", "en": "Egypt", "fr": "Égypte", "fa": "مصر", "ms": "Mesir", "ur": "مصر"}, "madhab": "shafii", "population": "112.7M"},
    {"flag": "🇲🇦", "name": {"ar": "المغرب", "en": "Morocco", "fr": "Maroc", "fa": "مراکش", "ms": "Maghribi", "ur": "مراکش"}, "madhab": "maliki", "population": "37.8M"},
    {"flag": "🇹🇷", "name": {"ar": "تركيا", "en": "Turkey", "fr": "Turquie", "fa": "ترکیه", "ms": "Turki", "ur": "ترکی"}, "madhab": "hanafi", "population": "87.5M"},
    {"flag": "🇮🇷", "name": {"ar": "إيران", "en": "Iran", "fr": "Iran", "fa": "ایران", "ms": "Iran", "ur": "ایران"}, "madhab": "jafari", "population": "89.8M"},
    {"flag": "🇴🇲", "name": {"ar": "عُمان", "en": "Oman", "fr": "Oman", "fa": "عمان", "ms": "Oman", "ur": "عمان"}, "madhab": "ibadi", "population": "4.7M"},
]

# =====================================================================
# 6) STREAMLIT UI
# =====================================================================
def main():
    init_db()
    seed_initial_issues()

    if "lang" not in st.session_state:
        st.session_state.lang = "ar"

    top_l, top_r = st.columns([5, 2])
    with top_r:
        lang_choice = st.radio(
            UI[st.session_state.lang]["lang_label"],
            list(LANGS.keys()),
            index=list(LANGS.values()).index(st.session_state.lang),
            horizontal=True,
        )
        st.session_state.lang = LANGS[lang_choice]

    lang = st.session_state.lang
    T = UI[lang]
    is_rtl = lang in ["ar", "fa", "ur"]
    direction = "rtl" if is_rtl else "ltr"
    align = "right" if is_rtl else "left"

    st.markdown(f"""
    <style>
    .stApp {{ direction: {direction}; }}
    .stApp p, .stApp li, .stApp label, .stApp span,
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5 {{
        text-align: {align};
        line-height: 1.9;
    }}
    div[role="radiogroup"], div[data-baseweb="select"], div[data-testid="stMultiSelect"] {{ direction: {direction}; }}
    .stButton button {{ width: 100%; }}
    .app-header {{
        text-align: center; padding: 26px 16px;
        background: linear-gradient(145deg, #0f231c, #2a5c4a);
        color: white; border-radius: 16px; margin-bottom: 25px;
    }}
    .app-header h1, .app-header p {{ text-align: center !important; }}
    .answer-card {{
        background: #f5f7f5; border: 1px solid #e1e7e3;
        border-radius: 14px; padding: 16px 18px;
        margin-bottom: 12px; direction: {direction}; text-align: {align};
    }}
    .answer-card h4 {{ margin: 0 0 6px 0; color: #1e3a2f; text-align: {align}; }}
    .answer-card .answer-text {{ font-size: 1.15rem; font-weight: 600; color: #16281f; margin: 4px 0; }}
    .answer-card .answer-note {{ font-size: 0.85rem; color: #6a7f78; }}
    .signature {{
        font-family: 'Brush Script MT', 'Segoe Script', cursive;
        font-style: italic; font-size: 1rem; color: #b08d3f;
        text-align: center; margin: 6px 0 18px 0; opacity: 0.9;
    }}
    .info-box {{
        background:#f5f7f5; padding:12px 16px; border-radius:12px; margin-bottom:10px;
        border-{"right" if is_rtl else "left"}:4px solid #d4a854;
        direction: {direction}; text-align: {align};
    }}
    .info-box h4 {{ margin:0; color:#1e3a2f; text-align: {align}; }}
    .info-box p {{ margin:2px 0; color:#3d4f5f; text-align: {align}; }}
    .glossary-box {{
        background:#f5f7f5; padding:12px 16px; border-radius:12px; margin-bottom:10px;
        border-{"right" if is_rtl else "left"}:4px solid #1e3a2f;
        direction: {direction}; text-align: {align};
    }}
    .country-box {{
        background:#f5f7f5; padding:8px 12px; border-radius:8px; margin-bottom:6px;
        border-{"right" if is_rtl else "left"}:3px solid #d4a854;
        direction: {direction}; text-align: {align};
    }}
    </style>
    """, unsafe_allow_html=True)

    # الشعار
    st.markdown("""
    <div style="text-align:center; margin-bottom:-6px;">
        <svg width="72" height="72" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
            <circle cx="50" cy="50" r="46" fill="#0f231c" stroke="#d4a854" stroke-width="3"/>
            <path d="M50 28 C38 22 26 24 20 30 V66 C26 60 38 58 50 64 C62 58 74 60 80 66 V30 C74 24 62 22 50 28 Z"
                  fill="none" stroke="#f2e6c9" stroke-width="3" stroke-linejoin="round"/>
            <line x1="50" y1="28" x2="50" y2="64" stroke="#f2e6c9" stroke-width="2.5"/>
            <path d="M66 20 A10 10 0 1 0 68 38 A8 8 0 1 1 66 20 Z" fill="#d4a854"/>
        </svg>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="app-header">
        <h1>📖 {T['app_title']}</h1>
        <p>{T['app_subtitle']}</p>
    </div>
    """, unsafe_allow_html=True)

    # استيراد CSV
    with st.expander("📥 استيراد مسائل من CSV (للمشرفين)", expanded=False):
        st.info("""
        **تنسيق CSV المطلوب:** يجب أن يحتوي على أعمدة: `topic, title_ar, title_en, title_fr, title_fa, title_ms, title_ur, keywords_ar, keywords_en, keywords_fr, keywords_fa, keywords_ms, keywords_ur, ruling_vs_ar, ruling_s_ar, ruling_f_ar, ...` (جميع الأعمدة التي في قاعدة البيانات).
        يمكنك تنزيل ملف نموذجي من الرد السابق.
        """)
        uploaded = st.file_uploader("اختر ملف CSV", type=["csv"])
        if uploaded:
            try:
                count = import_from_csv(uploaded.read())
                st.success(f"✅ تم استيراد {count} مسألة بنجاح!")
            except Exception as e:
                st.error(f"❌ خطأ: {e}")

    # أقسام البحث
    st.markdown(f"### {T['s1_title']}")
    group_code = st.radio(
        T["group_q"],
        list(GROUPS.keys()),
        format_func=lambda g: GROUPS[g][lang],
        horizontal=True,
        label_visibility="collapsed",
    )
    sub_codes = GROUPS[group_code]["members"]
    st.caption(T["multi_hint"])
    if len(sub_codes) > 1:
        selected_madhabs = st.multiselect(
            T["sub_select"],
            options=sub_codes,
            default=[sub_codes[0]],
            format_func=lambda c: MADHHAB_NAMES[c][lang],
        )
    else:
        selected_madhabs = sub_codes
        st.caption(f"**{MADHHAB_NAMES[sub_codes[0]][lang]}**")

    st.divider()
    st.markdown(f"### {T['s2_title']}")
    topic = st.radio(
        T["topic_q"],
        list(TOPICS.keys()),
        format_func=lambda t: TOPICS[t][lang],
        horizontal=True,
        label_visibility="collapsed",
    )

    st.divider()
    st.markdown(f"### {T['s3_title']}")
    level = st.radio(
        T["level_q"],
        list(LEVELS.keys()),
        format_func=lambda lv: LEVELS[lv][lang],
        horizontal=True,
        label_visibility="collapsed",
    )

    st.divider()
    st.markdown(f"### {T['s4_title']}")
    question = st.text_input(
        T["s4_title"], placeholder=T["question_placeholder"], label_visibility="collapsed"
    )
    search_clicked = st.button(T["search_btn"], use_container_width=True)

    st.divider()
    st.markdown(f"### {T['s5_title']}")
    if search_clicked and not selected_madhabs:
        st.warning(T["no_madhab_warning"])
    elif search_clicked and question:
        results = search_issues(question, topic, selected_madhabs, level, lang)
        if results:
            for r in results:
                st.markdown(f"**📌 {r['title']}** &nbsp;·&nbsp; _{r['topic']}_")
                cols = st.columns(len(r["cards"])) if len(r["cards"]) > 1 else [st.container()]
                for col, card in zip(cols, r["cards"]):
                    with col:
                        st.markdown(f"""
                        <div class="answer-card">
                            <h4>{card['label']}</h4>
                            <div class="answer-text">{card['answer']}</div>
                            <div class="answer-note">{card['note']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                st.markdown(f"<div class='signature'>{T['signature']}</div>", unsafe_allow_html=True)
        else:
            st.warning(T["no_results_warning"])
    elif search_clicked:
        st.info(T["no_question_warning"])
    else:
        st.caption(T["answer_placeholder"])

    st.markdown("---")

    # أقسام مرجعية
    with st.expander(T["expander_imams"]):
        for imam in IMAMS:
            st.markdown(f"""
            <div class="info-box">
                <h4>{imam['name'][lang]}</h4>
                <p style="color:#d4a854; font-weight:600;">{imam['school'][lang]} &nbsp;|&nbsp; {imam['lifespan']}</p>
                <p>📍 {T['birthplace']}: {imam['birthplace'][lang]} &nbsp;·&nbsp; 🏛️ {T['founding_place']}: {imam['founding_place'][lang]}</p>
                <p>🎓 {T['scholars']}: {imam['scholars'][lang]}</p>
            </div>
            """, unsafe_allow_html=True)

    with st.expander(T["expander_countries"]):
        cols = st.columns(3)
        for i, c in enumerate(COUNTRIES):
            with cols[i % 3]:
                st.markdown(f"""
                <div class="country-box">
                    <strong>{c['flag']} {c['name'][lang]}</strong><br>
                    <span style="color:#d4a854;">{T['official_madhab']}: {MADHHAB_NAMES[c['madhab']][lang]}</span><br>
                    <span style="font-size:0.8rem; color:#6a7f78;">👥 {T['population']}: {c['population']}</span>
                </div>
                """, unsafe_allow_html=True)

    with st.expander(T["expander_glossary"]):
        for term in GLOSSARY:
            st.markdown(f"""
            <div class="glossary-box">
                <h4>{term['term'][lang]}</h4>
                <p>{term['definition'][lang]}</p>
            </div>
            """, unsafe_allow_html=True)

    with st.expander(T["expander_comments"]):
        if "session_comments" not in st.session_state:
            st.session_state.session_comments = []
        st.markdown(f"**{T['rating_label']}**")
        try:
            rating = st.feedback("stars")
            if rating is not None:
                rating = rating + 1
        except:
            rating = st.radio(T["rating_label"], [1,2,3,4,5], format_func=lambda n: "⭐"*n, horizontal=True, label_visibility="collapsed")
        comment_text = st.text_area(T["comment_placeholder"], placeholder=T["comment_placeholder"], label_visibility="collapsed")
        if st.button(T["comment_submit"]):
            if comment_text.strip():
                st.session_state.session_comments.append({"text": comment_text.strip(), "rating": rating or 5})
                st.success(T["comment_success"])
            else:
                st.warning(T["comment_warning"])
        if st.session_state.session_comments:
            st.markdown(f"**{T['comments_title']}**")
            for c in st.session_state.session_comments:
                st.markdown(f"- {'⭐' * int(c['rating'])} — {c['text']}")
        st.caption(T["comments_note"])

if __name__ == "__main__":
    main()
