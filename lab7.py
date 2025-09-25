import streamlit as st
import os
import xml.etree.ElementTree as ET

st.title("File Handling GUI (Text, Binary, XML)")

file_type = st.radio("Choose File Type:", ["Text", "Binary", "XML"])
uploaded_file = st.file_uploader(f"Upload a {file_type} file", type=None)
mode = st.radio("Choose Operation:", ["Read", "Write", "Append"])

def save_uploaded_file(uploaded_file):
    file_path = os.path.join("uploaded_" + uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())
    return file_path

file_path = None
if uploaded_file is not None:
    file_path = save_uploaded_file(uploaded_file)
    st.success(f"File saved as {file_path}")

if file_path:
    if file_type == "Text":
        if mode == "Read":
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                st.text_area("File Content:", content, height=200)
            except Exception as e:
                st.error(f"Error: {e}")

        elif mode == "Write":
            new_text = st.text_area("Enter new text to overwrite:")
            if st.button("Write"):
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_text)
                st.success("File overwritten successfully!")
                st.text_area("Updated Content:", new_text, height=200)

        elif mode == "Append":
            new_text = st.text_area("Enter text to append:")
            if st.button("Append"):
                with open(file_path, "a", encoding="utf-8") as f:
                    f.write("\n" + new_text)
                with open(file_path, "r", encoding="utf-8") as f:
                    updated_content = f.read()
                st.success("Content appended successfully!")
                st.text_area("Updated Content:", updated_content, height=200)

    elif file_type == "Binary":
        if mode == "Read":
            try:
                with open(file_path, "rb") as f:
                    data = f.read()
                st.text_area("Binary Data:", str(data), height=200)
            except Exception as e:
                st.error(f"Error: {e}")

        elif mode == "Write":
            new_data = st.text_area("Enter text (will be saved as bytes):")
            if st.button("Write"):
                with open(file_path, "wb") as f:
                    f.write(new_data.encode())
                st.success("Binary file overwritten successfully!")

        elif mode == "Append":
            new_data = st.text_area("Enter text to append as bytes:")
            if st.button("Append"):
                with open(file_path, "ab") as f:
                    f.write(new_data.encode())
                st.success("Data appended successfully!")

    elif file_type == "XML":
        if mode == "Read":
            try:
                tree = ET.parse(file_path)
                root = tree.getroot()
                st.subheader("XML Content:")
                for elem in root.iter():
                    st.write(f"{elem.tag} : {elem.text}")
            except Exception as e:
                st.error(f"Error: {e}")

        elif mode == "Write":
            new_xml = st.text_area("Enter new XML content:")
            if st.button("Write"):
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_xml)
                st.success("XML file overwritten successfully!")

        elif mode == "Append":
            tag = st.text_input("Enter tag name:")
            value = st.text_input("Enter value for the tag:")
            if st.button("Append"):
                try:
                    tree = ET.parse(file_path)
                    root = tree.getroot()
                    new_elem = ET.Element(tag)
                    new_elem.text = value
                    root.append(new_elem)
                    tree.write(file_path, encoding="utf-8")
                    st.success("XML tag appended successfully!")
                    for elem in root.iter():
                        st.write(f"{elem.tag} : {elem.text}")
                except Exception as e:
                    st.error(f"Error: {e}")

else:
    st.info("Please upload a file to begin.")
