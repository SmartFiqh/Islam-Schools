import streamlit as st
import re

st.set_page_config(
    page_title="الجامع المختصر لآراء المذاهب",
    page_icon="📖",
    layout="wide",
)

# =========================================================
# LANGUAGE METADATA
# =========================================================
LANG_META = {
    "ar": {"name": "العربية", "dir": "rtl", "font": "Tahoma, 'Segoe UI', sans-serif"},
    "en": {"name": "English", "dir": "ltr", "font": "'Segoe UI', Arial, sans-serif"},
    "fr": {"name": "Français", "dir": "ltr", "font": "'Segoe UI', Arial, sans-serif"},
    "fa": {"name": "فارسی", "dir": "rtl", "font": "Tahoma, 'Segoe UI', sans-serif"},
    "ms": {"name": "Bahasa Melayu", "dir": "ltr", "font": "'Segoe UI', Arial, sans-serif"},
    "ur": {"name": "اردو", "dir": "rtl", "font": "Tahoma, 'Segoe UI', sans-serif"},
}
LANGS = list(LANG_META.keys())
# Languages with fully translated fiqh content. Others fall back to English content
# (with localized navigation/UI) to avoid publishing unverified religious-ruling translations.
CONTENT_LANGS = ["ar", "en"]

# =========================================================
# UI STRINGS
# =========================================================
UI = {
    "app_title": {"ar": "الجامع المختصر لآراء المذاهب", "en": "The Concise Compendium of Madhhab Opinions",
                  "fr": "Le Recueil concis des avis des écoles juridiques", "fa": "جامع مختصر آراء مذاهب",
                  "ms": "Himpunan Ringkas Pandangan Mazhab", "ur": "مذاہب کی آراء کا مختصر مجموعہ"},
    "app_subtitle": {"ar": "منصة عرض ومقارنة آراء المذاهب الفقهية — للفهم والتبصر، وليست موقع إفتاء.",
                      "en": "A platform for presenting and comparing juristic (fiqh) opinions — for understanding, not for issuing formal rulings (fatwas).",
                      "fr": "Une plateforme de présentation et de comparaison des avis juridiques (fiqh) — à but pédagogique, non un site de fatwa.",
                      "fa": "پلتفرمی برای نمایش و مقایسه آراء فقهی مذاهب — برای فهم و آگاهی، نه سایت فتوا.",
                      "ms": "Platform untuk memaparkan dan membandingkan pandangan fiqh mazhab — untuk kefahaman, bukan laman fatwa.",
                      "ur": "فقہی مذاہب کی آراء کے موازنے کا پلیٹ فارم — سمجھنے کے لیے، فتویٰ جاری کرنے کے لیے نہیں۔"},
    "language_label": {"ar": "اللغة", "en": "Language", "fr": "Langue", "fa": "زبان", "ms": "Bahasa", "ur": "زبان"},
    "content_fallback_note": {
        "ar": "", "en": "",
        "fr": "Remarque : le contenu détaillé des avis est actuellement disponible en arabe et en anglais uniquement ; il est affiché ici en anglais.",
        "fa": "توجه: محتوای تفصیلی آراء فعلاً فقط به عربی و انگلیسی موجود است و در اینجا به انگلیسی نمایش داده می‌شود.",
        "ms": "Nota: kandungan terperinci pandangan hukum kini hanya tersedia dalam bahasa Arab dan Inggeris; ia dipaparkan di sini dalam bahasa Inggeris.",
        "ur": "نوٹ: تفصیلی فقہی آراء فی الحال صرف عربی اور انگریزی میں دستیاب ہیں؛ یہاں انگریزی میں دکھائی جا رہی ہیں۔",
    },
    "search_section_title": {"ar": "🔍 ابحث عن حكم مسألة", "en": "🔍 Search for a Ruling",
                              "fr": "🔍 Rechercher un avis juridique", "fa": "🔍 جستجوی حکم یک مسئله",
                              "ms": "🔍 Cari Hukum Sesuatu Isu", "ur": "🔍 کسی مسئلے کا حکم تلاش کریں"},
    "step1_title": {"ar": "١. اختر المذهب", "en": "1. Choose the Madhhab", "fr": "1. Choisir l'école juridique",
                     "fa": "۱. انتخاب مذهب", "ms": "1. Pilih Mazhab", "ur": "۱. مذہب منتخب کریں"},
    "step1_group_prompt": {"ar": "مذاهب السنة، أم مذاهب الشيعة، أم المذهب الإباضي، أم آراء أخرى؟",
                             "en": "Sunni schools, Shia schools, the Ibadi school, or other views?",
                             "fr": "Écoles sunnites, écoles chiites, école ibadite, ou autres avis ?",
                             "fa": "مذاهب اهل سنت، مذاهب شیعه، مذهب اباضی، یا آراء دیگر؟",
                             "ms": "Mazhab Sunni, Syiah, Ibadi, atau pandangan lain?",
                             "ur": "اہل سنت کے مذاہب، شیعہ مذاہب، اباضی مذہب، یا دیگر آراء؟"},
    "step1_pick_prompt": {"ar": "اختر المذهب تحديداً:", "en": "Choose the specific madhhab:",
                            "fr": "Choisissez l'école précise :", "fa": "مذهب مشخص را انتخاب کنید:",
                            "ms": "Pilih mazhab khusus:", "ur": "مخصوص مذہب منتخب کریں:"},
    "selected_madhab_caption": {"ar": "المذهب المختار:", "en": "Selected madhhab:", "fr": "École sélectionnée :",
                                  "fa": "مذهب انتخاب‌شده:", "ms": "Mazhab dipilih:", "ur": "منتخب مذہب:"},
    "step2_title": {"ar": "٢. اختر الموضوع", "en": "2. Choose the Topic", "fr": "2. Choisir le thème",
                     "fa": "۲. انتخاب موضوع", "ms": "2. Pilih Topik", "ur": "۲. موضوع منتخب کریں"},
    "step2_prompt": {"ar": "العبادات، أم المعاملات، أم الأسرة، أم مواضيع أخرى؟",
                       "en": "Worship, transactions, family, or other topics?",
                       "fr": "Culte, transactions, famille, ou autres thèmes ?",
                       "fa": "عبادات، معاملات، خانواده، یا موضوعات دیگر؟",
                       "ms": "Ibadat, muamalat, keluarga, atau topik lain?",
                       "ur": "عبادات، معاملات، خاندان، یا دیگر موضوعات؟"},
    "step3_title": {"ar": "٣. طريقة عرض الإجابة", "en": "3. Answer Detail Level", "fr": "3. Niveau de détail de la réponse",
                     "fa": "۳. سطح نمایش پاسخ", "ms": "3. Tahap Perincian Jawapan", "ur": "۳. جواب کی تفصیل کی سطح"},
    "step3_prompt": {"ar": "مختصرة، أم مبسطة، أم مفصّلة؟", "en": "Very short, simplified, or detailed?",
                       "fr": "Très courte, simplifiée, ou détaillée ?", "fa": "بسیار مختصر، ساده، یا مفصل؟",
                       "ms": "Sangat ringkas, ringkas, atau terperinci?", "ur": "بہت مختصر، آسان، یا تفصیلی؟"},
    "level_very_short": {"ar": "مختصرة (كلمة)", "en": "Very short (one word)", "fr": "Très courte (un mot)",
                           "fa": "بسیار مختصر (یک واژه)", "ms": "Sangat ringkas (satu perkataan)",
                           "ur": "بہت مختصر (ایک لفظ)"},
    "level_short": {"ar": "مبسطة (سطر)", "en": "Simplified (one line)", "fr": "Simplifiée (une ligne)",
                     "fa": "ساده (یک خط)", "ms": "Ringkas (satu baris)", "ur": "آسان (ایک سطر)"},
    "level_full": {"ar": "مفصل (أكثر من سطر)", "en": "Detailed (multi-line)", "fr": "Détaillée (plusieurs lignes)",
                    "fa": "مفصل (چند خط)", "ms": "Terperinci (beberapa baris)", "ur": "تفصیلی (متعدد سطور)"},
    "step4_title": {"ar": "٤. اكتب سؤالك", "en": "4. Type Your Question", "fr": "4. Posez votre question",
                     "fa": "۴. سؤال خود را بنویسید", "ms": "4. Taip Soalan Anda", "ur": "۴. اپنا سوال لکھیں"},
    "question_placeholder": {"ar": "مثال: ما حكم صلاة الجماعة؟", "en": "e.g. What is the ruling on congregational prayer?",
                               "fr": "ex. Quel est l'avis sur la prière en groupe ?",
                               "fa": "مثال: حکم نماز جماعت چیست؟", "ms": "cth: Apakah hukum solat berjemaah?",
                               "ur": "مثال: نماز باجماعت کا کیا حکم ہے؟"},
    "search_button": {"ar": "🔍 ابحث عن الإجابة", "en": "🔍 Search for the Answer", "fr": "🔍 Rechercher la réponse",
                        "fa": "🔍 جستجوی پاسخ", "ms": "🔍 Cari Jawapan", "ur": "🔍 جواب تلاش کریں"},
    "step5_title": {"ar": "٥. الإجابة", "en": "5. The Answer", "fr": "5. La réponse", "fa": "۵. پاسخ",
                     "ms": "5. Jawapan", "ur": "۵. جواب"},
    "note_general": {"ar": "رأي عام موحّد — لم يُفصّل بعد لكل مذهب", "en": "Unified general opinion — not yet detailed per madhhab",
                       "fr": "Avis général unifié — pas encore détaillé par école", "fa": "نظر عمومی واحد — هنوز به‌تفکیک مذهب نیست",
                       "ms": "Pandangan umum bersatu — belum diperincikan mengikut mazhab",
                       "ur": "متفقہ عمومی رائے — ابھی تک مذہب کے لحاظ سے تفصیل نہیں دی گئی"},
    "note_madhab": {"ar": "رأي المذهب", "en": "Opinion of the", "fr": "Avis de l'école", "fa": "نظر مذهب",
                      "ms": "Pandangan mazhab", "ur": "مذہب کی رائے"},
    "fatwa_disclaimer": {"ar": "هذا والله أعلم", "en": "And Allah knows best.", "fr": "Et Allah est plus Savant.",
                           "fa": "و الله اعلم", "ms": "Dan Allah Maha Mengetahui.", "ur": "واللہ اعلم"},
    "no_results": {"ar": "🔍 لم نجد مسألة بهذا الوصف ضمن الموضوع المختار. جرّب صياغة أخرى أو وسّع نطاق البحث.",
                     "en": "🔍 No matching issue was found under the selected topic. Try different wording or broaden the search.",
                     "fr": "🔍 Aucune question correspondante n'a été trouvée dans le thème sélectionné. Essayez une autre formulation.",
                     "fa": "🔍 مسئله‌ای با این توضیح در موضوع انتخاب‌شده یافت نشد. عبارت دیگری را امتحان کنید.",
                     "ms": "🔍 Tiada isu sepadan ditemui dalam topik dipilih. Cuba kata kunci lain.",
                     "ur": "🔍 منتخب موضوع میں اس تفصیل کا کوئی مسئلہ نہیں ملا۔ دوسرے الفاظ آزمائیں۔"},
    "empty_question": {"ar": "الرجاء كتابة سؤالك أولاً في الفقرة الرابعة.", "en": "Please type your question first in step 4.",
                         "fr": "Veuillez d'abord saisir votre question à l'étape 4.",
                         "fa": "لطفاً ابتدا سؤال خود را در مرحله ۴ بنویسید.",
                         "ms": "Sila taip soalan anda dahulu di langkah 4.", "ur": "براہ کرم مرحلہ ۴ میں پہلے اپنا سوال لکھیں۔"},
    "empty_placeholder": {"ar": "ستظهر الإجابة هنا بعد كتابة السؤال والضغط على زر البحث.",
                            "en": "The answer will appear here after you type a question and press search.",
                            "fr": "La réponse apparaîtra ici après avoir saisi une question et cliqué sur rechercher.",
                            "fa": "پاسخ پس از نوشتن سؤال و کلیک روی جستجو در اینجا نمایش داده می‌شود.",
                            "ms": "Jawapan akan dipaparkan di sini selepas anda menaip soalan dan menekan cari.",
                            "ur": "سوال لکھنے اور تلاش پر کلک کرنے کے بعد جواب یہاں ظاہر ہوگا۔"},
    "resources_section_title": {"ar": "📚 الموارد الإضافية", "en": "📚 Additional Resources",
                                  "fr": "📚 Ressources supplémentaires", "fa": "📚 منابع تکمیلی",
                                  "ms": "📚 Sumber Tambahan", "ur": "📚 اضافی وسائل"},
    "tab_imams": {"ar": "📜 الأئمة المؤسسون", "en": "📜 Founding Imams", "fr": "📜 Imams fondateurs",
                   "fa": "📜 امامان بنیان‌گذار", "ms": "📜 Imam Pengasas", "ur": "📜 بانی ائمہ"},
    "tab_countries": {"ar": "🗺️ الدول والمذهب الرسمي", "en": "🗺️ Countries & Official Madhhab",
                        "fr": "🗺️ Pays et école officielle", "fa": "🗺️ کشورها و مذهب رسمی",
                        "ms": "🗺️ Negara & Mazhab Rasmi", "ur": "🗺️ ممالک اور سرکاری مذہب"},
    "tab_glossary": {"ar": "📖 مصطلحات فقهية", "en": "📖 Juristic Terminology", "fr": "📖 Terminologie juridique",
                       "fa": "📖 اصطلاحات فقهی", "ms": "📖 Istilah Fiqh", "ur": "📖 فقہی اصطلاحات"},
    "tab_comments": {"ar": "💬 التعليقات", "en": "💬 Comments", "fr": "💬 Commentaires", "fa": "💬 نظرات",
                       "ms": "💬 Ulasan", "ur": "💬 تبصرے"},
    "birthplace_label": {"ar": "📍 مكان الميلاد", "en": "📍 Birthplace", "fr": "📍 Lieu de naissance",
                           "fa": "📍 محل تولد", "ms": "📍 Tempat Lahir", "ur": "📍 جائے پیدائش"},
    "founding_place_label": {"ar": "🏛️ مكان تأسيس المذهب", "en": "🏛️ Where the School was Founded",
                               "fr": "🏛️ Lieu de fondation de l'école", "fa": "🏛️ محل تأسیس مذهب",
                               "ms": "🏛️ Tempat Pengasasan Mazhab", "ur": "🏛️ مذہب کے قیام کی جگہ"},
    "scholars_label": {"ar": "🎓 أشهر فقهاء المذهب", "en": "🎓 Notable Scholars", "fr": "🎓 Juristes notables",
                         "fa": "🎓 فقهای مشهور مذهب", "ms": "🎓 Ulama Terkemuka", "ur": "🎓 مشہور فقہاء"},
    "official_madhab_label": {"ar": "المذهب الرسمي", "en": "Official madhhab", "fr": "École officielle",
                                "fa": "مذهب رسمی", "ms": "Mazhab rasmi", "ur": "سرکاری مذہب"},
    "population_label": {"ar": "👥 عدد السكان", "en": "👥 Population", "fr": "👥 Population", "fa": "👥 جمعیت",
                           "ms": "👥 Populasi", "ur": "👥 آبادی"},
    "rating_label": {"ar": "قيّم فائدة الإجابة:", "en": "Rate the usefulness of the answer:",
                       "fr": "Évaluez l'utilité de la réponse :", "fa": "میزان مفید بودن پاسخ را ارزیابی کنید:",
                       "ms": "Nilaikan manfaat jawapan:", "ur": "جواب کی افادیت کی درجہ بندی کریں:"},
    "comment_placeholder": {"ar": "اكتب ملاحظتك هنا...", "en": "Write your note here...",
                              "fr": "Écrivez votre remarque ici...", "fa": "یادداشت خود را اینجا بنویسید...",
                              "ms": "Tulis ulasan anda di sini...", "ur": "اپنا تبصرہ یہاں لکھیں..."},
    "comment_area_label": {"ar": "تعليقك أو ملاحظتك:", "en": "Your comment or note:", "fr": "Votre commentaire :",
                             "fa": "نظر یا یادداشت شما:", "ms": "Ulasan atau nota anda:", "ur": "آپ کا تبصرہ یا نوٹ:"},
    "submit_comment": {"ar": "إرسال التعليق", "en": "Submit Comment", "fr": "Envoyer le commentaire",
                         "fa": "ارسال نظر", "ms": "Hantar Ulasan", "ur": "تبصرہ بھیجیں"},
    "comment_success": {"ar": "✅ تم إرسال تعليقك، شكراً لك.", "en": "✅ Your comment was submitted, thank you.",
                          "fr": "✅ Votre commentaire a été envoyé, merci.", "fa": "✅ نظر شما ارسال شد، سپاسگزاریم.",
                          "ms": "✅ Ulasan anda telah dihantar, terima kasih.", "ur": "✅ آپ کا تبصرہ موصول ہوگیا، شکریہ۔"},
    "comment_warning": {"ar": "⚠️ الرجاء كتابة تعليق قبل الإرسال.", "en": "⚠️ Please write a comment before submitting.",
                          "fr": "⚠️ Veuillez écrire un commentaire avant d'envoyer.",
                          "fa": "⚠️ لطفاً پیش از ارسال نظری بنویسید.", "ms": "⚠️ Sila tulis ulasan sebelum menghantar.",
                          "ur": "⚠️ براہ کرم بھیجنے سے پہلے تبصرہ لکھیں۔"},
    "session_comments_title": {"ar": "تعليقات هذه الجلسة:", "en": "Comments in this session:",
                                 "fr": "Commentaires de cette session :", "fa": "نظرات این نشست:",
                                 "ms": "Ulasan sesi ini:", "ur": "اس نشست کے تبصرے:"},
    "comments_note": {"ar": "ملاحظة: هذه التعليقات محفوظة لجلستك الحالية فقط. لحفظها بشكل دائم يلزم ربط البرنامج بقاعدة بيانات (مثل Firebase).",
                        "en": "Note: these comments are kept only for your current session. Permanent storage requires connecting the app to a database (e.g. Firebase).",
                        "fr": "Remarque : ces commentaires ne sont conservés que pour votre session actuelle. Un stockage permanent nécessite une base de données (p. ex. Firebase).",
                        "fa": "توجه: این نظرات فقط برای نشست فعلی شما نگه‌داری می‌شوند. برای ذخیره دائمی باید برنامه به پایگاه داده (مانند Firebase) متصل شود.",
                        "ms": "Nota: ulasan ini hanya disimpan untuk sesi semasa anda. Penyimpanan kekal memerlukan pangkalan data (cth. Firebase).",
                        "ur": "نوٹ: یہ تبصرے صرف آپ کی موجودہ نشست کے لیے محفوظ ہیں۔ مستقل محفوظ کرنے کے لیے ڈیٹا بیس (مثلاً Firebase) سے جوڑنا ضروری ہے۔"},
    "footer_text": {"ar": "المعرفة أمانة. نراجع كل مادة من مصادرها الأصلية، ونوضح مواضع الاتفاق والاختلاف بإنصاف — هذا البرنامج لعرض آراء المذاهب للفهم والتبصر، وليس موقع إفتاء.",
                      "en": "Knowledge is a trust. Every entry is reviewed against its original sources, presenting points of agreement and difference fairly — this app is for understanding, not for issuing fatwas.",
                      "fr": "Le savoir est une responsabilité. Chaque entrée est vérifiée à partir de ses sources originales, en présentant équitablement les points d'accord et de désaccord — cette application sert à comprendre, non à émettre des fatwas.",
                      "fa": "دانش امانت است. هر مطلب از منابع اصلی آن بازبینی می‌شود و نقاط اتفاق و اختلاف را منصفانه بیان می‌کند — این برنامه برای فهم است، نه صدور فتوا.",
                      "ms": "Ilmu adalah amanah. Setiap kandungan disemak daripada sumber asalnya, memaparkan persamaan dan perbezaan secara adil — aplikasi ini untuk kefahaman, bukan untuk mengeluarkan fatwa.",
                      "ur": "علم ایک امانت ہے۔ ہر مواد کو اصل مصادر سے جانچا جاتا ہے اور اتفاق و اختلاف کے نکات کو منصفانہ انداز میں پیش کیا جاتا ہے — یہ ایپ سمجھنے کے لیے ہے، فتویٰ دینے کے لیے نہیں۔"},
}


