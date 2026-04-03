
import streamlit as st
import google.generativeai as genai

# ---------------------------
# CONFIG
# ---------------------------
st.set_page_config(page_title="SmartReport AI", layout="wide")
st.title("📄 SmartReport AI - Project Report Generator (Gemini)")

# Load API Key
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-1.5-flash")

# ---------------------------
# STEP 1: SELECT SECTIONS
# ---------------------------
st.header("1. Select Report Sections")

sections = [
    "Abstract", "Introduction", "Literature Review",
    "Methodology", "Results", "Conclusion", "References"
]

selected_sections = st.multiselect(
    "Choose sections:",
    sections,
    default=sections
)

# ---------------------------
# STEP 2: ORDER SECTIONS
# ---------------------------
st.header("2. Arrange Sections")

ordered_sections = st.text_area(
    "Enter sections in order (comma separated):",
    ",".join(selected_sections)
)

# ---------------------------
# STEP 3: TOPIC INPUT
# ---------------------------
st.header("3. Enter Topic")

topic = st.text_input("Enter your project topic:")

# ---------------------------
# STEP 4: GENERATE REPORT
# ---------------------------
st.header("4. Generate Report")

if st.button("🚀 Generate Report"):

    if not topic:
        st.warning("Please enter a topic")

    elif not ordered_sections:
        st.warning("Please define sections")

    else:
        st.info("Generating report... please wait ⏳")

        final_report = ""

        for section in ordered_sections.split(","):
            section = section.strip()

            prompt = f"""
Write a professional {section} for a project report.

Topic: {topic}

Requirements:
- Formal academic tone
- Clear structure
- Human-like explanation
- Do not use bullet points unless necessary
"""

            try:
                # Generate 2 variations (better choice option)
                responses = []

                for i in range(2):
                    response = model.generate_content(prompt)
                    responses.append(response.text)

                # UI
                st.subheader(f"📌 {section} - Choose Best Version")

                choice = st.radio(
                    f"Select version for {section}",
                    ["Option 1", "Option 2"],
                    key=section
                )

                content = responses[0] if choice == "Option 1" else responses[1]

                st.write(content)

            except Exception as e:
                st.error(f"Error in {section}: {e}")
                content = "Error generating content."

            # Final display
            st.subheader(f"📌 Final: {section}")
            st.write(content)

            final_report += f"\n\n{section}\n{content}"

        # ---------------------------
        # DOWNLOAD OPTION
        # ---------------------------
        st.success("✅ Report Generated Successfully!")

        st.download_button(
            "📥 Download Report",
            final_report,
            file_name="SmartReport.txt")
      
