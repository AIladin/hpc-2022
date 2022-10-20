from PIL import Image


def downscale_image(image_path: str, output_path: str, size: tuple[int, int]):
    image = Image.open(image_path)
    downscaled = image.resize(size)
    downscaled.save(output_path)
