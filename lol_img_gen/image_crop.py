from PIL import Image

test_image = "../_samples/frame20sec.jpg"
original = Image.open(test_image)

width, height = original.size   # Get dimensions
left = width/4
top = height/4
right = 3 * width/4
bottom = 3 * height/4
print left
print top
print bottom
print right
top = 55
bottom = 68
right = 655
left = 625
cropped_example = original.crop((left, top, right, bottom))



cropped_example.show()
