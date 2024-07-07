## ![MetaTagger](https://metatagger.streamlit.app/)

MetaTagger is a tool designed to enhance and tag your images using metadata. This project leverages the detailed information embedded within your images to apply custom overlays, tags, and enhancements seamlessly. The streamlit app can be found ![here](https://metatagger.streamlit.app/)

### Features

- **Metadata-Driven Enhancements**: Automatically extracts and uses image metadata such as ISO, focal length, f-number, and exposure time to create informative overlays.
- **Customizable Text Alignment**: Choose between left and right alignment for text overlays to fit your image aesthetics.
- **Efficient Image Processing**: Processes and optimizes images without significant size increases, ensuring high-quality results.
- **Streamlit Integration**: User-friendly web interface built with Streamlit, allowing easy image uploads, processing, and downloads.
- **Individual Image Controls**: Each image can be processed independently with its own settings, ensuring a tailored enhancement experience.
- **Dynamic Updates**: Utilizes Streamlit's session state and dynamic containers to provide a seamless and interactive user experience.

### Example

Here’s an example of an enhanced image with metadata overlay:

![Enhanced Image](example_tagged_image.jpeg)

### Getting Started

1. **Clone the repository**:
   ```bash
   git clone https://github.com/sswadkar/metatagger.git
   cd metatagger
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit app**:
   ```bash
   streamlit run app.py
   ```

4. **Open your browser** to `http://localhost:8501` (or whatever port Streamlit runs on) to start using MetaTagger.

### Usage

- **Upload Images**: Easily upload multiple images via the Streamlit interface.
- **Select Alignment**: Choose text alignment for each image using the provided forms.
- **Generate and Download**: Generate enhanced images with metadata overlays and download them individually.

### License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.