import os
import json
import typing
import vertexai
from PIL import Image as PIL_Image
from PIL import ImageOps as PIL_ImageOps
from vertexai.generative_models import GenerativeModel, Image

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "GCP_Gemini_Pro_Vision.json"

with open('GCP_Gemini_Pro_Vision.json', 'r') as file:
    json_data = json.load(file)

PROJECT_ID = json_data.get('project_id')
LOCATION = "us-central1"

vertexai.init(project=PROJECT_ID, location=LOCATION)
multimodal_model = GenerativeModel("gemini-1.0-pro-vision")

def display_images(images: typing.Iterable[Image], max_width: int = 600, max_height: int = 350) -> None:
    for image in images:
        pil_image = typing.cast(PIL_Image.Image, image._pil_image)
        if pil_image.mode != "RGB":
            pil_image = pil_image.convert("RGB")
        image_width, image_height = pil_image.size
        if max_width < image_width or max_height < image_height:
            pil_image = PIL_ImageOps.contain(pil_image, (max_width, max_height))
        pil_image.show()

def get_image_bytes_from_file(image_path: str) -> bytes:
    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()
    return image_bytes

def load_image_from_file(image_path: str) -> Image:
    image_bytes = get_image_bytes_from_file(image_path)
    return Image.from_bytes(image_bytes)

def generate_caption_for_image(image_path: str) -> str:
    image = load_image_from_file(image_path)
    prompt = "The object in the image is a retail food item in a package or a somewhat of container, Describe this image in a following format: [food_item] in a [package_type] package, [color description of the package]. The image is taken from a [view_angle] angle, with the [side] of the package facing the viewer."
    contents = [image, prompt]
    responses = multimodal_model.generate_content(contents, stream=True)
    caption = "".join([response.text for response in responses])
    return caption.strip()

def process_images_in_folder(folder_path: str) -> dict:
    image_captions = {}
    image_files = [f for f in os.listdir(folder_path) if f.endswith((".jpg", ".jpeg", ".png"))]
    total_images = len(image_files)

    for count, filename in enumerate(image_files, start=1):
        image_path = os.path.join(folder_path, filename)
        caption = generate_caption_for_image(image_path)
        product_title = os.path.splitext(filename)[0]  # Remove the file extension for the title
        image_captions[product_title] = {"product_title": product_title, "caption": caption}
        print(f"Processed {count}/{total_images} images")

    return image_captions

def save_captions_to_json(captions: dict, output_file: str) -> None:
    with open(output_file, 'w') as json_file:
        json.dump(captions, json_file, indent=4)

# Folder containing images
folder_path = "test_images"

# Process images and generate captions
image_captions = process_images_in_folder(folder_path)

# Save captions to JSON file
output_json_file = "image_captions.json"
save_captions_to_json(image_captions, output_json_file)

print(f"Captions saved to {output_json_file}")