
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
import torch
from PIL import Image

# Load the pre-trained model and tokenizer, and initialize the ViTImageProcessor
model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
feature_extractor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)



max_length = 16
num_beams = 4
gen_kwargs = {"max_length": max_length, "num_beams": num_beams}
def predict_step(image_paths):
  
  """
    This function takes a list of image paths and generates a caption for each image using the pre-trained
    'VisionEncoderDecoderModel' from the Hugging Face Transformers library. It first loads the model and 
    tokenizer, and initializes the ViTImageProcessor for feature extraction. It then loops over the list of
    image paths, opens each image with PIL, and converts it to RGB format if necessary. The images are then
    processed by the ViTImageProcessor to extract features, and the resulting tensors are moved to the GPU
    if available. The pre-trained model is then used to generate captions for each image by running the 
    'generate' method, which takes the feature tensors as input and returns output token IDs. The predicted
    captions are decoded from token IDs to text using the tokenizer and are returned as a list.

    Args:
    - image_paths (list): a list of file paths to images

    Returns:
    - preds (list): a list of predicted captions for each input image
  """
  images = []
  for image_path in image_paths:
    i_image = Image.open(image_path)
    if i_image.mode != "RGB":
      i_image = i_image.convert(mode="RGB")

    images.append(i_image)
  # Extract features from the images and move the tensors to the GPU if available
  pixel_values = feature_extractor(images=images, return_tensors="pt").pixel_values
  pixel_values = pixel_values.to(device)

  # Generate captions for the images using the pre-trained model and tokenizer
  output_ids = model.generate(pixel_values, **gen_kwargs)

  preds = tokenizer.batch_decode(output_ids, skip_special_tokens=True)
  preds = [pred.strip() for pred in preds]

  # Return the list of predicted captions
  return preds

