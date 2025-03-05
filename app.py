import streamlit as st
from jamaibase import JamAI, protocol as p
from tempfile import NamedTemporaryFile
from PIL import Image
import base64

# Initialize JamAI client
jamai = JamAI(
    token="jamai_pat_867ef89d067abe9ff32e3746f3e203fadcf9d000a990ab4d",
    project_id="proj_a22518db64513185f65f62ec",
)

# Custom CSS for better styling
st.markdown(
    """
    <style>
    .title {
        font-size: 36px;
        font-weight: bold;
        font-family: 'Verdana', sans-serif;
        color: #FF69B4;
        text-align: center;
        margin-bottom: 20px;
    }
    .output-card {
        background-color: #222;
        color: #FFF;
        padding: 20px;
        margin: 10px 0;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .output-title {
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    body {
        background-color: #1E1E1E;
        color: #FFFFFF;
        font-family: 'Verdana', sans-serif;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Title
st.markdown(
    '<div class="title">Couples Heaven ˚˖𓍢ִ໋🌷͙֒✧˚.🎀༘⋆</div>', unsafe_allow_html=True
)

# File uploader
uploaded_file = st.file_uploader("Upload a file or image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    st.write(f"**Filename:** {uploaded_file.name}")

    # Show uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", width=300)

    # Convert to temporary file
    with NamedTemporaryFile(delete=False, suffix=".jpeg") as temp_file:
        image.convert("RGB").save(temp_file, format="JPEG")
        temp_file_path = temp_file.name

    # Upload to JamAI
    try:
        upload_response = jamai.file.upload_file(temp_file_path)
        st.success("✅ File uploaded successfully!")

        # Add to action table
        completion = jamai.table.add_table_rows(
            "action",
            p.RowAddRequest(
                table_id="poetry_bot",
                data=[dict(image=upload_response.uri)],
                stream=False,
            ),
        )

        if completion.rows:
            st.success("✅ File added to the verification table successfully.")
        else:
            st.error("⚠️ Failed to add the file to the verification table.")

        # Retrieve poetry results
        with st.spinner("⏳ Generating poetry..."):
            rows = jamai.table.list_table_rows("action", "poetry_bot")

        if rows.items:
            row = rows.items[0]
            llm1 = row.get("llm1", {}).get("value", "Awaiting response...")
            llm2 = row.get("llm2", {}).get("value", "Awaiting response...")
            llm3 = row.get("llm3", {}).get("value", "Awaiting response...")
            aggregator = row.get("aggregator", {}).get("value", "Awaiting response...")

            # Display results in better format
            st.subheader("📜 **Generated Poetry Output**")
            poetry_outputs = {
                "Llama 8B Instruct": llm1,
                "Llama 70B Instruct": llm2,
                "Qwen2.5 72B": llm3,
                "Aggregator": aggregator,
            }

            for model, text in poetry_outputs.items():
                st.markdown(
                    f'<div class="output-card"><div class="output-title">{model}</div><p>{text}</p></div>',
                    unsafe_allow_html=True,
                )

        else:
            st.warning("⚠️ No poetry results found.")

    except Exception as e:
        st.error(f"🚨 An error occurred: {e}")

else:
    st.info("📂 Please upload an image to proceed.")
