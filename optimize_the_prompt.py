import streamlit as st
from openai import OpenAI

# Initialize OpenAI client with NVIDIA endpoint
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"
)

model_name = "meta/llama-3.3-70b-instruct"

def optimize_any_prompt(user_prompt: str) -> str:
    system_prompt = (
        "You are an expert prompt engineer specializing in prompt optimization.\n\n"
        "**Your Task:** Transform the given prompt into a clean, organized, professional version while preserving all critical requirements.\n\n"
        "Universal Optimization Principles:\n"
        "1. Identify prompt type and adapt your strategy.\n"
        "2. Organize content with clear section separators (---) and lists.\n"
        "3. Preserve ALL functional/technical requirements, variables, and validation rules.\n"
        "4. Remove verbose explanations and code blocks; keep instructions only.\n"
        "5. Use bullets and concise directives for clarity; avoid markdown code blocks or headers.\n"
        "6. Output ONLY the optimized prompt, starting with any role declaration.\n"
    )
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        max_tokens=8192,
        temperature=0.2,
        top_p=0.95
    )
    return response.choices[0].message.content

def generate_meta_prompt(user_prompt: str) -> str:
    system_prompt = (
        "You are an expert prompt engineer. Analyze and refine the user's prompt to be:\n"
        "- Clear and unambiguous\n"
        "- Technically detailed (frameworks, APIs, formats)\n"
        "- Well-structured and professional\n"
        "- Free of redundancy\n"
        "Output only the refined prompt without explanations. Preserve the original role."
    )
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        max_tokens=8192,
        temperature=0.3,
        top_p=1.0
    )
    return response.choices[0].message.content

def optimize_html_email_prompt(user_prompt: str) -> str:
    system_prompt = (
        "You are an expert prompt engineer specializing in requirements structuring for cross-client compatible HTML email template generation.\n\n"
        "Transform any verbose email template generation prompt into a concise, professional requirements document with this structure:\n\n"
        "---\n"
        "1. Start with the role declaration from the input.\n"
        "2. Summarize core task in ONE sentence (purpose of the template).\n"
        "3. Present all requirements as easily scannable bullet or numbered lists under clear section headings (STRICT RULES, DYNAMIC VARIABLES HANDLING, STRUCTURE & LAYOUT REQUIREMENTS, COMPATIBILITY, TYPOGRAPHY & BUTTONS, FOOTER, ACCESSIBILITY, RESPONSIVENESS, DELIVERABLE FORMAT, etc.).\n"
        "4. Always include every technical, compatibility, variable handling, HTML, CSS, and JSON rule from the input prompt. Do not drop requirements.\n"
        "5. Prefer clear imperative bullets wherever possible.\n"
        "6. Omit redundant prose/boilerplate from input.\n"
        "7. Organize everything into clean sections, using ----- lines to separate blocks.\n"
        "8. Show variable rules as a list with examples.\n"
        "9. Do NOT add markdown code blocks, headings, or explanations outside the structure. Output as plain text.\n"
        "10. Mention input sections as variables, not as JSON.stringify calls.\n\n"
        "STRICTLY follow this structure and condensation style. Output must be instantly usable for advanced LLM prompt engineering."
    )
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        max_tokens=6000,
        temperature=0.2,
        top_p=0.95
    )
    return response.choices[0].message.content

st.set_page_config(page_title="Universal Prompt Optimizer", layout="wide")

# Sidebar with only minimal info
with st.sidebar:
    st.header("⚙️ Configuration")
    st.info("**Model:** meta/llama-3.3-70b-instruct")
    st.info("**Context:** 128K tokens")
    st.markdown("---")
    st.caption("Built for clear, concise, instantly usable prompt re-structuring.")

st.title("Prompt Optimizer")
st.markdown("*Transforms verbose prompts into clean, organized, professional versions*")
st.markdown("---")

col_mode, _ = st.columns([3, 1])
with col_mode:
    mode = st.radio(
        "Choose Mode",
        ["Prompt Optimization", "Meta Prompting", "HTML Email Template Optimizer"],
        help="Smart: for any prompt. Meta: technical reformulation. Email: best for verbose HTML email requirements."
    )

