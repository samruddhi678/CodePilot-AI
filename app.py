
import os
import streamlit as st
from openai import OpenAI

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="CodePilot AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

MODEL = "openai/gpt-oss-120b"

LANGUAGES = ["Python", "Java", "C", "C++", "JavaScript"]

ACE_LANGUAGES = {
    "Python": "python",
    "Java": "java",
    "C": "c_cpp",
    "C++": "c_cpp",
    "JavaScript": "javascript",
}

SAMPLE_CODE = {
    "Python": '''def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

print(factorial(5))''',

    "Java": '''public class Main {
    static int factorial(int n) {
        if (n <= 1) {
            return 1;
        }
        return n * factorial(n - 1);
    }

    public static void main(String[] args) {
        System.out.println(factorial(5));
    }
}''',

    "C": '''#include <stdio.h>

int factorial(int n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

int main(void) {
    printf("%d\\n", factorial(5));
    return 0;
}''',

    "C++": '''#include <iostream>
using namespace std;

int factorial(int n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

int main() {
    cout << factorial(5) << endl;
    return 0;
}''',

    "JavaScript": '''function factorial(n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

console.log(factorial(5));''',
}

# --------------------------------------------------
# API KEY
# --------------------------------------------------
def get_api_key():
    try:
        key = st.secrets.get("GROQ_API_KEY", "")
    except Exception:
        key = ""

    return key or os.getenv("GROQ_API_KEY", "")


def clear_editor(key):
    """Clear the selected editor before Streamlit reruns the page."""
    st.session_state[key] = ""


