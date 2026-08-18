import streamlit as st
import json
import os
from datetime import datetime

# ============================================================
# 1. إعداد الصفحة
# ============================================================
st.set_page_config(
    page_title="بيان - مرشد الآراء الفقهية",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# 2. البيانات الافتراضية
# ============================================================

def get_default_issues():
    return [
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
            "keywords": ["ربا", "حرام", "قرض", "فائدة", "بنوك", "معاملة", "ذنب"]
        }
    ]

def get_default_glossary():
    return [
        {"term": "الحلال", "definition": "ما أحله الله ورسوله، وثبوت حله في الكتاب والسنة، وفعله مباح لا إثم فيه، بل قد يثاب عليه الإنسان إذا نوى به التقوى أو العبادة."},
        {"term": "الحرام", "definition": "ما حرمه الله ورسوله بنص قطعي، وثبوت تحريمه في الكتاب أو السنة، وفاعله آثم مستحق للعقاب، وتاركه مثاب."},
        {"term": "المكروه", "definition": "ما طلب الشارع تركه طلباً غير جازم، ويثاب تاركه تقرباً إلى الله، ولا يعاقب فاعله، لكن تركه أولى وأفضل."},
        {"term": "المستحب", "definition": "ما رغب الشارع في فعله دون إلزام، ويثاب فاعله امتثالاً لأمره، ولا يعاقب تاركه، وهو أوسع أبواب الطاعات."},
        {"term": "الفرض", "definition": "ما طلب الشارع فعله طلباً جازماً على كل مكلف شخصياً، ويثاب فاعله ويعاقب تاركه، وهو أعلى مراتب التكليف."}
    ]

