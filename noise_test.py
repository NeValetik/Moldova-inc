import noise
from PIL import Image

def generate_perlin_noise(width, height, scale=100.0, octaves=6, persistence=0.5, lacunarity=2.0, seed=None):
    img = Image.new("RGB", (width, height))
    if seed is not None:
        noise.seed(seed)

    for y in range(height):
        for x in range(width):
            value = noise.pnoise2(x/scale,
                                  y/scale,
                                  octaves=octaves,
                                  persistence=persistence,
                                  lacunarity=lacunarity,
                                  repeatx=1024,
                                  repeaty=1024,
                                  base=0)
            color = int((value + 1) / 2 * 255)  # Scale noise to [0, 255]
            img.putpixel((x, y), (color, color, color))

    return img

def save_image(image, filename):
    image.save(filename)

if __name__ == "__main__":
    width = 512
    height = 512
    scale = 100.0
    octaves = 6
    persistence = 0.5
    lacunarity = 2.0
    seed = None  # Change to an integer value for reproducibility

    perlin_img = generate_perlin_noise(width, height, scale, octaves, persistence, lacunarity, seed)
    save_image(perlin_img, "perlin_noise.png")
