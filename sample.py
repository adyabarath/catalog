import streamlit as st
import tempfile
import fitz  # PyMuPDF for PDF processing

def extract_images_from_pdf(pdf_file, output_folder):
    pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
    st.write(pdf_document)
    image_paths = []
    
    # Process each page for images
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        images = page.get_images(full=True)
        
        for i, img in enumerate(images):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            
            # Save image to the output folder
            image_path = f"{output_folder}/page_{page_num+1}_img_{i+1}.png"
            with open(image_path, "wb") as img_file:
                img_file.write(image_bytes)
            image_paths.append(image_path)

    pdf_document.close()
    return image_paths

# File uploader in Streamlit
uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file is not None:
    # Create a temporary directory for storing images
    with tempfile.TemporaryDirectory() as temp_dir:
        # Extract images from the PDF
        image_paths = extract_images_from_pdf(uploaded_file, temp_dir)
        
        # Display and provide download links for each image
        for image_path in image_paths:
            st.image(image_path)
            st.markdown(f"[Download {image_path.split('/')[-1]}](file://{image_path})", unsafe_allow_html=True)