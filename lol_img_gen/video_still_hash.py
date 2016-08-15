from PIL import Image, ImageEnhance
import imagehash

HASH_SIZE_SMALL = 4
HASH_SIZE_LARGE = 64
CONTRAST = 9000.0

HASH_FUNCTION = imagehash.average_hash


def video_still_hash_small_file(path):
    return video_still_hash_small(Image.open(path))


def video_still_hash_large_file(path):
    return video_still_hash_large(Image.open(path))


def video_still_hash_small(image):
    return _video_still_hash(image, HASH_SIZE_SMALL)


def video_still_hash_large(image):
    return _video_still_hash(image, HASH_SIZE_LARGE)


def _video_still_hash(image, size):
    image = _prep_image(image)
    return str(HASH_FUNCTION(image, hash_size=size))


def _prep_image(image, show=False, contrast_val=CONTRAST):
    image = image.convert('LA')
    contrast = ImageEnhance.Contrast(image)
    image = contrast.enhance(contrast_val)
    if show:
        image.show()
    return image

if __name__ == "__main__":
    print(video_still_hash_large_file("/tmp/stills/15.png"))
