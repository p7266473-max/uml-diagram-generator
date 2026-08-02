import streamlit as st
import zlib
import base64
import requests
import re
from google import genai
from google.genai import types

st.set_page_config(page_title="Core Sandbox Engine", layout="wide")

import streamlit.components.v1 as components

st.markdown("""
<style>
/* Hide Streamlit top header, toolbar, GitHub fork badges, menu, and decoration */
#MainMenu {visibility: hidden !important; display: none !important;}
header {visibility: hidden !important; display: none !important;}
[data-testid="stHeader"] {visibility: hidden !important; display: none !important;}
[data-testid="stToolbar"] {visibility: hidden !important; display: none !important;}
[data-testid="stDecoration"] {visibility: hidden !important; display: none !important;}
[data-testid="stStatusWidget"] {visibility: hidden !important; display: none !important;}
.stAppDeployButton {visibility: hidden !important; display: none !important;}
#stDecoration {visibility: hidden !important; display: none !important;}

/* Hide Streamlit bottom footer and viewer/host badges */
footer {visibility: hidden !important; display: none !important;}
[data-testid="stFooter"] {visibility: hidden !important; display: none !important;}
.viewerBadge_container__16g3m {visibility: hidden !important; display: none !important;}
[class*="viewerBadge"] {visibility: hidden !important; display: none !important;}
[class*="styles_viewerBadge"] {visibility: hidden !important; display: none !important;}
[class*="ViewerBadge"] {visibility: hidden !important; display: none !important;}
.stActionButton {visibility: hidden !important; display: none !important;}
</style>
""", unsafe_allow_html=True)

components.html("""
<script>
function cleanupStreamlitUI() {
    const targetSelectors = [
        'footer', '[data-testid="stFooter"]', '[data-testid="stDecoration"]',
        '[data-testid="stStatusWidget"]', '[data-testid="stToolbar"]', '#MainMenu',
        'header', '.stAppDeployButton', '#stDecoration', '.viewerBadge_container__16g3m',
        '[class*="viewerBadge"]', '[class*="styles_viewerBadge"]', '[class*="ViewerBadge"]',
        '.stActionButton', 'button[title*="Streamlit"]', 'div[class*="StatusWidget"]'
    ];

    [document, window.parent.document].forEach(doc => {
        try {
            targetSelectors.forEach(selector => {
                doc.querySelectorAll(selector).forEach(el => {
                    el.style.setProperty('display', 'none', 'important');
                    el.style.setProperty('visibility', 'hidden', 'important');
                    el.style.setProperty('opacity', '0', 'important');
                });
            });
        } catch (err) {}
    });
}
cleanupStreamlitUI();
setInterval(cleanupStreamlitUI, 250);
</script>
""", height=0, width=0)



# Custom Premium Styling
import streamlit.components.v1 as components

st.markdown("""
<style>
/* Hide Streamlit top header, toolbar, GitHub fork badges, menu, and decoration */
#MainMenu {visibility: hidden !important; display: none !important;}
header {visibility: hidden !important; display: none !important;}
[data-testid="stHeader"] {visibility: hidden !important; display: none !important;}
[data-testid="stToolbar"] {visibility: hidden !important; display: none !important;}
[data-testid="stDecoration"] {visibility: hidden !important; display: none !important;}
[data-testid="stStatusWidget"] {visibility: hidden !important; display: none !important;}
.stAppDeployButton {visibility: hidden !important; display: none !important;}
#stDecoration {visibility: hidden !important; display: none !important;}

/* Hide Streamlit bottom footer and viewer/host badges */
footer {visibility: hidden !important; display: none !important;}
[data-testid="stFooter"] {visibility: hidden !important; display: none !important;}
.viewerBadge_container__16g3m {visibility: hidden !important; display: none !important;}
[class*="viewerBadge"] {visibility: hidden !important; display: none !important;}
[class*="styles_viewerBadge"] {visibility: hidden !important; display: none !important;}
[class*="ViewerBadge"] {visibility: hidden !important; display: none !important;}
.stActionButton {visibility: hidden !important; display: none !important;}
</style>
""", unsafe_allow_html=True)

components.html("""
<script>
function cleanupStreamlitUI() {
    const targetSelectors = [
        'footer', '[data-testid="stFooter"]', '[data-testid="stDecoration"]',
        '[data-testid="stStatusWidget"]', '[data-testid="stToolbar"]', '#MainMenu',
        'header', '.stAppDeployButton', '#stDecoration', '.viewerBadge_container__16g3m',
        '[class*="viewerBadge"]', '[class*="styles_viewerBadge"]', '[class*="ViewerBadge"]',
        '.stActionButton', 'button[title*="Streamlit"]', 'div[class*="StatusWidget"]'
    ];

    [document, window.parent.document].forEach(doc => {
        try {
            targetSelectors.forEach(selector => {
                doc.querySelectorAll(selector).forEach(el => {
                    el.style.setProperty('display', 'none', 'important');
                    el.style.setProperty('visibility', 'hidden', 'important');
                    el.style.setProperty('opacity', '0', 'important');
                });
            });
        } catch (err) {}
    });
}
cleanupStreamlitUI();
setInterval(cleanupStreamlitUI, 250);
</script>
""", height=0, width=0)

