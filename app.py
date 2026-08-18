```python
import streamlit as st
import re

st.set_page_config(
    page_title="الجامع المختصر لآراء المذاهب",
    page_icon="📖",
    layout="wide"
)

# ============================================================
# البيانات
# ============================================================

issues_data = [
    {
        "id": 1,
        "title": "صلاة الجماعة",
        "category": "العبادات",
        "rulings": {
            "very_short": "سنة مؤكدة",
            "short": "سنة مؤكدة عند الجمهور، واجبة عند الحنفية",
            "full": "تجب صلاة الجماعة في المسجد على الرجال عند جمهور الفقهاء؛ فهي فرض عين عند الحنابلة، واجب مؤكد عند الحنفية، فرض كفاية عند المالكية والشافعية، ومستحبة تأكيداً عند الجعفرية في زمن الغيبة."
        },
        "keywords": ["جماعة", "مسجد", "رجال", "صلاة", "فرض", "سنة", "واجب"]
    },
    {
        "id": 2,
        "title": "زكاة الأسهم",
        "category": "المعاملات",
        "rulings": {
            "very_short": "واجبة",
            "short": "زكاة الأسهم واجبة إذا بلغت النصاب",
            "full": "تجب زكاة الأسهم إذا كانت للاستثمار والتجارة، وبلغت قيمتها النصاب (85 جرام ذهب)، وتُحسب بقيمتها السوقية في نهاية الحول، ويُخرج 2.5% من قيمتها."
        },
        "keywords": ["زكاة", "أسهم", "استثمار", "تجارة", "نصاب", "مال"]
    },
    {
        "id": 3,
        "title": "الجمع في السفر",
        "category": "العبادات",
        "rulings": {
            "very_short": "جائز",
            "short": "يجوز جمع الصلاة في السفر للمسافر",
            "full": "يجوز للمسافر جمع صلاة الظهر مع العصر، والمغرب مع العشاء، تقديماً أو تأخيراً، في وقت إحداهما، وذلك تخفيفاً من الله تعالى على المسافرين."
        },
        "keywords": ["جمع", "سفر", "مسافر", "صلاة", "تخفيف", "رخصة"]
    },
    {
        "id": 4,
        "title": "نواقض الوضوء",
        "category": "العبادات",
        "rulings": {
            "very_short": "مبطل",
            "short": "نواقض الوضوء تبطل الطهارة وتوجب إعادته",
            "full": "نواقض الوضوء هي: الخارج من السبيلين (البول، الغائط، الريح)، النوم المستغرق، زوال العقل (بإغماء أو سكر)، مسّ الفرج بغير حائل، ولمس المرأة بشهوة عند بعض المذاهب."
        },
        "keywords": ["وضوء", "نواقض", "طهارة", "بول", "غائط", "نوم", "مس"]
    },
    {
        "id": 5,
        "title": "الربا",
        "category": "المعاملات",
        "rulings": {
            "very_short": "حرام",
            "short": "الربا من كبائر الذنوب ومحرم قطعاً",
            "full": "الربا محرم بنص القرآن والسنة، وهو كل زيادة مشروطة في القرض أو المعاملة، سواء كانت نقدية أو عينية. الربا من السبع الموبقات، والله ورسوله حاربا من يتعامل به."
        },
        "keywords": ["ربا", "حرام", "قرض", "فائدة", "بنوك", "معاملة"]
    },
    {
        "id": 6,
        "title": "صلاة المسافر",
        "category": "العبادات",
        "rulings": {
            "very_short": "جائز",
            "short": "يجوز للمسافر قصر الصلاة وجمعها",
            "full": "يجوز للمسافر قصر الصلاة الرباعية (الظهر، العصر، العشاء) إلى ركعتين، وجمع الصلاة (الظهر مع العصر، والمغرب مع العشاء). هذه رخصة من الله للتخفيف على المسافرين."
        },
        "keywords": ["سفر", "مسافر", "صلاة", "قصر", "جمع", "تخفيف", "رخصة"]
    }
]

# ============================================================
# بيانات المذاهب
# ============================================================

madhhab_data = {
    "المالكي": {"imam": "الإمام مالك بن أنس (93-179هـ)", "birth": "المدينة المنورة", "foundation": "المدينة المنورة", "life": "93-179هـ", "scholars": "ابن القاسم، سحنون، ابن رشد، القرافي، خليل بن إسحاق"},
    "الشافعي": {"imam": "الإمام محمد بن إدريس الشافعي (150-204هـ)", "birth": "غزة", "foundation": "مصر", "life": "150-204هـ", "scholars": "المزني، البويطي، النووي، ابن حجر الهيتمي، الرافعي"},
    "الحنبلي": {"imam": "الإمام أحمد بن حنبل (164-241هـ)", "birth": "بغداد", "foundation": "بغداد", "life": "164-241هـ", "scholars": "أبو بكر الخلال، ابن قدامة، ابن تيمية، ابن القيم، محمد بن عبد الوهاب"},
    "الحنفي": {"imam": "الإمام أبو حنيفة النعمان (80-150هـ)", "birth": "الكوفة", "foundation": "الكوفة", "life": "80-150هـ", "scholars": "أبو يوسف، محمد بن الحسن الشيباني، الطحاوي، الكاساني، ابن عابدين"},
    "الظاهري": {"imam": "الإمام داود الظاهري (202-270هـ)", "birth": "الكوفة", "foundation": "بغداد", "life": "202-270هـ", "scholars": "ابن حزم الأندلسي، عبد الله بن محمد القيرواني"},
    "الجعفري": {"imam": "الإمام جعفر الصادق (80-148هـ)", "birth": "المدينة المنورة", "foundation": "المدينة المنورة", "life": "80-148هـ", "scholars": "الشيخ المفيد، الشريف المرتضى، الشيخ الطوسي، المحقق الحلي، السيد الخميني، السيد السيستاني"},
    "الزيدي": {"imam": "الإمام زيد بن علي (80-122هـ)", "birth": "المدينة المنورة", "foundation": "الكوفة", "life": "80-122هـ", "scholars": "أبو خالد الواسطي، الناصر الأطروش، الهادي يحيى بن الحسين، الإمام المنصور بالله"},
    "الإباضي": {"imam": "الإمام جابر بن زيد (القرن الأول-93هـ)", "birth": "عُمان", "foundation": "عُمان", "life": "القرن الأول-93هـ", "scholars": "أبو سعيد الكدمي، أبو نزار الخروصي، نور الدين السالمي، الشيخ أحمد الخليلي"}
}

# ============================================================
# بيانات المصطلحات
# ============================================================

glossary_terms = [
    {"term": "فرض العين", "definition": "ما طلب الشارع فعله طلباً جازماً على كل مكلف شخصياً، ويثاب فاعله ويعاقب تاركه. مثل: الصلوات الخمس."},
    {"term": "فرض الكفاية", "definition": "ما طلب الشارع فعله طلباً جازماً على عموم المكلفين، ويسقط عن الجميع بفعل البعض، ويأثم الجميع إن تركه الكل. مثل: صلاة الجنازة."},
    {"term": "الواجب", "definition": "عند الحنفية: ما ثبت بدليل ظني (كصلاة الوتر). عند الجمهور: مرادف للفرض."},
    {"term": "السنة المؤكدة", "definition": "ما واظب النبي ﷺ على فعله في الغالب، وتركه أحياناً، وتركها مكروه عند الحنفية. مثل: سنة الفجر."},
    {"term": "السنة (غير المؤكدة)", "definition": "ما فعله النبي ﷺ أحياناً وتركه أحياناً، وتركها لا إثم فيه. مثل: سنة الظهر القبلية."},
    {"term": "المستحب (مندوب)", "definition": "ما رغب الشارع في فعله دون إلزام، ويثاب فاعله ولا يعاقب تاركه. مثل: صلاة الضحى."},
    {"term": "المندوب", "definition": "مرادف للمستحب، وهو ما ندب الشرع إليه وحث عليه دون إيجاب. مثل: الأضحية."},
    {"term": "المكروه", "definition": "ما طلب الشارع تركه طلباً غير جازم، ويثاب تاركه ولا يعاقب فاعله. مثل: الأكل بالشمال."},
    {"term": "الحرام", "definition": "ما حرمه الله ورسوله بنص قطعي، وفاعله آثم مستحق للعقاب، وتاركه مثاب. مثل: شرب الخمر."}
]

# ============================================================
# بيانات الدول
# ============================================================

countries_data = [
    {"country": "🇸🇦 السعودية", "madhab": "الحنبلي", "population": "36.4 مليون"},
    {"country": "🇪🇬 مصر", "madhab": "الشافعي", "population": "112.7 مليون"},
    {"country": "🇲🇦 المغرب", "madhab": "المالكي", "population": "37.8 مليون"},
    {"country": "🇩🇿 الجزائر", "madhab": "المالكي", "population": "46.3 مليون"},
    {"country": "🇹🇳 تونس", "madhab": "المالكي", "population": "12.5 مليون"},
    {"country": "🇹🇷 تركيا", "madhab": "الحنفي", "population": "87.5 مليون"},
    {"country": "🇮🇷 إيران", "madhab": "الجعفري", "population": "89.8 مليون"},
    {"country": "🇴🇲 عُمان", "madhab": "الإباضي", "population": "4.7 مليون"},
    {"country": "🇵🇰 باكستان", "madhab": "الحنفي", "population": "248.5 مليون"},
    {"country": "🇮🇩 إندونيسيا", "madhab": "الشافعي", "population": "281.6 مليون"}
]

# ============================================================
# دالة البحث الذكي
# ============================================================

def smart_search(query, issues_data, category_filter, level='full'):
    if not query:
        return []
    query = query.strip().lower()
    results = []
    for issue in issues_data:
        if category_filter != "الكل" and issue.get('category', '') != category_filter:
            continue
        title_match = query in issue.get('title', '').lower()
        keyword_match = any(query in kw.lower() for kw in issue.get('keywords', []))
        full_text_match = query in issue.get('rulings', {}).get('full', '').lower()
        if title_match or keyword_match or full_text_match:
            results.append(issue)
    if not results:
        query_words = re.findall(r'\w+', query)
        for issue in issues_data:
            if category_filter != "الكل" and issue.get('category', '') != category_filter:
                continue
            issue_text = issue.get('title', '').lower() + ' ' + ' '.join(issue.get('keywords', [])).lower()
            for word in query_words:
                if word in issue_text:
                    results.append(issue)
                    break
    final_results = []
    for issue in results:
        rulings = issue.get('rulings', {})
        answer = rulings.get(level, rulings.get('full', 'لا توجد إجابة'))
        final_results.append({
            'title': issue.get('title'),
            'category': issue.get('category'),
            'answer': answer
        })
    return final_results

# ============================================================
# الشعار والهوية
# ============================================================

st.markdown("""
<div style="text-align: center; padding: 20px 0; background: linear-gradient(145deg, #0f231c, #2a5c4a); color: white; border-radius: 16px; margin-bottom: 30px; direction: rtl;">
    <h1 style="font-size: 2.5rem; margin: 0;">📖 الجامع المختصر لآراء المذاهب</h1>
    <p style="font-size: 1.2rem; color: #d6e4de; margin: 0;">مرشد الآراء الفقهية</p>
    <p style="font-size: 0.95rem; color: #b2d1c4; margin: 0;">للفهم والتبصر، لا لإصدار الفتاوى</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div style="direction: rtl;">', unsafe_allow_html=True)

# ============================================================
# الفقرة الأولى: اختيار المذهب
# ============================================================

st.markdown("### 🏛️ الفقرة الأولى: اختيار المذهب")

madhab_group = st.radio(
    "اختر مجموعة المذاهب:",
    ["مذاهب السنة", "مذاهب الشيعة", "المذهب الإباضي", "آراء أخرى"],
    horizontal=True
)

if madhab_group == "مذاهب السنة":
    madhab_options = ["المالكي", "الشافعي", "الحنبلي", "الحنفي", "الظاهري"]
elif madhab_group == "مذاهب الشيعة":
    madhab_options = ["الجعفري", "الزيدي"]
elif madhab_group == "المذهب الإباضي":
    madhab_options = ["الإباضي"]
else:
    madhab_options = ["رأي آخر"]

selected_madhab = st.selectbox("اختر المذهب:", madhab_options)

# عرض معلومات عن المذهب المختار
if selected_madhab in madhhab_data:
    info = madhhab_data[selected_madhab]
    st.info(f"""
    **الإمام:** {info['imam']}  
    **مكان الميلاد:** {info['birth']}  
    **مكان التأسيس:** {info['foundation']}  
    **فترة الحياة:** {info['life']}  
    **أشهر الفقهاء:** {info['scholars']}
    """)

st.markdown("---")

# ============================================================
# الفقرة الثانية: اختيار الموضوع
# ============================================================

st.markdown("### 📂 الفقرة الثانية: اختيار الموضوع")

category_filter = st.radio(
    "اختر الموضوع:",
    ["العبادات", "المعاملات", "الأسرة", "مواضيع أخرى"],
    horizontal=True
)

if category_filter == "مواضيع أخرى":
    category_filter = "الكل"

st.markdown("---")

# ============================================================
# الفقرة الثالثة: طريقة عرض الإجابة
# ============================================================

st.markdown("### 📝 الفقرة الثالثة: طريقة عرض الإجابة")

answer_level = st.radio(
    "اختر مستوى الإجابة:",
    ["مختصرة (كلمة)", "مبسطة (سطر)", "مفصل (أكثر من سطر)"],
    horizontal=True
)

level_map = {
    "مختصرة (كلمة)": "very_short",
    "مبسطة (سطر)": "short",
    "مفصل (أكثر من سطر)": "full"
}
selected_level = level_map[answer_level]

st.markdown("---")

# ============================================================
# الفقرة الرابعة: كتابة السؤال
# ============================================================

st.markdown("### ✍️ الفقرة الرابعة: كتابة السؤال")

search_query = st.text_input("", placeholder="اكتب سؤالك هنا...", label_visibility="collapsed")

col1, col2, col3 = st.columns([1, 1, 4])
with col1:
    search_btn = st.button("🔍 ابحث", use_container_width=True)

st.markdown("---")

# ============================================================
# الفقرة الخامسة: عرض الإجابة
# ============================================================

st.markdown("### 📊 الفقرة الخامسة: الإجابة")

if search_btn and search_query:
    results = smart_search(search_query, issues_data, category_filter, selected_level)
    if results:
        st.markdown(f"**عدد النتائج:** {len(results)}")
        for r in results:
            with st.expander(f"📌 {r['title']} ({r['category']})"):
                st.markdown(f"**الإجابة:** {r['answer']}")
                st.markdown("*هذا والله أعلم*")
    else:
        st.warning("🔍 لم نجد مسألة بهذا الوصف. جرّب تغيير الفلتر أو كلمة أقصر.")
else:
    st.info("✍️ اكتب سؤالك ثم اضغط 'ابحث' للحصول على الإجابة")

st.markdown("---")

# ============================================================
# فقرات هامشية مطوية (اختيارية)
# ============================================================

st.markdown("### 📚 فقرات هامشية (اختيارية)")

# ============================================================
# 1. الأئمة المؤسسون
# ============================================================

with st.expander("📜 الأئمة المؤسسون للمذاهب", expanded=False):
    for madhab, info in madhhab_data.items():
        st.markdown(f"""
        <div style="background: #f5f7f5; padding: 12px 16px; border-radius: 12px; margin-bottom: 10px; border-right: 4px solid #d4a854; direction: rtl;">
            <h4 style="margin: 0; color: #1e3a2f;">{info['imam']}</h4>
            <p style="margin: 2px 0; color: #d4a854; font-weight: 600;">{madhab}</p>
            <p style="margin: 2px 0; color: #3d4f5f;">📍 {info['birth']} | 🏛️ {info['foundation']} | 🕰️ {info['life']}</p>
            <p style="margin: 4px 0 0 0; color: #3d4f5f;">أشهر الفقهاء: {info['scholars']}</p>
        </div>
        """, unsafe_allow_html=True)

# ============================================================
# 2. الدول والمذاهب الرسمية
# ============================================================

with st.expander("🗺️ الدول الإسلامية والمذهب الرسمي السائد", expanded=False):
    cols = st.columns(3)
    for i, country in enumerate(countries_data):
        with cols[i % 3]:
            st.markdown(f"""
            <div style="background: #f5f7f5; padding: 8px 12px; border-radius: 8px; margin-bottom: 6px; border-right: 3px solid #d4a854; direction: rtl;">
                <strong>{country['country']}</strong><br>
                <span style="color: #d4a854;">{country['madhab']}</span><br>
                <span style="font-size: 0.8rem; color: #6a7f78;">👥 {country['population']}</span>
            </div>
            """, unsafe_allow_html=True)

# ============================================================
# 3. المصطلحات الرئيسية
# ============================================================

with st.expander("📚 المصطلحات الفقهية الرئيسية", expanded=False):
    for term in glossary_terms:
        st.markdown(f"""
        <div style="background: #f5f7f5; padding: 12px 16px; border-radius: 12px; margin-bottom: 10px; border-right: 4px solid #1e3a2f; direction: rtl;">
            <h4 style="margin: 0; color: #1e3a2f;">{term['term']}</h4>
            <p style="margin: 4px 0 0 0; color: #3d4f5f;">{term['definition']}</p>
        </div>
        """, unsafe_allow_html=True)

# ============================================================
# 4. التقييم والتعليقات
# ============================================================

with st.expander("⭐ التقييم والملاحظات", expanded=False):
    st.markdown("#### كيف تقيم محتوى هذا التطبيق؟")
    rating = st.slider("", 1, 5, 3, label_visibility="collapsed")
    st.markdown(f"**تقييمك:** {'⭐' * rating} ({rating}/5)")
    
    comment = st.text_area("📝 أضف ملاحظاتك أو اقتراحاتك:", placeholder="اكتب هنا...")
    if st.button("إرسال"):
        if comment:
            st.success("✅ شكراً على ملاحظاتك! تم استلامها بنجاح.")
        else:
            st.warning("⚠️ الرجاء كتابة ملاحظاتك قبل الإرسال.")

# ============================================================
# 5. نبذة عن البرنامج
# ============================================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px 0; color: #6a7f78; direction: rtl; background: #f5f7f5; border-radius: 12px;">
    <p style="font-size: 1.1rem; font-weight: bold;">📖 نبذة عن البرنامج</p>
    <p>هذا التطبيق هو <strong>مرجع مختصر للآراء الفقهية</strong>، يهدف إلى تسهيل الوصول إلى آراء المذاهب المختلفة في المسائل الفقهية.</p>
    <p style="color: #d4a854; font-weight: bold;">⚠️ هذا التطبيق ليس موقع فتوى، ولا يصدر أحكاماً شرعية، بل يعرض آراء الفقهاء للفهم والتبصر.</p>
    <p style="font-size: 0.8rem; margin-top: 10px;">© ٢٠٢٤ الجامع المختصر لآراء المذاهب</p>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
```