def t(key, lang):
    return UI.get(key, {}).get(lang, UI.get(key, {}).get("en", key))


# =========================================================
# MADHHAB GROUPS & NAMES
# =========================================================
MADHHAB_NAMES = {
    "maliki": {"ar": "مالكي", "en": "Maliki", "fr": "Malikite", "fa": "مالکی", "ms": "Maliki", "ur": "مالکی"},
    "shafii": {"ar": "شافعي", "en": "Shafi'i", "fr": "Chaféite", "fa": "شافعی", "ms": "Syafie", "ur": "شافعی"},
    "hanafi": {"ar": "حنفي", "en": "Hanafi", "fr": "Hanafite", "fa": "حنفی", "ms": "Hanafi", "ur": "حنفی"},
    "hanbali": {"ar": "حنبلي", "en": "Hanbali", "fr": "Hanbalite", "fa": "حنبلی", "ms": "Hanbali", "ur": "حنبلی"},
    "dhahiri": {"ar": "ظاهري", "en": "Dhahiri (Literalist)", "fr": "Dhâhirite", "fa": "ظاهری", "ms": "Zahiri", "ur": "ظاہری"},
    "jafari": {"ar": "جعفري", "en": "Ja'fari", "fr": "Djaafarite", "fa": "جعفری", "ms": "Jaafari", "ur": "جعفری"},
    "zaydi": {"ar": "زيدي", "en": "Zaydi", "fr": "Zaydite", "fa": "زیدی", "ms": "Zaidi", "ur": "زیدی"},
    "ibadi": {"ar": "إباضي", "en": "Ibadi", "fr": "Ibadite", "fa": "اباضی", "ms": "Ibadi", "ur": "اباضی"},
}

