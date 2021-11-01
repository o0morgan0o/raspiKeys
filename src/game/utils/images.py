from PIL import Image, ImageTk


def create_image(img_path):
    mImage = Image.open(img_path)
    render = ImageTk.PhotoImage(mImage)
    return render
