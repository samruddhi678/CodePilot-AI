
import os

import streamlit as st
from openai import OpenAI


# --------------------------------------------------
# APP CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="CodePilot AI",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded",
)

MODEL = "openai/gpt-oss-120b"

LANGUAGES = ["Python", "Java", "C", "C++", "JavaScript"]

EXAMPLES = {
    "Python": """def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

number = 5
print(factorial(number))""",

    "Java": """public class Main {
    static int square(int n) {
        return n * n;
    }

    public static void main(String[] args) {
        System.out.println(square(5));
    }
}""",

    "C": """#include <stdio.h>

int main() {
    int numbers[] = {10, 20, 30};
    int sum = 0;

    for (int i = 0; i < 3; i++) {
        sum += numbers[i];
    }

    printf("Sum: %d\\n", sum);
    return 0;
}""",

    "C++": """#include <iostream>
using namespace std;

int main() {
    int number = 7;

    if (number % 2 == 0) {
        cout << "Even";
    } else {
        cout << "Odd";
    }

    return 0;
}""",

    "JavaScript": """const numbers = [1, 2, 3, 4, 5];

const squares = numbers.map((number) => {
    return number * number;
});

console.log(squares);""",
}

# --------------------------------------------------
# STYLING
# --------------------------------------------------

