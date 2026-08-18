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

LANGS = {"العربية": "ar", "English": "en", "Français": "fr"}

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
}

MADHHAB_NAMES = {
    "maliki": {"ar": "مالكي", "en": "Maliki", "fr": "Malikite"},
    "shafii": {"ar": "شافعي", "en": "Shafi'i", "fr": "Chaféite"},
    "hanafi": {"ar": "حنفي", "en": "Hanafi", "fr": "Hanafite"},
    "hanbali": {"ar": "حنبلي", "en": "Hanbali", "fr": "Hanbalite"},
    "zahiri": {"ar": "ظاهري", "en": "Zahiri", "fr": "Zahirite"},
    "jafari": {"ar": "جعفري", "en": "Ja'fari", "fr": "Jaafarite"},
    "zaidi": {"ar": "زيدي", "en": "Zaidi", "fr": "Zaydite"},
    "ibadi": {"ar": "إباضي", "en": "Ibadi", "fr": "Ibadite"},
}

GROUPS = {
    "sunni": {"ar": "مذاهب السنة", "en": "Sunni Schools", "fr": "Écoles sunnites",
              "members": ["maliki", "shafii", "hanafi", "hanbali", "zahiri"]},
    "shia": {"ar": "مذاهب الشيعة", "en": "Shia Schools", "fr": "Écoles chiites",
             "members": ["jafari", "zaidi"]},
    "ibadi": {"ar": "المذهب الإباضي", "en": "Ibadi School", "fr": "École ibadite",
              "members": ["ibadi"]},
}

TOPICS = {
    "ibadat": {"ar": "العبادات", "en": "Acts of Worship", "fr": "Actes d'adoration"},
    "muamalat": {"ar": "المعاملات", "en": "Transactions", "fr": "Transactions"},
    "family": {"ar": "الأسرة", "en": "Family", "fr": "Famille"},
    "other": {"ar": "مواضيع أخرى", "en": "Other Topics", "fr": "Autres sujets"},
}

LEVELS = {
    "very_short": {"ar": "مختصرة (كلمة)", "en": "Very short (one word)", "fr": "Très bref (un mot)"},
    "short": {"ar": "مبسطة (سطر)", "en": "Short (one line)", "fr": "Bref (une ligne)"},
    "full": {"ar": "مفصل (أكثر من سطر)", "en": "Detailed (full)", "fr": "Détaillé (complet)"},
}

# --- Issues ---------------------------------------------------------------