GROUP_LABELS = {
    "sunni": {"ar": "مذاهب السنة", "en": "Sunni Schools", "fr": "Écoles sunnites", "fa": "مذاهب اهل سنت",
               "ms": "Mazhab Sunni", "ur": "اہل سنت کے مذاہب"},
    "shia": {"ar": "مذاهب الشيعة", "en": "Shia Schools", "fr": "Écoles chiites", "fa": "مذاهب شیعه",
              "ms": "Mazhab Syiah", "ur": "شیعہ مذاہب"},
    "ibadi_group": {"ar": "المذهب الإباضي", "en": "The Ibadi School", "fr": "L'école ibadite", "fa": "مذهب اباضی",
                      "ms": "Mazhab Ibadi", "ur": "اباضی مذہب"},
    "other": {"ar": "آراء أخرى", "en": "Other Views", "fr": "Autres avis", "fa": "آراء دیگر",
               "ms": "Pandangan Lain", "ur": "دیگر آراء"},
}

MADHHAB_GROUPS = {
    "sunni": ["maliki", "shafii", "hanafi", "hanbali", "dhahiri"],
    "shia": ["jafari", "zaydi"],
    "ibadi_group": ["ibadi"],
    "other": ["other"],
}
MADHHAB_NAMES["other"] = {"ar": "أخرى", "en": "Other", "fr": "Autre", "fa": "دیگر", "ms": "Lain", "ur": "دیگر"}

