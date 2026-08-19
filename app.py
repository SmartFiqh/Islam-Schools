import streamlit as st
import re

st.set_page_config(
    page_title="الجامع المختصر لآراء المذاهب | Madhhab Compendium",
    page_icon="📖",
    layout="wide",
)

# =========================================================================
# 1) TRANSLATION / REFERENCE DATA
# =========================================================================

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

# --- Issues ---------------------------------------------------------------

ISSUES = [
    {
        "id": 1, "topic": "ibadat",
        "title": {"ar": "صلاة الجماعة", "en": "Congregational Prayer", "fr": "La prière en congrégation", "fa": "نماز جماعت", "ms": "Solat Berjemaah", "ur": "نماز باجماعت"},
        "keywords": {
            "ar": ["جماعة", "مسجد", "رجال", "صلاة", "فرض", "سنة", "واجب"],
            "en": ["congregation", "mosque", "men", "prayer", "obligatory", "sunnah"],
            "fr": ["congrégation", "mosquée", "hommes", "prière", "obligatoire", "sunna"],
            "fa": ["جماعت", "مسجد", "مردان", "نماز", "فرض", "سنت", "واجب"],
            "ms": ["jemaah", "masjid", "lelaki", "solat", "fardu", "sunnah", "wajib"],
            "ur": ["جماعت", "مسجد", "مرد", "نماز", "فرض", "سنت", "واجب"],
        },
        "rulings": {
            "ar": {"very_short": "سنة مؤكدة", "short": "سنة مؤكدة عند الجمهور، واجبة عند الحنفية", "full": "تجب صلاة الجماعة في المسجد على الرجال عند جمهور الفقهاء؛ فهي فرض عين عند الحنابلة، واجب مؤكد عند الحنفية، فرض كفاية عند المالكية والشافعية، ومستحبة تأكيداً عند الجعفرية في زمن الغيبة."},
            "en": {"very_short": "Emphasized Sunnah", "short": "Emphasized sunnah for most jurists, obligatory for the Hanafis", "full": "Congregational prayer in the mosque is required of men according to the majority of jurists: an individual obligation for the Hanbalis, an emphasized obligation for the Hanafis, a communal obligation for the Malikis and Shafi'is, and a strongly recommended act for the Ja'faris during the Occultation."},
            "fr": {"very_short": "Sunna fortement recommandée", "short": "Sunna fortement recommandée pour la majorité, obligatoire pour les hanafites", "full": "La prière en congrégation à la mosquée est requise des hommes selon la majorité des juristes : obligation individuelle chez les hanbalites, obligation appuyée chez les hanafites, obligation collective chez les malikites et les chaféites, et acte fortement recommandé chez les jaafarites durant l'Occultation."},
            "fa": {"very_short": "سنت مؤکد", "short": "سنت مؤکد نزد جمهور، واجب نزد حنفیان", "full": "نماز جماعت در مسجد بر مردان واجب است به اتفاق جمهور فقها؛ فرض عین برای حنبلی‌ها، واجب مؤکد برای حنفی‌ها، فرض کفایه برای مالکی‌ها و شافعی‌ها، و مستحب مؤکد برای جعفری‌ها در زمان غیبت."},
            "ms": {"very_short": "Sunnah muakkadah", "short": "Sunnah muakkadah bagi majoriti, wajib bagi Hanafi", "full": "Solat berjemaah di masjid diwajibkan ke atas lelaki menurut majoriti ulama; fardu ain bagi Hanbali, wajib muakkad bagi Hanafi, fardu kifayah bagi Maliki dan Syafii, dan mustahab muakkad bagi Jaafari semasa ghaib."},
            "ur": {"very_short": "سنت مؤکدہ", "short": "سنت مؤکدہ نزد جمہور، واجب نزد احناف", "full": "مسجد میں نماز باجماعت مردوں پر جمہور فقہاء کے نزدیک واجب ہے؛ حنابلہ کے نزدیک فرض عین، احناف کے نزدیک واجب مؤکد، مالکیہ و شافعیہ کے نزدیک فرض کفایہ، اور جعفریہ کے نزدیک مستحب مؤکد ہے۔"},
        },
        "rulings_by_madhab": {
            "maliki": {
                "ar": {"very_short": "فرض كفاية", "short": "فرض كفاية على أهل الحي، سنة مؤكدة للفرد", "full": "فرض كفاية على أهل الحي؛ وفي حق الفرد الواحد سنة مؤكدة لا يُكره تركها إلا لمن واظب عليه."},
                "en": {"very_short": "Fard Kifayah", "short": "Communal obligation on the locality, emphasized sunnah for the individual", "full": "It is a communal obligation (fard kifayah) upon the residents of a locality; for a single individual it is an emphasized sunnah, and abandoning it is disliked only for one who habitually neglects it."},
                "fr": {"very_short": "Fard kifaya", "short": "Obligation collective pour le quartier, sunna appuyée pour l'individu", "full": "C'est une obligation collective (fard kifaya) pour les habitants d'un quartier ; pour un individu seul, c'est une sunna fortement recommandée, et ne pas l'accomplir n'est blâmable que pour celui qui la délaisse habituellement."},
                "fa": {"very_short": "فرض کفایه", "short": "فرض کفایه بر اهل محله، سنت مؤکد برای فرد", "full": "فرض کفایه بر اهل محله است؛ و برای فرد واحد سنت مؤکدی است که ترک آن تنها برای کسی که همواره آن را ترک کند مکروه است."},
                "ms": {"very_short": "Fardu kifayah", "short": "Fardu kifayah ke atas penduduk kawasan, sunnah muakkadah untuk individu", "full": "Fardu kifayah ke atas penduduk sesuatu kawasan; bagi individu ia adalah sunnah muakkadah, dan meninggalkannya hanya makruh bagi yang selalu meninggalkannya."},
                "ur": {"very_short": "فرض کفایہ", "short": "محلہ والوں پر فرض کفایہ، فرد کے لیے سنت مؤکدہ", "full": "محلہ والوں پر فرض کفایہ ہے؛ اور فرد واحد کے لیے سنت مؤکدہ ہے، اور اسے ترک کرنا صرف اس شخص کے لیے مکروہ ہے جو ہمیشہ اسے ترک کرتا ہو۔"},
            },
            "shafii": {
                "ar": {"very_short": "سنة مؤكدة", "short": "فرض كفاية على المجتمع، سنة مؤكدة للفرد", "full": "فرض كفاية على المجتمع ككل، وسنة مؤكدة في حق الفرد؛ وهو الأصح في المذهب."},
                "en": {"very_short": "Emphasized Sunnah", "short": "Communal obligation on society, emphasized sunnah for the individual", "full": "It is a communal obligation upon society as a whole, and an emphasized sunnah for the individual — this is the most authoritative view in the school."},
                "fr": {"very_short": "Sunna fortement recommandée", "short": "Obligation collective pour la société, sunna appuyée pour l'individu", "full": "C'est une obligation collective pour la société dans son ensemble, et une sunna fortement recommandée pour l'individu — c'est l'avis le plus correct de l'école."},
                "fa": {"very_short": "سنت مؤکد", "short": "فرض کفایه بر جامعه، سنت مؤکد برای فرد", "full": "فرض کفایه بر جامعه به‌عنوان یک کل، و سنت مؤکد برای فرد است — این صحیح‌ترین دیدگاه در مذهب است."},
                "ms": {"very_short": "Sunnah muakkadah", "short": "Fardu kifayah ke atas masyarakat, sunnah muakkadah untuk individu", "full": "Fardu kifayah ke atas masyarakat secara keseluruhan, dan sunnah muakkadah untuk individu — ini adalah pandangan yang paling sahih dalam mazhab."},
                "ur": {"very_short": "سنت مؤکدہ", "short": "معاشرے پر فرض کفایہ، فرد کے لیے سنت مؤکدہ", "full": "معاشرے پر مجموعی طور پر فرض کفایہ ہے، اور فرد کے لیے سنت مؤکدہ ہے — یہ مذہب میں سب سے صحیح رائے ہے۔"},
            },
            "hanafi": {
                "ar": {"very_short": "واجب", "short": "واجبة على كل رجل حر بالغ عاقل", "full": "واجبة وجوباً غير ملزم على كل رجل حر بالغ عاقل قادر؛ وتركها بلا عذر مكروه تحريماً عند المتأخرين."},
                "en": {"very_short": "Wajib", "short": "Obligatory (wajib) on every free, sane, adult man", "full": "It is obligatory (wajib), one degree below fard, upon every free, sane, adult, capable man; abandoning it without excuse is strongly disliked according to later scholars."},
                "fr": {"very_short": "Wajib", "short": "Obligatoire pour tout homme libre, majeur et sain d'esprit", "full": "C'est une obligation (wajib), un degré en dessous du fard, pour tout homme libre, sain d'esprit, majeur et capable ; l'abandonner sans excuse est fortement blâmable selon les savants tardifs."},
                "fa": {"very_short": "واجب", "short": "بر هر مرد آزاد بالغ عاقل واجب است", "full": "واجب است (یک درجه پایین‌تر از فرض) بر هر مرد آزاد بالغ عاقل توانا؛ ترک آن بدون عذر به‌گفته متأخران مکروه تحریمی است."},
                "ms": {"very_short": "Wajib", "short": "Wajib ke atas setiap lelaki merdeka, baligh, berakal", "full": "Wajib (satu darjah di bawah fardu) ke atas setiap lelaki merdeka, baligh, berakal, dan mampu; meninggalkannya tanpa uzur adalah makruh tahrimi menurut ulama kemudian."},
                "ur": {"very_short": "واجب", "short": "ہر آزاد بالغ عاقل مرد پر واجب", "full": "فرض سے ایک درجہ نیچے واجب ہے ہر آزاد بالغ عاقل مرد پر؛ اسے بغیر عذر چھوڑنا متأخرین کے نزدیک مکروہ تحریمی ہے۔"},
            },
            "hanbali": {
                "ar": {"very_short": "فرض عين", "short": "فرض عين على كل رجل قادر", "full": "فرض عين على كل رجل مكلف قادر؛ لا يجوز تركها إلا لعذر شرعي معتبر."},
                "en": {"very_short": "Fard Ayn", "short": "Individual obligation on every capable man", "full": "It is an individual obligation (fard ayn) upon every legally accountable, capable man; it may not be abandoned except for a recognized legal excuse."},
                "fr": {"very_short": "Fard ayn", "short": "Obligation individuelle pour tout homme capable", "full": "C'est une obligation individuelle (fard ayn) pour tout homme responsable et capable ; elle ne peut être délaissée que pour une excuse légale reconnue."},
                "fa": {"very_short": "فرض عین", "short": "فرض عین بر هر مرد توانا", "full": "فرض عین بر هر مرد مکلف توانا است؛ ترک آن جز با عذر شرعی معتبر جایز نیست."},
                "ms": {"very_short": "Fardu ain", "short": "Fardu ain ke atas setiap lelaki yang mampu", "full": "Fardu ain ke atas setiap lelaki yang bertanggungjawab dan mampu; tidak boleh ditinggalkan kecuali dengan uzur syarie yang diiktiraf."},
                "ur": {"very_short": "فرض عین", "short": "ہر قابل مرد پر فرض عین", "full": "ہر مکلف قابل مرد پر فرض عین ہے؛ اسے صرف معتبر شرعی عذر کے ساتھ چھوڑا جا سکتا ہے۔"},
            },
            "zahiri": {
                "ar": {"very_short": "فرض عين", "short": "فرض عين؛ ظاهر الأمر النبوي يقتضي الوجوب", "full": "فرض عين أخذاً بظاهر الأمر النبوي بالمحافظة عليها، دون تأويل يصرفه عن الوجوب."},
                "en": {"very_short": "Fard Ayn", "short": "Individual obligation, based on the literal Prophetic command", "full": "It is an individual obligation, taken from the literal wording of the Prophet's command to maintain it, without interpretation that would divert it away from obligation."},
                "fr": {"very_short": "Fard ayn", "short": "Obligation individuelle selon le sens littéral de l'ordre prophétique", "full": "C'est une obligation individuelle, tirée du sens littéral de l'ordre du Prophète de la maintenir, sans interprétation qui la détournerait de l'obligation."},
                "fa": {"very_short": "فرض عین", "short": "فرض عین؛ ظاهر امر نبوی اقتضای وجوب دارد", "full": "فرض عین است به‌استناد ظاهر امر نبوی به محافظت بر آن، بدون تأویلی که آن را از وجوب منصرف کند."},
                "ms": {"very_short": "Fardu ain", "short": "Fardu ain berdasarkan zahir perintah Nabi", "full": "Fardu ain berdasarkan zahir perintah Nabi untuk menjaganya, tanpa takwilan yang memalingkannya daripada kewajipan."},
                "ur": {"very_short": "فرض عین", "short": "فرض عین؛ ظاہر امر نبوی وجوب کا تقاضا کرتا ہے", "full": "فرض عین ہے، نبی ﷺ کے امر کے ظاہر کو لے کر، بغیر کسی تأویل کے جو اسے وجوب سے ہٹا دے۔"},
            },
            "jafari": {
                "ar": {"very_short": "مستحب مؤكد", "short": "مستحبة استحباباً مؤكداً في زمن الغيبة", "full": "مستحبة استحباباً مؤكداً وليست واجبة عيناً في زمن الغيبة الكبرى، وثوابها عظيم."},
                "en": {"very_short": "Strongly recommended", "short": "Strongly recommended during the Occultation, not individually obligatory", "full": "It is strongly recommended rather than individually obligatory during the Major Occultation, and its reward is great."},
                "fr": {"very_short": "Fortement recommandée", "short": "Fortement recommandée durant l'Occultation, non obligatoire individuellement", "full": "Elle est fortement recommandée plutôt qu'individuellement obligatoire durant la Grande Occultation, et sa récompense est immense."},
                "fa": {"very_short": "مستحب مؤکد", "short": "در زمان غیبت مستحب مؤکد است نه واجب عینی", "full": "در زمان غیبت کبری مستحب مؤکد است نه واجب عینی، و ثواب آن عظیم است."},
                "ms": {"very_short": "Mustahab muakkad", "short": "Mustahab muakkad semasa ghaib, tidak wajib ain", "full": "Mustahab muakkad dan bukannya wajib ain semasa Ghaib Kubra, dan pahalanya besar."},
                "ur": {"very_short": "مستحب مؤکد", "short": "غیبت کے زمانے میں مستحب مؤکد، فرض عین نہیں", "full": "غیبت کبریٰ میں فرض عین نہیں بلکہ مستحب مؤکد ہے، اور اس کا ثواب عظیم ہے۔"},
            },
            "zaidi": {
                "ar": {"very_short": "فرض كفاية", "short": "قريب من رأي أهل السنة في تأكيدها", "full": "فرض كفاية، ويقترب الرأي الزيدي من الرأي السني في التأكيد على المحافظة عليها جماعة."},
                "en": {"very_short": "Fard Kifayah", "short": "Close to the Sunni emphasis on maintaining it", "full": "It is a communal obligation; the Zaidi view is close to the Sunni emphasis on maintaining it in congregation."},
                "fr": {"very_short": "Fard kifaya", "short": "Proche de l'insistance sunnite sur son maintien", "full": "C'est une obligation collective ; l'avis zaydite se rapproche de l'insistance sunnite sur son maintien en congrégation."},
                "fa": {"very_short": "فرض کفایه", "short": "نزدیک به نظر اهل سنت در تأکید بر آن", "full": "فرض کفایه است، و دیدگاه زیدی به دیدگاه اهل سنت در تأکید بر حفظ آن به‌صورت جماعت نزدیک است."},
                "ms": {"very_short": "Fardu kifayah", "short": "Dekat dengan pandangan Sunni dalam menekankannya", "full": "Fardu kifayah; pandangan Zaidi hampir dengan pandangan Sunni dalam menekankan penjagaannya secara berjemaah."},
                "ur": {"very_short": "فرض کفایہ", "short": "اس پر زور دینے میں اہل سنت کے قریب", "full": "فرض کفایہ ہے، اور زیدی رائے اہل سنت کی رائے کے قریب ہے کہ اسے جماعت کے ساتھ برقرار رکھا جائے۔"},
            },
            "ibadi": {
                "ar": {"very_short": "سنة مؤكدة", "short": "من أعلام الدين ولا تُترك باستمرار", "full": "من أعلام الدين الظاهرة، سنة مؤكدة لا ينبغي تركها باستمرار وإن لم تكن شرطاً لصحة الصلاة."},
                "en": {"very_short": "Emphasized Sunnah", "short": "A visible marker of the religion; should not be habitually abandoned", "full": "It is one of the visible markers of the religion, an emphasized sunnah that should not be habitually abandoned, though it is not a condition for the validity of the prayer."},
                "fr": {"very_short": "Sunna fortement recommandée", "short": "Un signe apparent de la religion, à ne pas délaisser habituellement", "full": "C'est l'un des signes apparents de la religion, une sunna fortement recommandée qu'il ne convient pas de délaisser habituellement, bien qu'elle ne soit pas une condition de validité de la prière."},
                "fa": {"very_short": "سنت مؤکد", "short": "از شعائر دین و نباید به‌طور پیوسته ترک شود", "full": "از شعائر ظاهر دین است، سنت مؤکدی که نباید به‌طور پیوسته ترک شود، هرچند شرط صحت نماز نیست."},
                "ms": {"very_short": "Sunnah muakkadah", "short": "Tanda agama yang jelas; tidak boleh ditinggalkan berterusan", "full": "Salah satu tanda agama yang jelas, sunnah muakkadah yang tidak patut ditinggalkan berterusan, walaupun ia bukan syarat sah solat."},
                "ur": {"very_short": "سنت مؤکدہ", "short": "دین کی علامات میں سے، مسلسل ترک نہ کریں", "full": "دین کی ظاہری علامات میں سے، سنت مؤکدہ ہے جسے مسلسل نہیں چھوڑنا چاہیے، اگرچہ یہ نماز کی صحت کے لیے شرط نہیں۔"},
            },
        },
    },
    {
        "id": 2, "topic": "muamalat",
        "title": {"ar": "زكاة الأسهم", "en": "Zakat on Stocks", "fr": "La zakat sur les actions", "fa": "زکات سهام", "ms": "Zakat Saham", "ur": "زکات اسٹاکس"},
        "keywords": {
            "ar": ["زكاة", "أسهم", "استثمار", "تجارة", "نصاب", "مال"],
            "en": ["zakat", "stocks", "shares", "investment", "trade", "nisab"],
            "fr": ["zakat", "actions", "investissement", "commerce", "nisab"],
            "fa": ["زکات", "سهام", "سرمایه‌گذاری", "تجارت", "نصاب", "مال"],
            "ms": ["zakat", "saham", "pelaburan", "perniagaan", "nisab", "harta"],
            "ur": ["زکات", "اسٹاکس", "سرمایہ کاری", "تجارت", "نصاب", "مال"],
        },
        "rulings": {
            "ar": {"very_short": "واجبة", "short": "زكاة الأسهم واجبة إذا بلغت النصاب", "full": "تجب زكاة الأسهم إذا كانت للاستثمار والتجارة، وبلغت قيمتها النصاب (85 جرام ذهب)، وتُحسب بقيمتها السوقية في نهاية الحول، ويُخرج 2.5% من قيمتها."},
            "en": {"very_short": "Obligatory", "short": "Zakat on stocks is due once it reaches the nisab", "full": "Zakat is due on stocks held for investment or trading once their value reaches the nisab (equivalent to 85 grams of gold); it is calculated on their market value at the end of the zakat year, and 2.5% of that value is paid."},
            "fr": {"very_short": "Obligatoire", "short": "La zakat sur les actions est due dès qu'elle atteint le nisab", "full": "La zakat est due sur les actions détenues pour l'investissement ou le commerce dès que leur valeur atteint le nisab (équivalent à 85 grammes d'or) ; elle est calculée sur la valeur marchande à la fin de l'année zakataire, et 2,5 % de cette valeur est versé."},
            "fa": {"very_short": "واجب", "short": "زکات سهام زمانی که به نصاب برسد واجب است", "full": "زکات بر سهامی که برای سرمایه‌گذاری یا تجارت نگهداری می‌شوند، زمانی که ارزش آن‌ها به نصاب (معادل ۸۵ گرم طلا) برسد واجب است؛ بر اساس ارزش بازار در پایان سال زکات محاسبه شده و ۲٫۵٪ آن پرداخت می‌شود."},
            "ms": {"very_short": "Wajib", "short": "Zakat saham wajib apabila mencapai nisab", "full": "Zakat dikenakan ke atas saham yang dipegang untuk pelaburan atau perniagaan apabila nilainya mencapai nisab (bersamaan 85 gram emas); ia dikira berdasarkan nilai pasaran pada akhir tahun zakat, dan 2.5% daripada nilai itu dibayar."},
            "ur": {"very_short": "واجب", "short": "اسٹاکس پر زکات واجب ہے جب نصاب تک پہنچ جائے", "full": "سرمایہ کاری یا تجارت کے لیے رکھے گئے اسٹاکس پر زکات واجب ہے جب ان کی مالیت نصاب (۸۵ گرام سونے کے برابر) تک پہنچ جائے؛ زکاتی سال کے آخر میں ان کی مارکیٹ ویلیو پر حساب لگایا جاتا ہے، اور اس کی ۲.۵ فیصد ادا کی جاتی ہے۔"},
        },
    },
    {
        "id": 3, "topic": "ibadat",
        "title": {"ar": "الجمع في السفر", "en": "Combining Prayers While Traveling", "fr": "Regrouper les prières en voyage", "fa": "جمع نماز در سفر", "ms": "Menggabungkan Solat dalam Perjalanan", "ur": "سفر میں نمازوں کا جمع کرنا"},
        "keywords": {
            "ar": ["جمع", "سفر", "مسافر", "صلاة", "تخفيف", "رخصة"],
            "en": ["combine", "travel", "traveler", "prayer", "concession"],
            "fr": ["regrouper", "voyage", "voyageur", "prière", "allègement"],
            "fa": ["جمع", "سفر", "مسافر", "نماز", "تخفیف", "رخصت"],
            "ms": ["gabung", "perjalanan", "musafir", "solat", "keringanan", "rukhsah"],
            "ur": ["جمع", "سفر", "مسافر", "نماز", "تخفیف", "رخصت"],
        },
        "rulings": {
            "ar": {"very_short": "جائز", "short": "يجوز جمع الصلاة في السفر للمسافر", "full": "يجوز للمسافر جمع صلاة الظهر مع العصر، والمغرب مع العشاء، تقديماً أو تأخيراً، في وقت إحداهما، وذلك تخفيفاً من الله تعالى على المسافرين."},
            "en": {"very_short": "Permissible", "short": "A traveler may combine prayers while on a journey", "full": "A traveler is permitted to combine the noon (Dhuhr) with the afternoon (Asr) prayer, and the sunset (Maghrib) with the night (Isha) prayer, performing them early or delayed within the time of either one, as a concession from God to travelers."},
            "fr": {"very_short": "Permis", "short": "Le voyageur peut regrouper les prières durant le voyage", "full": "Il est permis au voyageur de regrouper la prière du Dhuhr avec celle de l'Asr, et celle du Maghrib avec celle de l'Isha, en les avançant ou en les retardant dans le temps de l'une d'elles, comme allègement accordé par Dieu aux voyageurs."},
            "fa": {"very_short": "جایز", "short": "مسافر می‌تواند نمازها را در سفر جمع کند", "full": "به مسافر اجازه داده شده است که نماز ظهر را با عصر، و مغرب را با عشاء، به‌صورت تقدیم یا تأخیر، در وقت یکی از آنها جمع کند؛ این تخفیفی از سوی خداوند برای مسافران است."},
            "ms": {"very_short": "Harus", "short": "Musafir boleh menggabungkan solat semasa dalam perjalanan", "full": "Musafir dibenarkan menggabungkan solat Zohor dengan Asar, dan Maghrib dengan Isyak, sama ada didahulukan atau dilewatkan dalam waktu salah satu daripadanya, sebagai keringanan daripada Allah kepada musafir."},
            "ur": {"very_short": "جائز", "short": "مسافر سفر میں نمازوں کو جمع کر سکتا ہے", "full": "مسافر کو اجازت ہے کہ وہ ظہر کو عصر کے ساتھ، اور مغرب کو عشاء کے ساتھ، جمع کرے، یا تو تقدیم کر کے یا تأخیر کر کے، ان میں سے کسی ایک کے وقت میں؛ یہ اللہ کی طرف سے مسافروں پر تخفیف ہے۔"},
        },
    },
    {
        "id": 4, "topic": "ibadat",
        "title": {"ar": "نواقض الوضوء", "en": "Nullifiers of Ablution", "fr": "Les annulateurs des ablutions", "fa": "نواقض وضو", "ms": "Pembatal Wudu", "ur": "نواقض وضو"},
        "keywords": {
            "ar": ["وضوء", "نواقض", "طهارة", "بول", "غائط", "نوم", "مس"],
            "en": ["ablution", "wudu", "nullifiers", "purity", "sleep"],
            "fr": ["ablutions", "wudu", "annulateurs", "pureté", "sommeil"],
            "fa": ["وضو", "نواقض", "طهارت", "ادرار", "غائط", "خواب", "لمس"],
            "ms": ["wudu", "pembatal", "kesucian", "kencing", "najis", "tidur", "sentuh"],
            "ur": ["وضو", "نواقض", "طہارت", "بول", "غائط", "نیند", "مس"],
        },
        "rulings": {
            "ar": {"very_short": "مبطل", "short": "نواقض الوضوء تبطل الطهارة وتوجب إعادته", "full": "نواقض الوضوء هي: الخارج من السبيلين (البول، الغائط، الريح)، النوم المستغرق، زوال العقل (بإغماء أو سكر)، مسّ الفرج بغير حائل، ولمس المرأة بشهوة عند بعض المذاهب."},
            "en": {"very_short": "Invalidating", "short": "The nullifiers of ablution invalidate purity and require it to be repeated", "full": "The nullifiers of ablution include: what exits from the two private passages (urine, stool, wind), deep sleep, loss of consciousness (through fainting or intoxication), touching the private parts without a barrier, and, according to some schools, touching a woman with desire."},
            "fr": {"very_short": "Invalidant", "short": "Les annulateurs des ablutions invalident la pureté et imposent de la refaire", "full": "Les annulateurs des ablutions sont : ce qui sort des deux voies (urine, selles, vent), le sommeil profond, la perte de conscience (par évanouissement ou ivresse), le toucher des parties intimes sans barrière, et, selon certaines écoles, le toucher d'une femme avec désir."},
            "fa": {"very_short": "مبطل", "short": "نواقض وضو، طهارت را باطل کرده و اعاده آن را واجب می‌کند", "full": "نواقض وضو عبارتند از: آنچه از دو مجرا خارج شود (ادرار، غائط، باد)، خواب عمیق، زوال عقل (به‌دلیل غش یا مستی)، لمس عورت بدون حائل، و به‌گفته برخی مذاهب، لمس زن با شهوت."},
            "ms": {"very_short": "Membatalkan", "short": "Pembatal wudu membatalkan kesucian dan mewajibkan ia diulang", "full": "Pembatal wudu termasuk: apa yang keluar dari dua saluran (kencing, najis, angin), tidur yang nyenyak, hilang akal (kerana pengsan atau mabuk), menyentuh kemaluan tanpa penghalang, dan menurut sesetengah mazhab, menyentuh wanita dengan syahwat."},
            "ur": {"very_short": "مبطل", "short": "نواقض وضو طہارت کو باطل کرتے ہیں اور اسے دہرانے کا حکم دیتے ہیں", "full": "نواقض وضو یہ ہیں: پیشاب، پاخانہ، ریح، نیند غلیظ، زوال عقل (بے ہوشی یا نشہ کی وجہ سے)، بغیر حائل کے شرمگاہ کا چھونا، اور بعض مذاہب کے مطابق شہوت کے ساتھ عورت کا چھونا۔"},
        },
    },
    {
        "id": 5, "topic": "muamalat",
        "title": {"ar": "الربا", "en": "Usury / Interest (Riba)", "fr": "L'usure / intérêt (riba)", "fa": "ربا", "ms": "Riba", "ur": "سود"},
        "keywords": {
            "ar": ["ربا", "حرام", "قرض", "فائدة", "بنوك", "معاملة"],
            "en": ["riba", "usury", "interest", "loan", "banks"],
            "fr": ["riba", "usure", "intérêt", "prêt", "banques"],
            "fa": ["ربا", "حرام", "قرض", "بهره", "بانک‌ها", "معامله"],
            "ms": ["riba", "haram", "pinjaman", "faedah", "bank", "urusan"],
            "ur": ["سود", "حرام", "قرض", "بیاج", "بینک", "معاملہ"],
        },
        "rulings": {
            "ar": {"very_short": "حرام", "short": "الربا من كبائر الذنوب ومحرم قطعاً", "full": "الربا محرم بنص القرآن والسنة، وهو كل زيادة مشروطة في القرض أو المعاملة، سواء كانت نقدية أو عينية. الربا من السبع الموبقات."},
            "en": {"very_short": "Forbidden", "short": "Riba is among the major sins and is categorically forbidden", "full": "Riba (usury/interest) is forbidden by explicit text of the Qur'an and Sunnah; it is any stipulated increase in a loan or transaction, whether monetary or in kind. It is counted among the seven grave destructive sins."},
            "fr": {"very_short": "Interdit", "short": "Le riba est un péché majeur, formellement interdit", "full": "Le riba (usure/intérêt) est interdit par un texte explicite du Coran et de la Sunna ; c'est tout surplus stipulé dans un prêt ou une transaction, monétaire ou en nature. Il est compté parmi les sept péchés destructeurs majeurs."},
            "fa": {"very_short": "حرام", "short": "ربا از گناهان کبیره و قطعاً حرام است", "full": "ربا به‌نص قرآن و سنت حرام است؛ هر افزایش مشروط در قرض یا معامله، چه نقدی باشد چه جنسی. ربا از هفت گناه مهلکه محسوب می‌شود."},
            "ms": {"very_short": "Haram", "short": "Riba adalah dosa besar dan haram secara mutlak", "full": "Riba diharamkan melalui nas al-Quran dan Sunnah; iaitu sebarang tambahan yang disyaratkan dalam pinjaman atau urusan, sama ada wang atau barang. Riba termasuk dalam tujuh dosa besar yang membinasakan."},
            "ur": {"very_short": "حرام", "short": "سود کبیرہ گناہوں میں سے ہے اور قطعاً حرام ہے", "full": "سود قرآن و سنت کے نص سے حرام ہے؛ یہ قرض یا معاملے میں شرط کردہ کوئی بھی زیادتی ہے، خواہ نقد ہو یا چیز۔ سود سات مہلک گناہوں میں سے ہے۔"},
        },
    },
    {
        "id": 6, "topic": "ibadat",
        "title": {"ar": "صلاة المسافر", "en": "The Traveler's Prayer", "fr": "La prière du voyageur", "fa": "نماز مسافر", "ms": "Solat Musafir", "ur": "مسافر کی نماز"},
        "keywords": {
            "ar": ["سفر", "مسافر", "صلاة", "قصر", "جمع", "تخفيف", "رخصة"],
            "en": ["travel", "traveler", "prayer", "shorten", "combine", "concession"],
            "fr": ["voyage", "voyageur", "prière", "raccourcir", "regrouper", "allègement"],
            "fa": ["سفر", "مسافر", "نماز", "قصر", "جمع", "تخفیف", "رخصت"],
            "ms": ["perjalanan", "musafir", "solat", "qasar", "gabung", "rukhsah"],
            "ur": ["سفر", "مسافر", "نماز", "قصر", "جمع", "تخفیف", "رخصت"],
        },
        "rulings": {
            "ar": {"very_short": "جائز", "short": "يجوز للمسافر قصر الصلاة وجمعها", "full": "يجوز للمسافر قصر الصلاة الرباعية (الظهر، العصر، العشاء) إلى ركعتين، وجمع الصلاة (الظهر مع العصر، والمغرب مع العشاء). هذه رخصة من الله للتخفيف على المسافرين."},
            "en": {"very_short": "Permissible", "short": "A traveler may shorten and combine prayers", "full": "A traveler is permitted to shorten the four-unit prayers (Dhuhr, Asr, Isha) to two units, and to combine prayers (Dhuhr with Asr, and Maghrib with Isha). This is a concession from God to ease the burden on travelers."},
            "fr": {"very_short": "Permis", "short": "Le voyageur peut raccourcir et regrouper les prières", "full": "Il est permis au voyageur de raccourcir les prières à quatre unités (Dhuhr, Asr, Isha) à deux unités, et de regrouper les prières (Dhuhr avec Asr, et Maghrib avec Isha). C'est un allègement accordé par Dieu pour faciliter la tâche aux voyageurs."},
            "fa": {"very_short": "جایز", "short": "مسافر می‌تواند نماز را قصر کرده و جمع کند", "full": "به مسافر اجازه داده شده است که نمازهای چهار رکعتی (ظهر، عصر، عشاء) را به دو رکعت قصر کند، و نمازها را جمع کند (ظهر با عصر، و مغرب با عشاء). این رخصتی از سوی خداوند برای تخفیف بر مسافران است."},
            "ms": {"very_short": "Harus", "short": "Musafir boleh qasar dan menggabungkan solat", "full": "Musafir dibenarkan untuk menqasarkan solat empat rakaat (Zohor, Asar, Isyak) kepada dua rakaat, dan menggabungkan solat (Zohor dengan Asar, dan Maghrib dengan Isyak). Ini adalah keringanan daripada Allah untuk meringankan beban musafir."},
            "ur": {"very_short": "جائز", "short": "مسافر نماز قصر اور جمع کر سکتا ہے", "full": "مسافر کو اجازت ہے کہ وہ چار رکعت والی نمازوں (ظہر، عصر، عشاء) کو دو رکعت قصر کرے، اور نمازوں کو جمع کرے (ظہر کے ساتھ عصر، اور مغرب کے ساتھ عشاء)۔ یہ اللہ کی طرف سے مسافروں پر تخفیف ہے۔"},
        },
    },
    # ========== NEW ISSUE: Divorce of a Menstruating Woman ==========
    {
        "id": 7,
        "topic": "family",
        "title": {
            "ar": "طلاق الحائض",
            "en": "Divorce of a Menstruating Woman",
            "fr": "Le divorce de la femme en période de menstrues",
            "fa": "طلاق زن حائض",
            "ms": "Penceraian Wanita Haid",
            "ur": "حائضہ کا طلاق"
        },
        "keywords": {
            "ar": ["طلاق", "حائض", "حيض", "الطلاق", "الحيض", "العدة"],
            "en": ["divorce", "menstruating", "menstruation", "talaq", "iddah"],
            "fr": ["divorce", "menstrues", "menstruation", "talaq", "idda"],
            "fa": ["طلاق", "حائض", "حیض", "عدہ"],
            "ms": ["cerai", "haid", "menstruasi", "talaq", "iddah"],
            "ur": ["طلاق", "حائض", "حیض", "عدہ"],
        },
        "rulings": {
            "ar": {
                "very_short": "بدعي",
                "short": "طلاق الحائض بدعي ومحرم، ويقع مع الإثم",
                "full": "طلاق الحائض هو طلاق المرأة أثناء حيضها، وهو من الطلاق البدعي المحرم عند جمهور الفقهاء، ويقع الطلاق مع الإثم، ويجب على المطلق أن يراجعها إن كان في العدة، أو ينتظر حتى تطهر ثم يطلقها في طهر لم يمسها فيه."
            },
            "en": {
                "very_short": "Bid'ah (Innovative)",
                "short": "Divorcing a menstruating woman is a prohibited innovation, but the divorce is valid",
                "full": "Divorcing a menstruating woman is considered a prohibited innovation (bid'ah) according to the majority of jurists. The divorce is still valid but sinful. The husband is required to either take her back during the waiting period (iddah) or wait until she becomes pure and then divorce her in a state of purity without having intercourse."
            },
            "fr": {
                "very_short": "Bid'a (innovateur)",
                "short": "Divorcer une femme en période de menstrues est une innovation interdite, mais le divorce est valable",
                "full": "Divorcer une femme en période de menstrues est considéré comme une innovation interdite (bid'a) selon la majorité des juristes. Le divorce est néanmoins valable mais le mari commet un péché. Il doit soit la reprendre durant sa période d'attente (idda), soit attendre qu'elle soit pure pour la divorcer dans un état de pureté sans avoir eu de rapports."
            },
            "fa": {
                "very_short": "بدعت",
                "short": "طلاق زن حائض بدعت و حرام است، ولی طلاق واقع می‌شود",
                "full": "طلاق زن در حال حیض، بدعت و حرام است به‌اتفاق جمهور فقها، ولی طلاق واقع می‌شود و گناه بر طلاق‌دهنده است؛ باید در عدّه رجوع کند یا منتظر بماند تا پاک شود و در طهر بدون جماع طلاق دهد."
            },
            "ms": {
                "very_short": "Bid'ah",
                "short": "Menceraikan wanita haid adalah bid'ah dan haram, tetapi penceraian sah",
                "full": "Menceraikan wanita semasa haid adalah bid'ah dan haram menurut majoriti ulama, tetapi penceraian tetap sah. Suami wajib merujuknya jika masih dalam iddah, atau menunggu sehingga suci dan menceraikannya dalam keadaan suci tanpa persetubuhan."
            },
            "ur": {
                "very_short": "بدعت",
                "short": "حائضہ کو طلاق دینا بدعت اور حرام ہے، مگر طلاق واقع ہو جاتی ہے",
                "full": "حائضہ عورت کو طلاق دینا جمہور فقہاء کے نزدیک بدعت اور حرام ہے، تاہم طلاق واقع ہو جاتی ہے اور طلاق دینے والا گنہگار ہے۔ اسے چاہیے کہ عدت میں رجوع کرے، یا پاک ہونے کا انتظار کرے اور پاکی کی حالت میں جماع کیے بغیر طلاق دے۔"
            }
        },
        "rulings_by_madhab": {
            "maliki": {
                "ar": {"very_short": "بدعي", "short": "طلاق الحائض بدعي عند المالكية", "full": "طلاق الحائض بدعي عند المالكية، ولكنه يقع مع الإثم، ويجب على الزوج أن يراجعها إذا لم تنقض عدتها."},
                "en": {"very_short": "Bid'ah", "short": "Innovative according to Malikis, but valid", "full": "Divorcing a menstruating woman is considered an innovation according to Malikis, but it is still valid. The husband must take her back if her waiting period has not ended."},
                "fr": {"very_short": "Bid'a", "short": "Innovateur selon les malikites, mais valable", "full": "Divorcer une femme en période de menstrues est considéré comme une innovation selon les malikites, mais le divorce est valable. Le mari doit la reprendre si sa période d'attente n'est pas terminée."},
                "fa": {"very_short": "بدعت", "short": "بدعت نزد مالکیان، ولی واقع می‌شود", "full": "طلاق زن حائض بدعت نزد مالکیان است، ولی واقع می‌شود و گناه دارد؛ شوهر باید رجوع کند اگر عدّه تمام نشده است."},
                "ms": {"very_short": "Bid'ah", "short": "Bid'ah menurut Maliki, tetapi sah", "full": "Menceraikan wanita haid adalah bid'ah menurut Maliki, tetapi penceraian tetap sah. Suami wajib merujuknya jika iddahnya belum tamat."},
                "ur": {"very_short": "بدعت", "short": "مالکیہ کے نزدیک بدعت ہے، مگر واقع ہوتی ہے", "full": "مالکیہ کے نزدیک حائضہ کو طلاق دینا بدعت ہے، تاہم طلاق واقع ہو جاتی ہے اور گنہگار ہو گا۔ شوہر کو چاہیے کہ اگر عدت ختم نہ ہوئی ہو تو رجوع کرے۔"},
            },
            "shafii": {
                "ar": {"very_short": "محرم", "short": "طلاق الحائض محرم عند الشافعية، ويقع مع الإثم", "full": "طلاق الحائض محرم عند الشافعية، وهو من الطلاق البدعي، ويقع الطلاق مع الإثم، ويجب أن يطلقها في طهر لم يمسها فيه."},
                "en": {"very_short": "Forbidden", "short": "Forbidden according to Shafi'is, but valid", "full": "Divorcing a menstruating woman is forbidden according to Shafi'is, and it is considered an innovative divorce. The divorce is still valid but sinful. He must divorce her in a state of purity without having intercourse."},
                "fr": {"very_short": "Interdit", "short": "Interdit selon les chaféites, mais valable", "full": "Divorcer une femme en période de menstrues est interdit selon les chaféites, et c'est un divorce innovateur. Le divorce est valable mais le mari commet un péché. Il doit la divorcer dans un état de pureté sans avoir eu de rapports."},
                "fa": {"very_short": "حرام", "short": "حرام نزد شافعیان، ولی واقع می‌شود", "full": "طلاق زن حائض حرام نزد شافعیان است و بدعت محسوب می‌شود؛ طلاق واقع می‌شود و گناه دارد؛ باید در طهر بدون جماع طلاق دهد."},
                "ms": {"very_short": "Haram", "short": "Haram menurut Syafii, tetapi sah", "full": "Menceraikan wanita haid adalah haram menurut Syafii, dan ia dianggap penceraian bid'ah. Penceraian tetap sah tetapi berdosa; dia mesti menceraikannya dalam keadaan suci tanpa persetubuhan."},
                "ur": {"very_short": "حرام", "short": "شافعیہ کے نزدیک حرام ہے، مگر واقع ہوتی ہے", "full": "شافعیہ کے نزدیک حائضہ کو طلاق دینا حرام ہے اور بدعت ہے؛ طلاق واقع ہو جاتی ہے مگر گنہگار ہو گا؛ اسے چاہیے کہ پاکی کی حالت میں جماع کیے بغیر طلاق دے۔"},
            },
            "hanafi": {
                "ar": {"very_short": "بدعي", "short": "طلاق الحائض بدعي عند الحنفية، ويقع مع الإثم", "full": "طلاق الحائض بدعي عند الحنفية، وهو طلاق غير مشروع، لكنه يقع مع الإثم، ويجب على الزوج أن يراجعها إذا كانت في العدة."},
                "en": {"very_short": "Bid'ah", "short": "Innovative according to Hanafis, but valid", "full": "Divorcing a menstruating woman is considered an innovation according to Hanafis, and it is not legally sanctioned, but it is still valid. The husband must take her back if she is still in her waiting period."},
                "fr": {"very_short": "Bid'a", "short": "Innovateur selon les hanafites, mais valable", "full": "Divorcer une femme en période de menstrues est considéré comme une innovation selon les hanafites, et ce n'est pas légalement sanctionné, mais le divorce est valable. Le mari doit la reprendre si elle est encore dans sa période d'attente."},
                "fa": {"very_short": "بدعت", "short": "بدعت نزد حنفیان، ولی واقع می‌شود", "full": "طلاق زن حائض بدعت نزد حنفیان است و شرعاً جایز نیست، ولی واقع می‌شود و گناه دارد؛ شوهر باید رجوع کند اگر در عدّه باشد."},
                "ms": {"very_short": "Bid'ah", "short": "Bid'ah menurut Hanafi, tetapi sah", "full": "Menceraikan wanita haid adalah bid'ah menurut Hanafi, dan ia tidak dibenarkan secara syarak, tetapi penceraian tetap sah. Suami wajib merujuknya jika masih dalam iddah."},
                "ur": {"very_short": "بدعت", "short": "حنفیہ کے نزدیک بدعت ہے، مگر واقع ہوتی ہے", "full": "حنفیہ کے نزدیک حائضہ کو طلاق دینا بدعت ہے اور شرعاً جائز نہیں، تاہم طلاق واقع ہو جاتی ہے اور گنہگار ہو گا؛ شوہر کو چاہیے کہ اگر عدت میں ہو تو رجوع کرے۔"},
            },
            "hanbali": {
                "ar": {"very_short": "بدعي", "short": "طلاق الحائض بدعي عند الحنابلة، ويقع مع الإثم", "full": "طلاق الحائض بدعي عند الحنابلة، وهو طلاق غير جائز شرعاً، لكنه يقع مع الإثم، ويجب على الزوج أن يراجعها ويطلقها في طهر طاهر."},
                "en": {"very_short": "Bid'ah", "short": "Innovative according to Hanbalis, but valid", "full": "Divorcing a menstruating woman is considered an innovation according to Hanbalis, and it is not legally permissible, but it is still valid. The husband must take her back and divorce her in a pure state."},
                "fr": {"very_short": "Bid'a", "short": "Innovateur selon les hanbalites, mais valable", "full": "Divorcer une femme en période de menstrues est considéré comme une innovation selon les hanbalites, et ce n'est pas légalement permis, mais le divorce est valable. Le mari doit la reprendre et la divorcer dans un état de pureté."},
                "fa": {"very_short": "بدعت", "short": "بدعت نزد حنبلیان، ولی واقع می‌شود", "full": "طلاق زن حائض بدعت نزد حنبلیان است و شرعاً جایز نیست، ولی واقع می‌شود و گناه دارد؛ شوهر باید رجوع کند و در طهر طاهر طلاق دهد."},
                "ms": {"very_short": "Bid'ah", "short": "Bid'ah menurut Hanbali, tetapi sah", "full": "Menceraikan wanita haid adalah bid'ah menurut Hanbali, dan ia tidak dibenarkan secara syarak, tetapi penceraian tetap sah. Suami wajib merujuknya dan menceraikannya dalam keadaan suci."},
                "ur": {"very_short": "بدعت", "short": "حنبلیہ کے نزدیک بدعت ہے، مگر واقع ہوتی ہے", "full": "حنبلیہ کے نزدیک حائضہ کو طلاق دینا بدعت ہے اور شرعاً جائز نہیں، تاہم طلاق واقع ہو جاتی ہے اور گنہگار ہو گا؛ شوہر کو چاہیے کہ رجوع کرے اور پاکی کی حالت میں طلاق دے۔"},
            },
            "zahiri": {
                "ar": {"very_short": "محرم", "short": "طلاق الحائض محرم عند الظاهرية، ويقع مع الإثم", "full": "طلاق الحائض محرم عند الظاهرية، استناداً إلى ظاهر النهي عن ذلك، ويقع الطلاق مع الإثم."},
                "en": {"very_short": "Forbidden", "short": "Forbidden according to Zahiris, but valid", "full": "Divorcing a menstruating woman is forbidden according to Zahiris, based on the literal prohibition, and the divorce is valid but sinful."},
                "fr": {"very_short": "Interdit", "short": "Interdit selon les zahirites, mais valable", "full": "Divorcer une femme en période de menstrues est interdit selon les zahirites, sur la base de l'interdiction littérale, et le divorce est valable mais le mari commet un péché."},
                "fa": {"very_short": "حرام", "short": "حرام نزد ظاهریان، ولی واقع می‌شود", "full": "طلاق زن حائض حرام نزد ظاهریان است، بر اساس ظاهر نهی، و طلاق واقع می‌شود و گناه دارد."},
                "ms": {"very_short": "Haram", "short": "Haram menurut Zahiri, tetapi sah", "full": "Menceraikan wanita haid adalah haram menurut Zahiri, berdasarkan larangan zahir, dan penceraian tetap sah tetapi berdosa."},
                "ur": {"very_short": "حرام", "short": "ظاہریہ کے نزدیک حرام ہے، مگر واقع ہوتی ہے", "full": "ظاہریہ کے نزدیک حائضہ کو طلاق دینا حرام ہے، کیونکہ ظاہر نہی ہے، اور طلاق واقع ہو جاتی ہے مگر گنہگار ہو گا۔"},
            },
            "jafari": {
                "ar": {"very_short": "جائز", "short": "طلاق الحائض جائز عند الجعفرية في زمن الغيبة", "full": "طلاق الحائض جائز عند الجعفرية، ولا يعتبر بدعة، لكنه مكروه ما لم يكن هناك ضرورة، وتعتبر العدة من يوم الطلاق."},
                "en": {"very_short": "Permissible", "short": "Permissible according to Ja'faris during the Occultation", "full": "Divorcing a menstruating woman is permissible according to Ja'faris, and it is not considered an innovation, though it is disliked unless there is a necessity. The waiting period is counted from the day of divorce."},
                "fr": {"very_short": "Permis", "short": "Permis selon les jaafarites durant l'Occultation", "full": "Divorcer une femme en période de menstrues est permis selon les jaafarites, et ce n'est pas considéré comme une innovation, bien que ce soit blâmable à moins qu'il n'y ait une nécessité. La période d'attente est comptée à partir du jour du divorce."},
                "fa": {"very_short": "جایز", "short": "جایز نزد جعفریان در زمان غیبت", "full": "طلاق زن حائض نزد جعفریان جایز است و بدعت محسوب نمی‌شود، ولی مکروه است مگر ضرورت داشته باشد؛ عدّه از روز طلاق محاسبه می‌شود."},
                "ms": {"very_short": "Harus", "short": "Harus menurut Jaafari semasa ghaib", "full": "Menceraikan wanita haid adalah harus menurut Jaafari, dan tidak dianggap bid'ah, tetapi makruh kecuali ada keperluan. Iddah dikira dari hari penceraian."},
                "ur": {"very_short": "جائز", "short": "جعفریہ کے نزدیک غیبت کے زمانے میں جائز ہے", "full": "جعفریہ کے نزدیک حائضہ کو طلاق دینا جائز ہے اور بدعت نہیں، البتہ مکروہ ہے جب تک ضرورت نہ ہو۔ عدت طلاق کے دن سے شمار ہوگی۔"},
            },
            "zaidi": {
                "ar": {"very_short": "بدعي", "short": "طلاق الحائض بدعي عند الزيدية، ويقع مع الإثم", "full": "طلاق الحائض بدعي عند الزيدية، ويقترب من رأي أهل السنة في حرمة ذلك، ويقع الطلاق مع الإثم."},
                "en": {"very_short": "Bid'ah", "short": "Innovative according to Zaidis, but valid", "full": "Divorcing a menstruating woman is considered an innovation according to Zaidis, and it is close to the Sunni view on its prohibition. The divorce is valid but sinful."},
                "fr": {"very_short": "Bid'a", "short": "Innovateur selon les zaydites, mais valable", "full": "Divorcer une femme en période de menstrues est considéré comme une innovation selon les zaydites, et cela est proche de l'avis sunnite sur son interdiction. Le divorce est valable mais le mari commet un péché."},
                "fa": {"very_short": "بدعت", "short": "بدعت نزد زیدیان، ولی واقع می‌شود", "full": "طلاق زن حائض بدعت نزد زیدیان است و به رأی اهل سنت در حرمت آن نزدیک است؛ طلاق واقع می‌شود و گناه دارد."},
                "ms": {"very_short": "Bid'ah", "short": "Bid'ah menurut Zaidi, tetapi sah", "full": "Menceraikan wanita haid adalah bid'ah menurut Zaidi, dan ia hampir dengan pandangan Sunni tentang pengharamannya. Penceraian tetap sah tetapi berdosa."},
                "ur": {"very_short": "بدعت", "short": "زیدیہ کے نزدیک بدعت ہے، مگر واقع ہوتی ہے", "full": "زیدیہ کے نزدیک حائضہ کو طلاق دینا بدعت ہے اور اہل سنت کی رائے کے قریب ہے کہ یہ حرام ہے؛ طلاق واقع ہو جاتی ہے مگر گنہگار ہو گا۔"},
            },
            "ibadi": {
                "ar": {"very_short": "بدعي", "short": "طلاق الحائض بدعي عند الإباضية، ويقع مع الإثم", "full": "طلاق الحائض بدعي عند الإباضية، ولا يجوز شرعاً، لكنه يقع مع الإثم، ويجب على الزوج أن يراجعها إن كانت في العدة."},
                "en": {"very_short": "Bid'ah", "short": "Innovative according to Ibadis, but valid", "full": "Divorcing a menstruating woman is considered an innovation according to Ibadis, and it is not legally permissible, but it is still valid. The husband must take her back if she is still in her waiting period."},
                "fr": {"very_short": "Bid'a", "short": "Innovateur selon les ibadites, mais valable", "full": "Divorcer une femme en période de menstrues est considéré comme une innovation selon les ibadites, et ce n'est pas légalement permis, mais le divorce est valable. Le mari doit la reprendre si elle est encore dans sa période d'attente."},
                "fa": {"very_short": "بدعت", "short": "بدعت نزد اباضیان، ولی واقع می‌شود", "full": "طلاق زن حائض بدعت نزد اباضیان است و شرعاً جایز نیست، ولی واقع می‌شود و گناه دارد؛ شوهر باید رجوع کند اگر در عدّه باشد."},
                "ms": {"very_short": "Bid'ah", "short": "Bid'ah menurut Ibadi, tetapi sah", "full": "Menceraikan wanita haid adalah bid'ah menurut Ibadi, dan tidak dibenarkan secara syarak, tetapi penceraian tetap sah. Suami wajib merujuknya jika masih dalam iddah."},
                "ur": {"very_short": "بدعت", "short": "اباضیہ کے نزدیک بدعت ہے، مگر واقع ہوتی ہے", "full": "اباضیہ کے نزدیک حائضہ کو طلاق دینا بدعت ہے اور شرعاً جائز نہیں، تاہم طلاق واقع ہو جاتی ہے اور گنہگار ہو گا؛ شوہر کو چاہیے کہ اگر عدت میں ہو تو رجوع کرے۔"},
            }
        }
    }
]