# --------------------------------------------------
# CUSTOM STYLING
# --------------------------------------------------
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0b1020;
    }

    .block-container {
        max-width: 1250px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .hero {
        padding: 1.8rem 0 1.2rem 0;
    }

    .hero h1 {
        font-size: clamp(2.2rem, 5vw, 3.6rem);
        font-weight: 800;
        letter-spacing: -1.5px;
        margin-bottom: 0.6rem;
    }

    .hero p {
        color: #aab5ce;
        font-size: 1.08rem;
        line-height: 1.7;
        max-width: 760px;
    }

    .gradient-text {
        background: linear-gradient(90deg, #7c83ff, #42d6c5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .feature-card {
        background: #121a2d;
        border: 1px solid #27334c;
        border-radius: 14px;
        padding: 18px;
        min-height: 125px;
        margin-bottom: 12px;
    }

    .feature-card h3 {
        font-size: 1rem;
        color: #f1f5ff;
        margin: 0 0 8px 0;
    }

    .feature-card p {
        font-size: 0.88rem;
        color: #aab5ce;
        margin: 0;
        line-height: 1.5;
    }

    .section-label {
        color: #b6c3dd;
        font-size: 0.83rem;
        font-weight: 700;
        letter-spacing: 1.2px;
        text-transform: uppercase;
    }

    .stButton > button[kind="primary"] {
        border: none;
        border-radius: 10px;
        min-height: 3rem;
        font-weight: 700;
    }

    div[data-testid="stDownloadButton"] button {
        border-radius: 9px;
    }

    footer {
        visibility: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
with st.sidebar:
    st.markdown("## 🚀 CodePilot AI")
    st.caption("Your AI-powered coding companion")
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
        ],
        index=0,
    )

    st.divider()

    st.markdown("### 💡 Editor tips")
    st.caption("• Select a language to load its sample code.")
    st.caption("• Edit the sample or paste your own code.")
    st.caption("• Use Tab to indent your code.")
    st.caption("• Click Explain my code when ready.")

    


# --------------------------------------------------
# HERO
# --------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <h1>Understand code with
        <span class="gradient-text">CodePilot AI</span></h1>
        <p>
            Explore code line by line with AI-powered explanations.
            Write or paste code in a professional editor, choose your
            learning level, and make complex programming concepts easier
            to understand.
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
            <h3>⌨️ Code editor</h3>
            <p>A reliable editor for writing or pasting code
            in your selected programming language.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="feature-card">
            <h3>🧠 AI explanations</h3>
            <p>Understand program flow, functions,
            logic and important programming concepts.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div class="feature-card">
            <h3>🎯 Learn your way</h3>
            <p>Choose beginner, intermediate or advanced
            explanations based on your experience.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")

# --------------------------------------------------
# CODE EDITOR
# --------------------------------------------------
st.markdown(
    '<p class="section-label">01 / YOUR CODE</p>',
    unsafe_allow_html=True,
)

editor_col, info_col = st.columns([3, 1])

with editor_col:
    st.subheader(f"✍️ {language} Editor")
    st.caption(
        "Edit the example or replace it with your own code."
    )

    # Use Streamlit's built-in editor for a stable, dependency-light experience.
    editor_key = f"code_editor_{language}"
    if editor_key not in st.session_state:
        st.session_state[editor_key] = SAMPLE_CODE[language]

    code = st.text_area(
        "Code",
        key=editor_key,
        height=360,
        placeholder="Write or paste your code here...",
        label_visibility="collapsed",
    )

with info_col:
    st.markdown("### Editor features")
    st.markdown(
        """
        - **Simple, reliable editor**
        - **Editable sample code**
        - **Paste your own code**
        - **Multiple languages** supported
        - **AI complexity analysis**
        """
    )

    st.info(
        f"Language: {language}\n\n"
        f"Explanation: {level}"
    )

    st.caption(
        "CodePilot explains code but does not execute it."
    )

code = code or ""

st.write("")

explain_col, clear_col = st.columns([3, 1])

with explain_col:
    explain_clicked = st.button(
        "✨ Explain my code",
        type="primary",
        use_container_width=True,
    )

with clear_col:
    st.button(
        "🗑️ Clear editor",
        use_container_width=True,
        on_click=clear_editor,
        args=(editor_key,),
    )

# --------------------------------------------------
# AI EXPLANATION
# --------------------------------------------------
if explain_clicked:
    if not code.strip():
        st.warning("Please enter some code before requesting an explanation.")

    elif len(code) > 20000:
        st.warning(
            "This code is too long for this demo. "
            "Please keep it under 20,000 characters."
        )

    else:
        api_key = get_api_key()

        if not api_key:
            st.error(
                "Groq API key not found. Add GROQ_API_KEY "
                "to Streamlit Secrets or your local environment."
            )

        else:
            client = OpenAI(
                api_key=api_key,
                base_url="https://api.groq.com/openai/v1",
                timeout=120.0,
            )

            prompt = f"""
You are CodePilot AI, a patient and accurate programming tutor.

Explain the following {language} code for a {level.lower()} programmer.

Structure your response with these sections:

1. **Overview** — what the program does.
2. **Step-by-step explanation** — explain the code in its execution order.
3. **Important concepts** — describe relevant syntax, functions,
   variables, loops, conditions, classes, or algorithms.
4. **Example walkthrough** — trace the code with sample values when
   possible. Clearly state any assumptions.
5. **Output** — describe the expected output if it can be determined.
   Do not claim you executed the code.
6. **Time complexity** — give the Big-O time complexity, such as O(1),
   O(n), O(n log n), or O(n^2), and explain which operations, loops,
   recursion, or algorithmic steps determine it. State best, average,
   or worst case when relevant.
7. **Space complexity** — give the auxiliary space complexity in Big-O
   notation and explain the extra memory used. Account for recursion
   stack space and additional data structures. Clarify when input storage
   is excluded from auxiliary space.
8. **Assumptions and confidence** — state any assumptions about input size
   or data structures. If the snippet is incomplete or complexity cannot
   be determined reliably, say so rather than guessing. Do not claim you
   measured complexity by running the code.
9. **Key takeaways** — summarize what the learner should remember.

Use clear Markdown headings and code formatting.
Adapt the depth and terminology to the requested experience level.
If the code has an apparent error, point it out carefully rather
than silently assuming it works.
Do not invent program behavior that cannot be inferred from the code.

Programming language: {language}
Requested level: {level}

Code to explain:

```{language.lower()}
{code}
```
"""

            try:
                with st.spinner(
                    "CodePilot is analyzing your code..."
                ):
                    response = client.chat.completions.create(
                        model=MODEL,
                        messages=[
                            {
                                "role": "system",
                                "content": (
                                    "You are a helpful, precise programming "
                                    "teacher. Explain code accurately and "
                                    "never claim to execute code."
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

                    explanation = (
                        response.choices[0].message.content or ""
                    )

                if explanation.strip():
                    st.session_state["last_explanation"] = explanation
                    st.session_state["last_explained_code"] = code
                    st.session_state["last_language"] = language
                    st.session_state["last_level"] = level
                else:
                    st.warning(
                        "The AI returned an empty explanation. Please try again."
                    )

            except Exception as error:
                st.error(
                    "Unable to generate the explanation. "
                    "Please try again in a moment."
                )
                st.caption(
                    f"Technical details: {type(error).__name__}: {error}"
                )

# --------------------------------------------------
# DISPLAY SAVED EXPLANATION AND DOWNLOAD
# --------------------------------------------------
if st.session_state.get("last_explanation"):
    st.divider()

    st.markdown(
        '<p class="section-label">02 / YOUR EXPLANATION</p>',
        unsafe_allow_html=True,
    )

    st.subheader("🧠 Code explanation")

    st.markdown(st.session_state["last_explanation"])

    explanation_markdown = f"""# CodePilot AI — Code Explanation

**Language:** {st.session_state.get("last_language", language)}

**Explanation level:** {st.session_state.get("last_level", level)}

## Source code

```{st.session_state.get("last_language", language).lower()}
{st.session_state.get("last_explained_code", "")}
```

## Explanation

{st.session_state["last_explanation"]}
"""

    st.download_button(
        label="⬇️ Download explanation as Markdown",
        data=explanation_markdown,
        file_name="code_explanation.md",
        mime="text/markdown",
    )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.divider()
st.caption(
    "CodePilot AI • Learn, understand, and explore code with AI."
)