# =========================================================
# TOPICS
# =========================================================
TOPICS = {
    "ibadat": {"ar": "العبادات", "en": "Worship", "fr": "Culte", "fa": "عبادات", "ms": "Ibadat", "ur": "عبادات"},
    "muamalat": {"ar": "المعاملات", "en": "Transactions", "fr": "Transactions", "fa": "معاملات", "ms": "Muamalat", "ur": "معاملات"},
    "usra": {"ar": "الأسرة", "en": "Family", "fr": "Famille", "fa": "خانواده", "ms": "Keluarga", "ur": "خاندان"},
    "other": {"ar": "مواضيع أخرى", "en": "Other Topics", "fr": "Autres thèmes", "fa": "موضوعات دیگر", "ms": "Topik Lain", "ur": "دیگر موضوعات"},
}
TOPIC_ORDER = ["ibadat", "muamalat", "usra", "other"]

# =========================================================
# ISSUES DATA (fully translated for ar/en; other languages fall back to en)
# =========================================================
ISSUES = [
    {
        "id": 1, "topic": "ibadat",
        "keywords": {"ar": ["جماعة", "مسجد", "رجال", "صلاة", "فرض", "سنة", "واجب"],
                      "en": ["congregation", "mosque", "men", "prayer", "obligatory", "sunnah"]},
        "t": {
            "ar": {"title": "صلاة الجماعة", "very_short": "سنة مؤكدة",
                    "short": "سنة مؤكدة عند الجمهور، واجبة عند الحنفية",
                    "full": "تجب صلاة الجماعة في المسجد على الرجال عند جمهور الفقهاء؛ فهي فرض عين عند الحنابلة، واجب مؤكد عند الحنفية، فرض كفاية عند المالكية والشافعية، ومستحبة تأكيداً عند الجعفرية في زمن الغيبة."},
            "en": {"title": "Congregational Prayer", "very_short": "Strongly recommended",
                    "short": "A strongly recommended sunnah for most, obligatory for Hanafis",
                    "full": "Praying in congregation at the mosque is required of men according to most jurists; it is an individual obligation (fard 'ayn) for Hanbalis, a strong obligation for Hanafis, a communal obligation (fard kifayah) for Malikis and Shafi'is, and a strongly emphasized recommendation for Ja'faris during the occultation."},
        },
        "by_madhab": {
            "ar": {"maliki": {"very_short": "فرض كفاية", "short": "فرض كفاية على أهل الحي، سنة مؤكدة للفرد", "full": "فرض كفاية على أهل الحي؛ وفي حق الفرد الواحد سنة مؤكدة لا يُكره تركها إلا لمن واظب عليه."},
                    "shafii": {"very_short": "سنة مؤكدة", "short": "فرض كفاية على المجتمع، سنة مؤكدة للفرد", "full": "فرض كفاية على المجتمع ككل، وسنة مؤكدة في حق الفرد؛ وهو الأصح في المذهب."},
                    "hanafi": {"very_short": "واجب", "short": "واجبة على كل رجل حر بالغ عاقل", "full": "واجبة وجوباً غير ملزم على كل رجل حر بالغ عاقل قادر؛ وتركها بلا عذر مكروه تحريماً عند المتأخرين."},
                    "hanbali": {"very_short": "فرض عين", "short": "فرض عين على كل رجل قادر", "full": "فرض عين على كل رجل مكلف قادر؛ لا يجوز تركها إلا لعذر شرعي معتبر."},
                    "dhahiri": {"very_short": "فرض عين", "short": "فرض عين؛ ظاهر الأمر النبوي يقتضي الوجوب", "full": "فرض عين أخذاً بظاهر الأمر النبوي بالمحافظة عليها، دون تأويل يصرفه عن الوجوب."},
                    "jafari": {"very_short": "مستحب مؤكد", "short": "مستحبة استحباباً مؤكداً في زمن الغيبة", "full": "مستحبة استحباباً مؤكداً وليست واجبة عيناً في زمن الغيبة الكبرى، وثوابها عظيم."},
                    "zaydi": {"very_short": "فرض كفاية", "short": "قريب من رأي أهل السنة في تأكيدها", "full": "فرض كفاية، ويقترب الرأي الزيدي من الرأي السني في التأكيد على المحافظة عليها جماعة."},
                    "ibadi": {"very_short": "سنة مؤكدة", "short": "من أعلام الدين ولا تُترك باستمرار", "full": "من أعلام الدين الظاهرة، سنة مؤكدة لا ينبغي تركها باستمرار وإن لم تكن شرطاً لصحة الصلاة."}},
            "en": {"maliki": {"very_short": "Communal obligation", "short": "Communal obligation on the neighborhood; individually recommended", "full": "A communal obligation (fard kifayah) upon the residents of a locality; for a single individual it is a strongly recommended sunnah that should not habitually be abandoned."},
                    "shafii": {"very_short": "Strongly recommended", "short": "Communal obligation for society, recommended for individuals", "full": "A communal obligation on society as a whole, and a strongly recommended sunnah for the individual — this is the preferred view in the school."},
                    "hanafi": {"very_short": "Obligatory", "short": "Obligatory upon every free, adult, sane man", "full": "A binding-but-not-absolute obligation upon every free, adult, sane, capable man; later scholars held that abandoning it without excuse is strongly disliked."},
                    "hanbali": {"very_short": "Individual obligation", "short": "Individual obligation on every capable man", "full": "An individual obligation (fard 'ayn) upon every legally responsible, capable man; it may not be abandoned except for a recognized valid excuse."},
                    "dhahiri": {"very_short": "Individual obligation", "short": "Individual obligation, based on the literal prophetic command", "full": "An individual obligation, based on the literal wording of the prophetic command to maintain it, without interpretation that would remove the obligation."},
                    "jafari": {"very_short": "Strongly recommended", "short": "Strongly recommended during the occultation", "full": "Strongly recommended, though not an individual obligation during the Major Occultation; its reward is considered immense."},
                    "zaydi": {"very_short": "Communal obligation", "short": "Close to the Sunni emphasis on its importance", "full": "A communal obligation; the Zaydi view is close to the Sunni emphasis on maintaining it in congregation."},
                    "ibadi": {"very_short": "Strongly recommended", "short": "A prominent mark of the religion, not to be habitually left", "full": "A prominent outward mark of the religion; a strongly recommended sunnah that should not be habitually abandoned, though it is not a condition for the prayer's validity."}},
        },
    },
    {
        "id": 2, "topic": "muamalat",
        "keywords": {"ar": ["زكاة", "أسهم", "استثمار", "تجارة", "نصاب", "مال"],
                      "en": ["zakat", "stocks", "shares", "investment", "trade", "nisab"]},
        "t": {
            "ar": {"title": "زكاة الأسهم", "very_short": "واجبة",
                    "short": "زكاة الأسهم واجبة إذا بلغت النصاب",
                    "full": "تجب زكاة الأسهم إذا كانت للاستثمار والتجارة، وبلغت قيمتها النصاب (85 جرام ذهب)، وتُحسب بقيمتها السوقية في نهاية الحول، ويُخرج 2.5% من قيمتها."},
            "en": {"title": "Zakat on Stocks", "very_short": "Obligatory",
                    "short": "Zakat on stocks is due once they reach the nisab threshold",
                    "full": "Zakat on stocks is due when they are held for investment or trading purposes and their value reaches the nisab (equivalent to 85 grams of gold); it is calculated on their market value at the end of the zakat year, with 2.5% payable."},
        },
    },
    {
        "id": 3, "topic": "ibadat",
        "keywords": {"ar": ["جمع", "سفر", "مسافر", "صلاة", "تخفيف", "رخصة"],
                      "en": ["combine", "travel", "traveler", "prayer", "concession"]},
        "t": {
            "ar": {"title": "الجمع في السفر", "very_short": "جائز",
                    "short": "يجوز جمع الصلاة في السفر للمسافر",
                    "full": "يجوز للمسافر جمع صلاة الظهر مع العصر، والمغرب مع العشاء، تقديماً أو تأخيراً، في وقت إحداهما، وذلك تخفيفاً من الله تعالى على المسافرين."},
            "en": {"title": "Combining Prayers While Traveling", "very_short": "Permitted",
                    "short": "A traveler may combine prayers while on a journey",
                    "full": "A traveler is permitted to combine the noon and afternoon prayers, and the sunset and night prayers, either bringing the later one forward or delaying the earlier one, as an ease granted by Allah to travelers."},
        },
    },
    {
        "id": 4, "topic": "ibadat",
        "keywords": {"ar": ["وضوء", "نواقض", "طهارة", "بول", "غائط", "نوم", "مس"],
                      "en": ["wudu", "ablution", "nullifiers", "purity", "sleep"]},
        "t": {
            "ar": {"title": "نواقض الوضوء", "very_short": "مبطل",
                    "short": "نواقض الوضوء تبطل الطهارة وتوجب إعادته",
                    "full": "نواقض الوضوء هي: الخارج من السبيلين (البول، الغائط، الريح)، النوم المستغرق، زوال العقل (بإغماء أو سكر)، مسّ الفرج بغير حائل، ولمس المرأة بشهوة عند بعض المذاهب."},
            "en": {"title": "Nullifiers of Ablution (Wudu)", "very_short": "Invalidating",
                    "short": "These acts invalidate wudu and require it to be repeated",
                    "full": "The nullifiers of wudu include: what exits the two passages (urine, stool, wind), deep sleep, loss of consciousness (through fainting or intoxication), touching the private parts directly, and — according to some schools — touching a woman with desire."},
        },
    },
    {
        "id": 5, "topic": "muamalat",
        "keywords": {"ar": ["ربا", "حرام", "قرض", "فائدة", "بنوك", "معاملة"],
                      "en": ["riba", "usury", "interest", "loan", "bank", "forbidden"]},
        "t": {
            "ar": {"title": "الربا", "very_short": "حرام",
                    "short": "الربا من كبائر الذنوب ومحرم قطعاً",
                    "full": "الربا محرم بنص القرآن والسنة، وهو كل زيادة مشروطة في القرض أو المعاملة، سواء كانت نقدية أو عينية. الربا من السبع الموبقات."},
            "en": {"title": "Riba (Usury/Interest)", "very_short": "Forbidden",
                    "short": "Riba is a major sin, definitively forbidden",
                    "full": "Riba is forbidden by explicit texts of the Qur'an and Sunnah; it is any stipulated increase in a loan or transaction, whether monetary or in kind. Riba is counted among the seven grave destructive sins."},
        },
    },
    {
        "id": 6, "topic": "ibadat",
        "keywords": {"ar": ["سفر", "مسافر", "صلاة", "قصر", "جمع", "تخفيف", "رخصة"],
                      "en": ["travel", "traveler", "prayer", "shorten", "concession"]},
        "t": {
            "ar": {"title": "صلاة المسافر", "very_short": "جائز",
                    "short": "يجوز للمسافر قصر الصلاة وجمعها",
                    "full": "يجوز للمسافر قصر الصلاة الرباعية (الظهر، العصر، العشاء) إلى ركعتين، وجمع الصلاة (الظهر مع العصر، والمغرب مع العشاء). هذه رخصة من الله للتخفيف على المسافرين."},
            "en": {"title": "The Traveler's Prayer", "very_short": "Permitted",
                    "short": "A traveler may shorten and combine prayers",
                    "full": "A traveler is permitted to shorten the four-rak'ah prayers (noon, afternoon, night) to two rak'ahs, and to combine prayers (noon with afternoon, sunset with night). This is a concession from Allah to ease the journey for travelers."},
        },
    },
]