# --- Glossary ---------------------------------------------------------------

GLOSSARY = [
    {"term": {"ar": "الفرض / فرض العين", "en": "Fard / Fard Ayn (Individual Obligation)", "fr": "Le fard / fard ayn (Obligation individuelle)", "fa": "فرض / فرض عین", "ms": "Fardu / Fardu Ain (Kewajipan Individu)", "ur": "فرض / فرض عین"},
     "definition": {"ar": "ما طلب الشارع فعله طلباً جازماً من كل مكلف بعينه، يُثاب فاعله ويُعاقب تاركه.",
                    "en": "What the Lawgiver has decisively commanded every legally accountable individual to perform; one who does it is rewarded, and one who abandons it is sinful.",
                    "fr": "Ce que le Législateur a ordonné de façon décisive à tout individu responsable d'accomplir ; celui qui l'accomplit est récompensé, et celui qui l'abandonne est fautif.",
                    "fa": "آنچه شارع به‌طور قطعی بر هر مکلفی واجب کرده است؛ انجام‌دهنده پاداش می‌گیرد و ترک‌کننده گناهکار است.",
                    "ms": "Apa yang Pembuat Syariat telah perintahkan secara tegas kepada setiap individu yang bertanggungjawab untuk melaksanakannya; yang melaksanakannya diberi pahala, dan yang meninggalkannya berdosa.",
                    "ur": "وہ چیز جسے شارع نے ہر مکلف پر قطعی طور پر واجب کیا ہے؛ اسے کرنے والا ثواب پاتا ہے اور چھوڑنے والا گنہگار ہے۔"}},
    {"term": {"ar": "فرض الكفاية", "en": "Fard Kifayah (Communal Obligation)", "fr": "Fard kifaya (Obligation collective)", "fa": "فرض کفایه", "ms": "Fardu Kifayah (Kewajipan Komuniti)", "ur": "فرض کفایہ"},
     "definition": {"ar": "ما طلب الشارع فعله من عموم المكلفين، يسقط الإثم عن الجميع بفعل البعض، ويأثم الكل إن تركوه جميعاً.",
                    "en": "What the Lawgiver has requested from the community at large; if some perform it, the obligation is lifted from all, but if all abandon it, all are sinful.",
                    "fr": "Ce que le Législateur a demandé à la communauté dans son ensemble ; si certains l'accomplissent, l'obligation est levée pour tous, mais si tous l'abandonnent, tous sont fautifs.",
                    "fa": "آنچه شارع از عموم مکلفان خواسته است؛ اگر برخی انجام دهند، از دیگران ساقط می‌شود و اگر همه ترک کنند، همه گناهکارند.",
                    "ms": "Apa yang Pembuat Syariat minta daripada komuniti secara am; jika sebahagian melaksanakannya, kewajipan gugur daripada semua, tetapi jika semua meninggalkannya, semua berdosa.",
                    "ur": "وہ چیز جو شارع نے تمام مکلفین سے مانگی ہے؛ اگر کچھ لوگ کریں تو سب سے ساقط ہو جاتی ہے، اور اگر سب چھوڑ دیں تو سب گنہگار ہیں۔"}},
    {"term": {"ar": "الواجب", "en": "Al-Wajib (The Obligatory)", "fr": "Al-wajib (L'obligatoire)", "fa": "واجب", "ms": "Wajib", "ur": "واجب"},
     "definition": {"ar": "عند جمهور الفقهاء مرادف للفرض؛ وعند الحنفية: ما ثبت بدليل ظني دون قطعي.",
                    "en": "For the majority of jurists it is synonymous with fard; for the Hanafis, it is what is established by a probable, non-decisive proof.",
                    "fr": "Pour la majorité des juristes, il est synonyme de fard ; pour les hanafites, c'est ce qui est établi par une preuve probable, non décisive.",
                    "fa": "نزد جمهور فقها مترادف با فرض است؛ و نزد حنفیان چیزی است که با دلیل ظنی ثابت می‌شود نه قطعی.",
                    "ms": "Bagi majoriti ulama ia sinonim dengan fardu; bagi Hanafi, ia adalah apa yang ditetapkan oleh dalil yang mungkin (zanni), bukan muktamad.",
                    "ur": "جمہور فقہاء کے نزدیک فرض کا مترادف ہے؛ اور احناف کے نزدیک وہ چیز جو دلیل ظنی سے ثابت ہو، قطعی نہیں۔"}},
    {"term": {"ar": "السنة المؤكدة", "en": "Emphasized Sunnah", "fr": "Sunna fortement recommandée", "fa": "سنت مؤکد", "ms": "Sunnah Muakkadah", "ur": "سنت مؤکدہ"},
     "definition": {"ar": "ما واظب النبي ﷺ على فعله غالباً، ويُكره تركه بلا عذر عند أكثر الفقهاء.",
                    "en": "What the Prophet ﷺ regularly performed; abandoning it without excuse is disliked according to most jurists.",
                    "fr": "Ce que le Prophète ﷺ accomplissait régulièrement ; l'abandonner sans excuse est blâmable selon la plupart des juristes.",
                    "fa": "آنچه پیامبر ﷺ غالباً بر آن مداومت داشت؛ ترک آن بدون عذر نزد اکثر فقها مکروه است.",
                    "ms": "Apa yang Nabi ﷺ kerap melakukannya; meninggalkannya tanpa uzur adalah makruh menurut majoriti ulama.",
                    "ur": "وہ چیز جس پر نبی ﷺ اکثر مداومت فرماتے تھے؛ اسے بغیر عذر چھوڑنا اکثر فقہاء کے نزدیک مکروہ ہے۔"}},
    {"term": {"ar": "المستحب (المندوب)", "en": "Mustahabb (Recommended)", "fr": "Moustahabb (Recommandé)", "fa": "مستحب (مندوب)", "ms": "Mustahab (Sunat)", "ur": "مستحب (مندوب)"},
     "definition": {"ar": "ما رغّب الشارع في فعله دون إلزام، يُثاب فاعله ولا يُعاقب تاركه. والمندوب اسم آخر له عند أكثر الفقهاء.",
                    "en": "What the Lawgiver encouraged without obligation; one who does it is rewarded, and one who abandons it is not sinful.",
                    "fr": "Ce que le Législateur a encouragé sans l'imposer ; celui qui l'accomplit est récompensé, et celui qui l'abandonne n'est pas fautif.",
                    "fa": "آنچه شارع به انجام آن ترغیب کرده بدون الزام؛ انجام‌دهنده پاداش می‌گیرد و ترک‌کننده گناهکار نیست. مندوب نام دیگر آن نزد اکثر فقهاست.",
                    "ms": "Apa yang Pembuat Syariat galakkan tanpa kewajipan; yang melakukannya diberi pahala, dan yang meninggalkannya tidak berdosa. Mandub adalah nama lain bagi kebanyakan ulama.",
                    "ur": "وہ چیز جس کی طرف شارع نے بغیر الزام کے رغبت دلائی ہے؛ کرنے والا ثواب پاتا ہے اور چھوڑنے والا گنہگار نہیں۔ مندوب اس کا دوسرا نام ہے اکثر فقہاء کے نزدیک۔"}},
    {"term": {"ar": "المكروه", "en": "Al-Makruh (Disliked)", "fr": "Al-makrouh (Blâmable)", "fa": "مکروه", "ms": "Makruh", "ur": "مکروہ"},
     "definition": {"ar": "ما طلب الشارع تركه طلباً غير جازم، يُثاب تاركه ولا يُعاقب فاعله.",
                    "en": "What the Lawgiver requested to be avoided in a non-decisive manner; one who avoids it is rewarded, and one who does it is not sinful.",
                    "fr": "Ce que le Législateur a demandé d'éviter de façon non décisive ; celui qui l'évite est récompensé, et celui qui l'accomplit n'est pas fautif.",
                    "fa": "آنچه شارع به ترک آن به‌طور غیرجازم دستور داده است؛ ترک‌کننده پاداش می‌گیرد و انجام‌دهنده گناهکار نیست.",
                    "ms": "Apa yang Pembuat Syariat minta dielakkan secara tidak tegas; yang mengelaknya diberi pahala, dan yang melakukannya tidak berdosa.",
                    "ur": "وہ چیز جسے شارع نے غیر جازم طور پر ترک کرنے کا کہا ہے؛ ترک کرنے والا ثواب پاتا ہے اور کرنے والا گنہگار نہیں۔"}},
    {"term": {"ar": "الحرام", "en": "Al-Haram (Forbidden)", "fr": "Al-haram (Interdit)", "fa": "حرام", "ms": "Haram", "ur": "حرام"},
     "definition": {"ar": "ما طلب الشارع تركه طلباً جازماً بنص قطعي، يُعاقب فاعله ويُثاب تاركه.",
                    "en": "What the Lawgiver has decisively forbidden by a definitive text; one who does it is sinful, and one who avoids it is rewarded.",
                    "fr": "Ce que le Législateur a interdit de façon décisive par un texte définitif ; celui qui le fait est fautif, et celui qui l'évite est récompensé.",
                    "fa": "آنچه شارع به‌طور قطعی به‌واسطه نص قطعی حرام کرده است؛ انجام‌دهنده گناهکار است و ترک‌کننده پاداش می‌گیرد.",
                    "ms": "Apa yang Pembuat Syariat haramkan secara tegas melalui nas yang muktamad; yang melakukannya berdosa, dan yang mengelaknya diberi pahala.",
                    "ur": "وہ چیز جسے شارع نے نص قطعی کے ذریعے قطعی طور پر حرام کیا ہے؛ کرنے والا گنہگار ہے اور چھوڑنے والا ثواب پاتا ہے۔"}},
]

