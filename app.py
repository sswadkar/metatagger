from PIL import Image, ImageDraw, ImageFont, ExifTags
from PIL.ExifTags import TAGS
import streamlit as st
from io import BytesIO
from extract_gps_data import get_exif_data
from extract_gps_data import get_gps_info
from extract_gps_data import get_lat_lon
from coords_to_location import get_location_data

def orient_image(image):
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = image._getexif()
        if exif is not None:
            exif = dict(exif.items())
            orientation_value = exif.get(orientation, None)

            if orientation_value == 3:
                image = image.rotate(180, expand=True)
            elif orientation_value == 6:
                image = image.rotate(270, expand=True)
            elif orientation_value == 8:
                image = image.rotate(90, expand=True)
    except Exception as e:
        print(f"Error in correcting orientation: {e}")
    
    return image

def extract_gps_info(image):
    exif_data = get_exif_data(image)
    if not exif_data:
        print("No EXIF data found")
        return None, None

    gps_info = get_gps_info(exif_data)
    if not gps_info:
        print("No GPS info found")
        return None, None

    lat, lon = get_lat_lon(gps_info)
    print(f"Latitude: {lat}, Longitude: {lon}")
    return lat, lon

def overlay_text_on_image(input_image, align):
    # Load the image
    image = input_image

    # Get image metadata
    exif_data = image._getexif()
    metadata = {}
    if exif_data:
        for tag, value in exif_data.items():
            decoded = TAGS.get(tag, tag)
            metadata[decoded] = value

    # Get camera make and model from metadata
    make = metadata.get("Make", "Unknown make")
    model = metadata.get("Model", "Unknown model")

    # Get location metadata
    lat, long = extract_gps_info(image)
    if lat and long:
        city, state, country = get_location_data(lat, long)

    # Get ISO, focal length, f-number, and exposure time from metadata
    iso = metadata.get('ISOSpeedRatings', 'Unknown ISO')
    focal_length = metadata.get('FocalLength', 'Unknown focal length')
    f_number = metadata.get('FNumber', 'Unknown f-number')
    exposure_time = metadata.get('ExposureTime', 'Unknown exposure time')

    # Round focal length and f-number to 2 decimal points if they exist
    if isinstance(focal_length, tuple):
        focal_length = focal_length[0] / focal_length[1]
    if isinstance(f_number, tuple):
        f_number = f_number[0] / f_number[1]

    focal_length = float(round(focal_length, 2)) if focal_length else 'Unknown focal length'
    f_number = float(round(f_number, 2)) if f_number else 'Unknown f-number'

    # Exposure display -- 1 over D/N will get simplified fraction
    exposure_display = f"1 / {int(exposure_time.denominator / exposure_time.numerator)}" if exposure_time else "Unknown exposure time"

    # Prepare text to overlay
    top_text = f"{model}"
    middle_text = f"{city}, {state}, {country}" if lat and long else ""
    bottom_text = f"ISO {iso} | {focal_length} mm | f/{f_number} | {exposure_display} s"

    # Load fonts
    font_bold_59 = ImageFont.truetype("roboto/Roboto-Bold.ttf", 59)
    font_normal_54 = ImageFont.truetype("roboto/Roboto-Medium.ttf", 54)
    font_normal_49 = ImageFont.truetype("roboto/Roboto-Regular.ttf", 49)

    # Correct orientation based on EXIF tags
    image = orient_image(image)

    # Create a drawing context
    draw = ImageDraw.Draw(image)

    # Calculate the text size
    top_text_width = draw.textlength(top_text, font=font_bold_59)
    mid_text_width = draw.textlength(middle_text, font=font_normal_54)
    bottom_text_width = draw.textlength(bottom_text, font=font_normal_49)

    # Define text positions
    image_width, image_height = image.size

    # Define positionining of text based on existence of location
    if lat and long:
        top_mult = 4
        mid_mult = 3
        bottom_mult = 2
    else:
        top_mult = 3
        mid_mult = 3
        bottom_mult = 2


    if (align == 'left'):
        top_text_position = (80, image_height - 80 * top_mult)
        mid_text_position = (80, image_height - 80 * mid_mult)
        bottom_text_position = (80, image_height - 80 * bottom_mult)
    else:
        top_text_position = (image_width - top_text_width - 80, image_height - 80 * top_mult)
        mid_text_position = (image_width - mid_text_width - 80, image_height - 80 * mid_mult)
        bottom_text_position = (image_width - bottom_text_width - 80, image_height - 80 * bottom_mult)

    # Add text to image
    draw.text(top_text_position, top_text, font=font_bold_59, fill="white")
    
    # Only add middle text if it exists
    if lat and long:
        draw.text(mid_text_position, middle_text, font=font_normal_54, fill="white")
    
    draw.text(bottom_text_position, bottom_text, font=font_normal_49, fill="white")

    # Return the modified image
    return image

# Streamlit app
st.title("MetaTagger")

if 'aligns' not in st.session_state:
    st.session_state['aligns'] = {}

if 'processed_images' not in st.session_state:
    st.session_state['processed_images'] = {}

uploaded_files = st.file_uploader("Choose images...", type=["png", "jpg", "jpeg", "heic", "heif", "bmp"], accept_multiple_files=True)

if uploaded_files:
    for i, file in enumerate(uploaded_files):
        st.write(f"Image {i+1}: {file.name}")
        
        if file.name not in st.session_state['aligns']:
            st.session_state['aligns'][file.name] = 'left'
        
        with st.form(key=f'form_{file.name}'):
            align = st.selectbox(f"Choose text alignment for {file.name}", ['left', 'right'], key=f'align_{file.name}', index=['left', 'right'].index(st.session_state['aligns'][file.name]))
            generate_button = st.form_submit_button(label=f"Generate {file.name}")

        st.session_state['aligns'][file.name] = align

        image_container = st.empty()
        download_container = st.empty()

        # PIL image
        image = Image.open(file)

        if generate_button:
            processed_image= overlay_text_on_image(image, align)
            # Save image into Byte Array
            img_byte_arr = BytesIO()
            processed_image.save(img_byte_arr, format='JPEG', compress_level=1, quality=95)
            img_byte_arr = img_byte_arr.getvalue()


            st.session_state['processed_images'][file.name] = (processed_image, img_byte_arr)

        if file.name in st.session_state['processed_images']:
            processed_image, img_byte_arr = st.session_state['processed_images'][file.name]
            image_container.image(processed_image, caption=f'Processed Image: {file.name}', use_column_width=True)

            # Create a download button for the processed image
            download_container.download_button(
                label=f"Download {file.name}",
                data=img_byte_arr,
                file_name=f"processed_{file.name}"
            )
        else:
            # Orient image before displaying
            oriented_image = orient_image(image)
            image_container.image(oriented_image, caption=f'Original Image: {file.name}', use_column_width=True)