```python
import streamlit as st
import re

st.set_page_config(
    page_title="الجامع المختصر لآراء المذاهب",
    page_icon="📖",
    layout="wide",
)

# -----------------------------------------------------------------------
# فرض اتجاه RTL على كامل الواجهة
# -----------------------------------------------------------------------
st.markdown(
    """
    <style>
    .stApp, .stApp * {
        direction: rtl;
        text-align: right;
        font-family: 'Tahoma', 'Segoe UI', sans-serif;
    }
    .stRadio > div, .stMultiSelect > div {
        direction: rtl;
    }
    div[data-baseweb="radio"] label, div[data-baseweb="select"] {
        direction: rtl;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------
# البيانات
# -----------------------------------------------------------------------

issues_data = [
    {
        "id": 1,
        "title": "صلاة الجماعة",
        "topic": "العبادات",
        "keywords": ["جماعة", "مسجد", "رجال", "صلاة", "فرض", "سنة", "واجب"],
        "rulings": {
            "very_short": "سنة مؤكدة",
            "short": "سنة مؤكدة عند الجمهور، واجبة عند الحنفية",
            "full": "تجب صلاة الجماعة في المسجد على الرجال عند جمهور الفقهاء؛ فهي فرض عين عند الحنابلة، واجب مؤكد عند الحنفية، فرض كفاية عند المالكية والشافعية، ومستحبة تأكيداً عند الجعفرية في زمن الغيبة.",
        },
        "rulings_by_madhab": {
            "مالكي": {"very_short": "فرض كفاية", "short": "فرض كفاية على أهل الحي، سنة مؤكدة للفرد", "full": "فرض كفاية على أهل الحي؛ وفي حق الفرد الواحد سنة مؤكدة لا يُكره تركها إلا لمن واظب عليه."},
            "شافعي": {"very_short": "سنة مؤكدة", "short": "فرض كفاية على المجتمع، سنة مؤكدة للفرد", "full": "فرض كفاية على المجتمع ككل، وسنة مؤكدة في حق الفرد؛ وهو الأصح في المذهب."},
            "حنفي": {"very_short": "واجب", "short": "واجبة على كل رجل حر بالغ عاقل", "full": "واجبة وجوباً غير ملزم على كل رجل حر بالغ عاقل قادر؛ وتركها بلا عذر مكروه تحريماً عند المتأخرين."},
            "حنبلي": {"very_short": "فرض عين", "short": "فرض عين على كل رجل قادر", "full": "فرض عين على كل رجل مكلف قادر؛ لا يجوز تركها إلا لعذر شرعي معتبر."},
            "ظاهري": {"very_short": "فرض عين", "short": "فرض عين؛ ظاهر الأمر النبوي يقتضي الوجوب", "full": "فرض عين أخذاً بظاهر الأمر النبوي بالمحافظة عليها، دون تأويل يصرفه عن الوجوب."},
            "جعفري": {"very_short": "مستحب مؤكد", "short": "مستحبة استحباباً مؤكداً في زمن الغيبة", "full": "مستحبة استحباباً مؤكداً وليست واجبة عيناً في زمن الغيبة الكبرى، وثوابها عظيم."},
            "زيدي": {"very_short": "فرض كفاية", "short": "قريب من رأي أهل السنة في تأكيدها", "full": "فرض كفاية، ويقترب الرأي الزيدي من الرأي السني في التأكيد على المحافظة عليها جماعة."},
            "إباضي": {"very_short": "سنة مؤكدة", "short": "من أعلام الدين ولا تُترك باستمرار", "full": "من أعلام الدين الظاهرة، سنة مؤكدة لا ينبغي تركها باستمرار وإن لم تكن شرطاً لصحة الصلاة."},
        },
    },
    {
        "id": 2, "title": "زكاة الأسهم", "topic": "المعاملات",
        "keywords": ["زكاة", "أسهم", "استثمار", "تجارة", "نصاب", "مال"],
        "rulings": {
            "very_short": "واجبة",
            "short": "زكاة الأسهم واجبة إذا بلغت النصاب",
            "full": "تجب زكاة الأسهم إذا كانت للاستثمار والتجارة، وبلغت قيمتها النصاب (85 جرام ذهب)، وتُحسب بقيمتها السوقية في نهاية الحول، ويُخرج 2.5% من قيمتها.",
        },
    },
    {
        "id": 3, "title": "الجمع في السفر", "topic": "العبادات",
        "keywords": ["جمع", "سفر", "مسافر", "صلاة", "تخفيف", "رخصة"],
        "rulings": {
            "very_short": "جائز",
            "short": "يجوز جمع الصلاة في السفر للمسافر",
            "full": "يجوز للمسافر جمع صلاة الظهر مع العصر، والمغرب مع العشاء، تقديماً أو تأخيراً، في وقت إحداهما، وذلك تخفيفاً من الله تعالى على المسافرين.",
        },
    },
    {
        "id": 4, "title": "نواقض الوضوء", "topic": "العبادات",
        "keywords": ["وضوء", "نواقض", "طهارة", "بول", "غائط", "نوم", "مس"],
        "rulings": {
            "very_short": "مبطل",
            "short": "نواقض الوضوء تبطل الطهارة وتوجب إعادته",
            "full": "نواقض الوضوء هي: الخارج من السبيلين (البول، الغائط، الريح)، النوم المستغرق، زوال العقل (بإغماء أو سكر)، مسّ الفرج بغير حائل، ولمس المرأة بشهوة عند بعض المذاهب.",
        },
    },
    {
        "id": 5, "title": "الربا", "topic": "المعاملات",
        "keywords": ["ربا", "حرام", "قرض", "فائدة", "بنوك", "معاملة"],
        "rulings": {
            "very_short": "حرام",
            "short": "الربا من كبائر الذنوب ومحرم قطعاً",
            "full": "الربا محرم بنص القرآن والسنة، وهو كل زيادة مشروطة في القرض أو المعاملة، سواء كانت نقدية أو عينية. الربا من السبع الموبقات.",
        },
    },
    {
        "id": 6, "title": "صلاة المسافر", "topic": "العبادات",
        "keywords": ["سفر", "مسافر", "صلاة", "قصر", "جمع", "تخفيف", "رخصة"],
        "rulings": {
            "very_short": "جائز",
            "short": "يجوز للمسافر قصر الصلاة وجمعها",
            "full": "يجوز للمسافر قصر الصلاة الرباعية (الظهر، العصر، العشاء) إلى ركعتين، وجمع الصلاة (الظهر مع العصر، والمغرب مع العشاء). هذه رخصة من الله للتخفيف على المسافرين.",
        },
    },
]

# مصطلحات رئيسية
glossary_terms = [
    {"term": "الفرض / فرض العين", "definition": "ما طلب الشارع فعله طلباً جازماً من كل مكلف بعينه، يُثاب فاعله ويُعاقب تاركه."},
    {"term": "فرض الكفاية", "definition": "ما طلب الشارع فعله من عموم المكلفين، يسقط الإثم عن الجميع بفعل البعض، ويأثم الكل إن تركوه جميعاً."},
    {"term": "الواجب", "definition": "عند جمهور الفقهاء مرادف للفرض؛ وعند الحنفية: ما ثبت بدليل ظني دون قطعي."},
    {"term": "السنة المؤكدة", "definition": "ما واظب النبي ﷺ على فعله غالباً، ويُكره تركه بلا عذر عند أكثر الفقهاء."},
    {"term": "المستحب (المندوب)", "definition": "ما رغّب الشارع في فعله دون إلزام، يُثاب فاعله ولا يُعاقب تاركه. والمندوب اسم آخر له عند أكثر الفقهاء."},
    {"term": "المكروه", "definition": "ما طلب الشارع تركه طلباً غير جازم، يُثاب تاركه ولا يُعاقب فاعله."},
    {"term": "الحرام", "definition": "ما طلب الشارع تركه طلباً جازماً بنص قطعي، يُعاقب فاعله ويُثاب تاركه."},
]

# الأئمة المؤسسون
imams_data = [
    {"name": "الإمام مالك بن أنس الأصبحي", "school": "المذهب المالكي", "lifespan": "93 - 179هـ", "birthplace": "المدينة المنورة", "founding_place": "المدينة المنورة", "scholars": "ابن القاسم، سحنون، ابن رشد، القرافي، خليل بن إسحاق"},
    {"name": "الإمام محمد بن إدريس الشافعي", "school": "المذهب الشافعي", "lifespan": "150 - 204هـ", "birthplace": "غزة", "founding_place": "بغداد ثم مصر (المذهب الجديد)", "scholars": "المزني، البويطي، النووي، ابن حجر الهيتمي، الرافعي"},
    {"name": "الإمام أحمد بن حنبل الشيباني", "school": "المذهب الحنبلي", "lifespan": "164 - 241هـ", "birthplace": "بغداد", "founding_place": "بغداد", "scholars": "أبو بكر الخلال، ابن قدامة، ابن تيمية، ابن القيم، محمد بن عبد الوهاب"},
    {"name": "الإمام أبو حنيفة النعمان بن ثابت", "school": "المذهب الحنفي", "lifespan": "80 - 150هـ", "birthplace": "الكوفة", "founding_place": "الكوفة", "scholars": "أبو يوسف، محمد بن الحسن الشيباني، الطحاوي، الكاساني، ابن عابدين"},
    {"name": "الإمام داود بن علي الأصفهاني", "school": "المذهب الظاهري", "lifespan": "202 - 270هـ", "birthplace": "الكوفة", "founding_place": "بغداد", "scholars": "ابن حزم الأندلسي (أشهر من دوّنه في «المحلى»)"},
    {"name": "الإمام جعفر بن محمد الصادق", "school": "المذهب الجعفري", "lifespan": "80 - 148هـ", "birthplace": "المدينة المنورة", "founding_place": "المدينة المنورة", "scholars": "الشيخ المفيد، الشريف المرتضى، الشيخ الطوسي، المحقق الحلي، السيد الخميني، السيد السيستاني"},
    {"name": "الإمام زيد بن علي بن الحسين", "school": "المذهب الزيدي", "lifespan": "80 - 122هـ", "birthplace": "المدينة المنورة", "founding_place": "الكوفة", "scholars": "أبو خالد الواسطي، الناصر الأطروش، الهادي يحيى بن الحسين، الإمام المنصور بالله"},
    {"name": "الإمام جابر بن زيد الأزدي", "school": "المذهب الإباضي", "lifespan": "القرن الأول - 93هـ", "birthplace": "نزوى، عُمان", "founding_place": "البصرة", "scholars": "أبو سعيد الكدمي، أبو نزار الخروصي، نور الدين السالمي، الشيخ أحمد الخليلي"},
]

countries_data = [
    {"country": "🇸🇦 السعودية", "madhab": "الحنبلي", "population": "36.4 مليون"},
    {"country": "🇪🇬 مصر", "madhab": "الشافعي", "population": "112.7 مليون"},
    {"country": "🇲🇦 المغرب", "madhab": "المالكي", "population": "37.8 مليون"},
    {"country": "🇹🇷 تركيا", "madhab": "الحنفي", "population": "87.5 مليون"},
    {"country": "🇮🇷 إيران", "madhab": "الجعفري", "population": "89.8 مليون"},
    {"country": "🇴🇲 عُمان", "madhab": "الإباضي", "population": "4.7 مليون"},
]

MADHHAB_GROUPS = {
    "مذاهب السنة": ["مالكي", "شافعي", "حنفي", "حنبلي", "ظاهري"],
    "مذاهب الشيعة": ["جعفري", "زيدي"],
    "المذهب الإباضي": ["إباضي"],
    "آراء أخرى": ["أخرى"],
}
LEVEL_LABELS = {
    "مختصرة (كلمة)": "very_short",
    "مبسطة (سطر)": "short",
    "مفصل (أكثر من سطر)": "full",
}


# -----------------------------------------------------------------------
# منطق البحث
# -----------------------------------------------------------------------
def search_issues(query, topic_filter, selected_madhab, level):
    if not query:
        return []
    q = query.strip().lower()
    matches = []
    for issue in issues_data:
        if topic_filter != "مواضيع أخرى" and issue["topic"] != topic_filter and topic_filter != "الكل":
            continue
        text_pool = issue["title"].lower() + " " + " ".join(issue["keywords"]).lower() + " " + issue["rulings"]["full"].lower()
        if q in text_pool:
            matches.append(issue)

    if not matches:
        words = re.findall(r"\w+", q)
        for issue in issues_data:
            text_pool = issue["title"].lower() + " " + " ".join(issue["keywords"]).lower()
            if any(w in text_pool for w in words):
                matches.append(issue)

    results = []
    for issue in matches:
        per_madhab = issue.get("rulings_by_madhab", {}).get(selected_madhab)
        if per_madhab:
            answer = per_madhab.get(level, per_madhab.get("full"))
            source_note = f"(رأي المذهب {selected_madhab})"
        else:
            answer = issue["rulings"].get(level, issue["rulings"]["full"])
            source_note = "(رأي عام موحّد — لم يُفصّل بعد لكل مذهب)"
        results.append({"title": issue["title"], "topic": issue["topic"], "answer": answer, "note": source_note})
    return results


# -----------------------------------------------------------------------
# الترويسة
# -----------------------------------------------------------------------
st.markdown(
    """
    <div style="text-align: center; padding: 20px 0; background: linear-gradient(145deg, #0f231c, #2a5c4a); color: white; border-radius: 16px; margin-bottom: 25px;">
        <h1 style="font-size: 2.3rem; margin: 0;">📖 الجامع المختصر لآراء المذاهب</h1>
        <p style="font-size: 1rem; color: #d6e4de; margin: 6px 0 0;">منصة عرض ومقارنة آراء المذاهب الفقهية — للفهم والتبصر، وليست موقع إفتاء.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------
# الفقرة ١: اختيار المذهب
# -----------------------------------------------------------------------
st.markdown("### أولاً — اختر المذهب")
madhab_group = st.radio(
    "مذاهب السنة، أم مذاهب الشيعة، أم المذهب الإباضي، أم آراء أخرى؟",
    list(MADHHAB_GROUPS.keys()),
    horizontal=True,
    label_visibility="collapsed",
)

sub_options = MADHHAB_GROUPS[madhab_group]
if len(sub_options) > 1:
    selected_madhab = st.radio("اختر المذهب تحديداً:", sub_options, horizontal=True)
else:
    selected_madhab = sub_options[0]
    st.caption(f"المذهب المختار: **{selected_madhab}**")

st.divider()

# -----------------------------------------------------------------------
# الفقرة ٢: اختيار الموضوع
# -----------------------------------------------------------------------
st.markdown("### ثانياً — اختر الموضوع")
topic = st.radio(
    "العبادات، أم المعاملات، أم الأسرة، أم مواضيع أخرى؟",
    ["العبادات", "المعاملات", "الأسرة", "مواضيع أخرى"],
    horizontal=True,
    label_visibility="collapsed",
)

st.divider()

# -----------------------------------------------------------------------
# الفقرة ٣: طريقة عرض الإجابة
# -----------------------------------------------------------------------
st.markdown("### ثالثاً — طريقة عرض الإجابة")
level_label = st.radio(
    "مختصرة، أم مبسطة، أم مفصّلة؟",
    list(LEVEL_LABELS.keys()),
    horizontal=True,
    label_visibility="collapsed",
)
level = LEVEL_LABELS[level_label]

st.divider()

# -----------------------------------------------------------------------
# الفقرة ٤: كتابة السؤال
# -----------------------------------------------------------------------
st.markdown("### رابعاً — اكتب سؤالك")
question = st.text_input("سؤالك:", placeholder="مثال: ما حكم صلاة الجماعة؟", label_visibility="collapsed")
search_clicked = st.button("🔍 ابحث عن الإجابة", use_container_width=True)

st.divider()

# -----------------------------------------------------------------------
# الفقرة ٥: الإجابة
# -----------------------------------------------------------------------
st.markdown("### خامساً — الإجابة")
if search_clicked and question:
    results = search_issues(question, topic, selected_madhab, level)
    if results:
        for r in results:
            with st.container(border=True):
                st.markdown(f"**📌 {r['title']}** &nbsp;·&nbsp; _{r['topic']}_")
                st.markdown(f"### {r['answer']}")
                st.caption(r["note"])
                st.caption("هذا والله أعلم")
    else:
        st.warning("🔍 لم نجد مسألة بهذا الوصف ضمن الموضوع المختار. جرّب صياغة أخرى أو وسّع نطاق البحث.")
elif search_clicked:
    st.info("الرجاء كتابة سؤالك أولاً في الفقرة الرابعة.")
else:
    st.caption("ستظهر الإجابة هنا بعد كتابة السؤال والضغط على زر البحث.")

st.markdown("---")

# -----------------------------------------------------------------------
# فقرات هامشية اختيارية
# -----------------------------------------------------------------------
with st.expander("📜 الأئمة المؤسسون للمذاهب"):
    for imam in imams_data:
        st.markdown(
            f"""
            <div style="background:#f5f7f5; padding:12px 16px; border-radius:12px; margin-bottom:10px; border-right:4px solid #d4a854;">
                <h4 style="margin:0; color:#1e3a2f;">{imam['name']}</h4>
                <p style="margin:2px 0; color:#d4a854; font-weight:600;">{imam['school']} &nbsp;|&nbsp; {imam['lifespan']}</p>
                <p style="margin:2px 0; color:#3d4f5f;">📍 مكان الميلاد: {imam['birthplace']} &nbsp;·&nbsp; 🏛️ مكان تأسيس المذهب: {imam['founding_place']}</p>
                <p style="margin:4px 0 0; color:#3d4f5f;">🎓 أشهر فقهاء المذهب: {imam['scholars']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

with st.expander("🗺️ الدول الإسلامية والمذهب الرسمي السائد"):
    cols = st.columns(3)
    for i, c in enumerate(countries_data):
        with cols[i % 3]:
            st.markdown(
                f"""
                <div style="background:#f5f7f5; padding:8px 12px; border-radius:8px; margin-bottom:6px; border-right:3px solid #d4a854;">
                    <strong>{c['country']}</strong><br>
                    <span style="color:#d4a854;">المذهب الرسمي: {c['madhab']}</span><br>
                    <span style="font-size:0.8rem; color:#6a7f78;">👥 عدد السكان: {c['population']}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

with st.expander("📚 مصطلحات فقهية رئيسية"):
    for term in glossary_terms:
        st.markdown(
            f"""
            <div style="background:#f5f7f5; padding:12px 16px; border-radius:12px; margin-bottom:10px; border-right:4px solid #1e3a2f;">
                <h4 style="margin:0; color:#1e3a2f;">{term['term']}</h4>
                <p style="margin:4px 0 0; color:#3d4f5f;">{term['definition']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

# -----------------------------------------------------------------------
# التعليقات والملاحظات والتقييم
# -----------------------------------------------------------------------
with st.expander("💬 أضف تعليقك أو ملاحظتك"):
    if "session_comments" not in st.session_state:
        st.session_state.session_comments = []

    rating = st.slider("قيّم فائدة الإجابة:", 1, 5, 5)
    comment_text = st.text_area("تعليقك أو ملاحظتك:", placeholder="اكتب ملاحظتك هنا...")
    if st.button("إرسال التعليق"):
        if comment_text.strip():
            st.session_state.session_comments.append({"text": comment_text.strip(), "rating": rating})
            st.success("✅ تم إرسال تعليقك، شكراً لك.")
        else:
            st.warning("⚠️ الرجاء كتابة تعليق قبل الإرسال.")

    if st.session_state.session_comments:
        st.markdown("**تعليقات هذه الجلسة:**")
        for c in st.session_state.session_comments:
            st.markdown(f"- {'⭐' * c['rating']} — {c['text']}")
    st.caption("ملاحظة: هذه التعليقات محفوظة لجلستك الحالية فقط. لحفظها بشكل دائم يلزم ربط البرنامج بقاعدة بيانات (مثل Firebase).")

# -----------------------------------------------------------------------
# التذييل
# -----------------------------------------------------------------------
st.markdown(
    """
    <div style="text-align:center; padding:16px 0; color:#6a7f78;">
        <p>المعرفة أمانة. نراجع كل مادة من مصادرها الأصلية، ونوضح مواضع الاتفاق والاختلاف بإنصاف — هذا البرنامج لعرض آراء المذاهب للفهم والتبصر، وليس موقع إفتاء.</p>
        <p style="font-size:0.8rem; margin-top:6px;">© ٢٠٢٤ الجامع المختصر لآراء المذاهب</p>
    </div>
    """,
    unsafe_allow_html=True,
)
```