# --- Imams -------------------------------------------------------------------

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
    {"name": {"ar": "الإمام محمد بن إدريس الشافعي", "en": "Imam Muhammad ibn Idris al-Shafi'i", "fr": "L'imam Muhammad ibn Idris al-Chafi'i", "fa": "امام محمد بن ادریس شافعی", "ms": "Imam Muhammad bin Idris al-Syafie", "ur": "امام محمد بن ادریس شافعی"},
     "school": MADHHAB_NAMES["shafii"], "lifespan": "150 - 204 AH",
     "birthplace": {"ar": "غزة", "en": "Gaza", "fr": "Gaza", "fa": "غزه", "ms": "Gaza", "ur": "غزہ"},
     "founding_place": {"ar": "بغداد ثم مصر (المذهب الجديد)", "en": "Baghdad, then Egypt (the new doctrine)", "fr": "Bagdad, puis l'Égypte (la nouvelle doctrine)", "fa": "بغداد سپس مصر (مذهب جدید)", "ms": "Baghdad, kemudian Mesir (mazhab baru)", "ur": "بغداد پھر مصر (نیا مذہب)"},
     "scholars": {"ar": "المزني، البويطي، النووي، ابن حجر الهيتمي، الرافعي",
                  "en": "al-Muzani, al-Buwayti, al-Nawawi, Ibn Hajar al-Haytami, al-Rafi'i",
                  "fr": "al-Muzani, al-Buwayti, al-Nawawi, Ibn Hajar al-Haytami, al-Rafi'i",
                  "fa": "مزنی، بویطی، نووی، ابن حجر هیتمی، رافعی",
                  "ms": "al-Muzani, al-Buwayti, al-Nawawi, Ibn Hajar al-Haytami, al-Rafi'i",
                  "ur": "مزنی، بویطی، نووی، ابن حجر ہیتمی، رافعی"}},
    {"name": {"ar": "الإمام أحمد بن حنبل الشيباني", "en": "Imam Ahmad ibn Hanbal al-Shaybani", "fr": "L'imam Ahmad ibn Hanbal al-Chaybani", "fa": "امام احمد بن حنبل شیبانی", "ms": "Imam Ahmad bin Hanbal al-Syaibani", "ur": "امام احمد بن حنبل شیبانی"},
     "school": MADHHAB_NAMES["hanbali"], "lifespan": "164 - 241 AH",
     "birthplace": {"ar": "بغداد", "en": "Baghdad", "fr": "Bagdad", "fa": "بغداد", "ms": "Baghdad", "ur": "بغداد"},
     "founding_place": {"ar": "بغداد", "en": "Baghdad", "fr": "Bagdad", "fa": "بغداد", "ms": "Baghdad", "ur": "بغداد"},
     "scholars": {"ar": "أبو بكر الخلال، ابن قدامة، ابن تيمية، ابن القيم، محمد بن عبد الوهاب",
                  "en": "Abu Bakr al-Khallal, Ibn Qudamah, Ibn Taymiyyah, Ibn al-Qayyim, Muhammad ibn Abd al-Wahhab",
                  "fr": "Abu Bakr al-Khallal, Ibn Qudamah, Ibn Taymiyya, Ibn al-Qayyim, Muhammad ibn Abd al-Wahhab",
                  "fa": "ابوبکر خلال، ابن قدامه، ابن تیمیه، ابن قیم، محمد بن عبدالوهاب",
                  "ms": "Abu Bakr al-Khallal, Ibn Qudamah, Ibn Taymiyyah, Ibn al-Qayyim, Muhammad bin Abd al-Wahhab",
                  "ur": "ابوبکر خلال، ابن قدامہ، ابن تیمیہ، ابن قیم، محمد بن عبدالوہاب"}},
    {"name": {"ar": "الإمام أبو حنيفة النعمان بن ثابت", "en": "Imam Abu Hanifah al-Nu'man ibn Thabit", "fr": "L'imam Abou Hanifa al-Nu'man ibn Thabit", "fa": "امام ابوحنیفه نعمان بن ثابت", "ms": "Imam Abu Hanifah al-Nu'man bin Thabit", "ur": "امام ابوحنیفہ نعمان بن ثابت"},
     "school": MADHHAB_NAMES["hanafi"], "lifespan": "80 - 150 AH",
     "birthplace": {"ar": "الكوفة", "en": "Kufa", "fr": "Koufa", "fa": "کوفه", "ms": "Kufah", "ur": "کوفہ"},
     "founding_place": {"ar": "الكوفة", "en": "Kufa", "fr": "Koufa", "fa": "کوفه", "ms": "Kufah", "ur": "کوفہ"},
     "scholars": {"ar": "أبو يوسف، محمد بن الحسن الشيباني، الطحاوي، الكاساني، ابن عابدين",
                  "en": "Abu Yusuf, Muhammad ibn al-Hasan al-Shaybani, al-Tahawi, al-Kasani, Ibn Abidin",
                  "fr": "Abu Yusuf, Muhammad ibn al-Hasan al-Chaybani, al-Tahawi, al-Kasani, Ibn Abidin",
                  "fa": "ابویوسف، محمد بن حسن شیبانی، طحاوی، کاسانی، ابن عابدین",
                  "ms": "Abu Yusuf, Muhammad bin al-Hasan al-Shaybani, al-Tahawi, al-Kasani, Ibn Abidin",
                  "ur": "ابویوسف، محمد بن حسن شیبانی، طحاوی، کاسانی، ابن عابدین"}},
    {"name": {"ar": "الإمام داود بن علي الأصفهاني", "en": "Imam Dawud ibn Ali al-Isfahani", "fr": "L'imam Dawud ibn Ali al-Isfahani", "fa": "امام داود بن علی اصفهانی", "ms": "Imam Dawud bin Ali al-Isfahani", "ur": "امام داود بن علی اصفہانی"},
     "school": MADHHAB_NAMES["zahiri"], "lifespan": "202 - 270 AH",
     "birthplace": {"ar": "الكوفة", "en": "Kufa", "fr": "Koufa", "fa": "کوفه", "ms": "Kufah", "ur": "کوفہ"},
     "founding_place": {"ar": "بغداد", "en": "Baghdad", "fr": "Bagdad", "fa": "بغداد", "ms": "Baghdad", "ur": "بغداد"},
     "scholars": {"ar": "ابن حزم الأندلسي (أشهر من دوّنه في «المحلى»)", "en": "Ibn Hazm al-Andalusi (its most famous codifier, in 'al-Muhalla')", "fr": "Ibn Hazm al-Andalusi (son codificateur le plus célèbre, dans « al-Muhalla »)", "fa": "ابن حزم اندلسی (مشهورترین مدون آن در «المحلی»)", "ms": "Ibn Hazm al-Andalusi (pengkodifikasi paling terkenal, dalam 'al-Muhalla')", "ur": "ابن حزم اندلسی (اس کے سب سے مشہور مدون، «المحلی» میں)"}},
    {"name": {"ar": "الإمام جعفر بن محمد الصادق", "en": "Imam Ja'far ibn Muhammad al-Sadiq", "fr": "L'imam Ja'far ibn Muhammad al-Sadiq", "fa": "امام جعفر بن محمد صادق", "ms": "Imam Ja'far bin Muhammad al-Sadiq", "ur": "امام جعفر بن محمد صادق"},
     "school": MADHHAB_NAMES["jafari"], "lifespan": "80 - 148 AH",
     "birthplace": {"ar": "المدينة المنورة", "en": "Medina", "fr": "Médine", "fa": "مدینه منوره", "ms": "Madinah", "ur": "مدینہ منورہ"},
     "founding_place": {"ar": "المدينة المنورة", "en": "Medina", "fr": "Médine", "fa": "مدینه منوره", "ms": "Madinah", "ur": "مدینہ منورہ"},
     "scholars": {"ar": "الشيخ المفيد، الشريف المرتضى، الشيخ الطوسي، المحقق الحلي، السيد الخميني، السيد السيستاني", "en": "al-Shaykh al-Mufid, al-Sharif al-Murtada, al-Shaykh al-Tusi, al-Muhaqqiq al-Hilli, Imam Khomeini, al-Sayyid al-Sistani", "fr": "al-Shaykh al-Mufid, al-Charif al-Murtada, al-Shaykh al-Tusi, al-Muhaqqiq al-Hilli, l'imam Khomeini, al-Sayyid al-Sistani", "fa": "شیخ مفید، شریف مرتضی، شیخ طوسی، محقق حلی، امام خمینی، سید سیستانی", "ms": "al-Shaykh al-Mufid, al-Sharif al-Murtada, al-Shaykh al-Tusi, al-Muhaqqiq al-Hilli, Imam Khomeini, Sayyid al-Sistani", "ur": "شیخ مفید، شریف مرتضی، شیخ طوسی، محقق حلی، امام خمینی، سید سیستانی"}},
    {"name": {"ar": "الإمام زيد بن علي بن الحسين", "en": "Imam Zayd ibn Ali ibn al-Husayn", "fr": "L'imam Zayd ibn Ali ibn al-Husayn", "fa": "امام زید بن علی بن حسین", "ms": "Imam Zayd bin Ali bin al-Husayn", "ur": "امام زید بن علی بن حسین"},
     "school": MADHHAB_NAMES["zaidi"], "lifespan": "80 - 122 AH",
     "birthplace": {"ar": "المدينة المنورة", "en": "Medina", "fr": "Médine", "fa": "مدینه منوره", "ms": "Madinah", "ur": "مدینہ منورہ"},
     "founding_place": {"ar": "الكوفة", "en": "Kufa", "fr": "Koufa", "fa": "کوفه", "ms": "Kufah", "ur": "کوفہ"},
     "scholars": {"ar": "أبو خالد الواسطي، الناصر الأطروش، الهادي يحيى بن الحسين، الإمام المنصور بالله", "en": "Abu Khalid al-Wasiti, al-Nasir al-Utrush, al-Hadi Yahya ibn al-Husayn, Imam al-Mansur billah", "fr": "Abu Khalid al-Wasiti, al-Nasir al-Utrush, al-Hadi Yahya ibn al-Husayn, l'imam al-Mansur billah", "fa": "ابوخالد واسطی، ناصر اطروش، هادی یحیی بن حسین، امام منصور بالله", "ms": "Abu Khalid al-Wasiti, al-Nasir al-Utrush, al-Hadi Yahya bin al-Husayn, Imam al-Mansur billah", "ur": "ابوخالد واسطی، ناصر اطروش، ہادی یحیی بن حسین، امام منصور باللہ"}},
    {"name": {"ar": "الإمام جابر بن زيد الأزدي", "en": "Imam Jabir ibn Zayd al-Azdi", "fr": "L'imam Jabir ibn Zayd al-Azdi", "fa": "امام جابر بن زید ازدی", "ms": "Imam Jabir bin Zayd al-Azdi", "ur": "امام جابر بن زید ازدی"},
     "school": MADHHAB_NAMES["ibadi"], "lifespan": "1st century - 93 AH",
     "birthplace": {"ar": "نزوى، عُمان", "en": "Nizwa, Oman", "fr": "Nizwa, Oman", "fa": "نزوی، عمان", "ms": "Nizwa, Oman", "ur": "نزوی، عمان"},
     "founding_place": {"ar": "البصرة", "en": "Basra", "fr": "Bassora", "fa": "بصره", "ms": "Basrah", "ur": "بصرہ"},
     "scholars": {"ar": "أبو سعيد الكدمي، أبو نزار الخروصي، نور الدين السالمي، الشيخ أحمد الخليلي", "en": "Abu Sa'id al-Kudami, Abu Nizar al-Kharusi, Nur al-Din al-Salimi, Shaykh Ahmad al-Khalili", "fr": "Abu Sa'id al-Kudami, Abu Nizar al-Kharusi, Nur al-Din al-Salimi, le cheikh Ahmad al-Khalili", "fa": "ابوسعید کدمی، ابونزار خروصی، نورالدین سالمی، شیخ احمد خلیلی", "ms": "Abu Sa'id al-Kudami, Abu Nizar al-Kharusi, Nur al-Din al-Salimi, Shaykh Ahmad al-Khalili", "ur": "ابوسعید کدمی، ابونزار خروصی، نورالدین سالمی، شیخ احمد خلیلی"}},
]

