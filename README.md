# marc-iiif

This script exists as a counterpart to the ruby gem stored in BCDIgLib/aspaceiiif. The purpose is to generate IIIF manifests even if there is no description in ArchivesSpace.

# Installation

To install

```shell
# Clone this repository
git clone https://github.com/BCDigLib/marc-iiif.git
cd marc-iiif

# Create the app's .env file and edit if necessary
cp sample.env ./src/manifester/.env

# Create a Python virtualenv in this folder and use it
python -m venv venv
source ./venv/bin/activate

# Install setup tools and install the app
pip install --upgrade setuptools
python -m pip install .

```

Then edit the .env configuration file as appropriate.

If you want to modify the application, you can install it with the `--editable`
 option:

```shell
python -m pip install --editable .
```

# Upgrading

To upgrade, pull any changes to the main branch and install

```shell
git pull
pythom -m pip install .
```

# Usage

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

Then run the `manifester` command against a source record file.

For a MARC file:

```commandline
manifester --ssh my_user@scenery.bc.edu --image_base im-m057-2000 source_record.mrc 
```

For an ASpace record, use the URL path for the record:

```commandline
manifester --ssh my_user@scenery.bc.edu --image_base im-m057-2000  /repositories/###/resources/### 
```

For an Excel file with multiple records, use the path to the file. The `image_base` is not necessary, since the image URLs will be derived from the identifiers in the file:

```commandline
manifester --ssh my_user@scenery.bc.edu please-make-these-manifests.xlsx
```

The flags:

* `--image_base` - the identifier portion of the image
* `--ssh` - SSH credentials for a user who has access (using public key login) to the IIIF server.

The final parameter is a source record containing metadata necessary to build the manifest.

The full list of options:

* `-h`, `--help` - show this help message and exit
* `--attribution ATTRIBUTION` - text of attribution
* `--citation CITATION` - text of citation
* `--handle HANDLE` - Handle URL
* `--image_base IMAGE_BASE` - image file prefix (e.g. ms-2020-020-142452)
* `--image_dir IMAGE_DIR` - image directory on IIIF server
* `--ssh SSH` - IIIF server SSH connection string (ex. florinb@scenery.bc.edu
* `--view viewfile.html` - filename for view file output
* `--manifest manifestfile.json` - filename for manifest file output
* `-v, --verbose` - increase output verbosity

## Source formats

Currently supported source record formats:

* binary MARC records
* ArchivesSpace record URLs
* Excel files containing lists of metadata

To add a new source record format, create a new class inheriting from the SourceRecord abstract class. 