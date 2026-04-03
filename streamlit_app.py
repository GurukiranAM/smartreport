import streamlit as st
from openai import OpenAI
import os

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="SmartReport AI", layout="wide")

st.title("📄 SmartReport AI - Project Report Generator")

# Step 1: Select Sections
st.header("1. Select Report Sections")

sections = [
    "Abstract", "Introduction", "Literature Review",
    "Methodology", "Results", "Conclusion", "References"
]

selected_sections = st.multiselect("Choose sections:", sections, default=sections)

# Step 2: Order Sections
st.header("2. Arrange Sections")

ordered_sections = st.text_area(
    "Enter sections in order (comma separated):",
    ",".join(selected_sections)
)

# Step 3: Generate Content
st.header("3. Generate Report")

topic = st.text_input("Enter your project topic:")

if st.button("Generate Report"):
    if topic and ordered_sections:
        final_report = ""

        for section in ordered_sections.split(","):
            section = section.strip()

            prompt = f"""
            Write a professional {section} for a project report on the topic:
            {topic}.
            Keep it clear, formal, and structured.
            """

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )

            content = response.choices[0].message.content

            st.subheader(section)
            st.write(content)

            final_report += f"\n\n{section}\n{content}"

        st.success("Report Generated Successfully!")