# --- Countries -----------------------------------------------------------

COUNTRIES = [
    {"flag": "🇸🇦", "name": {"ar": "السعودية", "en": "Saudi Arabia", "fr": "Arabie saoudite", "fa": "عربستان سعودی", "ms": "Arab Saudi", "ur": "سعودی عرب"}, "madhab": "hanbali", "population": "36.4M"},
    {"flag": "🇪🇬", "name": {"ar": "مصر", "en": "Egypt", "fr": "Égypte", "fa": "مصر", "ms": "Mesir", "ur": "مصر"}, "madhab": "shafii", "population": "112.7M"},
    {"flag": "🇲🇦", "name": {"ar": "المغرب", "en": "Morocco", "fr": "Maroc", "fa": "مراکش", "ms": "Maghribi", "ur": "مراکش"}, "madhab": "maliki", "population": "37.8M"},
    {"flag": "🇹🇷", "name": {"ar": "تركيا", "en": "Turkey", "fr": "Turquie", "fa": "ترکیه", "ms": "Turki", "ur": "ترکی"}, "madhab": "hanafi", "population": "87.5M"},
    {"flag": "🇮🇷", "name": {"ar": "إيران", "en": "Iran", "fr": "Iran", "fa": "ایران", "ms": "Iran", "ur": "ایران"}, "madhab": "jafari", "population": "89.8M"},
    {"flag": "🇴🇲", "name": {"ar": "عُمان", "en": "Oman", "fr": "Oman", "fa": "عمان", "ms": "Oman", "ur": "عمان"}, "madhab": "ibadi", "population": "4.7M"},
    {"flag": "🇸🇩", "name": {"ar": "السودان", "en": "Sudan", "fr": "Soudan", "fa": "سودان", "ms": "Sudan", "ur": "سوڈان"}, "madhab": "maliki", "population": "48.1M"},
    {"flag": "🇸🇾", "name": {"ar": "سوريا", "en": "Syria", "fr": "Syrie", "fa": "سوریه", "ms": "Syria", "ur": "شام"}, "madhab": "hanafi", "population": "23.2M"},
    {"flag": "🇵🇰", "name": {"ar": "باكستان", "en": "Pakistan", "fr": "Pakistan", "fa": "پاکستان", "ms": "Pakistan", "ur": "پاکستان"}, "madhab": "hanafi", "population": "240.5M"},
    {"flag": "🇦🇫", "name": {"ar": "أفغانستان", "en": "Afghanistan", "fr": "Afghanistan", "fa": "افغانستان", "ms": "Afghanistan", "ur": "افغانستان"}, "madhab": "hanafi", "population": "41.1M"},
    {"flag": "🇲🇾", "name": {"ar": "ماليزيا", "en": "Malaysia", "fr": "Malaisie", "fa": "مالزی", "ms": "Malaysia", "ur": "ملائیشیا"}, "madhab": "shafii", "population": "34.3M"},
    {"flag": "🇮🇩", "name": {"ar": "إندونيسيا", "en": "Indonesia", "fr": "Indonésie", "fa": "اندونزی", "ms": "Indonesia", "ur": "انڈونیشیا"}, "madhab": "shafii", "population": "281.2M"},
]