def get_default_countries():
    return [
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

def get_default_imams():
    return [
        {"name": "الإمام مالك بن أنس (93-179هـ)", "school": "المذهب المالكي", "scholars": "ابن القاسم، سحنون، ابن رشد، القرافي، خليل بن إسحاق"},
        {"name": "الإمام محمد بن إدريس الشافعي (150-204هـ)", "school": "المذهب الشافعي", "scholars": "المزني، البويطي، النووي، ابن حجر الهيتمي، الرافعي"},
        {"name": "الإمام أحمد بن حنبل (164-241هـ)", "school": "المذهب الحنبلي", "scholars": "أبو بكر الخلال، ابن قدامة، ابن تيمية، ابن القيم، محمد بن عبد الوهاب"},
        {"name": "الإمام أبو حنيفة النعمان (80-150هـ)", "school": "المذهب الحنفي", "scholars": "أبو يوسف، محمد بن الحسن الشيباني، الطحاوي، الكاساني، ابن عابدين"},
        {"name": "الإمام داود الظاهري (202-270هـ)", "school": "المذهب الظاهري", "scholars": "ابن حزم الأندلسي، عبد الله بن محمد القيرواني"},
        {"name": "الإمام جعفر الصادق (80-148هـ)", "school": "المذهب الجعفري", "scholars": "الشيخ المفيد، الشريف المرتضى، الشيخ الطوسي، المحقق الحلي، السيد الخميني، السيد السيستاني"},
        {"name": "الإمام زيد بن علي (80-122هـ)", "school": "المذهب الزيدي", "scholars": "أبو خالد الواسطي، الناصر الأطروش، الهادي يحيى بن الحسين، الإمام المنصور بالله"},
        {"name": "الإمام جابر بن زيد (القرن الأول-93هـ)", "school": "المذهب الإباضي", "scholars": "أبو سعيد الكدمي، أبو نزار الخروصي، نور الدين السالمي، الشيخ أحمد الخليلي"}
    ]

# ============================================================
# 3. تحميل البيانات
# ============================================================

issues_data = get_default_issues()
glossary_terms = get_default_glossary()
countries_data = get_default_countries()
imams_data = get_default_imams()

# ============================================================
# 4. واجهة المستخدم
# ============================================================

# الشعار والهوية
st.markdown("""
<div style="text-align: center; padding: 20px 0; background: linear-gradient(145deg, #0f231c, #2a5c4a); color: white; border-radius: 16px; margin-bottom: 30px;">
    <h1 style="font-size: 3rem; margin: 0;">📖 بيان</h1>
    <p style="font-size: 1.2rem; color: #d6e4de; margin: 0;">مرشد الآراء الفقهية</p>
    <p style="font-size: 0.95rem; color: #b2d1c4; margin: 0;">للفهم والتبصر، لا لإصدار الفتاوى</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# 5. البحث
# ============================================================

st.markdown("### ❓ ماذا تريد أن تعرف اليوم？")

col1, col2 = st.columns([4, 1])
with col1:
    search_query = st.text_input("", placeholder="اسأل بأي طريقة... سيفهمك التطبيق", label_visibility="collapsed")
with col2:
    search_btn = st.button("🔍", use_container_width=True)

# مستوى الإجابة
answer_level = st.radio(
    "📝 اختر مستوى الإجابة:",
    ["⚡ مختصرة جداً (كلمة واحدة)", "📄 مختصرة (سطر واحد)", "📚 كاملة (تفصيلية)"],
    horizontal=True
)

level_map = {
    "⚡ مختصرة جداً (كلمة واحدة)": "very_short",
    "📄 مختصرة (سطر واحد)": "short",
    "📚 كاملة (تفصيلية)": "full"
}
selected_level = level_map[answer_level]

# ============================================================
# 6. عرض النتائج
# ============================================================

if search_query or search_btn:
    query = search_query.strip().lower()
    if query:
        results = []
        for issue in issues_data:
            if (query in issue.get('title', '').lower() or
                any(query in kw.lower() for kw in issue.get('keywords', [])) or
                query in issue.get('rulings', {}).get('full', '').lower()):
                results.append(issue)
        
        if results:
            st.markdown(f"### 📊 النتائج ({len(results)} مسألة)")
            for issue in results:
                with st.expander(f"📌 {issue['title']} ({issue['category']})"):
                    answer = issue.get('rulings', {}).get(selected_level, issue.get('rulings', {}).get('full', 'لا توجد إجابة'))
                    st.markdown(f"**الإجابة:** {answer}")
        else:
            st.warning("🔍 لم نجد مسألة بهذا الوصف. جرّب كلمة أقصر أو اختر موضوعاً آخر.")
    else:
        st.info("🔍 اكتب سؤالك في الأعلى للحصول على إجابة")

# ============================================================
# 7. الموضوعات
# ============================================================

st.markdown("---")
st.markdown("### ✦ كل الموضوعات")

categories = ["☽ العبادات", "◈ المعاملات", "⌂ الأسرة", "✧ الحياة اليومية"]
cols = st.columns(4)
for i, cat in enumerate(categories):
    with cols[i]:
        if st.button(cat, use_container_width=True):
            category_name = cat.replace("☽ ", "").replace("◈ ", "").replace("⌂ ", "").replace("✧ ", "")
            st.info(f"📂 عرض مسائل {category_name}")

# ============================================================
# 8. خريطة الآراء (المذاهب)
# ============================================================

st.markdown("---")
st.markdown("### 🗺️ خريطة الآراء")

with st.expander("المذاهب السنية", expanded=True):
    cols = st.columns(5)
    sunni_schools = ["المالكي", "الشافعي", "الحنبلي", "الحنفي", "الظاهري"]
    for i, school in enumerate(sunni_schools):
        with cols[i]:
            st.button(school, use_container_width=True)

with st.expander("المذاهب الشيعية", expanded=True):
    cols = st.columns(2)
    shia_schools = ["الجعفري الاثنا عشري", "الزيدي"]
    for i, school in enumerate(shia_schools):
        with cols[i]:
            st.button(school, use_container_width=True)

with st.expander("المذهب الإباضي", expanded=True):
    st.button("الإباضي", use_container_width=True)

st.button("رأي آخر", use_container_width=True)

# ============================================================
# 9. الأئمة المؤسسون
# ============================================================

st.markdown("---")
with st.expander("📜 الأئمة المؤسسون", expanded=False):
    for imam in imams_data:
        st.markdown(f"""
        <div style="background: #f5f7f5; padding: 12px 16px; border-radius: 12px; margin-bottom: 10px; border-right: 4px solid #d4a854;">
            <h4 style="margin: 0; color: #1e3a2f;">{imam['name']}</h4>
            <p style="margin: 2px 0; color: #d4a854; font-weight: 600;">{imam['school']}</p>
            <p style="margin: 4px 0 0 0; color: #3d4f5f;">أشهر العلماء: {imam['scholars']}</p>
        </div>
        """, unsafe_allow_html=True)

# ============================================================
# 10. الدول والمذاهب الرسمية
# ============================================================

with st.expander("🗺️ المذهب الرسمي السائد في الدول الإسلامية", expanded=False):
    cols = st.columns(3)
    for i, country in enumerate(countries_data):
        with cols[i % 3]:
            st.markdown(f"""
            <div style="background: #f5f7f5; padding: 8px 12px; border-radius: 8px; margin-bottom: 6px; border-right: 3px solid #d4a854;">
                <strong>{country['country']}</strong><br>
                <span style="color: #d4a854;">{country['madhab']}</span><br>
                <span style="font-size: 0.8rem; color: #6a7f78;">👥 {country['population']}</span>
            </div>
            """, unsafe_allow_html=True)

# ============================================================
# 11. قاموس المصطلحات
# ============================================================

with st.expander("📚 قاموس المصطلحات الفقهية", expanded=False):
    for term in glossary_terms:
        st.markdown(f"""
        <div style="background: #f5f7f5; padding: 12px 16px; border-radius: 12px; margin-bottom: 10px; border-right: 4px solid #1e3a2f;">
            <h4 style="margin: 0; color: #1e3a2f;">{term['term']}</h4>
            <p style="margin: 4px 0 0 0; color: #3d4f5f;">{term['definition']}</p>
        </div>
        """, unsafe_allow_html=True)

# ============================================================
# 12. التذييل
# ============================================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px 0; color: #6a7f78;">
    <p>المعرفة أمانة. نراجع كل مادة من مصادرها الأصلية، ونوضح مواضع الاتفاق والاختلاف بإنصاف.</p>
    <a href="#" style="color: #8bc4b0; text-decoration: none; font-weight: 600;">تعرّف على منهجيتنا →</a>
    <p style="font-size: 0.8rem; margin-top: 10px;">© ٢٠٢٤ بيان</p>
</div>
""", unsafe_allow_html=True)
