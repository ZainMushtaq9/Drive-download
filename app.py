apimport streamlit as st
import gdown
import os

st.set_page_config(page_title="Drive Downloader", page_icon="📁")

st.title("📁 Google Drive File Downloader")

st.markdown(
    """
Paste a **Google Drive file URL or File ID** below.  
Make sure the file is shared as: **Anyone with the link → Viewer**.
"""
)

def extract_file_id(text: str) -> str:
    """
    Accept either a full Google Drive URL or a bare file ID
    and return the file ID.
    """
    text = text.strip()

    # Typical URL formats:
    # https://drive.google.com/file/d/<FILE_ID>/view?usp=sharing
    # https://drive.google.com/open?id=<FILE_ID>
    # https://drive.google.com/uc?id=<FILE_ID>&export=download
    if "drive.google.com" in text:
        if "/d/" in text:
            # /file/d/<FILE_ID>/
            return text.split("/d/")[1].split("/")[0]
        if "id=" in text:
            return text.split("id=")[1].split("&")[0]

    # Fallback: assume it's already just an ID
    return text


drive_input = st.text_input(
    "Google Drive file URL or File ID",
    placeholder="https://drive.google.com/file/d/XXXXXXXXXXXX/view?usp=sharing",
)

download_clicked = st.button("Fetch from Google Drive")

if download_clicked:
    if not drive_input:
        st.error("Please paste a file URL or ID first.")
    else:
        file_id = extract_file_id(drive_input)
        with st.spinner("Downloading from Google Drive..."):
            try:
                # gdown will infer filename from Drive metadata if output=None
                downloaded_path = gdown.download(id=file_id, output=None, quiet=True)

                if downloaded_path is None or not os.path.exists(downloaded_path):
                    st.error("Download failed. Check sharing permissions and file ID.")
                else:
                    file_name = os.path.basename(downloaded_path)
                    st.success(f"Downloaded: {file_name}")

                    with open(downloaded_path, "rb") as f:
                        st.download_button(
                            label="⬇️ Download file",
                            data=f,
                            file_name=file_name,
                            mime="application/octet-stream",
                        )
            except Exception as e:
                st.error(f"Error while downloading: {e}")
