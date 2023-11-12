import streamlit as st
from utils import get_caption, generate_titles
from PIL import Image
from io import BytesIO


def main():
    st.set_page_config(page_title="Image community title", page_icon="\U0001F642", layout='wide')
    st.header("Image Collection Title")
    container = st.container()
    images = container.file_uploader(
        "Upload your images:", type="jpg", accept_multiple_files=True
    )
    cols_button = container.columns(5)
    title_button = cols_button[2].button('Generate title!', 
                                        use_container_width = True, 
                                        on_click=run_generation(images))


def run_generation(images):
    cols_main = st.columns(2)
    container_left = cols_main[0].container()
    container_right = cols_main[1].container()
    all_captions = ""
    all_cap_list = []
    all_img_names = []
    all_images = []

    for img in images:
        # get the image bytes and convert to PIL image
        img_bytes = img.getvalue()
        pil_image = Image.open(BytesIO(img_bytes))
        all_images.append(pil_image)

        caption = get_caption(pil_image)
        if all_captions:
            all_captions = all_captions + ", " + caption
        else:
            all_captions = caption
        all_cap_list.append(caption)

    for i, _ in enumerate(images):
        cols = container_left.columns(2)
        cols[0].image(all_images[i])
        cols[1].markdown(all_cap_list[i])


    if len(images) > 0:
        # create a few title ideas using GPT
        titles = generate_titles(all_captions)
        container_right.title('Title Ideas')
        container_right.write(titles)


if __name__ == "__main__":
    main()