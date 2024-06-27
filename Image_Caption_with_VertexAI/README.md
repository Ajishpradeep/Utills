# Gemini Pro Vision Image Captioning

This directory contains scripts to process images using the Gemini Pro Vision generative model to generate captions describing the image 
Example used in this case is to describe retail food items in packages.

## Prerequisites

Before running the scripts, ensure you have the following set up:

1. **Google Cloud Platform Service Account Credentials**:
   - Obtain a JSON key file (`GCP_Gemini_Pro_Vision.json`) for authentication with Google Cloud Platform (GCP).

2. **Python Dependencies**:
   - Ensure Python 3.10 or higher is installed.
   - vertexai: Python SDK for Google Cloud Vertex AI.
   - PIL: Python Imaging Library for image processing.
   - Other standard Python libraries (json, os) are typically included in Python distributions.

## Setup

1. **Authentication**:
   - copy and paste the GCP credentials json (Created in Step:1) to the directory

2. **Initialization**:
   - Initialize Vertex AI with your GCP project ID and location.

## Usage

### 1. Generating Image Captions

The script processes images in a specified folder (`test_images` by default), generates captions using the Gemini Pro Vision model, and saves the results to a JSON file.

```bash
python generate_captions.py
```

### 2. Input Images

Ensure the folder specified (`test_images` in the script) contains the images you want to process. Supported formats include `.jpg`, `.jpeg`, and `.png`.

### 3. Output

The generated captions are saved in a JSON file (`image_captions.json` by default) in the root directory.

## Scripts

### `generate_captions.py`

This script handles image processing and caption generation using the Gemini Pro Vision model. It includes the following functions:

- `process_images_in_folder(folder_path)`: Processes all images in the specified folder and generates captions.
- `save_captions_to_json(captions, output_file)`: Saves the generated captions to a JSON file.

## Example

To run the script and generate captions for images in the `test_images` folder:

```bash
python generate_captions.py
```

## Notes

- Ensure sufficient permissions and quotas on your GCP project for using Vertex AI and accessing models.
- Modify the script parameters as needed for your use case, such as image folder path and output file name.

## License

[MIT License](LICENSE)