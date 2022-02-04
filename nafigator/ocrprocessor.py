# coding: utf-8

"""OCR module."""

try:
    import pdf2image

    PDF2IMAGE = True
except:
    PDF2IMAGE = False
try:
    from PIL import Image

    IMAGE = True
except ImportError:
    try:
        import Image

        IMAGE = True
    except:
        IMAGE = False
try:
    import pytesseract

    PYTESSERACT = True
except:
    PYTESSERACT = False


def convert_ocr_pdf(path: str = None, format: str = "text", params: dict = None) -> str:
    """Function to process ocr on pdf to generate text

       Source: https://stackoverflow.com/questions/29657237/tesseract-ocr-pdf-as-input

    Args:
        path: location of the file to be converted
        format: text
        params: the general params dict to store results

    Returns:
        str: the result of the conversion

    """
    images = pdf2image.convert_from_path(path)
    text = [pytesseract.image_to_string(image) for page, image in enumerate(images)]
    return "\n".join(text)