# =========================================================
# GLOSSARY
# =========================================================
GLOSSARY = [
    {"ar": {"term": "الفرض / فرض العين", "definition": "ما طلب الشارع فعله طلباً جازماً من كل مكلف بعينه، يُثاب فاعله ويُعاقب تاركه."},
      "en": {"term": "Fard / Fard 'Ayn (Individual Obligation)", "definition": "An act the Lawgiver has decisively commanded every legally responsible individual to perform; its performer is rewarded and its abandoner is sinful."}},
    {"ar": {"term": "فرض الكفاية", "definition": "ما طلب الشارع فعله من عموم المكلفين، يسقط الإثم عن الجميع بفعل البعض، ويأثم الكل إن تركوه جميعاً."},
      "en": {"term": "Fard Kifayah (Communal Obligation)", "definition": "An act commanded of the community at large; if enough people perform it, the obligation is lifted from everyone else, but if all abandon it, all are sinful."}},
    {"ar": {"term": "الواجب", "definition": "عند جمهور الفقهاء مرادف للفرض؛ وعند الحنفية: ما ثبت بدليل ظني دون قطعي."},
      "en": {"term": "Wajib (Obligatory)", "definition": "Synonymous with fard for most jurists; for the Hanafis, it denotes what is established by a probable (rather than definitive) proof."}},
    {"ar": {"term": "السنة المؤكدة", "definition": "ما واظب النبي ﷺ على فعله غالباً، ويُكره تركه بلا عذر عند أكثر الفقهاء."},
      "en": {"term": "Sunnah Mu'akkadah (Emphasized Sunnah)", "definition": "An act the Prophet ﷺ regularly performed; most jurists hold that abandoning it without excuse is disliked."}},
    {"ar": {"term": "المستحب (المندوب)", "definition": "ما رغّب الشارع في فعله دون إلزام، يُثاب فاعله ولا يُعاقب تاركه. والمندوب اسم آخر له عند أكثر الفقهاء."},
      "en": {"term": "Mustahabb / Mandub (Recommended)", "definition": "An act the Lawgiver has encouraged without obligation; its performer is rewarded but its abandoner is not sinful."}},
    {"ar": {"term": "المكروه", "definition": "ما طلب الشارع تركه طلباً غير جازم، يُثاب تاركه ولا يُعاقب فاعله."},
      "en": {"term": "Makruh (Disliked)", "definition": "An act the Lawgiver has non-decisively asked to be avoided; its avoider is rewarded and its performer is not sinful."}},
    {"ar": {"term": "الحرام", "definition": "ما طلب الشارع تركه طلباً جازماً بنص قطعي، يُعاقب فاعله ويُثاب تاركه."},
      "en": {"term": "Haram (Forbidden)", "definition": "An act the Lawgiver has decisively prohibited by a definitive text; its performer is sinful and its avoider is rewarded."}},
]