# Header Section
st.markdown("""
<div class="title-container">
    <div class="title-main">UML Diagram Generator</div>
    <div class="title-sub">Transform your text descriptions into beautifully rendered UML diagrams instantly</div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------

def clean_plantuml_code(raw_code: str) -> str:
    """
    Cleans raw code output from the LLM, stripping markdown blocks or prefix/suffix garbage.
    """
    # Remove markdown code fences if present
    code = re.sub(r"```[a-zA-Z0-9_-]*", "", raw_code)
    code = code.replace("```", "")
    
    lines = code.split("\n")
    cleaned_lines = []
    started = False
    
    for line in lines:
        stripped = line.strip()
        if "@startuml" in stripped:
            started = True
            cleaned_lines.append("@startuml")
            continue
        if "@enduml" in stripped:
            cleaned_lines.append("@enduml")
            break
        if started:
            cleaned_lines.append(line)
            
    # Fallback to returning raw code stripped if start/end tags weren't cleanly matched
    if not cleaned_lines:
        return code.strip()
        
    return "\n".join(cleaned_lines)

def convert_puml_to_png(puml_text: str) -> bytes:
    """
    Encodes the PlantUML text and compiles it into binary PNG data using the official PlantUML web service.
    """
    cleaned_text = puml_text.strip()
    
    # 1. Compress text using zlib deflate (raw deflate, wbits=-15)
    compressor = zlib.compressobj(level=9, method=zlib.DEFLATED, wbits=-15)
    compressed = compressor.compress(cleaned_text.encode('utf-8'))
    compressed += compressor.flush()
    
    # 2. Translate standard base64 characters to PlantUML custom alphabet
    # Standard base64: A-Z a-z 0-9 + /
    # PlantUML base64: 0-9 A-Z a-z - _
    std_b64 = base64.b64encode(compressed).decode('utf-8')
    
    translation_table = str.maketrans(
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/",
        "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"
    )
    
    puml_encoded = std_b64.translate(translation_table).replace("=", "")
    
    # 3. Request compilation from PlantUML server
    server_url = f"http://www.plantuml.com/plantuml/png/{puml_encoded}"
    response = requests.get(server_url, timeout=20)
    response.raise_for_status()
    return response.content

# ---------------------------------------------------------
# User Inputs
# ---------------------------------------------------------

st.subheader("Configuration & Prompt")

# Dropdown for Diagram Type
diagram_type = st.selectbox(
    "UML Diagram Type",
    options=[
        "Sequence Diagram",
        "Class Diagram",
        "Use Case Diagram",
        "State Diagram",
        "Component Diagram"
    ]
)

# Text Area for Description
prompt_placeholder = (
    f"Describe the system or flow for the {diagram_type}. For example:\n"
    "\"A user logs in, sends a request to the server, server queries the database, and returns the results.\""
)
user_prompt = st.text_area(
    "Describe your diagram requirements:",
    height=200,
    placeholder=prompt_placeholder
)

# Retrieve API key: check secrets first, then fall back to sidebar input
api_key = None
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    pass
    
# If not found in secrets, check if it was provided in a sidebar input
if not api_key:
    api_key = st.sidebar.text_input(
        "API Key",
        type="password",
        help="Provide your API key to run queries."
    )

generate_btn = st.button("Generate Diagram")

# ---------------------------------------------------------
# Generation Pipeline
# ---------------------------------------------------------

if generate_btn:
    if not user_prompt.strip():
        st.warning("Please provide a text description to generate the diagram.")
    elif not api_key:
        st.error("Kindly enter API Key")
    else:
        with st.spinner("Please wait..."):
            try:
                # Initialize Gemini Flash Client
                client = genai.Client(api_key=api_key)
                
                # Instruction sets pure code generation
                system_instruction = (
                    "You are a strict PlantUML code generator. Output ONLY raw code lines. "
                    "Start exactly with @startuml and end with @enduml. "
                    "Do NOT use markdown code fences (like triple backticks) or include conversational text/explanations. "
                    "Ensure correct syntax: for state blocks with descriptive labels, always define an alias, e.g., state \"State Name\" as StateAlias { ... }."
                )
                
                full_prompt = f"Create a {diagram_type} representing the following specifications:\n{user_prompt}"
                
                # Try fallback models in case the API key has restricted access to specific versions
                model_names = ['gemini-1.5-flash', 'gemini-2.5-flash', 'gemini-1.5-flash-latest']
                response = None
                last_err = None
                
                for model_name in model_names:
                    try:
                        response = client.models.generate_content(
                            model=model_name,
                            contents=full_prompt,
                            config=types.GenerateContentConfig(
                                system_instruction=system_instruction,
                                temperature=0.2,
                            )
                        )
                        break
                    except Exception as e:
                        last_err = e
                        continue
                
                if not response:
                    raise last_err
                
                raw_code = response.text
                if not raw_code:
                    raise ValueError("Received empty response from Gemini API.")
                
                # Clean generated text code
                cleaned_puml = clean_plantuml_code(raw_code)
                
            except Exception as e:
                st.error("Due to high traffic model is currently busy, try again later.")
                st.stop()
                
        # Compile/Render Diagram
        with st.spinner("Please wait..."):
            try:
                png_bytes = convert_puml_to_png(cleaned_puml)
                
                # Render success message and diagram image
                st.success("UML Diagram Generated Successfully!")
                st.image(png_bytes, use_container_width=True)
                
                # Provide instant download button
                st.download_button(
                    label="📥 Download Diagram (PNG)",
                    data=png_bytes,
                    file_name="uml_diagram.png",
                    mime="image/png",
                )
                
            except Exception as e:
                st.error("Due to high traffic model is currently busy, try again later.")