ISSUES = [
    {
        "id": 1, "topic": "ibadat",
        "title": {"ar": "صلاة الجماعة", "en": "Congregational Prayer", "fr": "La prière en congrégation"},
        "keywords": {
            "ar": ["جماعة", "مسجد", "رجال", "صلاة", "فرض", "سنة", "واجب"],
            "en": ["congregation", "mosque", "men", "prayer", "obligatory", "sunnah"],
            "fr": ["congrégation", "mosquée", "hommes", "prière", "obligatoire", "sunna"],
        },
        "rulings": {
            "ar": {"very_short": "سنة مؤكدة", "short": "سنة مؤكدة عند الجمهور، واجبة عند الحنفية",
                   "full": "تجب صلاة الجماعة في المسجد على الرجال عند جمهور الفقهاء؛ فهي فرض عين عند الحنابلة، واجب مؤكد عند الحنفية، فرض كفاية عند المالكية والشافعية، ومستحبة تأكيداً عند الجعفرية في زمن الغيبة."},
            "en": {"very_short": "Emphasized Sunnah", "short": "Emphasized sunnah for most jurists, obligatory for the Hanafis",
                   "full": "Congregational prayer in the mosque is required of men according to the majority of jurists: an individual obligation for the Hanbalis, an emphasized obligation for the Hanafis, a communal obligation for the Malikis and Shafi'is, and a strongly recommended act for the Ja'faris during the Occultation."},
            "fr": {"very_short": "Sunna fortement recommandée", "short": "Sunna fortement recommandée pour la majorité, obligatoire pour les hanafites",
                   "full": "La prière en congrégation à la mosquée est requise des hommes selon la majorité des juristes : obligation individuelle chez les hanbalites, obligation appuyée chez les hanafites, obligation collective chez les malikites et les chaféites, et acte fortement recommandé chez les jaafarites durant l'Occultation."},
        },
        "rulings_by_madhab": {
            "maliki": {
                "ar": {"very_short": "فرض كفاية", "short": "فرض كفاية على أهل الحي، سنة مؤكدة للفرد",
                       "full": "فرض كفاية على أهل الحي؛ وفي حق الفرد الواحد سنة مؤكدة لا يُكره تركها إلا لمن واظب عليه."},
                "en": {"very_short": "Fard Kifayah", "short": "Communal obligation on the locality, emphasized sunnah for the individual",
                       "full": "It is a communal obligation (fard kifayah) upon the residents of a locality; for a single individual it is an emphasized sunnah, and abandoning it is disliked only for one who habitually neglects it."},
                "fr": {"very_short": "Fard kifaya", "short": "Obligation collective pour le quartier, sunna appuyée pour l'individu",
                       "full": "C'est une obligation collective (fard kifaya) pour les habitants d'un quartier ; pour un individu seul, c'est une sunna fortement recommandée, et ne pas l'accomplir n'est blâmable que pour celui qui la délaisse habituellement."},
            },
            "shafii": {
                "ar": {"very_short": "سنة مؤكدة", "short": "فرض كفاية على المجتمع، سنة مؤكدة للفرد",
                       "full": "فرض كفاية على المجتمع ككل، وسنة مؤكدة في حق الفرد؛ وهو الأصح في المذهب."},
                "en": {"very_short": "Emphasized Sunnah", "short": "Communal obligation on society, emphasized sunnah for the individual",
                       "full": "It is a communal obligation upon society as a whole, and an emphasized sunnah for the individual — this is the most authoritative view in the school."},
                "fr": {"very_short": "Sunna fortement recommandée", "short": "Obligation collective pour la société, sunna appuyée pour l'individu",
                       "full": "C'est une obligation collective pour la société dans son ensemble, et une sunna fortement recommandée pour l'individu — c'est l'avis le plus correct de l'école."},
            },
            "hanafi": {
                "ar": {"very_short": "واجب", "short": "واجبة على كل رجل حر بالغ عاقل",
                       "full": "واجبة وجوباً غير ملزم على كل رجل حر بالغ عاقل قادر؛ وتركها بلا عذر مكروه تحريماً عند المتأخرين."},
                "en": {"very_short": "Wajib", "short": "Obligatory (wajib) on every free, sane, adult man",
                       "full": "It is obligatory (wajib), one degree below fard, upon every free, sane, adult, capable man; abandoning it without excuse is strongly disliked according to later scholars."},
                "fr": {"very_short": "Wajib", "short": "Obligatoire pour tout homme libre, majeur et sain d'esprit",
                       "full": "C'est une obligation (wajib), un degré en dessous du fard, pour tout homme libre, sain d'esprit, majeur et capable ; l'abandonner sans excuse est fortement blâmable selon les savants tardifs."},
            },
            "hanbali": {
                "ar": {"very_short": "فرض عين", "short": "فرض عين على كل رجل قادر",
                       "full": "فرض عين على كل رجل مكلف قادر؛ لا يجوز تركها إلا لعذر شرعي معتبر."},
                "en": {"very_short": "Fard Ayn", "short": "Individual obligation on every capable man",
                       "full": "It is an individual obligation (fard ayn) upon every legally accountable, capable man; it may not be abandoned except for a recognized legal excuse."},
                "fr": {"very_short": "Fard ayn", "short": "Obligation individuelle pour tout homme capable",
                       "full": "C'est une obligation individuelle (fard ayn) pour tout homme responsable et capable ; elle ne peut être délaissée que pour une excuse légale reconnue."},
            },
            "zahiri": {
                "ar": {"very_short": "فرض عين", "short": "فرض عين؛ ظاهر الأمر النبوي يقتضي الوجوب",
                       "full": "فرض عين أخذاً بظاهر الأمر النبوي بالمحافظة عليها، دون تأويل يصرفه عن الوجوب."},
                "en": {"very_short": "Fard Ayn", "short": "Individual obligation, based on the literal Prophetic command",
                       "full": "It is an individual obligation, taken from the literal wording of the Prophet's command to maintain it, without interpretation that would divert it away from obligation."},
                "fr": {"very_short": "Fard ayn", "short": "Obligation individuelle selon le sens littéral de l'ordre prophétique",
                       "full": "C'est une obligation individuelle, tirée du sens littéral de l'ordre du Prophète de la maintenir, sans interprétation qui la détournerait de l'obligation."},
            },
            "jafari": {
                "ar": {"very_short": "مستحب مؤكد", "short": "مستحبة استحباباً مؤكداً في زمن الغيبة",
                       "full": "مستحبة استحباباً مؤكداً وليست واجبة عيناً في زمن الغيبة الكبرى، وثوابها عظيم."},
                "en": {"very_short": "Strongly recommended", "short": "Strongly recommended during the Occultation, not individually obligatory",
                       "full": "It is strongly recommended rather than individually obligatory during the Major Occultation, and its reward is great."},
                "fr": {"very_short": "Fortement recommandée", "short": "Fortement recommandée durant l'Occultation, non obligatoire individuellement",
                       "full": "Elle est fortement recommandée plutôt qu'individuellement obligatoire durant la Grande Occultation, et sa récompense est immense."},
            },
            "zaidi": {
                "ar": {"very_short": "فرض كفاية", "short": "قريب من رأي أهل السنة في تأكيدها",
                       "full": "فرض كفاية، ويقترب الرأي الزيدي من الرأي السني في التأكيد على المحافظة عليها جماعة."},
                "en": {"very_short": "Fard Kifayah", "short": "Close to the Sunni emphasis on maintaining it",
                       "full": "It is a communal obligation; the Zaidi view is close to the Sunni emphasis on maintaining it in congregation."},
                "fr": {"very_short": "Fard kifaya", "short": "Proche de l'insistance sunnite sur son maintien",
                       "full": "C'est une obligation collective ; l'avis zaydite se rapproche de l'insistance sunnite sur son maintien en congrégation."},
            },
            "ibadi": {
                "ar": {"very_short": "سنة مؤكدة", "short": "من أعلام الدين ولا تُترك باستمرار",
                       "full": "من أعلام الدين الظاهرة، سنة مؤكدة لا ينبغي تركها باستمرار وإن لم تكن شرطاً لصحة الصلاة."},
                "en": {"very_short": "Emphasized Sunnah", "short": "A visible marker of the religion; should not be habitually abandoned",
                       "full": "It is one of the visible markers of the religion, an emphasized sunnah that should not be habitually abandoned, though it is not a condition for the validity of the prayer."},
                "fr": {"very_short": "Sunna fortement recommandée", "short": "Un signe apparent de la religion, à ne pas délaisser habituellement",
                       "full": "C'est l'un des signes apparents de la religion, une sunna fortement recommandée qu'il ne convient pas de délaisser habituellement, bien qu'elle ne soit pas une condition de validité de la prière."},
            },
        },
    },
    {
        "id": 2, "topic": "muamalat",
        "title": {"ar": "زكاة الأسهم", "en": "Zakat on Stocks", "fr": "La zakat sur les actions"},
        "keywords": {
            "ar": ["زكاة", "أسهم", "استثمار", "تجارة", "نصاب", "مال"],
            "en": ["zakat", "stocks", "shares", "investment", "trade", "nisab"],
            "fr": ["zakat", "actions", "investissement", "commerce", "nisab"],
        },
        "rulings": {
            "ar": {"very_short": "واجبة", "short": "زكاة الأسهم واجبة إذا بلغت النصاب",
                   "full": "تجب زكاة الأسهم إذا كانت للاستثمار والتجارة، وبلغت قيمتها النصاب (85 جرام ذهب)، وتُحسب بقيمتها السوقية في نهاية الحول، ويُخرج 2.5% من قيمتها."},
            "en": {"very_short": "Obligatory", "short": "Zakat on stocks is due once it reaches the nisab",
                   "full": "Zakat is due on stocks held for investment or trading once their value reaches the nisab (equivalent to 85 grams of gold); it is calculated on their market value at the end of the zakat year, and 2.5% of that value is paid."},
            "fr": {"very_short": "Obligatoire", "short": "La zakat sur les actions est due dès qu'elle atteint le nisab",
                   "full": "La zakat est due sur les actions détenues pour l'investissement ou le commerce dès que leur valeur atteint le nisab (équivalent à 85 grammes d'or) ; elle est calculée sur la valeur marchande à la fin de l'année zakataire, et 2,5 % de cette valeur est versé."},
        },
    },
    {
        "id": 3, "topic": "ibadat",
        "title": {"ar": "الجمع في السفر", "en": "Combining Prayers While Traveling", "fr": "Regrouper les prières en voyage"},
        "keywords": {
            "ar": ["جمع", "سفر", "مسافر", "صلاة", "تخفيف", "رخصة"],
            "en": ["combine", "travel", "traveler", "prayer", "concession"],
            "fr": ["regrouper", "voyage", "voyageur", "prière", "allègement"],
        },
        "rulings": {
            "ar": {"very_short": "جائز", "short": "يجوز جمع الصلاة في السفر للمسافر",
                   "full": "يجوز للمسافر جمع صلاة الظهر مع العصر، والمغرب مع العشاء، تقديماً أو تأخيراً، في وقت إحداهما، وذلك تخفيفاً من الله تعالى على المسافرين."},
            "en": {"very_short": "Permissible", "short": "A traveler may combine prayers while on a journey",
                   "full": "A traveler is permitted to combine the noon (Dhuhr) with the afternoon (Asr) prayer, and the sunset (Maghrib) with the night (Isha) prayer, performing them early or delayed within the time of either one, as a concession from God to travelers."},
            "fr": {"very_short": "Permis", "short": "Le voyageur peut regrouper les prières durant le voyage",
                   "full": "Il est permis au voyageur de regrouper la prière du Dhuhr avec celle de l'Asr, et celle du Maghrib avec celle de l'Isha, en les avançant ou en les retardant dans le temps de l'une d'elles, comme allègement accordé par Dieu aux voyageurs."},
        },
    },
    {
        "id": 4, "topic": "ibadat",
        "title": {"ar": "نواقض الوضوء", "en": "Nullifiers of Ablution", "fr": "Les annulateurs des ablutions"},
        "keywords": {
            "ar": ["وضوء", "نواقض", "طهارة", "بول", "غائط", "نوم", "مس"],
            "en": ["ablution", "wudu", "nullifiers", "purity", "sleep"],
            "fr": ["ablutions", "wudu", "annulateurs", "pureté", "sommeil"],
        },
        "rulings": {
            "ar": {"very_short": "مبطل", "short": "نواقض الوضوء تبطل الطهارة وتوجب إعادته",
                   "full": "نواقض الوضوء هي: الخارج من السبيلين (البول، الغائط، الريح)، النوم المستغرق، زوال العقل (بإغماء أو سكر)، مسّ الفرج بغير حائل، ولمس المرأة بشهوة عند بعض المذاهب."},
            "en": {"very_short": "Invalidating", "short": "The nullifiers of ablution invalidate purity and require it to be repeated",
                   "full": "The nullifiers of ablution include: what exits from the two private passages (urine, stool, wind), deep sleep, loss of consciousness (through fainting or intoxication), touching the private parts without a barrier, and, according to some schools, touching a woman with desire."},
            "fr": {"very_short": "Invalidant", "short": "Les annulateurs des ablutions invalident la pureté et imposent de la refaire",
                   "full": "Les annulateurs des ablutions sont : ce qui sort des deux voies (urine, selles, vent), le sommeil profond, la perte de conscience (par évanouissement ou ivresse), le toucher des parties intimes sans barrière, et, selon certaines écoles, le toucher d'une femme avec désir."},
        },
    },
    {
        "id": 5, "topic": "muamalat",
        "title": {"ar": "الربا", "en": "Usury / Interest (Riba)", "fr": "L'usure / intérêt (riba)"},
        "keywords": {
            "ar": ["ربا", "حرام", "قرض", "فائدة", "بنوك", "معاملة"],
            "en": ["riba", "usury", "interest", "loan", "banks"],
            "fr": ["riba", "usure", "intérêt", "prêt", "banques"],
        },
        "rulings": {
            "ar": {"very_short": "حرام", "short": "الربا من كبائر الذنوب ومحرم قطعاً",
                   "full": "الربا محرم بنص القرآن والسنة، وهو كل زيادة مشروطة في القرض أو المعاملة، سواء كانت نقدية أو عينية. الربا من السبع الموبقات."},
            "en": {"very_short": "Forbidden", "short": "Riba is among the major sins and is categorically forbidden",
                   "full": "Riba (usury/interest) is forbidden by explicit text of the Qur'an and Sunnah; it is any stipulated increase in a loan or transaction, whether monetary or in kind. It is counted among the seven grave destructive sins."},
            "fr": {"very_short": "Interdit", "short": "Le riba est un péché majeur, formellement interdit",
                   "full": "Le riba (usure/intérêt) est interdit par un texte explicite du Coran et de la Sunna ; c'est tout surplus stipulé dans un prêt ou une transaction, monétaire ou en nature. Il est compté parmi les sept péchés destructeurs majeurs."},
        },
    },
    {
        "id": 6, "topic": "ibadat",
        "title": {"ar": "صلاة المسافر", "en": "The Traveler's Prayer", "fr": "La prière du voyageur"},
        "keywords": {
            "ar": ["سفر", "مسافر", "صلاة", "قصر", "جمع", "تخفيف", "رخصة"],
            "en": ["travel", "traveler", "prayer", "shorten", "combine", "concession"],
            "fr": ["voyage", "voyageur", "prière", "raccourcir", "regrouper", "allègement"],
        },
        "rulings": {
            "ar": {"very_short": "جائز", "short": "يجوز للمسافر قصر الصلاة وجمعها",
                   "full": "يجوز للمسافر قصر الصلاة الرباعية (الظهر، العصر، العشاء) إلى ركعتين، وجمع الصلاة (الظهر مع العصر، والمغرب مع العشاء). هذه رخصة من الله للتخفيف على المسافرين."},
            "en": {"very_short": "Permissible", "short": "A traveler may shorten and combine prayers",
                   "full": "A traveler is permitted to shorten the four-unit prayers (Dhuhr, Asr, Isha) to two units, and to combine prayers (Dhuhr with Asr, and Maghrib with Isha). This is a concession from God to ease the burden on travelers."},
            "fr": {"very_short": "Permis", "short": "Le voyageur peut raccourcir et regrouper les prières",
                   "full": "Il est permis au voyageur de raccourcir les prières à quatre unités (Dhuhr, Asr, Isha) à deux unités, et de regrouper les prières (Dhuhr avec Asr, et Maghrib avec Isha). C'est un allègement accordé par Dieu pour faciliter la tâche aux voyageurs."},
        },
    },
]