# =========================================================
# IMAMS (proper names kept transliterated for non-Arabic UI)
# =========================================================
IMAMS = [
    {"ar_name": "الإمام مالك بن أنس الأصبحي", "en_name": "Imam Malik ibn Anas al-Asbahi", "madhab": "maliki",
      "lifespan": "93 - 179 AH", "birthplace": {"ar": "المدينة المنورة", "en": "Medina"},
      "founding_place": {"ar": "المدينة المنورة", "en": "Medina"},
      "scholars": {"ar": "ابن القاسم، سحنون، ابن رشد، القرافي، خليل بن إسحاق",
                    "en": "Ibn al-Qasim, Sahnun, Ibn Rushd, al-Qarafi, Khalil ibn Ishaq"}},
    {"ar_name": "الإمام محمد بن إدريس الشافعي", "en_name": "Imam Muhammad ibn Idris al-Shafi'i", "madhab": "shafii",
      "lifespan": "150 - 204 AH", "birthplace": {"ar": "غزة", "en": "Gaza"},
      "founding_place": {"ar": "بغداد ثم مصر (المذهب الجديد)", "en": "Baghdad, then Egypt (the 'new' school)"},
      "scholars": {"ar": "المزني، البويطي، النووي، ابن حجر الهيتمي، الرافعي",
                    "en": "al-Muzani, al-Buwayti, al-Nawawi, Ibn Hajar al-Haytami, al-Rafi'i"}},
    {"ar_name": "الإمام أحمد بن حنبل الشيباني", "en_name": "Imam Ahmad ibn Hanbal al-Shaybani", "madhab": "hanbali",
      "lifespan": "164 - 241 AH", "birthplace": {"ar": "بغداد", "en": "Baghdad"},
      "founding_place": {"ar": "بغداد", "en": "Baghdad"},
      "scholars": {"ar": "أبو بكر الخلال، ابن قدامة، ابن تيمية، ابن القيم، محمد بن عبد الوهاب",
                    "en": "Abu Bakr al-Khallal, Ibn Qudamah, Ibn Taymiyyah, Ibn al-Qayyim, Muhammad ibn Abd al-Wahhab"}},
    {"ar_name": "الإمام أبو حنيفة النعمان بن ثابت", "en_name": "Imam Abu Hanifah al-Nu'man ibn Thabit", "madhab": "hanafi",
      "lifespan": "80 - 150 AH", "birthplace": {"ar": "الكوفة", "en": "Kufa"},
      "founding_place": {"ar": "الكوفة", "en": "Kufa"},
      "scholars": {"ar": "أبو يوسف، محمد بن الحسن الشيباني، الطحاوي، الكاساني، ابن عابدين",
                    "en": "Abu Yusuf, Muhammad ibn al-Hasan al-Shaybani, al-Tahawi, al-Kasani, Ibn Abidin"}},
    {"ar_name": "الإمام داود بن علي الأصفهاني", "en_name": "Imam Dawud ibn Ali al-Isfahani", "madhab": "dhahiri",
      "lifespan": "202 - 270 AH", "birthplace": {"ar": "الكوفة", "en": "Kufa"},
      "founding_place": {"ar": "بغداد", "en": "Baghdad"},
      "scholars": {"ar": "ابن حزم الأندلسي (أشهر من دوّنه في «المحلى»)",
                    "en": "Ibn Hazm al-Andalusi (its most famous codifier, in al-Muhalla)"}},
    {"ar_name": "الإمام جعفر بن محمد الصادق", "en_name": "Imam Ja'far ibn Muhammad al-Sadiq", "madhab": "jafari",
      "lifespan": "80 - 148 AH", "birthplace": {"ar": "المدينة المنورة", "en": "Medina"},
      "founding_place": {"ar": "المدينة المنورة", "en": "Medina"},
      "scholars": {"ar": "الشيخ المفيد، الشريف المرتضى، الشيخ الطوسي، المحقق الحلي، السيد الخميني، السيد السيستاني",
                    "en": "Shaykh al-Mufid, al-Sharif al-Murtada, Shaykh al-Tusi, al-Muhaqqiq al-Hilli, Sayyid Khomeini, Sayyid al-Sistani"}},
    {"ar_name": "الإمام زيد بن علي بن الحسين", "en_name": "Imam Zayd ibn Ali ibn al-Husayn", "madhab": "zaydi",
      "lifespan": "80 - 122 AH", "birthplace": {"ar": "المدينة المنورة", "en": "Medina"},
      "founding_place": {"ar": "الكوفة", "en": "Kufa"},
      "scholars": {"ar": "أبو خالد الواسطي، الناصر الأطروش، الهادي يحيى بن الحسين، الإمام المنصور بالله",
                    "en": "Abu Khalid al-Wasiti, al-Nasir al-Utrush, al-Hadi Yahya ibn al-Husayn, al-Mansur billah"}},
    {"ar_name": "الإمام جابر بن زيد الأزدي", "en_name": "Imam Jabir ibn Zayd al-Azdi", "madhab": "ibadi",
      "lifespan": "1st century - 93 AH", "birthplace": {"ar": "نزوى، عُمان", "en": "Nizwa, Oman"},
      "founding_place": {"ar": "البصرة", "en": "Basra"},
      "scholars": {"ar": "أبو سعيد الكدمي، أبو نزار الخروصي، نور الدين السالمي، الشيخ أحمد الخليلي",
                    "en": "Abu Sa'id al-Kudami, Abu Nizar al-Kharusi, Nur al-Din al-Salimi, Shaykh Ahmad al-Khalili"}},
]