if mode == "Prompt Optimization":
    st.header("Prompt Optimization")
    user_prompt = st.text_area(
        "Enter your prompt (any type):",
        key="universal_prompt_input",
        height=400,
        placeholder="Paste your prompt here..."
    )
    cols_action = st.columns(2)
    if cols_action[0].button("Optimize Prompt", use_container_width=True):
        if user_prompt.strip():
            with st.spinner("🔄 Optimizing..."):
                optimized_prompt = optimize_any_prompt(user_prompt)
            st.success("✅ Optimization Complete!")
            st.text_area("Optimized Prompt:", value=optimized_prompt, height=500, key="result_display")
            st.download_button(
                label="📥 Download Optimized Prompt",
                data=optimized_prompt,
                file_name="optimized_prompt.txt"
            )
            with st.expander("🔍 Compare Original vs. Optimized"):
                compare_cols = st.columns(2)
                with compare_cols[0]: st.markdown("**Original:**"); st.text_area("", value=user_prompt, height=300, key="compare_original", disabled=True)
                with compare_cols[1]: st.markdown("**Optimized:**"); st.text_area("", value=optimized_prompt, height=300, key="compare_optimized", disabled=True)
        else:
            st.warning("⚠️ Please enter a prompt to optimize.")
    if cols_action[1].button("🗑️ Clear", use_container_width=True):
        st.experimental_rerun()

elif mode == "Meta Prompting":
    st.header("Meta Prompting")
    user_prompt = st.text_area(
        "Enter your task prompt:",
        key="meta_prompt_input",
        height=300,
        placeholder="Paste your original prompt here..."
    )
    cols_action = st.columns(2)
    if cols_action[0].button("Generate Meta Prompt", use_container_width=True):
        if user_prompt.strip():
            with st.spinner("🔄 Generating meta prompt..."):
                meta_prompt = generate_meta_prompt(user_prompt)
            st.success("✅ Generated Meta Prompt")
            st.code(meta_prompt, language="text")
            st.download_button(
                label="📋 Download Result",
                data=meta_prompt,
                file_name="meta_prompt.txt"
            )
        else:
            st.warning("⚠️ Please enter a prompt before generating.")
    if cols_action[1].button("🗑️ Clear", use_container_width=True):
        st.experimental_rerun()

elif mode == "HTML Email Template Optimizer":
    st.header("📧 HTML Email Template Prompt Optimizer")
    user_prompt = st.text_area(
        "Enter your HTML email template prompt:",
        key="email_prompt_input",
        height=400,
        placeholder="Paste your verbose HTML email template prompt here..."
    )
    cols_action = st.columns(2)
    if cols_action[0].button("Optimize Email Prompt", use_container_width=True):
        if user_prompt.strip():
            with st.spinner("🔄 Optimizing HTML email template prompt..."):
                optimized_email_prompt = optimize_html_email_prompt(user_prompt)
            st.success("✅ Optimized HTML Email Template Prompt")
            st.text_area("Optimized Prompt:", value=optimized_email_prompt, height=500, key="email_result_display")
            st.download_button(
                label="📋 Download Optimized Prompt",
                data=optimized_email_prompt,
                file_name="optimized_email_prompt.txt"
            )
            with st.expander("🔍 Compare Original vs. Optimized"):
                compare_cols = st.columns(2)
                with compare_cols[0]: st.markdown("**Original:**"); st.text_area("", value=user_prompt, height=300, key="compare_email_original", disabled=True)
                with compare_cols[1]: st.markdown("**Optimized:**"); st.text_area("", value=optimized_email_prompt, height=300, key="compare_email_optimized", disabled=True)
        else:
            st.warning("⚠️ Please enter an HTML email template prompt before optimizing.")
    if cols_action[1].button("🗑️ Clear", use_container_width=True):
        st.experimental_rerun()

st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray; font-size: 0.9em;'>"
    " Powered by Meta Llama 3.3 70B via NVIDIA API | Built with Streamlit"
    "</div>",
    unsafe_allow_html=True
)