# --- Glossary ---------------------------------------------------------------

GLOSSARY = [
    {"term": {"ar": "الفرض / فرض العين", "en": "Fard / Fard Ayn (Individual Obligation)", "fr": "Le fard / fard ayn (Obligation individuelle)"},
     "definition": {"ar": "ما طلب الشارع فعله طلباً جازماً من كل مكلف بعينه، يُثاب فاعله ويُعاقب تاركه.",
                    "en": "What the Lawgiver has decisively commanded every legally accountable individual to perform; one who does it is rewarded, and one who abandons it is sinful.",
                    "fr": "Ce que le Législateur a ordonné de façon décisive à tout individu responsable d'accomplir ; celui qui l'accomplit est récompensé, et celui qui l'abandonne est fautif."}},
    {"term": {"ar": "فرض الكفاية", "en": "Fard Kifayah (Communal Obligation)", "fr": "Fard kifaya (Obligation collective)"},
     "definition": {"ar": "ما طلب الشارع فعله من عموم المكلفين، يسقط الإثم عن الجميع بفعل البعض، ويأثم الكل إن تركوه جميعاً.",
                    "en": "What the Lawgiver has requested from the community at large; if some perform it, the obligation is lifted from all, but if all abandon it, all are sinful.",
                    "fr": "Ce que le Législateur a demandé à la communauté dans son ensemble ; si certains l'accomplissent, l'obligation est levée pour tous, mais si tous l'abandonnent, tous sont fautifs."}},
    {"term": {"ar": "الواجب", "en": "Al-Wajib (The Obligatory)", "fr": "Al-wajib (L'obligatoire)"},
     "definition": {"ar": "عند جمهور الفقهاء مرادف للفرض؛ وعند الحنفية: ما ثبت بدليل ظني دون قطعي.",
                    "en": "For the majority of jurists it is synonymous with fard; for the Hanafis, it is what is established by a probable, non-decisive proof.",
                    "fr": "Pour la majorité des juristes, il est synonyme de fard ; pour les hanafites, c'est ce qui est établi par une preuve probable, non décisive."}},
    {"term": {"ar": "السنة المؤكدة", "en": "Emphasized Sunnah", "fr": "Sunna fortement recommandée"},
     "definition": {"ar": "ما واظب النبي ﷺ على فعله غالباً، ويُكره تركه بلا عذر عند أكثر الفقهاء.",
                    "en": "What the Prophet ﷺ regularly performed; abandoning it without excuse is disliked according to most jurists.",
                    "fr": "Ce que le Prophète ﷺ accomplissait régulièrement ; l'abandonner sans excuse est blâmable selon la plupart des juristes."}},
    {"term": {"ar": "المستحب (المندوب)", "en": "Mustahabb (Recommended)", "fr": "Moustahabb (Recommandé)"},
     "definition": {"ar": "ما رغّب الشارع في فعله دون إلزام، يُثاب فاعله ولا يُعاقب تاركه. والمندوب اسم آخر له عند أكثر الفقهاء.",
                    "en": "What the Lawgiver encouraged without obligation; one who does it is rewarded, and one who abandons it is not sinful.",
                    "fr": "Ce que le Législateur a encouragé sans l'imposer ; celui qui l'accomplit est récompensé, et celui qui l'abandonne n'est pas fautif."}},
    {"term": {"ar": "المكروه", "en": "Al-Makruh (Disliked)", "fr": "Al-makrouh (Blâmable)"},
     "definition": {"ar": "ما طلب الشارع تركه طلباً غير جازم، يُثاب تاركه ولا يُعاقب فاعله.",
                    "en": "What the Lawgiver requested to be avoided in a non-decisive manner; one who avoids it is rewarded, and one who does it is not sinful.",
                    "fr": "Ce que le Législateur a demandé d'éviter de façon non décisive ; celui qui l'évite est récompensé, et celui qui l'accomplit n'est pas fautif."}},
    {"term": {"ar": "الحرام", "en": "Al-Haram (Forbidden)", "fr": "Al-haram (Interdit)"},
     "definition": {"ar": "ما طلب الشارع تركه طلباً جازماً بنص قطعي، يُعاقب فاعله ويُثاب تاركه.",
                    "en": "What the Lawgiver has decisively forbidden by a definitive text; one who does it is sinful, and one who avoids it is rewarded.",
                    "fr": "Ce que le Législateur a interdit de façon décisive par un texte définitif ; celui qui le fait est fautif, et celui qui l'évite est récompensé."}},
]

