import os
import re
import streamlit as st
from serpapi import GoogleSearch
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="KisanMandi & Krishi Mitra",
    page_icon="🌾",
    layout="wide"
)

# Clean Card Styling
st.markdown("""
<style>
    /* Light Sky Blue Main Background */
    .stApp {
        background: linear-gradient(180deg, #E8F5E9 0%, #F1F8E9 50%, #F9FBF9 100%) !important;
        color: #143622 !important;
    }

    /* Input boxes ko white karein */
    div[data-baseweb="input"] > div {
        background-color: #FFFFFF !important;
        color: #143622 !important;
    }

    /* Success banner ke inner container ko light green karein */
    [data-testid="stAlert"] > div {
        background-color: #DDF3E4 !important;
        color: #143622 !important;
    }

    /* Metric ke neeche wale dark pill badges ko light green karein */
    [data-testid="stMetricDelta"] > div {
        background-color: #E8F5E9 !important;
        color: #1B5E20 !important;
        padding: 2px 8px;
        border-radius: 6px;
    }

    /* Sidebar Sky Blue */
    [data-testid="stSidebar"] {
        background-color: #BFE6FF;
        border-right: 1px solid #90CAF9;
    }
    [data-testid="stSidebar"] * {
        color: #0B2545 !important;
    }

    /* Readable Dark Text for Headings & Labels */
    h1, h2, h3, p, label, .stMarkdown {
        color: #0B2545 !important;
    }

    /* Clean White Input Boxes */
    .stTextInput input {
        background-color: #FFFFFF !important;
        color: #0B2545 !important;
        border: 2px solid #64B5F6 !important;
        border-radius: 10px !important;
        font-size: 1.05rem !important;
    }

    /* Green Farmer-Friendly Action Button */
    .stButton > button {
        background-color: #1B7F3A !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 10px !important;
        font-size: 1.05rem !important;
        font-weight: 700 !important;
    }
    .stButton > button:hover {
        background-color: #14632D !important;
    }

    /* Top Metric Cards */
    [data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1.5px solid #90CAF9;
        border-top: 5px solid #0288D1;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 3px 10px rgba(2, 136, 209, 0.08);
    }
    [data-testid="stMetricLabel"] {
        color: #37474F !important;
        font-weight: 600 !important;
    }
    [data-testid="stMetricValue"] {
        color: #0B2545 !important;
        font-weight: 800 !important;
    }

    /* Data Cards */
    .info-card {
        background-color: #FFFFFF;
        border: 1px solid #B3E5FC;
        border-left: 6px solid #1B7F3A;
        padding: 16px;
        border-radius: 12px;
        margin-bottom: 12px;
        box-shadow: 0 3px 8px rgba(0, 0, 0, 0.05);
    }
    .card-title {
        font-size: 1.08rem;
        font-weight: 700;
        color: #0D47A1;
        margin-bottom: 6px;
    }
    .card-body {
        font-size: 0.96rem;
        color: #1E293B;
        line-height: 1.55;
    }
    .card-meta {
        font-size: 0.84rem;
        font-weight: 600;
        color: #2E7D32;
        margin-top: 8px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🌾 KisanMandi & Krishi Mitra")
st.markdown("Sirf apni **Fasal (Crop)** ka naam daalein — Live Mandi Bhav, Mausam, Najdeeki Mandis, aur Sarkari Yojanayein seedha yahin dekhein.")
st.divider()

# Sidebar
with st.sidebar:
    st.header("🔑 SerpApi Configuration")
    serpapi_key = os.getenv("SERPAPI_KEY") or st.text_input("Enter SerpApi Key", type="password")
    st.divider()
    st.markdown("**100% On-Page Dashboard:**")
    st.markdown("- 💰 Extracted Mandi Price Metrics\n- 🌦️ Live Weather & Forecast\n- 📍 Nearby APMC Mandis (Maps)\n- 🏛️ Govt Schemes & Subsidies")
    st.caption("🏆 Beyond 9TO5 Buildathon | Track 1")

# Main Inputs (City optional hai, default Maharashtra/India lega)
col1, col2, col3 = st.columns([2, 2, 1])
with col1:
    crop = st.text_input("🌱 Fasal ka Naam (Crop) *", placeholder="e.g., Onion, Wheat, Tomato, Soybean, Cotton")
with col2:
    city = st.text_input("📍 District / Shehar (Optional)", placeholder="Default: Maharashtra (ya Pune, Nashik, Indore...)")
with col3:
    st.write("")
    st.write("")
    search_btn = st.button("🔍 Live Data Dekhein", type="primary", use_container_width=True)

def fetch_serp_data(params):
    search = GoogleSearch(params)
    return search.get_dict()

def extract_prices(snippets_list):
    """Snippets me se ₹ wale mandi prices (quintal rates) extract karta hai"""
    prices = []
    for text in snippets_list:
        matches = re.findall(r'₹\s?([0-9,]+)', text)
        for m in matches:
            val = int(m.replace(",", ""))
            # Per quintal realistic range filter (₹300 se ₹50,000)
            if 300 <= val <= 50000:
                prices.append(val)
    return sorted(list(set(prices)))

if search_btn:
    if not serpapi_key:
        st.error("⚠️ Kripya `.env` file mein ya sidebar mein apni SERPAPI_KEY daalein.")
    elif not crop.strip():
        st.warning("⚠️ Kripya kam se kam Fasal (Crop) ka naam likhein.")
    else:
        target_location = city.strip() if city.strip() else "Maharashtra"
        with st.spinner(f"{target_location} ke liye {crop.title()} ka live data nikala ja raha hai..."):
            try:
                # 1. Google Search: Live Mandi Bhav
                mandi_data = fetch_serp_data({
                    "engine": "google",
                    "q": f"{crop} mandi bhav today {target_location} agmarknet modal price per quintal",
                    "location": "India",
                    "hl": "en",
                    "gl": "in",
                    "api_key": serpapi_key
                })

                # 2. Google Search: Weather
                weather_data = fetch_serp_data({
                    "engine": "google",
                    "q": f"weather {target_location}",
                    "location": "India",
                    "hl": "en",
                    "gl": "in",
                    "api_key": serpapi_key
                })

                # 3. Google Maps: Nearby APMC Mandis
                maps_data = fetch_serp_data({
                    "engine": "google_maps",
                    "q": f"APMC mandi market in {target_location}",
                    "hl": "en",
                    "gl": "in",
                    "api_key": serpapi_key
                })

                # 4. Google Search: Govt Schemes & Subsidies (Detailed snippets ke liye)
                schemes_data = fetch_serp_data({
                    "engine": "google",
                    "q": f"government scheme subsidy for {crop} farmers India eligibility benefits 2026",
                    "location": "India",
                    "hl": "en",
                    "gl": "in",
                    "api_key": serpapi_key
                })

                st.success(f"✅ {target_location.title()} — {crop.title()} ki Sampoorna Jankari")

                # --- TOP KPI METRICS (Price + Weather ek hi row mein) ---
                organic_mandi = mandi_data.get("organic_results", [])
                all_snippets = [item.get("snippet", "") for item in organic_mandi[:5]]
                if mandi_data.get("answer_box", {}).get("snippet"):
                    all_snippets.insert(0, mandi_data["answer_box"]["snippet"])

                extracted_rates = extract_prices(all_snippets)
                weather_box = weather_data.get("answer_box", {})

                m1, m2, m3, m4 = st.columns(4)
                with m1:
                    if extracted_rates:
                        avg_rate = sum(extracted_rates) // len(extracted_rates)
                        st.metric("💰 Anumanit Mandi Rate", f"₹{avg_rate:,} / Qtl", f"Range: ₹{min(extracted_rates):,} - ₹{max(extracted_rates):,}")
                    else:
                        st.metric("💰 Mandi Status", "Live Reports Below", "Check Market Cards")
                with m2:
                    st.metric("🌡️ Temperature", f"{weather_box.get('temperature', 'N/A')}°C", weather_box.get("weather", "Clear"))
                with m3:
                    st.metric("💧 Humidity (Nami)", weather_box.get("humidity", "N/A"), f"Wind: {weather_box.get('wind', 'N/A')}")
                with m4:
                    mandi_count = len(maps_data.get("local_results", []))
                    st.metric("📍 Najdeeki Mandis", f"{mandi_count} Markets Found", target_location.title())

                st.divider()

                # --- 3 COLUMNS: 100% ON-PAGE CARDS (NO EXTERNAL LINKS) ---
                c1, c2, c3 = st.columns(3)

                # Column 1: Live Mandi Bhav
                with c1:
                    st.subheader("💰 Live Mandi Bhav Details")
                    if organic_mandi:
                        for item in organic_mandi[:4]:
                            title = item.get("title", "Market Report")
                            snippet = item.get("snippet", "No details available.")
                            source = item.get("displayed_link", "Agmarknet / Mandi Source").split("›")[0]
                            st.markdown(f"""
                            <div class="info-card">
                                <div class="card-title">{title}</div>
                                <div class="card-body">{snippet}</div>
                                <div class="card-meta">📊 Source: {source}</div>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.info("Is fasal ke liye abhi koi live rate snippet uplabdh nahi hai.")

                # Column 2: Nearby APMC Mandis
                with c2:
                    st.subheader("📍 Najdeeki APMC Mandis")
                    places = maps_data.get("local_results", [])
                    if places:
                        for place in places[:4]:
                            title = place.get("title", "APMC Market")
                            address = place.get("address", "Address unavailable")
                            rating = place.get("rating", "N/A")
                            phone = place.get("phone", "Not listed")
                            hours = place.get("hours", "Open hours not listed")
                            st.markdown(f"""
                            <div class="info-card">
                                <div class="card-title">{title} (⭐ {rating})</div>
                                <div class="card-body">📌 {address}</div>
                                <div class="card-meta">📞 {phone} | 🕒 {hours}</div>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.info("Is location ke paas APMC mandi listing nahi mili.")

                # Column 3: Govt Schemes & Subsidies
                with c3:
                    st.subheader("🏛️ Sarkari Yojanayein & Subsidies")
                    scheme_results = schemes_data.get("organic_results", [])
                    if scheme_results:
                        for scheme in scheme_results[:4]:
                            title = scheme.get("title", "Government Scheme")
                            snippet = scheme.get("snippet", "")
                            source = scheme.get("displayed_link", "Govt Portal").split("›")[0]
                            st.markdown(f"""
                            <div class="info-card">
                                <div class="card-title">{title}</div>
                                <div class="card-body">{snippet}</div>
                                <div class="card-meta">🏛️ Portal: {source}</div>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.info("Koi scheme jankari nahi mili.")

            except Exception as e:
                st.error(f"Data fetch karne mein samasya aayi: {e}")
