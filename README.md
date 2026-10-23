# 🌿 ReFashion & ReFurnish AI (Multi-Agent Edition)

> **A Multi-Agent Circular Crafting, Upcycling & Micro-Business Platform**  
> Built with **Python**, **Streamlit**, and **Plotly**. Features a transparent, deterministic **Multi-Agent System** with **zero paid APIs** and 100% offline functionality. Perfect for BCA / BSc IT / Computer Science capstone presentations and real-world DIY creators.

---

## 📌 Project Overview

**ReFashion & ReFurnish AI** addresses the global crises of textile waste (over 92M tons/year) and discarded furniture (over 80% sent to landfills) through a coordinated, multi-agent AI framework:

1. **👗 Fashion Agent:** Analyzes old garments, fabric off-cuts, and condition to formulate cutting patterns, no-sew designs, and step-by-step upcycling blueprints.
2. **🪑 Furniture Agent:** Recommends restoration, woodworking, and renovation techniques for pallets, broken chairs, old ladders, and drawers (including pallet safety validation).
3. **💼 Business Agent:** Computes unit production economics (COGS), fair hourly wages, and viable retail profit margins, while writing tailored social media captions.
4. **🤖 Agent Coordinator:** Central intent classifier that inspects user queries in natural language, determines keyword domain density, and routes requests to the right specialist agent with transparent reasoning logs.

---

## 🎨 Theme & Aesthetic

The application features a sleek, high-contrast **Professional Dark Mode** design:
- **Main Page Background:** Deep Near-Black (`#121212`).
- **Sidebar Background:** Dark Charcoal (`#1E1E1E`).
- **Cards, Panels & Inputs:** Textured Dark Grey (`#242424`) with subtle borders (`#383838`).
- **Typography:** Crisp White (`#FFFFFF`) headings and Light Grey (`#E0E0E0`) text.
- **Buttons & Highlights:** Deep Green (`#176B4D`) with Mint Green (`#69DB9B`) accents.
- **Badge Accents:** Terracotta (`#FFA585`) and Craft Gold (`#FFD278`).

---

## 📂 Project Architecture

```text
agentic ai/
│
├── image_to_image.py      # Real AI Image-to-Image Upcycling & Before-After Transformation Service
├── agents.py              # Multi-Agent classes: FashionAgent, FurnitureAgent, BusinessAgent, AgentCoordinator
├── app.py                 # Streamlit web UI with Before-After Gallery, Agents & Coordinator hub
├── requirements.txt       # Dependencies (streamlit, pandas, plotly, Pillow, requests, numpy)
├── run_app.bat            # One-click Windows runner
└── README.md              # Project documentation & BCA viva defense guide
```

---

## 🔄 AI Image-to-Image Upcycling Studio (`image_to_image.py`)

Takes an uploaded photo of a **broken chair, old table, damaged furniture, wooden waste, plastic waste, or denim/fabric** as its direct visual reference and synthesizes **4 separate upcycled product designs**:

1. **UPCYCLED PRODUCT IDEA 1:** Redesigned Modern Chair / Primary Furniture Item (preserving original legs, frame, and materials).
2. **UPCYCLED PRODUCT IDEA 2:** Creative Stool or Small Accent Table (repurposing turned legs and cross-stretchers).
3. **UPCYCLED PRODUCT IDEA 3:** Decorative Plant Stand or Wall Shelf (reclaiming backrest slats & spindles).
4. **UPCYCLED PRODUCT IDEA 4:** Unique Sculptural Home Decor (Ambient Desk Lamp / Organizer from solid offcuts).

### Multi-Provider Neural Pipeline
- **⚡ Local Vision Synthesis Engine:** 100% free offline engine that extracts the exact material texture, patina, and colors directly from the uploaded photo to generate high-resolution studio product images.
- **🤗 Hugging Face Serverless API:** Supports real neural image-to-image translation models using a free Hugging Face token (`HF_TOKEN`).
- **🎨 Stability AI SDXL:** Supports native `init_image` image-to-image transformation via `STABILITY_API_KEY`.
- **🐝 Pollinations AI:** Supports neural prompt generation with Pollen keys.

### Before-and-After Gallery Features
- **BEFORE — Original Waste Item:** Displays the original uploaded photo alongside computer vision material and palette detection.
- **AFTER — Redesigned Product:** Displays newly generated visual images with title, reusable parts breakdown, and INR costing.
- **Full 4-Idea Gallery:** 4-column responsive grid displaying all newly synthesized designs with instant image downloads.
- **Unified Composite Picture:** Merges Before & After into one branded graphic file ready for academic viva presentation.

---

## 🤖 How the Agents Work (Deterministic & Transparent)

> [!NOTE]
> **No Paid API Required:** This application does **NOT** rely on external LLM APIs (OpenAI, Anthropic, etc.). It uses deterministic expert-system rules, heuristic matrices, and keyword density classifiers. This ensures **zero API costs**, **no rate-limits**, **instant execution**, and **complete explainability** during college vivas.

### 1. `FashionAgent` (`agents.py`)
- **Knowledge Base:** Curated blueprints for Denim Jeans, Cotton T-Shirts, Silk Sarees/Scarves, Woolen Sweaters, Flannel Shirts, and Scraps.
- **Dynamic Generator:** Accepts custom garments + wear conditions + desired targets (e.g. Tote Bag, Pillow, Pet Toy) + skill levels (No-Sew, Hand Needle, Sewing Machine) and dynamically constructs step-by-step instructions.
- **Reasoning Trace:** Explains how fabric thickness, edge treatment, and structural reinforcement were chosen.

