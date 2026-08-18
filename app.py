import streamlit as st
import re

st.set_page_config(
    page_title="الجامع المرشد للآراء الفقهية",
    page_icon="📖",
    layout="wide"
)

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

glossary_terms = [
    {"term": "الحلال", "definition": "ما أحله الله ورسوله، وثبوت حله في الكتاب والسنة، وفعله مباح لا إثم فيه."},
    {"term": "الحرام", "definition": "ما حرمه الله ورسوله بنص قطعي، وفاعله آثم مستحق للعقاب."},
    {"term": "المكروه", "definition": "ما طلب الشارع تركه طلباً غير جازم، ويثاب تاركه ولا يعاقب فاعله."},
    {"term": "المستحب", "definition": "ما رغب الشارع في فعله دون إلزام، ويثاب فاعله ولا يعاقب تاركه."},
    {"term": "الفرض", "definition": "ما طلب الشارع فعله طلباً جازماً على كل مكلف، ويثاب فاعله ويعاقب تاركه."}
]

countries_data = [
    {"country": "🇸🇦 السعودية", "madhab": "الحنبلي", "population": "36.4 مليون"},
    {"country": "🇪🇬 مصر", "madhab": "الشافعي", "population": "112.7 مليون"},
    {"country": "🇲🇦 المغرب", "madhab": "المالكي", "population": "37.8 مليون"},
    {"country": "🇹🇷 تركيا", "madhab": "الحنفي", "population": "87.5 مليون"},
    {"country": "🇮🇷 إيران", "madhab": "الجعفري", "population": "89.8 مليون"},
    {"country": "🇴🇲 عُمان", "madhab": "الإباضي", "population": "4.7 مليون"}
]

imams_data = [
    {"name": "الإمام مالك بن أنس (93-179هـ)", "school": "المذهب المالكي", "scholars": "ابن القاسم، سحنون، ابن رشد، القرافي، خليل بن إسحاق"},
    {"name": "الإمام محمد بن إدريس الشافعي (150-204هـ)", "school": "المذهب الشافعي", "scholars": "المزني، البويطي، النووي، ابن حجر الهيتمي، الرافعي"},
    {"name": "الإمام أحمد بن حنبل (164-241هـ)", "school": "المذهب الحنبلي", "scholars": "أبو بكر الخلال، ابن قدامة، ابن تيمية، ابن القيم، محمد بن عبد الوهاب"},
    {"name": "الإمام أبو حنيفة النعمان (80-150هـ)", "school": "المذهب الحنفي", "scholars": "أبو يوسف، محمد بن الحسن الشيباني، الطحاوي، الكاساني، ابن عابدين"},
    {"name": "الإمام جعفر الصادق (80-148هـ)", "school": "المذهب الجعفري", "scholars": "الشيخ المفيد، الشريف المرتضى، الشيخ الطوسي، المحقق الحلي، السيد الخميني، السيد السيستاني"},
    {"name": "الإمام زيد بن علي (80-122هـ)", "school": "المذهب الزيدي", "scholars": "أبو خالد الواسطي، الناصر الأطروش، الهادي يحيى بن الحسين، الإمام المنصور بالله"},
    {"name": "الإمام جابر بن زيد (القرن الأول-93هـ)", "school": "المذهب الإباضي", "scholars": "أبو سعيد الكدمي، أبو نزار الخروصي، نور الدين السالمي، الشيخ أحمد الخليلي"}
]

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

