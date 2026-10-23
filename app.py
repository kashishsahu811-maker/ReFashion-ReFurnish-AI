"""
================================================================================
ReFashion & ReFurnish AI - Multi-Agent Web Application (app.py)
--------------------------------------------------------------------------------
A professional, beginner-friendly circular crafting platform powered by three
collaborating rule-based agents and an Agent Coordinator.

AGENTS:
1. Fashion Agent: Upcycles old clothes and fabric waste.
2. Furniture Agent: Reuses and renovates discarded furniture.
3. Business Agent: Computes unit costs, selling price, profit, & marketing copy.
4. Agent Coordinator: Classifies user intent and routes requests to the right agent.

Theme: Professional Dark Mode (Near-Black #121212, Charcoal #1E1E1E & Deep Green #176B4D)
Logic: 100% Transparent Rule-Based (Zero Paid APIs or external LLMs required)
================================================================================
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import urllib.parse
from agents import (
    FashionAgent, 
    FurnitureAgent, 
    BusinessAgent, 
    AgentCoordinator,
    PhotoDesignStudioEngine
)
from image_to_image import (
    AIImageToImageService,
    WasteItemAnalyzer,
    LocalVisionSynthesisEngine,
    create_sample_waste_image,
    create_composite_before_after
)

# ==========================================
# 1. PAGE CONFIGURATION & THEME STYLING
# ==========================================
st.set_page_config(
    page_title="ReFashion & ReFurnish AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Agents & Studio Engines
coordinator = AgentCoordinator()
fashion_agent = coordinator.fashion_agent
furniture_agent = coordinator.furniture_agent
business_agent = coordinator.business_agent
design_engine = PhotoDesignStudioEngine()
img2img_service = AIImageToImageService()

if "saved_design_ideas" not in st.session_state:
    st.session_state["saved_design_ideas"] = []

# Professional Dark Theme CSS
CUSTOM_CSS = """
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Playfair+Display:ital,wght@0,600;0,700;1,400&display=swap');

    :root {
        --bg-main: #121212;
        --bg-sidebar: #1E1E1E;
        --bg-card: #242424;
        --bg-card-hover: #2A2A2A;
        --border-color: #383838;
        --border-subtle: #2C2C2C;
        --text-white: #FFFFFF;
        --text-light: #E0E0E0;
        --text-muted: #A0A0A0;
        --btn-green: #176B4D;
        --btn-green-hover: #1E825E;
        --accent-mint: #69DB9B;
    }

    /* Overall App Background */
    .stApp {
        background-color: var(--bg-main) !important;
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: var(--text-light);
    }

    /* Top Header Bar */
    header[data-testid="stHeader"] {
        background-color: rgba(18, 18, 18, 0.95) !important;
    }

    /* Left Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: var(--bg-sidebar) !important;
        border-right: 1px solid var(--border-color) !important;
    }
    
    section[data-testid="stSidebar"] .stMarkdown h1, 
    section[data-testid="stSidebar"] .stMarkdown h2, 
    section[data-testid="stSidebar"] .stMarkdown h3,
    section[data-testid="stSidebar"] .stMarkdown h4 {
        color: var(--text-white) !important;
        font-family: 'Playfair Display', serif;
    }

    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] span, 
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] div {
        color: var(--text-light) !important;
    }

    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Playfair Display', serif;
        color: var(--text-white) !important;
        font-weight: 700;
    }

    p, span, div {
        color: var(--text-light);
    }

    label, [data-testid="stWidgetLabel"] p, [data-testid="stWidgetLabel"] label {
        color: var(--text-light) !important;
        font-weight: 500;
        font-size: 0.95rem;
    }

    /* Hero Banner */
    .hero-banner {
        background: linear-gradient(135deg, #0F2D1F 0%, #164831 60%, #176B4D 100%);
        border: 1px solid #1E5C3E;
        border-radius: 20px;
        padding: 38px 34px;
        color: #FAF8F5;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        margin-bottom: 25px;
    }
    
    .hero-banner h1 {
        font-family: 'Playfair Display', serif;
        font-size: 2.7rem;
        font-weight: 700;
        color: #FFFFFF !important;
        margin-bottom: 10px;
        letter-spacing: -0.5px;
    }
    
    .hero-banner p {
        font-size: 1.1rem;
        color: #D4E5DC !important;
        max-width: 780px;
        line-height: 1.6;
        margin-bottom: 16px;
    }

    .badge-pill {
        display: inline-block;
        padding: 5px 13px;
        background: rgba(255, 255, 255, 0.12);
        border: 1px solid rgba(255, 255, 255, 0.25);
        border-radius: 50px;
        font-size: 0.82rem;
        font-weight: 600;
        color: #FFFFFF !important;
        margin-right: 8px;
        margin-bottom: 6px;
    }

    /* Card Containers */
    .eco-card {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35);
        margin-bottom: 20px;
        transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
    }

    .eco-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.5);
        border-color: #176B4D;
        background: var(--bg-card-hover);
    }

    .eco-card h3 {
        font-family: 'Playfair Display', serif;
        color: var(--text-white) !important;
        margin-top: 0;
        font-size: 1.45rem;
        font-weight: 700;
    }

    .eco-card h4 {
        color: var(--accent-mint) !important;
        font-size: 1.1rem;
        font-weight: 600;
    }

    /* Metric Cards */
    .metric-card {
        background: var(--bg-card);
        border-radius: 14px;
        border: 1px solid var(--border-color);
        border-left: 5px solid var(--btn-green);
        padding: 16px 18px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }

    .metric-value {
        font-size: 1.85rem;
        font-weight: 800;
        color: #FFFFFF !important;
        line-height: 1.1;
    }

    .metric-label {
        font-size: 0.82rem;
        color: var(--text-muted) !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 600;
        margin-top: 5px;
    }

    /* Tags */
    .tag-green {
        background-color: #133926;
        color: #69DB9B !important;
        border: 1px solid #1E5C3E;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
        margin-right: 6px;
    }

    .tag-terracotta {
        background-color: #381E19;
        color: #FFA585 !important;
        border: 1px solid #5C2D24;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
        margin-right: 6px;
    }

    .tag-gold {
        background-color: #362914;
        color: #FFD278 !important;
        border: 1px solid #5E461F;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
        margin-right: 6px;
    }

    /* Step / Instructions box */
    .step-box {
        background: #1A1A1A;
        border: 1px solid var(--border-color);
        border-left: 3px solid var(--btn-green);
        padding: 10px 14px;
        border-radius: 0 8px 8px 0;
        margin-bottom: 10px;
        font-size: 0.95rem;
        color: var(--text-light);
    }

    .step-num {
        font-weight: 700;
        color: var(--accent-mint) !important;
    }

    /* Reasoning Trace Box */
    .reasoning-box {
        background: #15271E;
        border: 1px dashed #2E6B4A;
        border-radius: 10px;
        padding: 12px 16px;
        margin: 12px 0 16px 0;
        font-size: 0.88rem;
        color: #C2E2D0 !important;
    }

    .reasoning-box b {
        color: #FFFFFF !important;
    }

    .tip-box {
        background: #17241D;
        border: 1px solid #284435;
        border-left: 4px solid var(--btn-green);
        padding: 14px 18px;
        border-radius: 0 10px 10px 0;
        margin: 14px 0;
        color: #D5E5DC !important;
        font-size: 0.95rem;
    }

    .tip-box b {
        color: #69DB9B !important;
    }

    /* Custom Streamlit Buttons */
    div.stButton > button:first-child, div[data-testid="stButton"] > button {
        background-color: var(--btn-green) !important;
        color: #FFFFFF !important;
        border: 1px solid #1E825E !important;
        padding: 9px 22px;
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.2s ease;
    }

    div.stButton > button:first-child:hover, div[data-testid="stButton"] > button:hover {
        background-color: var(--btn-green-hover) !important;
        color: #FFFFFF !important;
        border-color: #27A678 !important;
        box-shadow: 0 4px 14px rgba(23, 107, 77, 0.45);
    }

    /* Inputs: text, number, selectbox, textarea */
    div[data-baseweb="input"] > div, 
    div[data-baseweb="base-input"] > textarea, 
    div[data-baseweb="select"] > div {
        background-color: var(--bg-card) !important;
        color: #FFFFFF !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
    }

    input, textarea {
        color: #FFFFFF !important;
        background-color: transparent !important;
    }

    ::placeholder {
        color: #7E7E7E !important;
    }

    /* Selectbox dropdown options */
    ul[role="listbox"], div[data-baseweb="popover"], div[data-baseweb="menu"] {
        background-color: var(--bg-card) !important;
        color: #FFFFFF !important;
        border: 1px solid var(--border-color) !important;
    }

    li[role="option"] {
        color: #E0E0E0 !important;
        background-color: var(--bg-card) !important;
    }

    li[role="option"]:hover, li[aria-selected="true"] {
        background-color: var(--btn-green) !important;
        color: #FFFFFF !important;
    }

    /* Expanders */
    div[data-testid="stExpander"] {
        background-color: var(--bg-card) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 12px !important;
        box-shadow: 0 3px 10px rgba(0,0,0,0.2);
    }

    div[data-testid="stExpander"] summary {
        color: #FFFFFF !important;
        background-color: var(--bg-card) !important;
        font-weight: 600;
    }

    div[data-testid="stExpander"] summary:hover {
        color: var(--accent-mint) !important;
    }

    div[data-testid="stExpander"] div[data-testid="stExpanderDetails"] {
        background-color: #1A1A1A !important;
        color: #E0E0E0 !important;
        border-top: 1px solid var(--border-color);
        padding: 16px;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: transparent !important;
        gap: 8px;
        border-bottom: 1px solid var(--border-color);
    }

    .stTabs [data-baseweb="tab"] {
        color: var(--text-muted) !important;
        background-color: var(--bg-sidebar) !important;
        border: 1px solid var(--border-color) !important;
        border-bottom: none !important;
        border-radius: 8px 8px 0 0 !important;
        padding: 9px 18px !important;
        font-weight: 600;
    }

    .stTabs [aria-selected="true"] {
        color: #FFFFFF !important;
        background-color: var(--bg-card) !important;
        border-top: 2px solid var(--btn-green) !important;
        border-left: 1px solid var(--border-color) !important;
        border-right: 1px solid var(--border-color) !important;
        border-bottom: none !important;
    }

    /* Checkbox & Radio Labels */
    div[data-testid="stCheckbox"] label span, 
    div[data-testid="stRadio"] label span,
    div[data-testid="stRadio"] div[role="radiogroup"] label {
        color: var(--text-light) !important;
    }

    /* Captions & Alerts */
    div[data-testid="stCaptionContainer"] p {
        color: #9E9E9E !important;
    }

    div[data-testid="stAlert"] {
        background-color: #15271E !important;
        color: #C2E2D0 !important;
        border: 1px solid #234E35 !important;
    }

    div[data-testid="stAlert"] p {
        color: #C2E2D0 !important;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ==========================================
# 2. HELPER CALCULATIONS
# ==========================================
def get_quick_eco_impact(clothes_count: int, furniture_count: int):
    """Calculates cumulative savings based on user actions."""
    water_liters = clothes_count * 2000
    co2_kg = (clothes_count * 1.8) + (furniture_count * 18.0)
    landfill_kg = (clothes_count * 0.6) + (furniture_count * 15.0)
    return {
        "water_liters": water_liters,
        "co2_kg": round(co2_kg, 1),
        "landfill_kg": round(landfill_kg, 1)
    }


# ==========================================
# 3. SIDEBAR NAVIGATION
# ==========================================
with st.sidebar:
    st.markdown("### 🌿 ReFashion & ReFurnish")
    st.markdown("<p style='font-size: 0.88rem; color: #A0A0A0;'>Multi-Agent Circular Crafting System</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    page = st.radio(
        "Navigation:",
        [
            "🏠 Home & Impact Hub",
            "🔄 AI Image-to-Image Studio",
            "🤖 Agent Coordinator (Auto-Route)",
            "👗 Fashion Agent (Clothes & Fabric)",
            "🪑 Furniture Agent (Wood & Decor)",
            "💼 Business Agent (Cost & Marketing)"
        ],
        index=0
    )
    
    st.markdown("---")
    st.markdown("#### 🌍 Quick Eco-Impact Gauge")
    sb_clothes = st.slider("Garments Upcycled:", 0, 50, 4)
    sb_furn = st.slider("Furniture Items Saved:", 0, 10, 2)
    eco_stats = get_quick_eco_impact(sb_clothes, sb_furn)
    
    st.markdown(f"""
    <div style='background: #183324; border: 1px solid #27543A; border-radius: 10px; padding: 12px;'>
        <p style='margin:0; font-size:0.82rem; color: #8BE0B0;'>💧 <b>{eco_stats['water_liters']:,} L</b> fresh water conserved</p>
        <p style='margin:4px 0 0 0; font-size:0.82rem; color: #8BE0B0;'>🌱 <b>{eco_stats['co2_kg']} kg</b> CO₂ emissions prevented</p>
        <p style='margin:4px 0 0 0; font-size:0.82rem; color: #8BE0B0;'>📦 <b>{eco_stats['landfill_kg']} kg</b> solid waste diverted</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
    <div style='font-size: 0.78rem; color: #A0A0A0; line-height: 1.4;'>
        <b>🛡️ Architecture Note:</b><br>
        Operates on transparent, deterministic expert-system rules. 
        Zero paid APIs or external LLMs required.
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# 4. PAGE ROUTING & MULTI-AGENT SECTIONS
# ==========================================

# -------------------------------------------------------------
# PAGE 1: HOME & IMPACT HUB
# -------------------------------------------------------------
if page == "🏠 Home & Impact Hub":
    st.markdown("""
    <div class="hero-banner">
        <span class="badge-pill">🤖 3 Autonomous Working Agents</span>
        <span class="badge-pill">🧭 Intelligent Coordinator</span>
        <span class="badge-pill">🛡️ 100% Free & Transparent Rules</span>
        <h1>ReFashion & ReFurnish AI</h1>
        <p>
            Meet your trio of specialized AI agents working together to convert textile scrap and old furniture 
            into marketable, beautiful home creations.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Feature Spotlight
    st.markdown("""
    <div class="eco-card" style="border: 2px solid #174D3B; background: linear-gradient(135deg, #10291D 0%, #174D3B 100%); margin-bottom: 25px;">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <span class="tag-gold">✨ AI IMAGE-TO-IMAGE STUDIO</span>
            <span style="font-size:0.85rem; color:#8FC0A9; font-weight:600;">Real Visual Reference • 4 Generated Upcycled Designs • Instant Before-After</span>
        </div>
        <h3 style="color:#FAF8F0 !important; margin: 8px 0 6px 0;">🔄 AI Image-to-Image Upcycling Studio</h3>
        <p style="color:#D4E5DC; font-size:0.95rem; line-height: 1.5; margin-bottom:12px;">
            Upload a photo of a broken chair, old table, damaged furniture, wooden waste, plastic waste, or fabric scraps. Our real AI Image-to-Image engine takes your uploaded photo as its direct visual reference and generates 4 newly synthesized upcycled product designs in a clear Before-and-After gallery with instant download buttons.
        </p>
        <div style="font-size: 0.85rem; color: #FAF8F0; font-weight: 600;">
            👉 <i>Select <b>"🔄 AI Image-to-Image Studio"</b> in the left sidebar to start!</i>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 3 Working Agents Showcase Cards
    st.markdown("## 🤖 Meet the Three Working Agents")
    
    ag1, ag2, ag3 = st.columns(3)
    with ag1:
        st.markdown("""
        <div class="eco-card">
            <span class="tag-green">Agent 1: Textiles</span>
            <h3>👗 Fashion Agent</h3>
            <p style="color: #CCCCCC; font-size: 0.92rem; line-height: 1.5;">
                Analyzes fabric weaves, denim weights, and condition to formulate cutting patterns, no-sew designs, and step-by-step garment upcycling blueprints.
            </p>
            <div style="font-size: 0.8rem; color: #69DB9B; font-weight: 600;">
                ✓ No-Sew filters • ✓ Custom textile generator
            </div>
        </div>
        """, unsafe_allow_html=True)

    with ag2:
        st.markdown("""
        <div class="eco-card">
            <span class="tag-terracotta">Agent 2: Woodwork</span>
            <h3>🪑 Furniture Agent</h3>
            <p style="color: #CCCCCC; font-size: 0.92rem; line-height: 1.5;">
                Inspects structural integrity of pallets, broken chairs, and drawers to prescribe sanding schedules, chalk painting, and non-toxic protective seals.
            </p>
            <div style="font-size: 0.8rem; color: #69DB9B; font-weight: 600;">
                ✓ Pallet HT safety check • ✓ Hand-tools filter
            </div>
        </div>
        """, unsafe_allow_html=True)

    with ag3:
        st.markdown("""
        <div class="eco-card">
            <span class="tag-gold">Agent 3: Economics</span>
            <h3>💼 Business Agent</h3>
            <p style="color: #CCCCCC; font-size: 0.92rem; line-height: 1.5;">
                Calculates production costs (COGS), labor wages, and fair retail profit margins, while generating high-converting social media marketing captions.
            </p>
            <div style="font-size: 0.8rem; color: #69DB9B; font-weight: 600;">
                ✓ Cost & Profit graphs • ✓ Social caption writer
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Global Environmental Counters
    st.markdown("## 🌍 Global Impact Statistics")
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">92M+</div>
            <div class="metric-label">Tons Textile Waste/Year</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">2,700 L</div>
            <div class="metric-label">Water for 1 New T-Shirt</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">80%</div>
            <div class="metric-label">Furniture Sent to Landfills</div>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">₹0</div>
            <div class="metric-label">Raw Material Starting Cost</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # The 5-Step Lifecycle
    st.markdown("## 🔄 The Upcycling Lifecycle")
    l1, l2, l3, l4, l5 = st.columns(5)
    with l1:
        st.markdown("""
        <div style="background:#242424; border:1px solid #383838; border-radius:12px; padding:16px; text-align:center;">
            <div style="font-size:1.6rem;">📦</div>
            <h5 style="color:#FFFFFF; margin:6px 0 2px 0;">1. Source</h5>
            <p style="font-size:0.78rem; color:#A0A0A0; margin:0;">Identify old clothing or discarded wood.</p>
        </div>
        """, unsafe_allow_html=True)
    with l2:
        st.markdown("""
        <div style="background:#242424; border:1px solid #383838; border-radius:12px; padding:16px; text-align:center;">
            <div style="font-size:1.6rem;">🧼</div>
            <h5 style="color:#FFFFFF; margin:6px 0 2px 0;">2. Prep</h5>
            <p style="font-size:0.78rem; color:#A0A0A0; margin:0;">Clean, sanitize, and sand surfaces.</p>
        </div>
        """, unsafe_allow_html=True)
    with l3:
        st.markdown("""
        <div style="background:#242424; border:1px solid #383838; border-radius:12px; padding:16px; text-align:center;">
            <div style="font-size:1.6rem;">✂️</div>
            <h5 style="color:#FFFFFF; margin:6px 0 2px 0;">3. Craft</h5>
            <p style="font-size:0.78rem; color:#A0A0A0; margin:0;">Stitch, glue, or join structure.</p>
        </div>
        """, unsafe_allow_html=True)
    with l4:
        st.markdown("""
        <div style="background:#242424; border:1px solid #383838; border-radius:12px; padding:16px; text-align:center;">
            <div style="font-size:1.6rem;">🎨</div>
            <h5 style="color:#FFFFFF; margin:6px 0 2px 0;">4. Finish</h5>
            <p style="font-size:0.78rem; color:#A0A0A0; margin:0;">Chalk paint, wax, or add lining.</p>
        </div>
        """, unsafe_allow_html=True)
    with l5:
        st.markdown("""
        <div style="background:#242424; border:1px solid #383838; border-radius:12px; padding:16px; text-align:center;">
            <div style="font-size:1.6rem;">💚</div>
            <h5 style="color:#FFFFFF; margin:6px 0 2px 0;">5. Monetize</h5>
            <p style="font-size:0.78rem; color:#A0A0A0; margin:0;">Price with Business Agent & market!</p>
        </div>
        """, unsafe_allow_html=True)


# -------------------------------------------------------------
# PAGE: AI PHOTO-TO-DESIGN STUDIO
# -------------------------------------------------------------
elif page in ["🔄 AI Image-to-Image Studio", "📸 AI Photo-to-Design Studio", "📸 AI Image-to-Image Studio"]:
    st.markdown("""
    <div class="hero-banner" style="background: linear-gradient(135deg, #0C261B 0%, #174D3B 55%, #1F6B51 100%);">
        <span class="badge-pill">🔄 Real AI Image-to-Image</span>
        <span class="badge-pill">📸 Visual Reference Guided</span>
        <span class="badge-pill">🎨 4 Distinct Upcycled Products</span>
        <span class="badge-pill">🛡️ Zero-Key & API Ready</span>
        <h1 style="color:#FAF8F0 !important;">AI Image-to-Image Upcycling Studio</h1>
        <p style="color:#D4E5DC !important;">
            Upload a photo of a broken chair, old table, damaged furniture, wooden waste, plastic waste, or fabric scraps.
            Our real AI Image-to-Image pipeline analyzes the visual reference, preserves its reusable materials,
            and generates 4 newly synthesized upcycled product designs in a clear Before-and-After gallery.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="tip-box">
        <b>💡 Real AI Image-to-Image Architecture:</b><br>
        This studio takes your uploaded photo as its direct visual reference. It extracts the raw material textures, 
        wood grain/patina, and reusable structural components (legs, slats, frame) to generate 
        <b>4 genuine, newly synthesized upcycled product designs</b>. 
        Works <b>100% free out-of-the-box</b> via the Local Vision Synthesis Engine, with optional support for Hugging Face, Stability AI, and Pollinations.
    </div>
    """, unsafe_allow_html=True)

    # Input Configuration Area
    col_upload, col_params = st.columns([1.15, 1.1])

    with col_upload:
        st.markdown("#### 1. 📸 Upload Waste Item Image")
        st.markdown("<p style='font-size:0.88rem; color:#A0A0A0;'>Upload a photo of a broken chair, old table, damaged furniture, wooden waste, plastic waste, or any discarded item.</p>", unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Upload Waste Item Photo (JPG, JPEG, PNG, WEBP):",
            type=["jpg", "jpeg", "png", "webp"],
            key="img2img_photo_uploader",
            help="Supported formats: JPG, JPEG, PNG, WEBP. Max size: 15MB."
        )

        # Quick Starter Presets for instant testing
        st.markdown("<p style='font-size:0.8rem; color:#8FC0A9; margin: 4px 0;'>Or test immediately with a sample waste photo:</p>", unsafe_allow_html=True)
        btn_c1, btn_c2, btn_c3 = st.columns(3)
        with btn_c1:
            if st.button("🪑 Broken Chair", use_container_width=True, key="preset_chair"):
                st.session_state["studio_uploaded_bytes"] = create_sample_waste_image("chair")
                st.session_state["studio_uploaded_name"] = "broken_wooden_chair.jpg"
                st.session_state["studio_uploaded_type"] = "image/jpeg"
                st.rerun()
        with btn_c2:
            if st.button("🪵 Pallet Wood", use_container_width=True, key="preset_pallet"):
                st.session_state["studio_uploaded_bytes"] = create_sample_waste_image("pallet")
                st.session_state["studio_uploaded_name"] = "weathered_pallet_wood.jpg"
                st.session_state["studio_uploaded_type"] = "image/jpeg"
                st.rerun()
        with btn_c3:
            if st.button("👖 Torn Denim", use_container_width=True, key="preset_denim"):
                st.session_state["studio_uploaded_bytes"] = create_sample_waste_image("denim")
                st.session_state["studio_uploaded_name"] = "discarded_denim_jeans.jpg"
                st.session_state["studio_uploaded_type"] = "image/jpeg"
                st.rerun()

        if uploaded_file is not None:
            # Store uploaded photo bytes immediately in session state
            st.session_state["studio_uploaded_bytes"] = uploaded_file.getvalue()
            st.session_state["studio_uploaded_name"] = uploaded_file.name
            st.session_state["studio_uploaded_type"] = uploaded_file.type
            st.success(f"✅ Waste Photo Loaded: **{uploaded_file.name}** ({len(st.session_state['studio_uploaded_bytes']) // 1024} KB)")

        # Display preview if bytes are present in memory
        if "studio_uploaded_bytes" in st.session_state:
            active_bytes = st.session_state["studio_uploaded_bytes"]
            active_name = st.session_state.get("studio_uploaded_name", "waste_item.jpg")
            
            # Run Computer Vision Analysis
            try:
                active_pil = Image.open(io.BytesIO(active_bytes)).convert("RGB")
                palette_data = WasteItemAnalyzer.extract_palette(active_pil)
                detected_analysis = WasteItemAnalyzer.detect_material_and_archetype(palette_data, active_name)
                st.session_state["studio_active_analysis"] = detected_analysis
            except Exception:
                palette_data = []
                detected_analysis = None

            with st.expander("👁️ View Uploaded Reference Photo & Material Analysis", expanded=True):
                st.image(active_bytes, caption=f"Active Visual Reference: {active_name}", use_container_width=True)
                if detected_analysis:
                    swatch_html = "".join([f"<span style='display:inline-block; width:18px; height:18px; border-radius:50%; background-color:{c['hex']}; margin-right:5px; border:1px solid #FAF8F0;' title='{c['hex']}'></span>" for c in palette_data])
                    st.markdown(f"""
                    <div style="background:#1C2620; border:1px solid #284435; border-radius:8px; padding:10px; font-size:0.83rem; color:#D4E5DC; margin-top:6px;">
                        <b>Detected Material:</b> {detected_analysis['material_name']}<br>
                        <b>Extracted Palette:</b> {swatch_html}<br>
                        <b>Reusable Parts:</b> {', '.join(detected_analysis['reusable_parts'][:2])}
                    </div>
                    """, unsafe_allow_html=True)

            if st.button("🗑️ Clear / Upload Another Photo", key="studio_clear_photo_btn"):
                st.session_state.pop("studio_uploaded_bytes", None)
                st.session_state.pop("studio_uploaded_name", None)
                st.session_state.pop("studio_uploaded_type", None)
                st.session_state.pop("img2img_active_results", None)
                st.rerun()
        else:
            st.markdown("""
            <div style="border: 2px dashed #174D3B; background: #16261E; border-radius: 12px; padding: 25px; text-align: center; margin-top: 10px;">
                <div style="font-size: 2.2rem; margin-bottom: 8px;">📷</div>
                <p style="margin: 0; font-size: 0.95rem; color: #FAF8F0; font-weight: 600;">Drag and drop your waste photo here</p>
                <p style="margin: 4px 0 0 0; font-size: 0.8rem; color: #8FC0A9;">Works with broken chairs, tables, pallets, fabric scraps, plastic & more</p>
            </div>
            """, unsafe_allow_html=True)

    with col_params:
        st.markdown("#### 2. ⚙️ AI Engine & Generation Settings")
        
        ai_provider = st.selectbox(
            "Select AI Image-to-Image Provider:",
            [
                "⚡ Local Vision Synthesis (Zero-Key / Free / Real Material Transfer)",
                "🤗 Hugging Face Serverless (Real Img2Img - Free HF Token)",
                "🎨 Stability AI SDXL (Native Img2Img - API Key)",
                "🐝 Pollinations AI (Pollen Key)"
            ],
            index=0,
            help="Local Vision Synthesis works 100% free offline with real material texture transfer. Cloud providers connect to remote diffusion models."
        )

        custom_notes = st.text_input(
            "Specific Notes / Flaws to Factor In (Optional):",
            placeholder="e.g. 'Broken wooden chair with intact mahogany legs and curved backrest'",
            help="Add any specific details or damaged parts you want the AI to factor into the upcycling designs."
        )

        # Advanced API Configuration Expander
        with st.expander("🔑 AI API Key & Model Settings (Optional)", expanded=False):
            st.markdown("""
            <p style="font-size:0.83rem; color:#A0A0A0; line-height:1.4;">
                <b>100% Free Default:</b> The Local Vision Synthesis Engine runs without any API key or subscription.<br>
                <b>Cloud Models:</b> To use remote diffusion models, paste your key below. Keys are stored in session memory only and never exposed in frontend code.
            </p>
            """, unsafe_allow_html=True)
            
            user_api_key = st.text_input(
                "Enter API Token / Key (Masked):",
                type="password",
                value=st.session_state.get("user_custom_api_key", ""),
                placeholder="hf_... or sk-...",
                help="Enter your free Hugging Face token or Stability AI key. Left blank = Uses Local Vision Synthesis."
            )
            if user_api_key:
                st.session_state["user_custom_api_key"] = user_api_key

            st.markdown("""
            <div style="font-size:0.75rem; color:#8FC0A9; margin-top:4px;">
                • <a href="https://huggingface.co/settings/tokens" target="_blank" style="color:#69DB9B;">Get Free Hugging Face Token</a> (No credit card required)<br>
                • <a href="https://platform.stability.ai/account/keys" target="_blank" style="color:#69DB9B;">Get Stability AI Key</a><br>
                • <a href="https://enter.pollinations.ai" target="_blank" style="color:#69DB9B;">Get Pollen Key</a>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        generate_btn = st.button("✨ Generate New Designs", type="primary", use_container_width=True)

    # Auto-initialize default designs if not present so gallery is never blank
    if "img2img_active_results" not in st.session_state:
        # Default starter broken chair reference
        starter_bytes = st.session_state.get("studio_uploaded_bytes")
        if not starter_bytes:
            starter_bytes = create_sample_waste_image("chair")
            st.session_state["studio_uploaded_bytes"] = starter_bytes
            st.session_state["studio_uploaded_name"] = "broken_wooden_chair.jpg"
            st.session_state["studio_uploaded_type"] = "image/jpeg"
            
        st.session_state["img2img_active_results"] = img2img_service.generate_four_upcycled_designs(
            image_bytes=starter_bytes,
            filename=st.session_state.get("studio_uploaded_name", "broken_wooden_chair.jpg"),
            custom_notes="",
            provider="local"
        )

    # Handle explicit generation click
    if generate_btn:
        active_bytes = st.session_state.get("studio_uploaded_bytes")
        if not active_bytes:
            active_bytes = create_sample_waste_image("chair")
            st.session_state["studio_uploaded_bytes"] = active_bytes
            st.session_state["studio_uploaded_name"] = "broken_wooden_chair.jpg"

        provider_code = "local"
        if "Hugging Face" in ai_provider:
            provider_code = "huggingface"
        elif "Stability" in ai_provider:
            provider_code = "stability"
        elif "Pollinations" in ai_provider:
            provider_code = "pollinations"

        with st.spinner("🤖 AI Image-to-Image Engine is analyzing material textures and synthesizing 4 new upcycled designs..."):
            key_to_use = st.session_state.get("user_custom_api_key", None)
            new_results = img2img_service.generate_four_upcycled_designs(
                image_bytes=active_bytes,
                filename=st.session_state.get("studio_uploaded_name", "waste_item.jpg"),
                custom_notes=custom_notes,
                provider=provider_code,
                api_key=key_to_use
            )
            st.session_state["img2img_active_results"] = new_results
            st.success("✨ Successfully generated 4 new upcycled product designs inspired by your visual reference!")

    # Retrieve current active results
    active_results = st.session_state.get("img2img_active_results")

    if active_results and "designs" in active_results:
        designs = active_results["designs"]
        analysis = active_results.get("analysis", {})
        original_bytes = active_results.get("original_image_bytes", st.session_state.get("studio_uploaded_bytes"))

        st.markdown("<br><hr style='border-color: #383838;'><br>", unsafe_allow_html=True)
        
        # =============================================================
        # SECTION 1: INTERACTIVE BEFORE-AND-AFTER GALLERY (SIDE-BY-SIDE)
        # =============================================================
        st.markdown("## 🔄 Before-and-After Gallery")
        st.markdown("<p style='color:#A0A0A0;'>Inspect your original waste item alongside the newly generated upcycled transformation. Toggle between the 4 design concepts below.</p>", unsafe_allow_html=True)

        idea_labels = [f"{d['label']}: {d['name']}" for d in designs]
        selected_idea_label = st.radio(
            "Select an Upcycled Product Idea for Before & After Showcase:",
            idea_labels,
            index=0,
            horizontal=True,
            key="ba_idea_radio_selector"
        )
        selected_idx = idea_labels.index(selected_idea_label)
        active_design = designs[selected_idx]

        ba_col_left, ba_col_right = st.columns(2)

        # -------------------------------------------------------------
        # LEFT: BEFORE — Original Waste Item
        # -------------------------------------------------------------
        with ba_col_left:
            st.markdown("""
            <div style="background:#1E1E1E; border:1px solid #383838; border-radius:12px; padding:12px; text-align:center; margin-bottom:10px;">
                <h4 style="color:#FAF8F0; margin:0;">📸 BEFORE — Original Waste Item</h4>
            </div>
            """, unsafe_allow_html=True)

            if original_bytes:
                st.image(
                    original_bytes,
                    caption=f"Visual Reference: {active_results.get('filename', 'Original Discarded Item')}",
                    use_container_width=True
                )
            
            reusable_str = "<br>• ".join(analysis.get("reusable_parts", ["Structure", "Material"]))
            st.markdown(f"""
            <div style="background:#242424; border:1px solid #383838; border-radius:8px; padding:12px; font-size:0.85rem; color:#A0A0A0; margin-top:10px; line-height:1.6;">
                <b style="color:#FAF8F0;">Identified Waste Material:</b> {analysis.get('material_name', 'Reclaimed Material')}<br>
                <b style="color:#FAF8F0;">Reusable Components Catalogued:</b><br>• {reusable_str}
            </div>
            """, unsafe_allow_html=True)

        # -------------------------------------------------------------
        # RIGHT: AFTER — Redesigned Product
        # -------------------------------------------------------------
        with ba_col_right:
            st.markdown(f"""
            <div style="background:#162E22; border:1px solid #174D3B; border-radius:12px; padding:12px; text-align:center; margin-bottom:10px;">
                <h4 style="color:#69DB9B; margin:0;">✨ AFTER — Redesigned Product</h4>
            </div>
            """, unsafe_allow_html=True)

            # Display the actual newly generated image
            st.image(
                active_design["image_bytes"],
                caption=f"AI Generated Design: {active_design['name']} ({active_design['label']})",
                use_container_width=True
            )

            # Active Design Details Card
            st.markdown(f"""
            <div class="eco-card" style="border: 1px solid #174D3B; background: #1C2620; margin-top: 10px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                    <span class="tag-green">{active_design['label']}</span>
                    <span class="tag-gold" style="font-weight:700;">Est. Cost: ₹{active_design['cost_inr']}</span>
                </div>
                <h3 style="color:#FAF8F0 !important; margin: 4px 0 6px 0;">{active_design['name']}</h3>
                <p style="color:#D4E5DC; font-size:0.9rem; line-height:1.5; margin-bottom:8px;">{active_design['description']}</p>
                <div style="font-size:0.83rem; color:#8FC0A9; margin-bottom:8px;">
                    <b>Reusable Parts Utilized:</b> {active_design['reusable_used']}
                </div>
                <div style="font-size:0.8rem; color:#A0A0A0; line-height:1.5;">
                    ⏱️ <b>Craft Time:</b> {active_design['time_estimate']} &nbsp;|&nbsp; 
                    🛠️ <b>Difficulty:</b> {active_design['difficulty']} &nbsp;|&nbsp;
                    🌱 <b>Eco Savings:</b> {active_design['eco_savings']}
                </div>
                <div style="font-size:0.75rem; color:#5A7D6C; margin-top:6px; font-style:italic;">
                    Generation Mode: {active_design.get('generation_mode', 'AI Synthesis')}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Action Buttons for Active Concept
            col_dl1, col_dl2 = st.columns(2)
            with col_dl1:
                safe_name = "".join(ch if ch.isalnum() or ch in ('_', '-') else '_' for ch in active_design['name'].lower())
                st.download_button(
                    label=f"📥 Download Design Image (.jpg)",
                    data=active_design["image_bytes"],
                    file_name=f"upcycled_{active_design['index']}_{safe_name}.jpg",
                    mime="image/jpeg",
                    key=f"dl_img_btn_{active_design['index']}",
                    use_container_width=True
                )
            with col_dl2:
                plan_md = f"""# ReFashion & ReFurnish AI - Upcycled Product Blueprint
================================================================================
PRODUCT: {active_design['name']}
IDEA: {active_design['label']}
ORIGINAL SOURCE: {active_results.get('filename', 'Discarded Item')}
ESTIMATED COST: INR {active_design['cost_inr']} | TIME: {active_design['time_estimate']}
DIFFICULTY: {active_design['difficulty']}
================================================================================

DESIGN DESCRIPTION:
{active_design['description']}

REUSABLE PARTS FROM ORIGINAL ITEM:
{active_design['reusable_used']}

MATERIALS REQUIRED:
{chr(10).join([f'- {m}' for m in active_design['materials_needed']])}

STEP-BY-STEP UPCYCLING INSTRUCTIONS:
{chr(10).join([f'{i}. {s}' for i, s in enumerate(active_design['steps'], 1)])}

ENVIRONMENTAL SAVINGS:
{active_design['eco_savings']}

GENERATION ENGINE:
{active_design.get('generation_mode', 'AI Neural Synthesis')}
================================================================================
Generated by ReFashion & ReFurnish AI Image-to-Image Upcycling Studio
"""
                st.download_button(
                    label=f"📋 Download Blueprint (.md)",
                    data=plan_md,
                    file_name=f"plan_{active_design['index']}_{safe_name}.md",
                    mime="text/markdown",
                    key=f"dl_plan_btn_{active_design['index']}",
                    use_container_width=True
                )

        # =============================================================
        # SECTION 2: ALL 4 UPCYCLED PRODUCT IDEAS GALLERY (FULL GRID)
        # =============================================================
        st.markdown("<br><hr style='border-color: #383838;'>", unsafe_allow_html=True)
        st.markdown("### 🎨 All 4 Newly Generated Upcycled Designs")
        st.markdown("<p style='color:#A0A0A0;'>All four distinct product concepts synthesized from your original uploaded item's reusable materials.</p>", unsafe_allow_html=True)

        grid_cols = st.columns(4)
        for g_idx, (g_col, d_item) in enumerate(zip(grid_cols, designs), 1):
            with g_col:
                st.markdown(f"""
                <div style="background:#162E22; border:1px solid #174D3B; border-radius:8px; padding:6px; text-align:center; margin-bottom:8px;">
                    <b style="color:#69DB9B; font-size:0.8rem;">{d_item['label']}</b>
                </div>
                """, unsafe_allow_html=True)
                
                # Show generated image
                st.image(d_item["image_bytes"], use_container_width=True)
                
                st.markdown(f"""
                <div style="background:#1E2620; border:1px solid #284435; border-radius:8px; padding:10px; margin-bottom:10px;">
                    <b style="color:#FAF8F0; font-size:0.92rem;">{d_item['name']}</b><br>
                    <span style="font-size:0.8rem; color:#69DB9B; font-weight:700;">Est. ₹{d_item['cost_inr']}</span> • 
                    <span style="font-size:0.78rem; color:#A0A0A0;">{d_item['time_estimate']}</span>
                    <p style="font-size:0.8rem; color:#D4E5DC; margin:6px 0 0 0; line-height:1.4;">{d_item['description'][:95]}...</p>
                </div>
                """, unsafe_allow_html=True)
                
                s_name = "".join(ch if ch.isalnum() or ch in ('_', '-') else '_' for ch in d_item['name'].lower())
                st.download_button(
                    label=f"📥 Download Idea {g_idx}",
                    data=d_item["image_bytes"],
                    file_name=f"upcycled_idea_{g_idx}_{s_name}.jpg",
                    mime="image/jpeg",
                    key=f"grid_dl_btn_{g_idx}",
                    use_container_width=True
                )

        # =============================================================
        # SECTION 3: UNIFIED SIDE-BY-SIDE GRAPHIC FOR DOWNLOAD
        # =============================================================
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("🖼️ View & Download Unified Side-by-Side Before & After Graphic", expanded=False):
            st.markdown("<p style='font-size:0.88rem; color:#A0A0A0;'>A unified high-resolution image showing the original waste item on the left and the active upcycled design on the right with branded project headers.</p>", unsafe_allow_html=True)
            composite_data = create_composite_before_after(
                before_bytes=original_bytes,
                after_bytes=active_design["image_bytes"],
                product_name=active_design["name"],
                idea_label=active_design["label"]
            )
            st.image(composite_data, caption=f"Combined Before & After: {active_design['name']}", use_container_width=True)
            st.download_button(
                label=f"📥 Download Unified Before & After Picture (.jpg)",
                data=composite_data,
                file_name=f"before_after_{active_design['index']}_{s_name}.jpg",
                mime="image/jpeg",
                key="dl_composite_graphic_btn",
                use_container_width=True
            )

        # =============================================================
        # SECTION 4: STEP-BY-STEP DIY GUIDES & MATERIALS TABS
        # =============================================================
        st.markdown("<br><hr style='border-color: #383838;'>", unsafe_allow_html=True)
        st.markdown("### 📋 Step-by-Step Upcycling DIY Guides")
        st.markdown("<p style='color:#A0A0A0;'>Detailed materials shopping list and step-by-step maker instructions for building each of the 4 upcycled designs.</p>", unsafe_allow_html=True)

        guide_tabs = st.tabs([f"{d['label']}: {d['name']}" for d in designs])

        for g_tab, d_data in zip(guide_tabs, designs):
            with g_tab:
                gt_col1, gt_col2 = st.columns([1.6, 1])

                with gt_col1:
                    st.markdown(f"#### 🛠️ Step-by-Step Upcycling Guide: {d_data['name']}")
                    st.markdown(f"<p style='color:#D4E5DC; font-size:0.95rem; line-height:1.5;'>{d_data['description']}</p>", unsafe_allow_html=True)
                    
                    for s_num, step in enumerate(d_data["steps"], 1):
                        st.markdown(f"""
                        <div class="step-box">
                            <span class="step-num">Step {s_num}:</span> {step}
                        </div>
                        """, unsafe_allow_html=True)

                    st.info(f"🌍 **Environmental Impact:** {d_data['eco_savings']}")

                with gt_col2:
                    st.markdown("#### 📊 Production Summary")
                    st.markdown(f"""
                    <div class="eco-card" style="background:#1A261F; border:1px solid #284435; margin-bottom:15px;">
                        <p style="margin:0; font-size:0.8rem; color:#A0A0A0;">ESTIMATED PRODUCTION COST</p>
                        <h2 style="color:#69DB9B !important; margin:4px 0 10px 0;">₹{d_data['cost_inr']}</h2>
                        <p style="margin:0; font-size:0.8rem; color:#A0A0A0;">DIFFICULTY & TIME</p>
                        <p style="margin:4px 0 10px 0; font-weight:600; color:#FAF8F0;">{d_data['difficulty']} • {d_data['time_estimate']}</p>
                        <p style="margin:0; font-size:0.8rem; color:#A0A0A0;">REUSABLE PARTS RECLAIMED</p>
                        <p style="margin:4px 0 0 0; font-size:0.85rem; color:#69DB9B;">{d_data['reusable_used']}</p>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown("#### 🧰 Materials Required")
                    for mat in d_data["materials_needed"]:
                        st.markdown(f"- {mat}")

                    if st.button(f"💾 Save '{d_data['name']}' to Notebook", key=f"save_notebook_{d_data['index']}", use_container_width=True):
                        saved_entry = {
                            "id": f"img2img_{d_data['index']}",
                            "title": d_data["name"],
                            "style": d_data["label"],
                            "cost_inr": d_data["cost_inr"],
                            "difficulty": d_data["difficulty"],
                            "symbol": "🔄"
                        }
                        if not any(s.get("title") == d_data["name"] for s in st.session_state["saved_design_ideas"]):
                            st.session_state["saved_design_ideas"].append(saved_entry)
                            st.toast(f"Saved '{d_data['name']}' to your notebook! 🎉")
                            st.success(f"Added to Notebook! Total saved: {len(st.session_state['saved_design_ideas'])}")
                        else:
                            st.info("This design is already in your notebook!")

        # SAVED PROJECTS DRAWER
        if st.session_state.get("saved_design_ideas"):
            st.markdown("<br><hr style='border-color: #383838;'>", unsafe_allow_html=True)
            with st.expander(f"📁 Your Saved Design Projects ({len(st.session_state['saved_design_ideas'])})", expanded=False):
                for s_item in st.session_state["saved_design_ideas"]:
                    st.markdown(f"- **{s_item.get('symbol', '✨')} {s_item['title']}** ({s_item['style']} | Est. ₹{s_item['cost_inr']} | {s_item['difficulty']})")
                
                if st.button("🗑️ Clear All Saved Projects", key="studio_clear_saved"):
                    st.session_state["saved_design_ideas"] = []
                    st.rerun()


# -------------------------------------------------------------
# PAGE 2: AGENT COORDINATOR (AUTO-ROUTE)
# -------------------------------------------------------------
elif page == "🤖 Agent Coordinator (Auto-Route)":
    st.markdown("## 🤖 Agent Coordinator Hub")
    st.markdown("""
    The **Agent Coordinator** serves as the central router for user requests. Type any question or project idea in natural language, 
    and the Coordinator will inspect keywords and assign the task to the most qualified agent.
    """)
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_req, col_guide = st.columns([1.3, 1])
    
    with col_req:
        st.markdown("#### 💬 Enter Your Project Request")
        user_query = st.text_area(
            "What would you like help with today?",
            placeholder="e.g., 'I have 2 old pairs of denim jeans with torn knees, how can I turn them into a tote bag?'\nOR 'How do I repaint an old wooden pallet for my balcony?'\nOR 'What price should I sell my upcycled denim pouch for and what caption should I post on Instagram?'",
            height=130
        )
        
        route_button = st.button("🚀 Route Request to Agent")
        
        if route_button:
            if not user_query.strip():
                st.warning("Please type a project description or request.")
            else:
                with st.spinner("Analyzing intent and routing via Agent Coordinator..."):
                    coordination = coordinator.execute_coordinated_task(user_query)
                    routing = coordination["routing"]
                    
                    st.success(f"🎯 Assigned to: **{routing['selected_agent']}** (Confidence: {routing['confidence']})")
                    
                    st.markdown(f"""
                    <div class="reasoning-box">
                        <b>🧭 Coordinator Routing Rationale:</b><br>
                        {routing['routing_reason']}<br>
                        <i>Keyword Match Scores:</i> {routing['keyword_scores']}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    agent_res = coordination["agent_output"]
                    target = routing["selected_agent"]
                    
                    if target == "Fashion Agent":
                        st.markdown("### 👗 Fashion Agent Output")
                        for r_step in agent_res["reasoning"]:
                            st.caption(f"• {r_step}")
                        for p in agent_res["projects"]:
                            with st.expander(f"✨ {p['name']} ({p['difficulty']})", expanded=True):
                                st.write(f"**⏱️ Time:** {p['time_estimate']} | **💧 Water Saved:** {p['water_saved']}")
                                st.write(f"**🛠️ Tools:** {', '.join(p['tools_needed'])}")
                                for idx, stp in enumerate(p["steps"], 1):
                                    st.markdown(f"**Step {idx}:** {stp}")
                                st.info(f"💡 Pro Tip: {p['pro_tip']}")
                                
                    elif target == "Furniture Agent":
                        st.markdown("### 🪑 Furniture Agent Output")
                        for r_step in agent_res["reasoning"]:
                            st.caption(f"• {r_step}")
                        for b in agent_res["blueprints"]:
                            with st.expander(f"🪵 {b['name']} ({b['difficulty']})", expanded=True):
                                st.write(f"**⏱️ Time:** {b['time_estimate']} | **📦 Diverted:** {b['landfill_diverted']}")
                                st.write(f"**🛠️ Tools:** {', '.join(b['tools_needed'])}")
                                for idx, stp in enumerate(b["steps"], 1):
                                    st.markdown(f"**Phase {idx}:** {stp}")
                                st.success(f"🎨 Finishing: {b['finishing_tip']}")
                                
                    else: # Business Agent
                        st.markdown("### 💼 Business Agent Output")
                        st.text_area("Generated Social Media Copy:", value=agent_res["caption"], height=320)
                        st.info("Tip: Head over to the 'Business Agent' tab to fine-tune unit costs, profit margins, and currency!")

    with col_guide:
        st.markdown("#### 🔍 How Intent Routing Works")
        st.markdown("""
        <div class="eco-card">
            <h4>Routing Architecture</h4>
            <p style="font-size:0.86rem; color:#CCCCCC; line-height:1.5;">
                The Coordinator performs transparent lexical pattern matching across domain taxonomies:
            </p>
            <ul style="font-size:0.84rem; color:#E0E0E0; margin-left: -15px;">
                <li><b>Fashion Agent:</b> jeans, fabric, clothes, tee, saree, sweater, stitch, sew, tote.</li>
                <li><b>Furniture Agent:</b> wood, pallet, chair, table, drawer, ladder, sand, paint, drill.</li>
                <li><b>Business Agent:</b> cost, price, profit, sell, margin, calculate, caption, Instagram, Etsy.</li>
            </ul>
            <div class="tip-box" style="margin-top: 10px; font-size: 0.82rem;">
                <b>Academic Viva Note:</b> Demonstrates a deterministic multi-agent dispatcher without API latency or subscription fees.
            </div>
        </div>
        """, unsafe_allow_html=True)


# -------------------------------------------------------------
# PAGE 3: FASHION AGENT (CLOTHES & FABRIC)
# -------------------------------------------------------------
elif page == "👗 Fashion Agent (Clothes & Fabric)":
    st.markdown("## 👗 Fashion Agent Studio")
    st.markdown("Your dedicated textile upcycling specialist. Suggests verified DIY projects or generates custom cutting plans.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    f_tab1, f_tab2 = st.tabs(["📚 Curated Garment Library", "✨ Custom Fabric Blueprint Generator"])
    
    with f_tab1:
        col_sel, col_out = st.columns([1, 2])
        
        with col_sel:
            st.markdown("#### 1. Garment Input")
            sel_material = st.selectbox(
                "Select Discarded Material:",
                fashion_agent.get_supported_materials(),
                index=0
            )
            
            show_no_sew = st.checkbox("Show Only 'No-Sew' (Zero Stitching)", value=False)
            
            btn_fetch_fashion = st.button("🧵 Consult Fashion Agent")
            
            st.markdown("""
            <div class="tip-box">
                <b>💡 Fashion Agent Insight:</b><br>
                Denim is one of the most durable textiles on earth. A single pair of worn jeans contains enough heavy cotton twill to construct a reinforced tote bag and two insulated kitchen pot holders!
            </div>
            """, unsafe_allow_html=True)
            
        with col_out:
            st.markdown(f"#### 2. Upcycling Solutions for: **{sel_material}**")
            
            projects = fashion_agent.get_preset_projects(sel_material, no_sew_only=show_no_sew)
            
            if not projects:
                st.warning("No purely No-Sew projects found for this category. Uncheck the filter to view all beginner guides!")
            else:
                for proj in projects:
                    with st.expander(f"✨ {proj['name']} ({proj['difficulty']})", expanded=True):
                        c1, c2, c3 = st.columns(3)
                        with c1:
                            st.write(f"**⏱️ Time:** {proj['time_estimate']}")
                        with c2:
                            badge = "tag-green" if proj['no_sew'] else "tag-terracotta"
                            st.markdown(f"<span class='{badge}'>{'No-Sew' if proj['no_sew'] else 'Sewing Needed'}</span>", unsafe_allow_html=True)
                        with c3:
                            st.write(f"**💧 Water Saved:** {proj['water_saved']}")
                            
                        st.markdown("---")
                        
                        tc, mc = st.columns(2)
                        with tc:
                            st.markdown("**🛠️ Tools Required:**")
                            for t in proj["tools_needed"]:
                                st.markdown(f"- {t}")
                        with mc:
                            st.markdown("**📦 Materials Required:**")
                            for m in proj["materials_needed"]:
                                st.markdown(f"- {m}")
                                
                        st.markdown("<br><b>📝 Step-by-Step Instructions:</b>", unsafe_allow_html=True)
                        for idx, step in enumerate(proj["steps"], 1):
                            st.markdown(f"""
                            <div class="step-box">
                                <span class="step-num">Step {idx}:</span> {step}
                            </div>
                            """, unsafe_allow_html=True)
                            
                        st.info(f"💡 **Maker's Pro Tip:** {proj['pro_tip']}")

    with f_tab2:
        st.markdown("#### ✨ Custom Textile Blueprint Generator")
        st.markdown("Input any fabric, linen, or custom garment to let the Fashion Agent generate a tailored blueprint.")
        
        cf1, cf2 = st.columns(2)
        with cf1:
            custom_garment = st.text_input("Garment / Fabric Description:", placeholder="e.g., Old Corduroy Pants, Silk Scarf, Baby Romper, Canvas Curtain")
            custom_condition = st.selectbox("Current Condition:", ["Minor Stains / Discoloration", "Torn at Seams / Worn Knees", "Faded Color but Sturdy", "Just Small Scraps & Ribbons"])
        with cf2:
            custom_target = st.selectbox("Desired Product Type:", ["Tote Bag / Carry Pouch", "Home Cushion / Pillow", "Desk Organizer / Basket", "Pet Toy or Bed", "Fashion Accessory / Hairband"])
            custom_skill = st.selectbox("Your Skill Level:", ["Beginner (No-Sew)", "Intermediate (Hand Needle)", "Advanced (Sewing Machine)"])
            
        btn_gen_fashion = st.button("🚀 Generate Custom Textile Blueprint")
        
        if btn_gen_fashion:
            blueprint = fashion_agent.generate_custom_blueprint(custom_garment, custom_condition, custom_target, custom_skill)
            
            st.success("🎉 Fashion Agent Formulated Your Blueprint!")
            
            st.markdown(f"""
            <div class="reasoning-box">
                <b>🧠 Fashion Agent Reasoning Trace:</b><br>
                {"<br>".join(blueprint['reasoning'])}
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="eco-card">
                <span class="tag-green">{blueprint['skill']}</span>
                <span class="tag-gold">{custom_target}</span>
                <h3>{blueprint['title']}</h3>
                <p style='color:#A0A0A0;'>{blueprint['eco_highlight']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("#### 🛠️ Recommended Tool Kit")
            for tool in blueprint["tools"]:
                st.markdown(f"- {tool}")
                
            st.markdown("#### 📋 Step-by-Step Instructions")
            for step in blueprint["steps"]:
                st.markdown(f"""
                <div class="step-box">
                    {step}
                </div>
                """, unsafe_allow_html=True)


# -------------------------------------------------------------
# PAGE 4: FURNITURE AGENT (WOOD & DECOR)
# -------------------------------------------------------------
elif page == "🪑 Furniture Agent (Wood & Decor)":
    st.markdown("## 🪑 Furniture Agent Studio")
    st.markdown("Your dedicated woodworking and renovation specialist. Prescribes restoration sequences, sanding grits, and protective finishes.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    u_tab1, u_tab2 = st.tabs(["🪵 Curated Furniture Blueprints", "🛠️ Custom Furniture Renovation Planner"])
    
    with u_tab1:
        col_u1, col_u2 = st.columns([1, 2])
        
        with col_u1:
            st.markdown("#### 1. Furniture Item")
            sel_furniture = st.selectbox(
                "Select Discarded Furniture:",
                furniture_agent.get_supported_furniture(),
                index=0
            )
            
            show_hand_tools = st.checkbox("Hand Tools Only (No Power Tools)", value=False)
            
            btn_fetch_furn = st.button("🔨 Consult Furniture Agent")
            
            st.markdown("""
            <div class="tip-box">
                <b>🪵 Pallet Safety Rules:</b><br>
                Always inspect pallet stamps! 
                <br>• <b>HT</b> = Heat Treated (Safe for indoor furniture & plant herbs).
                <br>• <b>MB</b> = Methyl Bromide (Pesticide treated — DO NOT use for home crafts).
            </div>
            """, unsafe_allow_html=True)
            
        with col_u2:
            st.markdown(f"#### 2. Restoration Plans for: **{sel_furniture}**")
            blueprints = furniture_agent.get_preset_blueprints(sel_furniture, hand_tools_only=show_hand_tools)
            
            if not blueprints:
                st.warning("All preset projects for this item use power tools. Uncheck the filter to view the guides with hand-tool alternatives!")
            else:
                for b in blueprints:
                    with st.expander(f"🪵 {b['name']} ({b['difficulty']})", expanded=True):
                        c1, c2, c3 = st.columns(3)
                        with c1:
                            st.write(f"**⏱️ Time:** {b['time_estimate']}")
                        with c2:
                            badge = "tag-terracotta" if b['power_tools_needed'] else "tag-green"
                            st.markdown(f"<span class='{badge}'>{'Power Tools Needed' if b['power_tools_needed'] else 'Hand Tools Only'}</span>", unsafe_allow_html=True)
                        with c3:
                            st.write(f"**📦 Landfill Diverted:** {b['landfill_diverted']}")
                            
                        st.markdown("---")
                        
                        tc, mc = st.columns(2)
                        with tc:
                            st.markdown("**🛠️ Tools Required:**")
                            for t in b["tools_needed"]:
                                st.markdown(f"- {t}")
                        with mc:
                            st.markdown("**🧱 Materials Required:**")
                            for m in b["materials_needed"]:
                                st.markdown(f"- {m}")
                                
                        st.markdown("<br><b>📝 Step-by-Step Restoration Plan:</b>", unsafe_allow_html=True)
                        for idx, step in enumerate(b["steps"], 1):
                            st.markdown(f"""
                            <div class="step-box">
                                <span class="step-num">Phase {idx}:</span> {step}
                            </div>
                            """, unsafe_allow_html=True)
                            
                        st.success(f"🎨 **Finishing Secret:** {b['finishing_tip']}")

    with u_tab2:
        st.markdown("#### 🛠️ Custom Furniture Renovation Planner")
        st.markdown("Describe an unusual wooden piece or damaged furniture item to receive a tailored renovation plan.")
        
        uf1, uf2 = st.columns(2)
        with uf1:
            custom_furn_desc = st.text_input("Furniture Item Name:", placeholder="e.g., Old Wooden Cable Drum, Grandma's Trunk, 90s Television Cabinet")
            custom_furn_damage = st.selectbox("Condition / Problem:", ["Chipped Varnish & Surface Scratches", "Wobbly Joints & Loose Legs", "Outdated Dark Stain / Peeling Paint", "Missing Part or Hardware"])
        with uf2:
            custom_furn_room = st.selectbox("Target Room / Space:", ["Living Room", "Balcony & Garden", "Bedroom & Wardrobe", "Home Office / Study", "Entryway / Hallway"])
            custom_furn_tools = st.selectbox("Available Tool Kit:", ["Hand Tools Only (Sandpaper, Screwdriver, Brush)", "Power Tools Available (Drill, Orbital Sander, Jigsaw)"])
            
        btn_gen_furn = st.button("🔨 Generate Furniture Renovation Plan")
        
        if btn_gen_furn:
            f_plan = furniture_agent.generate_custom_plan(custom_furn_desc, custom_furn_damage, custom_furn_room, custom_furn_tools)
            
            st.success("🎉 Furniture Agent Formulated Your Renovation Plan!")
            
            st.markdown(f"""
            <div class="reasoning-box">
                <b>🧠 Furniture Agent Reasoning Trace:</b><br>
                {"<br>".join(f_plan['reasoning'])}
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="eco-card">
                <span class="tag-gold">{custom_furn_room}</span>
                <span class="tag-green">{custom_furn_tools}</span>
                <h3>{f_plan['title']}</h3>
                <p style='color:#A0A0A0;'>{f_plan['eco_highlight']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("#### 🛠️ Required Tools & Safety Gear")
            for t in f_plan["tools"]:
                st.markdown(f"- {t}")
                
            st.markdown("#### 📋 Execution Phases")
            for step in f_plan["steps"]:
                st.markdown(f"""
                <div class="step-box">
                    {step}
                </div>
                """, unsafe_allow_html=True)


# -------------------------------------------------------------
# PAGE 5: BUSINESS AGENT (COST & MARKETING)
# -------------------------------------------------------------
elif page == "💼 Business Agent (Cost & Marketing)":
    st.markdown("## 💼 Business Agent Studio")
    st.markdown("Your dedicated micro-business and marketing strategist. Computes cost structures, profit margins, and generates multi-platform social media copy.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    b_tab1, b_tab2 = st.tabs(["📊 Cost & Profit Economics", "📢 Social Marketing Copy Generator"])
    
    with b_tab1:
        col_b_in, col_b_out = st.columns([1, 1.2])
        
        with col_b_in:
            st.markdown("#### 1. Production Cost Inputs")
            currency = st.selectbox("Currency:", ["₹ INR", "$ USD", "€ EUR", "£ GBP"], index=0)
            curr_sym = currency.split()[0]
            
            st.markdown("**Materials**")
            b_raw = st.number_input(f"Base Item Cost ({curr_sym}) (thrift/pallet):", min_value=0.0, value=50.0, step=10.0)
            b_aux = st.number_input(f"Supplies ({curr_sym}) (thread, paint, glue, screws):", min_value=0.0, value=80.0, step=10.0)
            b_pack = st.number_input(f"Packaging & Tags ({curr_sym}):", min_value=0.0, value=30.0, step=5.0)
            
            st.markdown("**Labor & Wages**")
            b_hours = st.number_input("Crafting Time (Hours):", min_value=0.1, value=1.5, step=0.5)
            b_wage = st.number_input(f"Fair Hourly Wage ({curr_sym}/hr):", min_value=0.0, value=150.0, step=25.0)
            
            st.markdown("**Platform & Margin Targets**")
            b_fee_pct = st.slider("Marketplace Fee / Shipping (%):", 0, 25, 5)
            b_margin_pct = st.slider("Target Profit Margin (%):", 10, 80, 35)
            
            btn_calc_business = st.button("📈 Run Financial Calculations")

        with col_b_out:
            fin = business_agent.calculate_cost_and_profit(
                raw_material_cost=b_raw,
                aux_material_cost=b_aux,
                packaging_cost=b_pack,
                labor_hours=b_hours,
                hourly_rate=b_wage,
                platform_fee_pct=b_fee_pct,
                target_margin_pct=b_margin_pct
            )
            
            st.markdown("#### 2. Financial Metrics & Pricing Model")
            
            st.markdown(f"""
            <div class="reasoning-box">
                <b>🧠 Business Agent Reasoning Trace:</b><br>
                {"<br>".join(fin['reasoning'])}
            </div>
            """, unsafe_allow_html=True)
            
            r1, r2 = st.columns(2)
            with r1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{curr_sym}{fin['base_cogs']:,.2f}</div>
                    <div class="metric-label">Production Cost (COGS)</div>
                </div>
                """, unsafe_allow_html=True)
            with r2:
                st.markdown(f"""
                <div class="metric-card" style="border-left-color: #176B4D;">
                    <div class="metric-value" style="color: #69DB9B;">{curr_sym}{fin['suggested_retail']:,.2f}</div>
                    <div class="metric-label">Suggested Retail Price</div>
                </div>
                """, unsafe_allow_html=True)
                
            st.markdown("<br>", unsafe_allow_html=True)
            
            r3, r4 = st.columns(2)
            with r3:
                st.markdown(f"""
                <div class="metric-card" style="border-left-color: #C06E52;">
                    <div class="metric-value" style="color: #FFA585;">{curr_sym}{fin['net_profit_val']:,.2f}</div>
                    <div class="metric-label">Net Profit / Unit</div>
                </div>
                """, unsafe_allow_html=True)
            with r4:
                st.markdown(f"""
                <div class="metric-card" style="border-left-color: #C8963E;">
                    <div class="metric-value" style="color: #FFD278;">{fin['actual_margin_pct']:.1f}%</div>
                    <div class="metric-label">Actual Profit Margin</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Plotly Donut Chart
            breakdown_df = pd.DataFrame({
                "Component": ["Direct Materials", "Packaging", "Labor Wage", "Platform Commission", "Net Profit"],
                "Amount": [b_raw + b_aux, b_pack, fin['labor_cost'], fin['platform_fee_val'], fin['net_profit_val']]
            })
            
            fig = px.pie(
                breakdown_df, 
                values="Amount", 
                names="Component",
                hole=0.45,
                color_discrete_sequence=["#1E825E", "#2A9D6E", "#176B4D", "#3E6651", "#D4A34E"]
            )
            fig.update_layout(
                title="Per-Unit Cost & Profit Distribution",
                margin=dict(t=40, b=10, l=10, r=10),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Plus Jakarta Sans", color="#FFFFFF")
            )
            st.plotly_chart(fig, use_container_width=True)

    with b_tab2:
        st.markdown("#### 📢 Social Media & E-Commerce Marketing Generator")
        st.markdown("Generate high-converting, story-driven captions with viral sustainability hooks and 20+ hashtags.")
        
        mc1, mc2 = st.columns([1, 1.2])
        
        with mc1:
            st.markdown("#### 1. Product Details")
            p_title = st.text_input("Product Title:", value="Vintage Denim Patchwork Tote Bag")
            p_origin = st.text_input("Original Discarded Material:", value="Worn Levi's 501 Jeans & Vintage Floral Bedding")
            
            p_plat = st.selectbox(
                "Target Social Platform:",
                [
                    "Instagram Post / Reel",
                    "Pinterest Pin Description",
                    "Facebook Marketplace / Groups",
                    "Etsy / Website Product Listing"
                ],
                index=0
            )
            
            p_vibe = st.selectbox(
                "Brand Tone:",
                [
                    "Eco-Conscious & Sustainable",
                    "Trendy Gen-Z & Aesthetic",
                    "Artisan & Handcrafted Story",
                    "Urgent & Sales-Driven"
                ],
                index=0
            )
            
            p_tag_price = st.text_input("Price Tag (Optional):", value="₹799 / $28")
            
            f1 = st.checkbox("100% Zero-Waste & Diverted from Landfill", value=True)
            f2 = st.checkbox("Reinforced Heavy-Duty Box-Cross Stitching", value=True)
            f3 = st.checkbox("Original Denim Pockets Intact & Functional", value=True)
            f4 = st.checkbox("One-of-a-Kind (Only 1 Made in the World!)", value=True)
            f5 = st.checkbox("Machine Washable & Built to Last", value=False)
            
            selected_features = []
            if f1: selected_features.append("100% Zero-Waste & Diverted from Landfill")
            if f2: selected_features.append("Reinforced Heavy-Duty Box-Cross Stitching")
            if f3: selected_features.append("Original Denim Pockets Intact & Functional")
            if f4: selected_features.append("One-of-a-Kind (Only 1 Made in the World!)")
            if f5: selected_features.append("Machine Washable & Built to Last")

            btn_gen_caption = st.button("✨ Generate Marketing Copy")

        with mc2:
            st.markdown("#### 2. Generated Marketing Copy")
            
            mkt_res = business_agent.generate_marketing_caption(
                product_name=p_title,
                original_material=p_origin,
                platform=p_plat,
                tone=p_vibe,
                features=selected_features,
                price_str=p_tag_price
            )
            
            st.text_area("Your Ready-to-Publish Caption:", value=mkt_res["caption"], height=380)
            
            st.markdown("""
            <div class="tip-box">
                <b>💡 Viral Marketing Strategy:</b><br>
                For upcycled creations, <b>'Before & After' split videos</b> achieve 3.5x higher engagement than static photos! Show the torn jeans or dusty pallet in the first 2 seconds, followed by the luxury finished item.
            </div>
            """, unsafe_allow_html=True)


# ==========================================
# 5. FOOTER
# ==========================================
st.markdown("<br><hr style='border-color: #333333;'><br>", unsafe_allow_html=True)
ft1, ft2, ft3 = st.columns(3)

with ft1:
    st.markdown("**🌿 ReFashion & ReFurnish AI**")
    st.caption("Multi-Agent System for Sustainable Circular Economy & Craft Entrepreneurship.")

with ft2:
    st.markdown("**🎓 Academic Presentation Ready**")
    st.caption("Powered by 3 cooperating deterministic agents + 1 Agent Coordinator in pure Python.")

with ft3:
    st.markdown("**🚀 Windows Execution**")
    st.caption("Run `run_app.bat` or run: `streamlit run app.py`")