# =========================================================
# COUNTRIES
# =========================================================
COUNTRIES = [
    {"flag": "🇸🇦", "name": {"ar": "السعودية", "en": "Saudi Arabia"}, "madhab": "hanbali", "population": "36.4M"},
    {"flag": "🇪🇬", "name": {"ar": "مصر", "en": "Egypt"}, "madhab": "shafii", "population": "112.7M"},
    {"flag": "🇲🇦", "name": {"ar": "المغرب", "en": "Morocco"}, "madhab": "maliki", "population": "37.8M"},
    {"flag": "🇹🇷", "name": {"ar": "تركيا", "en": "Turkey"}, "madhab": "hanafi", "population": "87.5M"},
    {"flag": "🇮🇷", "name": {"ar": "إيران", "en": "Iran"}, "madhab": "jafari", "population": "89.8M"},
    {"flag": "🇴🇲", "name": {"ar": "عُمان", "en": "Oman"}, "madhab": "ibadi", "population": "4.7M"},
]

# =========================================================
# HELPERS
# =========================================================


def cl(lang):
    """Content language: use lang if fully translated, else fall back to English."""
    return lang if lang in CONTENT_LANGS else "en"


def madhab_name(key, lang):
    return MADHHAB_NAMES.get(key, {}).get(lang, key)


def topic_name(key, lang):
    return TOPICS.get(key, {}).get(lang, key)


def search_issues(query, topic_filter, selected_madhab_key, level, lang):
    language = cl(lang)
    if not query:
        return []
    q = query.strip().lower()
    matches = []
    for issue in ISSUES:
        if topic_filter != "all" and issue["topic"] != topic_filter:
            continue
        tr = issue["t"].get(language, issue["t"]["en"])
        kw = issue["keywords"].get(language, issue["keywords"]["en"])
        text_pool = (tr["title"] + " " + " ".join(kw) + " " + tr["full"]).lower()
        if q in text_pool:
            matches.append(issue)

    if not matches:
        words = re.findall(r"\w+", q)
        for issue in ISSUES:
            if topic_filter != "all" and issue["topic"] != topic_filter:
                continue
            tr = issue["t"].get(language, issue["t"]["en"])
            kw = issue["keywords"].get(language, issue["keywords"]["en"])
            text_pool = (tr["title"] + " " + " ".join(kw)).lower()
            if any(w in text_pool for w in words):
                matches.append(issue)

    results = []
    for issue in matches:
        tr = issue["t"].get(language, issue["t"]["en"])
        by_madhab = issue.get("by_madhab", {}).get(language, {})
        per_madhab = by_madhab.get(selected_madhab_key)
        if per_madhab:
            answer = per_madhab.get(level, per_madhab.get("full"))
            note = f"{t('note_madhab', lang)} {madhab_name(selected_madhab_key, lang)}"
        else:
            answer = tr.get(level, tr["full"])
            note = t("note_general", lang)
        results.append({"title": tr["title"], "topic": topic_name(issue["topic"], lang), "answer": answer, "note": note})
    return results


# =========================================================
# LANGUAGE SELECTOR (top of page, always LTR-safe control)
# =========================================================
if "lang" not in st.session_state:
    st.session_state.lang = "ar"

top_l, top_r = st.columns([5, 1])
with top_r:
    lang = st.selectbox(
        t("language_label", st.session_state.lang),
        options=LANGS,
        index=LANGS.index(st.session_state.lang),
        format_func=lambda code: LANG_META[code]["name"],
        key="lang_selector",
    )
st.session_state.lang = lang
meta = LANG_META[lang]
DIR = meta["dir"]
FONT = meta["font"]

