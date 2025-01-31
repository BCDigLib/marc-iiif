# marc-iiif

This script exists as a counterpart to the ruby gem stored in BCDIgLib/aspaceiiif. The purpose is to generate IIIF manifests even if there is no description in ArchivesSpace.

# Installation

To install

```shell
pip install --upgrade setuptools
python -m pip install .
```

If you want to modify the application, you can install it with the `--editable`
 option:

```shell
pip install --upgrade setuptools
python -m pip install --editable .
```

# Usage

To generate views and manifests for MARC records in a binary MARC record called *records.mrc*:

```shell
manifester records.mrc
```

Check the manifester help (`manifester -h`) for additional options.

# Instructions

Make sure the JPEG2000 images have been uploaded to the IIIF server image and have the naming format
_identifier_counter.jp2_, where _identifier_ is the identifier defined in the source record and _counter_ is a 4-digit 
zero-padded string that indicates the position in the image sequence. 

For example:

```commandline
im-m057-2000_0001
im-m057-2000_0002
im-m057-2000_0003
im-m057-2000_0004
...
```

Then run the `manifester` command against a source record file:

```commandline
manifester --ssh my_user@scenery.bc.edu --image_base im-m057-2000 source_record.mrc 
```

The flags:

* `--ssh` - SSH credentials for a user who has access (using public key login) to the IIIF server
* `--image_base` - the identifier portion of the image

The final parameter is a source record containing metadata necessary to build the manifest.

## Source formats

Currently supported source record formats:

* binary MARC records

To add a new source record format, create a new class inheriting from the SourceRecord abstract class. 