st.markdown(
    """
    <style>
    .stApp {
        background: #0b1020;
        color: #eef2ff;
    }

    [data-testid="stSidebar"] {
        background: #10172a;
        border-right: 1px solid #25304a;
    }

    .hero {
        padding: 30px 8px 22px 8px;
    }

    .hero h1 {
        font-size: clamp(2rem, 4vw, 3.2rem);
        font-weight: 800;
        letter-spacing: -1.5px;
        margin-bottom: 10px;
        color: #f4f6ff;
    }

    .hero p {
        font-size: 1.05rem;
        color: #a6b2cc;
    }

    .status-pill {
        display: inline-block;
        border: 1px solid #34405e;
        background: #151e35;
        color: #b9c6ff;
        padding: 6px 12px;
        border-radius: 30px;
        font-size: 0.82rem;
        margin-bottom: 14px;
    }

    .feature-card {
        background: linear-gradient(135deg, #141d34, #11182a);
        border: 1px solid #273450;
        border-radius: 15px;
        padding: 18px;
        min-height: 125px;
    }

    .feature-card h3 {
        font-size: 1rem;
        margin: 0 0 8px 0;
        color: #e5eaff;
    }

    .feature-card p {
        color: #a6b2cc;
        font-size: 0.88rem;
        margin: 0;
    }

    .section-title {
        font-size: 1.2rem;
        font-weight: 700;
        margin: 18px 0 10px 0;
        color: #eef2ff;
    }

    .stTextArea textarea {
        background: #0d1425 !important;
        color: #e6edff !important;
        border: 1px solid #303d5a !important;
        border-radius: 12px !important;
        font-family: Consolas, monospace !important;
    }

    .stButton > button {
        border-radius: 10px;
        min-height: 43px;
        font-weight: 600;
        border: 1px solid #394766;
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #6257e8, #3977ed);
        border: none;
        color: white;
    }

    .result-card {
        background: #111a2e;
        border: 1px solid #293754;
        border-radius: 14px;
        padding: 20px;
    }

    div[data-testid="stDownloadButton"] button {
        border-radius: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# API KEY
# --------------------------------------------------

def get_api_key():
    """Read the key from Streamlit Secrets or an environment variable."""
    try:
        key = st.secrets.get("GROQ_API_KEY", "")
        if key:
            return key
    except Exception:
        pass

    return os.getenv("GROQ_API_KEY", "")


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:
    st.markdown("## 💻 CodePilot AI")
    st.caption("Your personal coding companion")

    st.divider()

    st.markdown("### ⚙️ Preferences")

    language = st.selectbox(
        "Programming language",
        LANGUAGES,
        index=0,
    )

    level = st.selectbox(
        "Explanation level",
        [
            "Beginner",
            "Intermediate",
            "Advanced",
            "Interview Preparation",
        ],
        index=0,
    )

    st.divider()

    st.markdown("### ✨ What you can do")
    st.markdown(
        """
        - Understand code step by step
        - Learn programming concepts
        - Explore examples and outputs
        - Prepare for coding interviews
        """
    )

# --------------------------------------------------
# MAIN HEADER
# --------------------------------------------------

st.markdown(
    """
    <div class="hero">
        <div class="status-pill">● AI-powered code explanations</div>
        <h1>Understand code.<br>One step at a time.</h1>
        <p>
            Paste your code, choose your learning level,
            and turn complex logic into clear explanations.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# FEATURE CARDS
# --------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="feature-card">
            <h3>🧩 Step-by-step</h3>
            <p>Break complicated code into understandable steps.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="feature-card">
            <h3>🎯 Learn your way</h3>
            <p>Choose an explanation level that fits your experience.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div class="feature-card">
            <h3>📘 Learn by example</h3>
            <p>Explore logic, important concepts, and expected output.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("")
st.markdown(
    '<div class="section-title">⌨️ Your code</div>',
    unsafe_allow_html=True,
)

# --------------------------------------------------
# CODE INPUT
# --------------------------------------------------

if "code_input" not in st.session_state:
    st.session_state.code_input = ""

if "explanation" not in st.session_state:
    st.session_state.explanation = ""

if "last_code" not in st.session_state:
    st.session_state.last_code = ""

if "last_language" not in st.session_state:
    st.session_state.last_language = language

button_col1, button_col2 = st.columns([1, 4])

with button_col1:
    if st.button("✨ Load sample", use_container_width=True):
        st.session_state.code_input = EXAMPLES[language]
        st.session_state.explanation = ""
        st.session_state.last_code = ""
        st.rerun()

with button_col2:
    if st.button("🗑️ Clear", use_container_width=True):
        st.session_state.code_input = ""
        st.session_state.explanation = ""
        st.session_state.last_code = ""
        st.rerun()

code = st.text_area(
    "Paste or write your code below",
    key="code_input",
    height=300,
    placeholder="Paste your code here...",
    label_visibility="collapsed",
)

# --------------------------------------------------
# PROMPT BUILDER
# --------------------------------------------------

def build_prompt(source_code, programming_language, explanation_level):
    level_instructions = {
        "Beginner": (
            "Assume the reader is new to programming. "
            "Use simple language, define technical terms, "
            "and include small examples."
        ),
        "Intermediate": (
            "Explain the logic clearly, including important "
            "programming concepts and control flow."
        ),
        "Advanced": (
            "Discuss implementation details, edge cases, "
            "trade-offs, and relevant optimizations."
        ),
        "Interview Preparation": (
            "Explain the algorithm, important concepts, "
            "time and space complexity where applicable, "
            "and likely interview questions with answers."
        ),
    }

    return f"""
You are CodePilot AI, a careful programming tutor.

Programming language: {programming_language}
Explanation level: {explanation_level}

Explain the supplied code using this structure:

1. **Overview**
   Summarize what the program does.

2. **Step-by-step explanation**
   Explain important lines or blocks in execution order.
   Refer to the actual code. Do not invent line numbers.

3. **Important concepts**
   Explain relevant variables, functions, loops,
   conditions, data structures, or algorithms.

4. **Example walkthrough**
   Trace the code with a small input when possible.
   Show how important values change.

5. **Expected output**
   State the expected output if it can be determined.
   Explain that output briefly.

6. **Complexity**
   Explain time and space complexity when meaningful.
   If not applicable or uncertain, say so.

7. **Potential issues**
   Mention relevant edge cases or likely errors.
   Do not invent problems that are not present.

Instructions:
- {level_instructions[explanation_level]}
- Be accurate and beginner-friendly where appropriate.
- Use Markdown headings, lists, and code formatting.
- If the code is incomplete, explain what is missing.
- If the language is uncertain, mention that.
- Never claim you executed the code unless you actually did.

CODE TO EXPLAIN:

```{programming_language.lower()}
{source_code}
```
"""


# --------------------------------------------------
# GENERATE EXPLANATION
# --------------------------------------------------

st.markdown("")

if st.button(
    "✨ Explain my code",
    type="primary",
    use_container_width=True,
):
    if not code.strip():
        st.warning("Please enter some code first.")

    else:
        api_key = get_api_key()

        if not api_key:
            st.error(
                "The AI API key is not configured. "
                "Add GROQ_API_KEY to Streamlit Secrets "
                "before using the app."
            )
        else:
            prompt = build_prompt(code, language, level)

            try:
                with st.spinner("Analyzing your code..."):
                    client = OpenAI(
                        api_key=api_key,
                        base_url="https://api.groq.com/openai/v1",
                        timeout=120.0,
                    )

                    response = client.chat.completions.create(
                        model=MODEL,
                        messages=[
                            {
                                "role": "system",
                                "content": (
                                    "You are CodePilot AI, a helpful "
                                    "and accurate programming tutor."
                                ),
                            },
                            {
                                "role": "user",
                                "content": prompt,
                            },
                        ],
                        temperature=0.2,
                        max_tokens=4000,
                    )

                    result = response.choices[0].message.content

                    if not result:
                        st.error(
                            "The AI returned an empty response. "
                            "Please try again."
                        )
                    else:
                        st.session_state.explanation = result
                        st.session_state.last_code = code
                        st.session_state.last_language = language

            except Exception as error:
                st.error(
                    "Sorry, the AI request failed. "
                    "Please check your API key, internet connection, "
                    "model availability, and API usage limits."
                )
                with st.expander("Technical details"):
                    st.code(str(error))


# --------------------------------------------------
# DISPLAY RESULTS
# --------------------------------------------------

if st.session_state.explanation:
    st.divider()

    st.markdown(
        '<div class="section-title">📖 Code explanation</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="result-card">',
        unsafe_allow_html=True,
    )

    st.markdown(st.session_state.explanation)

    st.markdown("</div>", unsafe_allow_html=True)

    download_text = (
        "# CodePilot AI — Code Explanation\n\n"
        f"**Language:** {st.session_state.last_language}\n\n"
        f"## Original code\n\n"
        f"```{st.session_state.last_language.lower()}\n"
        f"{st.session_state.last_code}\n"
        f"```\n\n"
        f"## Explanation\n\n"
        f"{st.session_state.explanation}\n"
    )

    st.download_button(
        label="⬇️ Download explanation",
        data=download_text,
        file_name="code_explanation.md",
        mime="text/markdown",
        use_container_width=True,
    )

st.divider()

st.caption(
    "CodePilot AI • Review AI-generated explanations before relying on them."
)
