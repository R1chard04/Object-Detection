from sentence_transformers import SentenceTransformer, util
from PIL import Image
import glob
import os

'''
# Load the OpenAI CLIP Model
print('Loading CLIP Model...')
model = SentenceTransformer('clip-ViT-B-32')

# Next we compute the embeddings
# To encode an image, you can use the following code:
# from PIL import Image
# encoded_image = model.encode(Image.open(filepath))
image_names = list(glob.glob('./*.jpg'))
print("Images:", len(image_names))
encoded_image = model.encode([Image.open(filepath) for filepath in image_names], batch_size=128, convert_to_tensor=True, show_progress_bar=True)

# Now we run the clustering algorithm. This function compares images aganist 
# all other images and returns a list with the pairs that have the highest 
# cosine similarity score
processed_images = util.paraphrase_mining_embeddings(encoded_image)
NUM_SIMILAR_IMAGES = 10 

# =================
# DUPLICATES
# =================
print('Finding duplicate images...')
# Filter list for duplicates. Results are triplets (score, image_id1, image_id2) and is scorted in decreasing order
# A duplicate image will have a score of 1.00
# It may be 0.9999 due to lossy image compression (.jpg)
duplicates = [image for image in processed_images if image[0] >= 0.999]

# Output the top X duplicate images
for score, image_id1, image_id2 in duplicates[0:NUM_SIMILAR_IMAGES]:
    print("\nScore: {:.3f}%".format(score * 100))
    print(image_names[image_id1])
    print(image_names[image_id2])

# =================
# NEAR DUPLICATES
# =================
print('Finding near duplicate images...')
# Use a threshold parameter to identify two images as similar. By setting the threshold lower, 
# you will get larger clusters which have less similar images in it. Threshold 0 - 1.00
# A threshold of 1.00 means the two images are exactly the same. Since we are finding near 
# duplicate images, we can set it at 0.99 or any number 0 < X < 1.00.
threshold = 0.99
near_duplicates = [image for image in processed_images if image[0] < threshold]

for score, image_id1, image_id2 in near_duplicates[0:NUM_SIMILAR_IMAGES]:
    print("\nScore: {:.3f}%".format(score * 100))
    print(image_names[image_id1])
    print(image_names[image_id2]) '''
    
    
print("Loading CLIP Model...")
model = SentenceTransformer('clip-ViT-B-32')

# glob.glob(()) returns a list of files or folders that matches the path specified in the pathname argument
# list(): convert other sequences or iterables to a list, create an empty list

# image_names = list(glob.glob('Image_Processing\photos\Test\Fault./*.jpg'))
# print("Images:", len(image_names))

# sentence transformers documentation
# encoded_image = model.encode([Image.open(filepath) for filepath in image_names], batch_size=128, convert_to_tensor=True, show_progress_bar=True)
# processed_images = util.paraphrase_mining_embeddings(encoded_image)
# NUM_SIMILAR_IMAGES = 20

# print("Finding near duplicate images...")
# threshold = 0.95
# near_duplicates = [image for image in processed_images if image[0]<threshold]

# for score, image_id1, image_id2 in near_duplicates[0:NUM_SIMILAR_IMAGES]:
#     print("\nScore: {:.3f}%".format(score * 100))
#     print(image_names[image_id1])
#     print(image_names[image_id2])
    
    
    
# samples = list (glob.glob('Image_Processing\comparePairs./*.jpg'))
# samples = list (glob.glob('Image_Processing\photos\Test\Fault./*.jpg'))
samples = list (glob.glob('Image_Processing\photos\Test\Reference./*.jpg'))

encoded_image = model.encode([Image.open(filepath) for filepath in samples], batch_size=128, convert_to_tensor=True, show_progress_bar=True)
processed_images = util.paraphrase_mining_embeddings(encoded_image)
# NUM_SIMILAR_IMAGES = 5
print("Images: ", len(samples))
print("Finding near duplicate images...")
for score, image_id1, image_id2 in processed_images:
    # if (samples[image_id1]  == "Image_Processing\photos\Test\Fault.\STANDARD.jpg") or (samples[image_id2]  == "Image_Processing\photos\Test\Fault.\STANDARD.jpg") :
    if (samples[image_id1]  == "Image_Processing\photos\Test\Reference.\STANDARD.jpg") or (samples[image_id2]  == "Image_Processing\photos\Test\Reference.\STANDARD.jpg") :
        print("\nScore: {:.3f}%".format(score * 100))
        print(samples[image_id1])
        print(samples[image_id2])
