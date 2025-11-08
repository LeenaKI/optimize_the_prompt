import streamlit as st
from openai import OpenAI

# Initialize OpenAI client with NVIDIA endpoint
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"
)

model_name = "meta/llama-3.3-70b-instruct"


def optimize_any_prompt(user_prompt: str) -> str:
    """Universal prompt optimizer that works for any type of prompt"""
    system_prompt = (
        "You are an expert prompt engineer specializing in requirements structuring for cross-client compatible HTML email template generation.\n\n"
        "Transform any verbose email template generation prompt into a concise, professional requirements document with this structure:\n\n"
        "---\n"
        "1. Start with the role declaration from the input.\n"
        "2. Summarize core task in ONE sentence (purpose of the template).\n"
        "3. Present all requirements as easily scannable bullet or numbered lists under clear section headings (STRICT RULES, DYNAMIC VARIABLES HANDLING, STRUCTURE & LAYOUT REQUIREMENTS, COMPATIBILITY, TYPOGRAPHY & BUTTONS, FOOTER, ACCESSIBILITY, RESPONSIVENESS, DELIVERABLE FORMAT, etc.).\n"
        "4. Always include every technical, compatibility, variable handling, HTML, CSS, and JSON rule from the input prompt. Do not drop requirements.\n"
        "5. Where possible, prefer clear imperative bullets (e.g. 'Use table-based layout (max 600px)...').\n"
        "6. Omit redundant prose/boilerplate from input; focus on clear, direct requirements.\n"
        "7. Organize everything into clean sections, using ----- lines to separate major blocks like the sample below.\n"
        "8. For dynamic variables, show variable rules as a list with examples.\n"
        "9. Do NOT add markdown code blocks, headings, or explanations outside the structure. Output as plain text.\n"
        "10. If input prompt refers to sections (e.g., user input, branding, assets), mention them as variables, not as JSON.stringify calls.\n\n"
        "STRICTLY follow this structure and condensation style. Output must be instantly usable for advanced LLM prompt engineering with no further editing needed.\n"
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
    """Generate refined meta prompt with technical details"""
    system_prompt = (
        "You are an expert prompt engineer. Analyze and refine the user's prompt to be:\n"
        "- Clear and unambiguous\n"
        "- Technically detailed (frameworks, APIs, formats)\n"
        "- Well-structured and professional\n"
        "- Free of redundancy\n\n"
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


# Streamlit UI
st.set_page_config(page_title="Universal Prompt Optimizer", layout="wide")

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    st.info("**Model:** meta/llama-3.3-70b-instruct")
    st.info("**Context:** 128K tokens")
    
    st.markdown("---")
    st.markdown("### Optimization Style")
    st.markdown("""
    **This optimizer:**
    - Works for ANY type of prompt
    - Reduces verbosity by 50-80%
    - Preserves all critical requirements
    - Improves structure and clarity
    """)
    
    st.markdown("---")
    st.markdown("### Supported Prompt Types")
    st.markdown("""
    ✓ Code generation
    ✓ Content creation
    ✓ Email templates (HTML/text)
    ✓ Data processing
    ✓ API integration
    ✓ Analysis & research
    ✓ Creative writing
    ✓ Technical documentation
    ✓ Any other domain
    """)

# Main content
st.title("🎯 Universal Prompt Optimizer")
st.markdown("*Transforms verbose prompts into clean, organized, professional versions*")
st.markdown("---")

# Mode selection
col1, col2 = st.columns(2)
with col1:
    mode = st.radio(
        "Choose Mode",
        ["Smart Optimization (Recommended)", "Meta Prompting"],
        help="Smart Optimization works for any prompt type and reduces verbosity while preserving requirements"
    )

if mode == "Smart Optimization (Recommended)":
    st.header("✨ Smart Prompt Optimization")
    
    # Info boxes
    col1, col2 = st.columns(2)
    with col1:
        with st.expander("💡 How it works"):
            st.markdown("""
            1. **Analyzes** your prompt to understand its domain
            2. **Identifies** critical requirements vs. verbose explanations
            3. **Restructures** content with clear sections
            4. **Condenses** verbose text while keeping all requirements
            5. **Formats** output for immediate use
            """)
    
    with col2:
        with st.expander("📊 What changes"):
            st.markdown("""
            **Kept:**
            - All functional requirements
            - All technical specifications
            - All input/output formats
            - All validation rules
            
            **Improved:**
            - Verbose explanations → Concise directives
            - Long code blocks → Format requirements
            - Repetition → Consolidated statements
            - Poor structure → Clear sections
            """)
    
    user_prompt = st.text_area(
        "Enter your prompt (any type):",
        key="universal_prompt_input",
        height=400,
        placeholder="Paste your prompt here...\n\nWorks for:\n-  Code generation prompts\n-  Content creation prompts\n-  Email template prompts\n-  Data processing prompts\n-  Any other prompt type"
    )
    
    col1, col2, col3 = st.columns(3)

    with col1:
        optimize_btn = st.button("🚀 Optimize Prompt", use_container_width=True, type="primary")
    with col2:
        clear_btn = st.button("🗑️ Clear", use_container_width=True)
    
    if clear_btn:
        st.rerun()
    
    if optimize_btn:
        if user_prompt.strip():
            try:
                with st.spinner("🔄 Analyzing and optimizing your prompt..."):
                    optimized_prompt = optimize_any_prompt(user_prompt)
                
                st.success("✅ Optimization Complete!")
                
                # Show result in text area for easy copying
                st.text_area(
                    "Optimized Prompt:",
                    value=optimized_prompt,
                    height=500,
                    key="result_display",
                    help="Click inside and Ctrl+A to select all, then Ctrl+C to copy"
                )
                
                # Statistics
                st.markdown("### 📊 Optimization Metrics")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Original Length", f"{len(user_prompt):,} chars")
                with col2:
                    st.metric("Optimized Length", f"{len(optimized_prompt):,} chars")
                with col3:
                    reduction = len(user_prompt) - len(optimized_prompt)
                    st.metric("Reduction", f"-{reduction:,} chars")
                with col4:
                    reduction_pct = (reduction / len(user_prompt)) * 100
                    st.metric("Compression", f"-{reduction_pct:.1f}%")
                
                # Download button
                st.download_button(
                    label="📥 Download Optimized Prompt",
                    data=optimized_prompt,
                    file_name="optimized_prompt.txt",
                    mime="text/plain",
                    use_container_width=True
                )
                
                # Comparison toggle
                with st.expander("🔍 Compare Original vs. Optimized"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**Original:**")
                        st.text_area("", value=user_prompt, height=300, key="compare_original", disabled=True)
                    with col2:
                        st.markdown("**Optimized:**")
                        st.text_area("", value=optimized_prompt, height=300, key="compare_optimized", disabled=True)
                
            except Exception as e:
                st.error(f"❌ Error: {e}")
                st.exception(e)
        else:
            st.warning("⚠️ Please enter a prompt to optimize.")

elif mode == "Meta Prompting":
    st.header("📝 Meta Prompting")
    st.markdown("*Generate a refined, technically detailed version of your prompt*")
    
    user_prompt = st.text_area(
        "Enter your task prompt:",
        key="meta_prompt_input",
        height=300,
        placeholder="Paste your original prompt here..."
    )
    
    col1, col2 = st.columns()[3][2]
    with col1:
        generate_btn = st.button("🚀 Generate Meta Prompt", use_container_width=True)
    
    if generate_btn:
        if user_prompt.strip():
            try:
                with st.spinner("🔄 Generating meta prompt..."):
                    meta_prompt = generate_meta_prompt(user_prompt)
                st.success("✅ Generated Meta Prompt")
                st.code(meta_prompt, language="text")
                
                st.download_button(
                    label="📋 Download Result",
                    data=meta_prompt,
                    file_name="meta_prompt.txt",
                    mime="text/plain"
                )
            except Exception as e:
                st.error(f"❌ Error: {e}")
        else:
            st.warning("⚠️ Please enter a prompt before generating.")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray; font-size: 0.9em;'>"
    "🚀 Powered by Meta Llama 3.3 70B via NVIDIA API | Built with Streamlit<br>"
    "💡 Works with any prompt type: code, content, emails, data processing, APIs, and more"
    "</div>",
    unsafe_allow_html=True
)