# =========================================================================
# 2) LANGUAGE SELECTION & STYLING
# =========================================================================

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
font_stack = "'Tahoma','Segoe UI','Amiri',sans-serif" if is_rtl else "'Segoe UI','Georgia',sans-serif"

st.markdown(
    f"""
    <style>
    html, body {{ overflow-x: hidden; }}
    .stApp {{
        direction: {direction};
        font-family: {font_stack};
    }}
    .stApp p, .stApp li, .stApp label, .stApp span,
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5 {{
        text-align: {align};
        line-height: 1.9;
        word-spacing: normal;
        letter-spacing: normal;
        text-shadow: none;
    }}
    div[data-testid="stVerticalBlockBorderWrapper"] {{
        box-shadow: none !important;
    }}
    div[role="radiogroup"], div[data-baseweb="select"], div[data-testid="stMultiSelect"] {{
        direction: {direction};
    }}
    .stButton button {{ width: 100%; }}
    .app-header {{
        text-align: center;
        padding: 26px 16px;
        background: linear-gradient(145deg, #0f231c, #2a5c4a);
        color: white;
        border-radius: 16px;
        margin-bottom: 25px;
    }}
    .app-header h1 {{
        text-align: center !important;
        font-size: 2.2rem;
        margin: 8px 0 0;
    }}
    .app-header p {{
        text-align: center !important;
        font-size: 1rem;
        color: #d6e4de;
        margin: 8px 0 0;
    }}
    .answer-card {{
        background: #f5f7f5;
        border: 1px solid #e1e7e3;
        border-radius: 14px;
        padding: 16px 18px;
        margin-bottom: 12px;
        direction: {direction};
        text-align: {align};
    }}
    .answer-card h4 {{ margin: 0 0 6px 0; color: #1e3a2f; text-align: {align}; }}
    .answer-card .answer-text {{ font-size: 1.15rem; font-weight: 600; color: #16281f; margin: 4px 0; }}
    .answer-card .answer-note {{ font-size: 0.85rem; color: #6a7f78; }}
    .signature {{
        font-family: 'Brush Script MT', 'Segoe Script', cursive;
        font-style: italic;
        font-size: 1rem;
        color: #b08d3f;
        text-align: center;
        margin: 6px 0 18px 0;
        opacity: 0.9;
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
    """,
    unsafe_allow_html=True,
)