# --- Imams -------------------------------------------------------------------

IMAMS = [
    {"name": {"ar": "الإمام مالك بن أنس الأصبحي", "en": "Imam Malik ibn Anas al-Asbahi", "fr": "L'imam Malik ibn Anas al-Asbahi"},
     "school": MADHHAB_NAMES["maliki"], "lifespan": "93 - 179 AH",
     "birthplace": {"ar": "المدينة المنورة", "en": "Medina", "fr": "Médine"},
     "founding_place": {"ar": "المدينة المنورة", "en": "Medina", "fr": "Médine"},
     "scholars": {"ar": "ابن القاسم، سحنون، ابن رشد، القرافي، خليل بن إسحاق",
                  "en": "Ibn al-Qasim, Sahnun, Ibn Rushd, al-Qarafi, Khalil ibn Ishaq",
                  "fr": "Ibn al-Qasim, Sahnun, Ibn Rushd, al-Qarafi, Khalil ibn Ishaq"}},
    {"name": {"ar": "الإمام محمد بن إدريس الشافعي", "en": "Imam Muhammad ibn Idris al-Shafi'i", "fr": "L'imam Muhammad ibn Idris al-Chafi'i"},
     "school": MADHHAB_NAMES["shafii"], "lifespan": "150 - 204 AH",
     "birthplace": {"ar": "غزة", "en": "Gaza", "fr": "Gaza"},
     "founding_place": {"ar": "بغداد ثم مصر (المذهب الجديد)", "en": "Baghdad, then Egypt (the new doctrine)", "fr": "Bagdad, puis l'Égypte (la nouvelle doctrine)"},
     "scholars": {"ar": "المزني، البويطي، النووي، ابن حجر الهيتمي، الرافعي",
                  "en": "al-Muzani, al-Buwayti, al-Nawawi, Ibn Hajar al-Haytami, al-Rafi'i",
                  "fr": "al-Muzani, al-Buwayti, al-Nawawi, Ibn Hajar al-Haytami, al-Rafi'i"}},
    {"name": {"ar": "الإمام أحمد بن حنبل الشيباني", "en": "Imam Ahmad ibn Hanbal al-Shaybani", "fr": "L'imam Ahmad ibn Hanbal al-Chaybani"},
     "school": MADHHAB_NAMES["hanbali"], "lifespan": "164 - 241 AH",
     "birthplace": {"ar": "بغداد", "en": "Baghdad", "fr": "Bagdad"},
     "founding_place": {"ar": "بغداد", "en": "Baghdad", "fr": "Bagdad"},
     "scholars": {"ar": "أبو بكر الخلال، ابن قدامة، ابن تيمية، ابن القيم، محمد بن عبد الوهاب",
                  "en": "Abu Bakr al-Khallal, Ibn Qudamah, Ibn Taymiyyah, Ibn al-Qayyim, Muhammad ibn Abd al-Wahhab",
                  "fr": "Abu Bakr al-Khallal, Ibn Qudamah, Ibn Taymiyya, Ibn al-Qayyim, Muhammad ibn Abd al-Wahhab"}},
    {"name": {"ar": "الإمام أبو حنيفة النعمان بن ثابت", "en": "Imam Abu Hanifah al-Nu'man ibn Thabit", "fr": "L'imam Abou Hanifa al-Nu'man ibn Thabit"},
     "school": MADHHAB_NAMES["hanafi"], "lifespan": "80 - 150 AH",
     "birthplace": {"ar": "الكوفة", "en": "Kufa", "fr": "Koufa"},
     "founding_place": {"ar": "الكوفة", "en": "Kufa", "fr": "Koufa"},
     "scholars": {"ar": "أبو يوسف، محمد بن الحسن الشيباني، الطحاوي، الكاساني، ابن عابدين",
                  "en": "Abu Yusuf, Muhammad ibn al-Hasan al-Shaybani, al-Tahawi, al-Kasani, Ibn Abidin",
                  "fr": "Abu Yusuf, Muhammad ibn al-Hasan al-Chaybani, al-Tahawi, al-Kasani, Ibn Abidin"}},
    {"name": {"ar": "الإمام داود بن علي الأصفهاني", "en": "Imam Dawud ibn Ali al-Isfahani", "fr": "L'imam Dawud ibn Ali al-Isfahani"},
     "school": MADHHAB_NAMES["zahiri"], "lifespan": "202 - 270 AH",
     "birthplace": {"ar": "الكوفة", "en": "Kufa", "fr": "Koufa"},
     "founding_place": {"ar": "بغداد", "en": "Baghdad", "fr": "Bagdad"},
     "scholars": {"ar": "ابن حزم الأندلسي (أشهر من دوّنه في «المحلى»)",
                  "en": "Ibn Hazm al-Andalusi (its most famous codifier, in 'al-Muhalla')",
                  "fr": "Ibn Hazm al-Andalusi (son codificateur le plus célèbre, dans « al-Muhalla »)"}},
    {"name": {"ar": "الإمام جعفر بن محمد الصادق", "en": "Imam Ja'far ibn Muhammad al-Sadiq", "fr": "L'imam Ja'far ibn Muhammad al-Sadiq"},
     "school": MADHHAB_NAMES["jafari"], "lifespan": "80 - 148 AH",
     "birthplace": {"ar": "المدينة المنورة", "en": "Medina", "fr": "Médine"},
     "founding_place": {"ar": "المدينة المنورة", "en": "Medina", "fr": "Médine"},
     "scholars": {"ar": "الشيخ المفيد، الشريف المرتضى، الشيخ الطوسي، المحقق الحلي، السيد الخميني، السيد السيستاني",
                  "en": "al-Shaykh al-Mufid, al-Sharif al-Murtada, al-Shaykh al-Tusi, al-Muhaqqiq al-Hilli, Imam Khomeini, al-Sayyid al-Sistani",
                  "fr": "al-Shaykh al-Mufid, al-Charif al-Murtada, al-Shaykh al-Tusi, al-Muhaqqiq al-Hilli, l'imam Khomeini, al-Sayyid al-Sistani"}},
    {"name": {"ar": "الإمام زيد بن علي بن الحسين", "en": "Imam Zayd ibn Ali ibn al-Husayn", "fr": "L'imam Zayd ibn Ali ibn al-Husayn"},
     "school": MADHHAB_NAMES["zaidi"], "lifespan": "80 - 122 AH",
     "birthplace": {"ar": "المدينة المنورة", "en": "Medina", "fr": "Médine"},
     "founding_place": {"ar": "الكوفة", "en": "Kufa", "fr": "Koufa"},
     "scholars": {"ar": "أبو خالد الواسطي، الناصر الأطروش، الهادي يحيى بن الحسين، الإمام المنصور بالله",
                  "en": "Abu Khalid al-Wasiti, al-Nasir al-Utrush, al-Hadi Yahya ibn al-Husayn, Imam al-Mansur billah",
                  "fr": "Abu Khalid al-Wasiti, al-Nasir al-Utrush, al-Hadi Yahya ibn al-Husayn, l'imam al-Mansur billah"}},
    {"name": {"ar": "الإمام جابر بن زيد الأزدي", "en": "Imam Jabir ibn Zayd al-Azdi", "fr": "L'imam Jabir ibn Zayd al-Azdi"},
     "school": MADHHAB_NAMES["ibadi"], "lifespan": "1st century - 93 AH",
     "birthplace": {"ar": "نزوى، عُمان", "en": "Nizwa, Oman", "fr": "Nizwa, Oman"},
     "founding_place": {"ar": "البصرة", "en": "Basra", "fr": "Bassora"},
     "scholars": {"ar": "أبو سعيد الكدمي، أبو نزار الخروصي، نور الدين السالمي، الشيخ أحمد الخليلي",
                  "en": "Abu Sa'id al-Kudami, Abu Nizar al-Kharusi, Nur al-Din al-Salimi, Shaykh Ahmad al-Khalili",
                  "fr": "Abu Sa'id al-Kudami, Abu Nizar al-Kharusi, Nur al-Din al-Salimi, le cheikh Ahmad al-Khalili"}},
]