st.markdown("""
<div style="text-align: center; padding: 20px 0; background: linear-gradient(145deg, #0f231c, #2a5c4a); color: white; border-radius: 16px; margin-bottom: 30px; direction: rtl;">
    <h1 style="font-size: 2.5rem; margin: 0;">📖 الجامع المرشد للآراء الفقهية</h1>
    <p style="font-size: 1.2rem; color: #d6e4de; margin: 0;">مرشد الآراء الفقهية</p>
    <p style="font-size: 0.95rem; color: #b2d1c4; margin: 0;">للفهم والتبصر، لا لإصدار الفتاوى</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div style="direction: rtl;">', unsafe_allow_html=True)

st.markdown("### 🔍 خطوات البحث")

category_filter = st.radio("١. اختر المجال الفقهي:", ["الكل", "العبادات", "المعاملات", "الأسرة", "الحياة اليومية"], horizontal=True)

madhabs = st.multiselect("٢. اختر المذاهب التي تريد عرضها:", ["المالكي", "الشافعي", "الحنبلي", "الحنفي", "الظاهري", "الجعفري", "الزيدي", "الإباضي", "رأي آخر"], default=["المالكي", "الشافعي", "الحنبلي", "الحنفي"])

answer_level = st.radio("٣. اختر مستوى الإجابة:", ["⚡ مختصرة جداً (كلمة واحدة)", "📄 مختصرة (سطر واحد)", "📚 كاملة (تفصيلية)"], horizontal=True)
level_map = {"⚡ مختصرة جداً (كلمة واحدة)": "very_short", "📄 مختصرة (سطر واحد)": "short", "📚 كاملة (تفصيلية)": "full"}

search_query = st.text_input("٤. اكتب سؤالك:", placeholder="مثال: ما حكم صلاة المسافر؟")

if st.button("🔍 ابحث", use_container_width=True) and search_query:
    results = smart_search(search_query, issues_data, category_filter, level_map[answer_level])
    if results:
        st.markdown(f"### 📊 النتائج ({len(results)})")
        for r in results:
            with st.expander(f"📌 {r['title']} ({r['category']})"):
                st.markdown(f"**الإجابة:** {r['answer']}")
                st.markdown("*هذا والله أعلم*")
    else:
        st.warning("🔍 لم نجد مسألة بهذا الوصف في المجال والمذاهب المختارة. جرّب تغيير الفلتر أو كلمة أقصر.")

st.markdown("---")
st.markdown("### ✦ كل الموضوعات")
cols = st.columns(4)
for i, cat in enumerate(["☽ العبادات", "◈ المعاملات", "⌂ الأسرة", "✧ الحياة اليومية"]):
    with cols[i]:
        if st.button(cat, use_container_width=True):
            category_name = cat.replace("☽ ", "").replace("◈ ", "").replace("⌂ ", "").replace("✧ ", "")
            st.info(f"📂 عرض مسائل {category_name}")

st.markdown("---")
st.markdown("### 🗺️ خريطة الآراء")

with st.expander("المذاهب السنية", expanded=True):
    cols = st.columns(5)
    sunni_schools = ["المالكي", "الشافعي", "الحنبلي", "الحنفي", "الظاهري"]
    for i, school in enumerate(sunni_schools):
        with cols[i]:
            if st.button(school, use_container_width=True):
                st.info(f"🗺️ تم اختيار المذهب: {school}")

with st.expander("المذاهب الشيعية", expanded=True):
    cols = st.columns(2)
    shia_schools = ["الجعفري الاثنا عشري", "الزيدي"]
    for i, school in enumerate(shia_schools):
        with cols[i]:
            if st.button(school, use_container_width=True):
                st.info(f"🗺️ تم اختيار المذهب: {school}")

with st.expander("المذهب الإباضي", expanded=True):
    if st.button("الإباضي", use_container_width=True):
        st.info("🗺️ تم اختيار المذهب: الإباضي")

if st.button("رأي آخر", use_container_width=True):
    st.info("🗺️ تم اختيار: رأي آخر")

with st.expander("📜 الأئمة المؤسسون", expanded=False):
    for imam in imams_data:
        st.markdown(f"""
        <div style="background: #f5f7f5; padding: 12px 16px; border-radius: 12px; margin-bottom: 10px; border-right: 4px solid #d4a854; direction: rtl;">
            <h4 style="margin: 0; color: #1e3a2f;">{imam['name']}</h4>
            <p style="margin: 2px 0; color: #d4a854; font-weight: 600;">{imam['school']}</p>
            <p style="margin: 4px 0 0 0; color: #3d4f5f;">أشهر العلماء: {imam['scholars']}</p>
        </div>
        """, unsafe_allow_html=True)

with st.expander("🗺️ المذهب الرسمي السائد في الدول الإسلامية", expanded=False):
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

with st.expander("📚 قاموس المصطلحات الفقهية", expanded=False):
    for term in glossary_terms:
        st.markdown(f"""
        <div style="background: #f5f7f5; padding: 12px 16px; border-radius: 12px; margin-bottom: 10px; border-right: 4px solid #1e3a2f; direction: rtl;">
            <h4 style="margin: 0; color: #1e3a2f;">{term['term']}</h4>
            <p style="margin: 4px 0 0 0; color: #3d4f5f;">{term['definition']}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; padding: 20px 0; color: #6a7f78; direction: rtl;">
    <p>المعرفة أمانة. نراجع كل مادة من مصادرها الأصلية، ونوضح مواضع الاتفاق والاختلاف بإنصاف.</p>
    <a href="#" style="color: #8bc4b0; text-decoration: none; font-weight: 600;">تعرّف على منهجيتنا →</a>
    <p style="font-size: 0.8rem; margin-top: 10px;">© ٢٠٢٤ الجامع المرشد للآراء الفقهية</p>
</div>
""", unsafe_allow_html=True)