# =========================================================================
# 3) HEADER / LOGO
# =========================================================================

st.markdown(
    """
    <div style="text-align:center; margin-bottom:-6px;">
        <svg width="72" height="72" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
            <circle cx="50" cy="50" r="46" fill="#0f231c" stroke="#d4a854" stroke-width="3"/>
            <path d="M50 28 C38 22 26 24 20 30 V66 C26 60 38 58 50 64 C62 58 74 60 80 66 V30 C74 24 62 22 50 28 Z"
                  fill="none" stroke="#f2e6c9" stroke-width="3" stroke-linejoin="round"/>
            <line x1="50" y1="28" x2="50" y2="64" stroke="#f2e6c9" stroke-width="2.5"/>
            <path d="M66 20 A10 10 0 1 0 68 38 A8 8 0 1 1 66 20 Z" fill="#d4a854"/>
        </svg>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div class="app-header">
        <h1>📖 {T['app_title']}</h1>
        <p>{T['app_subtitle']}</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# =========================================================================
# 4) SECTION 1 — MADHHAB SELECTION (multi-select)
# =========================================================================

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

# =========================================================================
# 5) SECTION 2 — TOPIC
# =========================================================================

st.markdown(f"### {T['s2_title']}")
topic = st.radio(
    T["topic_q"],
    list(TOPICS.keys()),
    format_func=lambda t: TOPICS[t][lang],
    horizontal=True,
    label_visibility="collapsed",
)

st.divider()

# =========================================================================
# 6) SECTION 3 — DETAIL LEVEL
# =========================================================================

st.markdown(f"### {T['s3_title']}")
level = st.radio(
    T["level_q"],
    list(LEVELS.keys()),
    format_func=lambda lv: LEVELS[lv][lang],
    horizontal=True,
    label_visibility="collapsed",
)

st.divider()

# =========================================================================
# 7) SECTION 4 — QUESTION
# =========================================================================

st.markdown(f"### {T['s4_title']}")
question = st.text_input(
    T["s4_title"], placeholder=T["question_placeholder"], label_visibility="collapsed"
)
search_clicked = st.button(T["search_btn"], use_container_width=True)

st.divider()

# =========================================================================
# 8) SEARCH LOGIC
# =========================================================================


def search_issues(query, topic_filter, madhabs, level, lang):
    if not query:
        return []
    q = query.strip().lower()
    matches = []
    for issue in ISSUES:
        if issue["topic"] != topic_filter:
            continue
        pool = (
            issue["title"][lang].lower()
            + " "
            + " ".join(issue["keywords"][lang]).lower()
            + " "
            + issue["rulings"][lang]["full"].lower()
        )
        if q in pool:
            matches.append(issue)

    if not matches:
        words = re.findall(r"\w+", q)
        for issue in ISSUES:
            if issue["topic"] != topic_filter:
                continue
            pool = issue["title"][lang].lower() + " " + " ".join(issue["keywords"][lang]).lower()
            if any(w in pool for w in words):
                matches.append(issue)

    results = []
    for issue in matches:
        cards = []
        per_madhab = issue.get("rulings_by_madhab")
        if per_madhab:
            for m in madhabs:
                data = per_madhab.get(m)
                if data:
                    cards.append({
                        "label": MADHHAB_NAMES[m][lang],
                        "answer": data[lang].get(level, data[lang]["full"]),
                        "note": T["note_madhab"].format(MADHHAB_NAMES[m][lang]),
                    })
        if not cards:
            cards.append({
                "label": TOPICS[issue["topic"]][lang],
                "answer": issue["rulings"][lang].get(level, issue["rulings"][lang]["full"]),
                "note": T["note_general"],
            })
        results.append({
            "title": issue["title"][lang],
            "topic": TOPICS[issue["topic"]][lang],
            "cards": cards,
        })
    return results


# =========================================================================
# 9) SECTION 5 — ANSWER
# =========================================================================

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
                    st.markdown(
                        f"""
                        <div class="answer-card">
                            <h4>{card['label']}</h4>
                            <div class="answer-text">{card['answer']}</div>
                            <div class="answer-note">{card['note']}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
            st.markdown(f"<div class='signature'>{T['signature']}</div>", unsafe_allow_html=True)
    else:
        st.warning(T["no_results_warning"])
elif search_clicked:
    st.info(T["no_question_warning"])
else:
    st.caption(T["answer_placeholder"])

st.markdown("---")

# =========================================================================
# 10) REFERENCE SECTIONS (accordion / expanders)
# =========================================================================

with st.expander(T["expander_imams"]):
    for imam in IMAMS:
        st.markdown(
            f"""
            <div class="info-box">
                <h4>{imam['name'][lang]}</h4>
                <p style="color:#d4a854; font-weight:600;">{imam['school'][lang]} &nbsp;|&nbsp; {imam['lifespan']}</p>
                <p>📍 {T['birthplace']}: {imam['birthplace'][lang]} &nbsp;·&nbsp; 🏛️ {T['founding_place']}: {imam['founding_place'][lang]}</p>
                <p>🎓 {T['scholars']}: {imam['scholars'][lang]}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

with st.expander(T["expander_countries"]):
    cols = st.columns(3)
    for i, c in enumerate(COUNTRIES):
        with cols[i % 3]:
            st.markdown(
                f"""
                <div class="country-box">
                    <strong>{c['flag']} {c['name'][lang]}</strong><br>
                    <span style="color:#d4a854;">{T['official_madhab']}: {MADHHAB_NAMES[c['madhab']][lang]}</span><br>
                    <span style="font-size:0.8rem; color:#6a7f78;">👥 {T['population']}: {c['population']}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

with st.expander(T["expander_glossary"]):
    for term in GLOSSARY:
        st.markdown(
            f"""
            <div class="glossary-box">
                <h4>{term['term'][lang]}</h4>
                <p>{term['definition'][lang]}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

with st.expander(T["expander_comments"]):
    if "session_comments" not in st.session_state:
        st.session_state.session_comments = []

    st.markdown(f"**{T['rating_label']}**")
    rating = None
    try:
        rating = st.feedback("stars")
        if rating is not None:
            rating = rating + 1
    except Exception:
        star_options = [1, 2, 3, 4, 5]
        rating = st.radio(
            T["rating_label"],
            star_options,
            format_func=lambda n: "⭐" * n,
            horizontal=True,
            label_visibility="collapsed",
        )

    comment_text = st.text_area(T["comment_placeholder"], placeholder=T["comment_placeholder"], label_visibility="collapsed")
    if st.button(T["comment_submit"]):
        if comment_text.strip():
            st.session_state.session_comments.append(
                {"text": comment_text.strip(), "rating": rating or 5}
            )
            st.success(T["comment_success"])
        else:
            st.warning(T["comment_warning"])

    if st.session_state.session_comments:
        st.markdown(f"**{T['comments_title']}**")
        for c in st.session_state.session_comments:
            st.markdown(f"- {'⭐' * int(c['rating'])} — {c['text']}")
    st.caption(T["comments_note"])