# =========================================================
# GLOBAL STYLE (direction-aware; title always centered)
# =========================================================
st.markdown(
    f"""
    <style>
    .stApp, .stApp * {{
        direction: {DIR};
        font-family: {FONT};
    }}
    .stApp p, .stApp li, .stApp label, .stApp span, .stApp div {{
        text-align: {"right" if DIR == "rtl" else "left"};
    }}
    .main-title-block {{
        text-align: center !important;
    }}
    .main-title-block * {{
        text-align: center !important;
    }}
    .stRadio > div, .stMultiSelect > div, .stTabs {{
        direction: {DIR};
    }}
    div[data-baseweb="radio"] label, div[data-baseweb="select"] {{
        direction: {DIR};
    }}
    .stButton button {{
        width: 100%;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# HEADER — main title centered regardless of language direction
# =========================================================
st.markdown(
    f"""
    <div class="main-title-block" style="padding: 20px 0; background: linear-gradient(145deg, #0f231c, #2a5c4a); color: white; border-radius: 16px; margin-bottom: 25px;">
        <h1 style="font-size: 2.3rem; margin: 0;">📖 {t('app_title', lang)}</h1>
        <p style="font-size: 1rem; color: #d6e4de; margin: 6px 0 0;">{t('app_subtitle', lang)}</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if lang not in CONTENT_LANGS and t("content_fallback_note", lang):
    st.info(t("content_fallback_note", lang))

# =========================================================
# SECTION 1 — SEARCH (cumulative sub-parts within one expander)
# =========================================================
with st.expander(t("search_section_title", lang), expanded=True):

    st.markdown(f"#### {t('step1_title', lang)}")
    group_keys = list(MADHHAB_GROUPS.keys())
    madhab_group = st.radio(
        t("step1_group_prompt", lang),
        group_keys,
        format_func=lambda k: GROUP_LABELS[k][lang],
        horizontal=True,
        label_visibility="collapsed",
        key="madhab_group",
    )

    sub_options = MADHHAB_GROUPS[madhab_group]
    if len(sub_options) > 1:
        selected_madhab = st.radio(
            t("step1_pick_prompt", lang),
            sub_options,
            format_func=lambda k: madhab_name(k, lang),
            horizontal=True,
            key="madhab_pick",
        )
    else:
        selected_madhab = sub_options[0]
        st.caption(f"{t('selected_madhab_caption', lang)} **{madhab_name(selected_madhab, lang)}**")

    st.markdown("---")
    st.markdown(f"#### {t('step2_title', lang)}")
    topic_keys = TOPIC_ORDER
    topic = st.radio(
        t("step2_prompt", lang),
        topic_keys,
        format_func=lambda k: topic_name(k, lang),
        horizontal=True,
        label_visibility="collapsed",
        key="topic_pick",
    )

    st.markdown("---")
    st.markdown(f"#### {t('step3_title', lang)}")
    level_keys = ["very_short", "short", "full"]
    level_label_map = {"very_short": t("level_very_short", lang), "short": t("level_short", lang), "full": t("level_full", lang)}
    level = st.radio(
        t("step3_prompt", lang),
        level_keys,
        format_func=lambda k: level_label_map[k],
        horizontal=True,
        label_visibility="collapsed",
        key="level_pick",
    )

    st.markdown("---")
    st.markdown(f"#### {t('step4_title', lang)}")
    question = st.text_input(
        t("step4_title", lang),
        placeholder=t("question_placeholder", lang),
        label_visibility="collapsed",
        key="question_input",
    )
    search_clicked = st.button(t("search_button", lang), use_container_width=True)

    st.markdown("---")
    st.markdown(f"#### {t('step5_title', lang)}")
    if search_clicked and question:
        results = search_issues(question, topic, selected_madhab, level, lang)
        if results:
            for r in results:
                with st.container(border=True):
                    st.markdown(f"**📌 {r['title']}** &nbsp;·&nbsp; _{r['topic']}_")
                    st.markdown(f"### {r['answer']}")
                    st.caption(r["note"])
                    st.caption(t("fatwa_disclaimer", lang))
        else:
            st.warning(t("no_results", lang))
    elif search_clicked:
        st.info(t("empty_question", lang))
    else:
        st.caption(t("empty_placeholder", lang))

# =========================================================
# SECTION 2 — RESOURCES (cumulative sub-parts as tabs inside one expander)
# =========================================================
with st.expander(t("resources_section_title", lang), expanded=False):

    tab_imams, tab_countries, tab_glossary, tab_comments = st.tabs(
        [t("tab_imams", lang), t("tab_countries", lang), t("tab_glossary", lang), t("tab_comments", lang)]
    )

    with tab_imams:
        language = cl(lang)
        for imam in IMAMS:
            name = imam["ar_name"] if language == "ar" else imam["en_name"]
            school = madhab_name(imam["madhab"], lang)
            birthplace = imam["birthplace"].get(language, imam["birthplace"]["en"])
            founding_place = imam["founding_place"].get(language, imam["founding_place"]["en"])
            scholars = imam["scholars"].get(language, imam["scholars"]["en"])
            st.markdown(
                f"""
                <div style="background:#f5f7f5; padding:12px 16px; border-radius:12px; margin-bottom:10px; border-{"right" if DIR=="rtl" else "left"}:4px solid #d4a854;">
                    <h4 style="margin:0; color:#1e3a2f;">{name}</h4>
                    <p style="margin:2px 0; color:#d4a854; font-weight:600;">{school} &nbsp;|&nbsp; {imam['lifespan']}</p>
                    <p style="margin:2px 0; color:#3d4f5f;">{t('birthplace_label', lang)}: {birthplace} &nbsp;·&nbsp; {t('founding_place_label', lang)}: {founding_place}</p>
                    <p style="margin:4px 0 0; color:#3d4f5f;">{t('scholars_label', lang)}: {scholars}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with tab_countries:
        language = cl(lang)
        cols = st.columns(3)
        for i, c in enumerate(COUNTRIES):
            with cols[i % 3]:
                country_name = c["name"].get(language, c["name"]["en"])
                st.markdown(
                    f"""
                    <div style="background:#f5f7f5; padding:8px 12px; border-radius:8px; margin-bottom:6px; border-{"right" if DIR=="rtl" else "left"}:3px solid #d4a854;">
                        <strong>{c['flag']} {country_name}</strong><br>
                        <span style="color:#d4a854;">{t('official_madhab_label', lang)}: {madhab_name(c['madhab'], lang)}</span><br>
                        <span style="font-size:0.8rem; color:#6a7f78;">{t('population_label', lang)}: {c['population']}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    with tab_glossary:
        language = cl(lang)
        for term in GLOSSARY:
            tr = term.get(language, term["en"])
            st.markdown(
                f"""
                <div style="background:#f5f7f5; padding:12px 16px; border-radius:12px; margin-bottom:10px; border-{"right" if DIR=="rtl" else "left"}:4px solid #1e3a2f;">
                    <h4 style="margin:0; color:#1e3a2f;">{tr['term']}</h4>
                    <p style="margin:4px 0 0; color:#3d4f5f;">{tr['definition']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with tab_comments:
        if "session_comments" not in st.session_state:
            st.session_state.session_comments = []

        rating = st.slider(t("rating_label", lang), 1, 5, 5)
        comment_text = st.text_area(t("comment_area_label", lang), placeholder=t("comment_placeholder", lang))
        if st.button(t("submit_comment", lang)):
            if comment_text.strip():
                st.session_state.session_comments.append({"text": comment_text.strip(), "rating": rating})
                st.success(t("comment_success", lang))
            else:
                st.warning(t("comment_warning", lang))

        if st.session_state.session_comments:
            st.markdown(f"**{t('session_comments_title', lang)}**")
            for c in st.session_state.session_comments:
                st.markdown(f"- {'⭐' * c['rating']} — {c['text']}")
        st.caption(t("comments_note", lang))

# =========================================================
# FOOTER
# =========================================================
st.markdown(
    f"""
    <div style="text-align:center; padding:16px 0; color:#6a7f78;">
        <p>{t('footer_text', lang)}</p>
        <p style="font-size:0.8rem; margin-top:6px;">© 2024 {t('app_title', lang)}</p>
    </div>
    """,
    unsafe_allow_html=True,
)
