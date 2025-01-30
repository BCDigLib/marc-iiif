import pytest

from manifester.image import Image

def test_image_url():
    image = Image('/opt/cantaloupe/images/bc2023-159_0019.jp2')
    assert image.image_url == 'https://iiif.bc.edu/iiif/2/bc2023-159_0019.jp2'

def test_image_counter():
    image = Image('/opt/cantaloupe/images/bc2023-159_0019.jp2')
    assert image.counter == '0019'

def test_image_short_name():
    image = Image('/opt/cantaloupe/images/bc2023-159_0019.jp2')
    assert image.short_name == 'bc2023-159_0019'

def test_cui():
    image = Image('/opt/cantaloupe/images/bc2023-159_0019.jp2')
    assert image.cui == 'bc2023-159'

def test_info_url():
    image = Image('/opt/cantaloupe/images/bc2023-159_0019.jp2')
    assert image.info_url == 'https://iiif.bc.edu/iiif/2/bc2023-159_0019.jp2/info.json'

def test_thumbnail_url():
    image = Image('/opt/cantaloupe/images/bc2023-159_0019.jp2')
    assert image.thumbnail_url == 'https://iiif.bc.edu/iiif/2/bc2023-159_0019.jp2/full/!200,200/0/default.jpg'

def test_annotation_url():
    image = Image('/opt/cantaloupe/images/bc2023-159_0019.jp2')
    assert image.annotation_url == 'https://iiif.bc.edu/iiif/2/bc2023-159/0019/annotation/1'

def test_canvas_url():
    image = Image('/opt/cantaloupe/images/bc2023-159_0019.jp2')
    assert image.canvas_url == 'https://iiif.bc.edu/iiif/2/bc2023-159/canvas/0019'

def test_range_url():
    image = Image('/opt/cantaloupe/images/bc2023-159_0019.jp2')
    assert image.range_url == 'https://iiif.bc.edu/iiif/2/bc2023-159/range/r-18'