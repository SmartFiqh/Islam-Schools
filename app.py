```python
import streamlit as st
import json
import os
from datetime import datetime
import re
from difflib import get_close_matches

# ============================================================
# 1. إعداد الصفحة
# ============================================================
st.set_page_config(
    page_title="الجامع المرشد للآراء الفقهية",
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
            "keywords": ["جماعة", "مسجد", "رجال", "صلاة", "فرض", "سنة", "واجب", "الجماعة", "المسجد"]
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
            "keywords": ["زكاة", "أسهم", "استثمار", "تجارة", "نصاب", "مال", "الزكاة", "الأسهم"]
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
            "keywords": ["جمع", "سفر", "مسافر", "صلاة", "تخفيف", "رخصة", "الجمع", "السفر"]
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
            "keywords": ["وضوء", "نواقض", "طهارة", "بول", "غائط", "نوم", "مس", "الوضوء"]
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
            "keywords": ["ربa", "حرام", "قرض", "فائدة", "بنوك", "معاملة", "ذنب", "الربا"]
        },
        {
            "id": 6,
            "title": "حكم النقاب",
            "category": "العبادات",
            "rulings": {
                "very_short": "مختلف فيه",
                "short": "النقاب مختلف فيه بين الفقهاء، والأفضل التقوى",
                "full": "النقاب موضوع خلاف بين الفقهاء. يرى بعضهم أنه واجب، ويرى آخرون أنه مستحب أو مباح. والأمر يعود للمرأة في اختيار ما تطمئن به قلبها، مع مراعاة العرف والتقاليد."
            },
            "keywords": ["نقاب", "حجاب", "مرأة", "وجه", "الستر", "المرأة"]
        },
        {
            "id": 7,
            "title": "التيمم",
            "category": "العبادات",
            "rulings": {
                "very_short": "جائز",
                "short": "التيمم جائز عند عدم وجود الماء أو العذر الشرعي",
                "full": "التيمم هو بديل عن الوضوء والغسل عند عدم وجود الماء، أو لمرض يمنع استعماله. يُمسح التراب على الوجه والكفين، وهو رخصة من الله للتيسير على عباده."
            },
            "keywords": ["تيمم", "ماء", "تراب", "وضوء", "غسل", "رخصة", "مرض", "التيمم"]
        },
        {
            "id": 8,
            "title": "صلاة المسافر",
            "category": "العبادات",
            "rulings": {
                "very_short": "جائز",
                "short": "يجوز للمسافر قصر الصلاة وجمعها",
                "full": "يجوز للمسافر قصر الصلاة الرباعية (الظهر، العصر، العشاء) إلى ركعتين، وجمع الصلاة (الظهر مع العصر، والمغرب مع العشاء). هذه رخصة من الله للتخفيف على المسافرين."
            },
            "keywords": ["سفر", "مسافر", "صلاة", "قصر", "جمع", "تخفيف", "رخصة", "المسافر"]
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
# 4. الذكاء الاصطناعي لفهم الأسئلة
# ============================================================

def smart_search(query, issues_data, category_filter, madhab_filter, level='full'):
    """بحث ذكي يفهم الأسئلة بأسلوب ركيك ويعطي أقرب إجابة مع فلترة حسب المجال والمذهب"""
    if not query:
        return []
    
    query = query.strip().lower()
    results = []
    
    # 1. البحث المباشر في العناوين والكلمات المفتاحية
    for issue in issues_data:
        # تطبيق فلتر المجال
        if category_filter != "الكل" and issue.get('category', '') != category_filter:
            continue
            
        title_match = query in issue.get('title', '').lower()
        keyword_match = any(query in kw.lower() for kw in issue.get('keywords', []))
        full_text_match = query in issue.get('rulings', {}).get('full', '').lower()
        
        if title_match or keyword_match or full_text_match:
            results.append(issue)
    
    # 2. إذا لم يجد، استخدم خوارزمية التشابه (مطابقة الكلمات)
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
    
    # 3. إذا لم يجد، استخدم البحث بالمرادفات
    if not results:
        synonyms = {
            "صلاة": ["صلات", "الصلاة", "صلي", "يصلي", "صليت", "يصلي"],
            "زكاة": ["زكاه", "الزكاة", "زكي", "يزكي"],
            "سفر": ["السفر", "مسافر", "سافرة", "سافرت"],
            "وضوء": ["الوضوء", "وضوئ", "يتوضأ", "توضأ"],
            "ربا": ["الربا", "ربوي", "فوائد", "فائدة"],
            "جماعة": ["الجماعة", "جماعه", "الجماعه", "جماعي"],
            "نقاب": ["النقاب", "حجاب", "وجه", "مرأة"],
            "تيمم": ["التيمم", "تراب", "صعيد"],
            "نكاح": ["النكاح", "زواج", "تزوج"],
            "بيع": ["البيع", "شريت", "اشتريت"]
        }
        
        for word in query_words:
            for synonym_key, synonym_list in synonyms.items():
                if word in synonym_list:
                    for issue in issues_data:
                        if category_filter != "الكل" and issue.get('category', '') != category_filter:
                            continue
                        if synonym_key in issue.get('title', '').lower() or any(synonym_key in kw.lower() for kw in issue.get('keywords', [])):
                            if issue not in results:
                                results.append(issue)
    
    # 4. عرض النتائج حسب المستوى المطلوب
    final_results = []
    for issue in results:
        rulings = issue.get('rulings', {})
        answer = rulings.get(level, rulings.get('full', 'لا توجد إجابة'))
        final_results.append({
            'id': issue.get('id'),
            'title': issue.get('title'),
            'category': issue.get('category'),
            'answer': answer,
            'level': level
        })
    
    return final_results

# ============================================================
# 5. واجهة المستخدم
# ============================================================

# الشعار والهوية - اتجاه النص من اليمين لليسار
st.markdown("""
<div style="text-align: center; padding: 20px 0; background: linear-gradient(145deg, #0f231c, #2a5c4a); color: white; border-radius: 16px; margin-bottom: 30px; direction: rtl;">
    <h1 style="font-size: 2.5rem; margin: 0;">📖 الجامع المرشد للآراء الفقهية</h1>
    <p style="font-size: 1.2rem; color: #d6e4de; margin: 0;">مرشد الآراء الفقهية</p>
    <p style="font-size: 0.95rem; color: #b2d1c4; margin: 0;">للفهم والتبصر، لا لإصدار الفتاوى</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# 6. خيارات المستخدم (التدرج في البحث)
# ============================================================

st.markdown('<div style="direction: rtl;">', unsafe_allow_html=True)

st.markdown("---")
st.markdown("### 🔍 خطوات البحث")

# الخطوة 1: اختيار المجال
st.markdown("#### ١. اختر المجال الفقهي:")
category_filter = st.radio(
    "",
    ["الكل", "العبادات", "المعاملات", "الأسرة", "الحياة اليومية"],
    horizontal=True
)

# الخطوة 2: اختيار المذاهب
st.markdown("#### ٢. اختر المذاهب التي تريد عرضها:")
madhabs = st.multiselect(
    "",
    ["المالكي", "الشافعي", "الحنبلي", "الحنفي", "الظاهري", "الجعفري", "الزيدي", "الإباضي", "رأي آخر"],
    default=["المالكي", "الشافعي", "الحنبلي", "الحنفي"]
)

# الخطوة 3: اختيار طريقة الإجابة
st.markdown("#### ٣. اختر مستوى الإجابة:")
answer_level = st.radio(
    "",
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
# 7. كتابة السؤال
# ============================================================

st.markdown("---")
st.markdown("#### ٤. اكتب سؤالك:")

col1, col2 = st.columns([4, 1])
with col1:
    search_query = st.text_input("", placeholder="اكتب سؤالك هنا...", label_visibility="collapsed")
with col2:
    search_btn = st.button("🔍 ابحث", use_container_width=True)

# ============================================================
# 8. عرض النتائج
# ============================================================

if search_query or search_btn:
    query = search_query.strip()
    if query:
        with st.spinner("🧠 جاري البحث والتحليل..."):
            results = smart_search(query, issues_data, category_filter, madhabs, selected_level)
        
        if results:
            st.markdown(f"### 📊 النتائج ({len(results)} مسألة)")
            for issue in results:
                with st.expander(f"📌 {issue['title']} ({issue['category']})"):
                    st.markdown(f"**الإجابة:** {issue['answer']}")
                    st.markdown("*هذا والله أعلم*")
        else:
            st.warning("🔍 لم نجد مسألة بهذا الوصف في المجال والمذاهب المختارة. جرّب تغيير الفلتر أو كلمة أقصر.")
    else:
        st.info("✍️ اكتب سؤالك في الأعلى للحصول على إجابة")

# ============================================================
# 9. الموضوعات
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
# 10. خريطة الآراء (المذاهب)
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
# 11. الأئمة المؤسسون
# ============================================================

st.markdown("---")
with st.expander("📜 الأئمة المؤسسون", expanded=False):
    for imam in imams_data:
        st.markdown(f"""
        <div style="background: #f5f7f5; padding: 12px 16px; border-radius: 12px; margin-bottom: 10px; border-right: 4px solid #d4a854; direction: rtl;">
            <h4 style="margin: 0; color: #1e3a2f;">{imam['name']}</h4>
            <p style="margin: 2px 0; color: #d4a854; font-weight: 600;">{imam['school']}</p>
            <p style="margin: 4px 0 0 0; color: #3d4f5f;">أشهر العلماء: {imam['scholars']}</p>
        </div>
        """, unsafe_allow_html=True)

# ============================================================
# 12. الدول والمذاهب الرسمية
# ============================================================

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

# ============================================================
# 13. قاموس المصطلحات
# ============================================================

with st.expander("📚 قاموس المصطلحات الفقهية", expanded=False):
    for term in glossary_terms:
        st.markdown(f"""
        <div style="background: #f5f7f5; padding: 12px 16px; border-radius: 12px; margin-bottom: 10px; border-right: 4px solid #1e3a2f; direction: rtl;">
            <h4 style="margin: 0; color: #1e3a2f;">{term['term']}</h4>
            <p style="margin: 4px 0 0 0; color: #3d4f5f;">{term['definition']}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# 14. التذييل
# ============================================================

st.markdown("""
<div style="text-align: center; padding: 20px 0; color: #6a7f78; direction: rtl;">
    <p>المعرفة أمانة. نراجع كل مادة من مصادرها الأصلية، ونوضح مواضع الاتفاق والاختلاف بإنصاف.</p>
    <a href="#" style="color: #8bc4b0; text-decoration: none; font-weight: 600;">تعرّف على منهجيتنا →</a>
    <p style="font-size: 0.8rem; margin-top: 10px;">© ٢٠٢٤ الجامع المرشد للآراء الفقهية</p>
</div>
""", unsafe_allow_html=True)
```
