import xml.etree.ElementTree as ET

namespaces = {'fitsout': 'http://hul.harvard.edu/ois/xml/ns/fits/fits_output'}

def image_names(fits_file: str)->list[str]:
    """
    Get a  list of image names from a FITS output file

    :param fits_file: str the path to the FITS file
    :return: list[str] a list of image names
    """
    tree = ET.parse(fits_file)
    root = tree.getroot()
    return [get_image_name(fits) for fits in root]

def get_image_name(fits)->str:
    """
    Get the name of a single image

    :param fits: a <fits> element
    :return: str a singly filename
    """
    fileinfo = fits.find('fitsout:fileinfo', namespaces)
    filename = fileinfo.find('fitsout:filename', namespaces)
    return filename.text.rstrip()