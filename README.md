# AI PlantUML Diagram Generator

A complete, production-ready Streamlit web application that allows users to generate UML diagrams from text descriptions using Gemini Flash and a local/remote PlantUML rendering engine.

## Features

1. **UML Type Selection**: Support for Sequence Diagrams, Class Diagrams, Use Case Diagrams, State Diagrams, and Component Diagrams.
2. **AI-Powered Code Generation**: Integrates the official `google-genai` SDK using the `gemini-1.5-flash` model.
3. **PlantUML Compilation**: Converts the generated code string to binary PNG using compressed URI format.
4. **Beautiful Interface**: Customized CSS design with gradients and glassmorphism.
5. **Instant Downloads**: Dedicated button to download generated diagrams as `uml_diagram.png`.

## Installation & Setup

1. **Install Dependencies**:
   ```bash
   pip install streamlit google-genai requests
   ```

2. **Configure API Key**:
   Create a `.streamlit/secrets.toml` file in the project directory:
   ```toml
   GEMINI_API_KEY = "your-actual-api-key-here"
   ```

3. **Run the Application**:
   ```bash
   streamlit run app.py
   ```
