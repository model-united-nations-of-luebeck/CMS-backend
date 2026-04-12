import os

from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import stringWidth, registerFont
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4, A3
from reportlab.lib.utils import ImageReader

from django.conf import settings

def _register_MUNOL_fonts() -> None:
    """
    Registers the MUNOL CenturyGothic fonts if they exist in the media directory so that they are available for PDF generation.
    """
    _register_font('CenturyGothic', os.path.join(settings.MEDIA_ROOT, 'fonts/Century Gothic Regular.TTF'))
    _register_font('CenturyGothicBold', os.path.join(settings.MEDIA_ROOT, 'fonts/Century Gothic Bold.TTF'))
    _register_font('CenturyGothicItalic', os.path.join(settings.MEDIA_ROOT, 'fonts/Century Gothic Italic.TTF'))

def _register_font(font_name:str, font_file:str) -> None:
    """Helper function to register a single font if the font file exists.
    Args:
        font_name (str): The name to register the font under.
        font_file (str): The path to the font file.
    """
    if os.path.exists(font_file):
        registerFont(TTFont(font_name, font_file))
    else:
        print(f"Font file {font_file} not found. {font_name} will not be registered.")

def _get_fitting_font_size(text: str, default_font_size: int=16, font_name: str='CenturyGothicBold', max_width=50*mm) -> int:
    """Calculates the maximum font size that allows the given text to fit within the specified maximum width when rendered with the specified font.
    Args:        
        text (str): The text to fit.
        default_font_size (int, optional): The starting font size to check from. Defaults to 16.
        font_name (str, optional): The name of the registered font to use for width calculations. Defaults to 'CenturyGothicBold'.
        max_width (float, optional): The maximum width in points that the text should fit within. Defaults to 50*mm.
    
    Returns:
        int: The maximum font size that allows the text to fit within the max_width.
    """
    
    width = max_width
    font_size = default_font_size
    while width >= max_width:
        width = stringWidth(text, font_name, font_size)
        font_size -= 1
    return font_size
        
def _get_transparent_background_logo():
    """Helper function to get the ImageReader for the transparent logo used in badges and placards.
    Returns:
        ImageReader: The ImageReader object for the transparent logo.
    """
    return ImageReader(os.path.join(settings.MEDIA_ROOT, 'images/logograytransparent.png'))

def _filter_queryset_by_uuid(queryset, request):
    """
    Filters a queryset by a list of UUIDs provided in the request. The UUIDs should be passed as a comma-separated string in the 'uuid' query parameter. If the 'uuid' parameter is not provided or is empty, the original queryset is returned unfiltered, i.e. all entries are returned.

    Args:        
        queryset: The initial queryset to filter.
        request: The HTTP request object containing the query parameters.

    Returns:
        The filtered queryset if 'uuid' parameter is provided and valid, otherwise the original queryset.
    """
    if request.GET is not None and 'uuid' in request.GET and request.GET['uuid'] != '':
        queryset = queryset.filter(id__in=request.GET['uuid'].split(","))
    return queryset.all()

def _get_page_size_from_request(request):
    """Helper function to determine the page size for PDF generation based on the 'pagesize' query parameter in the request. If 'pagesize' is set to 'A3', A3 page size is returned; otherwise, A4 is returned by default.
    
    Args:
        request: The HTTP request object containing the query parameters.
        
    Returns:
        A tuple representing the page size (width, height) in points. A3 or A4 depending on the 'pagesize' parameter.
    """
    if request.GET is not None and 'pagesize' in request.GET:
        return A3 if request.GET['pagesize'] == 'A3' else A4
    return A4
