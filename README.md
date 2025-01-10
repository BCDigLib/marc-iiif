# marc-iiif

This script exists as a counterpart to the ruby gem stored in BCDIgLib/aspaceiiif. The purpose is to generate IIIF manifests even if there is no description in ArchivesSpace.

# Installation

To install

```shell
pip install --upgrade setuptools
python -m pip install .
```

# Usage

To generate views and manifests for MARC records in a binary MARC record called *records.mrc*:

```shell
manifester records.mrc
```

Check the manifester help (`manifester -h`) for additional options.

# Instructions

1. Digitize material, using Alma 001 fields as file names.
2. Convert digitized images to JP2s and upload copies to the IIIF server.
3. Export existing MARC bibliographic records for digitized materials from Alma, binary format, all records in a single file.
4. Place script and MARC file in the same directory, and place the JP2s in the _jp2s_ directory.
5. Run script.
6. Upload views and manifests to IIIF server.
7. Run the generated Handle batchfile.
8. Update bibliographic records in Alma with links to the viewer.