### 2. `FurnitureAgent` (`agents.py`)
- **Knowledge Base:** Blueprints for Shipping Pallets, Broken Wooden Chairs, Vintage Drawers, Wooden Ladders, and Industrial Cable Drums.
- **Safety Enforcement:** Validates pallet heat treatment stamps (`HT` safe vs `MB` toxic).
- **Dynamic Renovation Planner:** Formulates multi-phase plans (Cleaning $\rightarrow$ Structural repair $\rightarrow$ Sanding sequence $\rightarrow$ Primer $\rightarrow$ Chalk Paint $\rightarrow$ Wax Seal $\rightarrow$ Hardware).
- **Reasoning Trace:** Documents tool constraints (Hand tools vs Power tools) and protective finishes.

### 3. `BusinessAgent` (`agents.py`)
- **Costing Engine:** Computes:
  $$\text{COGS} = \text{Raw Material} + \text{Auxiliary Supplies} + \text{Packaging} + (\text{Labor Hours} \times \text{Hourly Wage})$$
  $$\text{Retail Price} = \frac{\text{COGS}}{1 - (\text{Margin \%} + \text{Platform Fee \%})}$$
- **Data Visualization:** Generates an interactive Plotly donut chart of cost vs profit distribution.
- **Marketing Generator:** Creates platform-specific copy (Instagram, Pinterest, Facebook Marketplace, Etsy) with brand tones, persuasive hooks, and 20+ curated hashtags.

### 4. `AgentCoordinator` (`agents.py`)
- **Intent Analysis:** Calculates keyword density across domain vocabularies.
- **Dynamic Routing:** Directs requests to the best-matching agent.
- **Transparent Output:** Displays routing rationale, confidence scores, and keyword match counts directly in the UI.

### 5. `PhotoDesignStudioEngine` (`agents.py` - AI Photo-to-Design Studio)
- **Photo Upload:** Accepts JPG, JPEG, and PNG images of old garments or furniture.
- **Categories:** Old Clothes / Fabric Waste & Old Furniture.
- **5 Aesthetic Styles:** Modern, Traditional, Minimalist, Luxury, and Eco-Friendly.
- **4 Custom Blueprints per Upload:** Generates 4 detailed redesign blueprints with:
  * Proposed product name and design narrative.
  * Complete materials required checklist.
  * Difficulty rating (Beginner, Intermediate, Advanced).
  * Estimated production cost in INR (₹).
  * 5-step detailed upcycling guide.
  * Curated color palette swatches.
- **Before-and-After Comparison:** Side-by-side view comparing original uploaded photo and proposed redesign concept card.
- **Action Buttons:** One-click markdown blueprint download (`.md`) and project notebook saving.
- **Optional Photorealistic AI Preview:** Free open inference integration (Pollinations.ai) for realistic renderings without requiring paid API tokens.

---

## 💻 How to Run on Windows

### Option 1: Double-Click Launcher (Recommended)
Double-click [**`run_app.bat`**](file:///c:/Users/kashi/OneDrive/Desktop/agentic%20ai/run_app.bat) in File Explorer. It automatically checks Python, verifies packages, and starts the server in your default browser.

---

### Option 2: Using Command Prompt or PowerShell

1. Open PowerShell or Command Prompt.
2. Navigate to your project folder:
   ```powershell
   cd "c:\Users\kashi\OneDrive\Desktop\agentic ai"
   ```
3. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
4. Launch the Streamlit application:
   ```powershell
   streamlit run app.py
   ```
5. Open your browser at:
   ```text
   http://localhost:8501
   ```

---

## 🎓 BCA Viva & Project Defense Guide

### Q1: What is a Multi-Agent System (MAS), and how is it implemented here?
> **Answer:**  
> *"A Multi-Agent System is an architectural design where complex problems are decomposed into specialized, modular agents. In our project, rather than having a monolithic script, we separated domain responsibilities into three distinct agents (`FashionAgent`, `FurnitureAgent`, and `BusinessAgent`), managed by a central `AgentCoordinator` that routes incoming user prompts."*

### Q2: Does this project use a Large Language Model (LLM) or a paid API?
> **Answer:**  
> *"No, this project uses a transparent, deterministic rule-based expert system and NLP keyword density heuristics. This guarantees 100% offline availability, zero recurring API expenses, immediate execution latency, and deterministic reproducibility—making it ideal for academic demonstration and reliable deployment."*

### Q3: How does the Agent Coordinator route user queries?
> **Answer:**  
> *"The Coordinator analyzes the query's tokenized words against specialized domain lexicons (textile terms for Fashion, carpentry/renovation terms for Furniture, and financial/social commerce terms for Business). It computes frequency scores, calculates a confidence rating, and delegates the task to the highest-scoring agent while providing an explainable routing trace."*

### Q4: Why is the Business Agent an essential component of an upcycling platform?
> **Answer:**  
> *"Upcycling often fails commercially because crafters underprice their labor and omit platform commissions. The Business Agent calculates the true Cost of Goods Sold (COGS), ensures fair hourly wages, and generates targeted social marketing copy, transforming eco-crafting into a viable circular micro-enterprise."*

### Q5: What is the future scope for expanding this system?
> **Answer:**  
> *"Future enhancements include integrating a Computer Vision model (e.g. YOLOv8 or MobileNet) to automatically classify fabric composition and furniture defects directly from camera uploads, as well as integrating local open-source LLMs (such as Ollama or Llama-3) for conversational capabilities."*

---

## 📦 Dependencies
- `streamlit` - Web interface and reactive components
- `pandas` - Financial and tabular computations
- `plotly` - Interactive price and cost distribution charts