# --- Countries -----------------------------------------------------------

COUNTRIES = [
    {"flag": "🇸🇦", "name": {"ar": "السعودية", "en": "Saudi Arabia", "fr": "Arabie saoudite"}, "madhab": "hanbali", "population": "36.4M"},
    {"flag": "🇪🇬", "name": {"ar": "مصر", "en": "Egypt", "fr": "Égypte"}, "madhab": "shafii", "population": "112.7M"},
    {"flag": "🇲🇦", "name": {"ar": "المغرب", "en": "Morocco", "fr": "Maroc"}, "madhab": "maliki", "population": "37.8M"},
    {"flag": "🇹🇷", "name": {"ar": "تركيا", "en": "Turkey", "fr": "Turquie"}, "madhab": "hanafi", "population": "87.5M"},
    {"flag": "🇮🇷", "name": {"ar": "إيران", "en": "Iran", "fr": "Iran"}, "madhab": "jafari", "population": "89.8M"},
    {"flag": "🇴🇲", "name": {"ar": "عُمان", "en": "Oman", "fr": "Oman"}, "madhab": "ibadi", "population": "4.7M"},
    {"flag": "🇸🇩", "name": {"ar": "السودان", "en": "Sudan", "fr": "Soudan"}, "madhab": "maliki", "population": "48.1M"},
    {"flag": "🇸🇾", "name": {"ar": "سوريا", "en": "Syria", "fr": "Syrie"}, "madhab": "hanafi", "population": "23.2M"},
    {"flag": "🇵🇰", "name": {"ar": "باكستان", "en": "Pakistan", "fr": "Pakistan"}, "madhab": "hanafi", "population": "240.5M"},
    {"flag": "🇦🇫", "name": {"ar": "أفغانستان", "en": "Afghanistan", "fr": "Afghanistan"}, "madhab": "hanafi", "population": "41.1M"},
    {"flag": "🇲🇾", "name": {"ar": "ماليزيا", "en": "Malaysia", "fr": "Malaisie"}, "madhab": "shafii", "population": "34.3M"},
    {"flag": "🇮🇩", "name": {"ar": "إندونيسيا", "en": "Indonesia", "fr": "Indonésie"}, "madhab": "shafii", "population": "281.2M"},
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
is_rtl = lang == "ar"
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
