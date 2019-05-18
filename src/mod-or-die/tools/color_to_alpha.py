import glob
from PIL import Image

def transparent(img, color: (int, int, int)):
    img = Image.open(img)
    img = img.convert("RGBA")

    pixdata = img.load()

    width, height = img.size
    for y in range(height):
        for x in range(width):
            if pixdata[x, y][:3] == color:
                pixdata[x, y] = (255, 255, 255, 0)

    img.save(img, "PNG")


def main(color: (int, int, int)):
    for image in glob.glob("*.png"):
        transparent(image, color)


if __name__ == "__main__":
    color = (255, 255, 255)
    main(color)