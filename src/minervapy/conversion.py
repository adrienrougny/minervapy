import dataclasses

import requests

import minervapy.utils
import minervapy.session


_conversion_url = "convert/"
_conversion_image_url = "convert/image/"

_short_format_to_minerva_default_format = {
    "sbgnml": "lcsb.mapviewer.converter.model.sbgnml.SbgnmlXmlConverter",
    "celldesigner": "lcsb.mapviewer.converter.model.celldesigner.CellDesignerXmlParser",
    "sbml": "lcsb.mapviewer.converter.model.sbml.SbmlParser",
    "gpml": "lcsb.mapviewer.wikipathway.GpmlParser",
    "png": "lcsb.mapviewer.converter.graphics.PngImageGenerator",
    "pdf": "lcsb.mapviewer.converter.graphics.PdfImageGenerator",
    "svg": "lcsb.mapviewer.converter.graphics.SvgImageGenerator",
}

_minerva_format_to_short_format = {
    "lcsb.mapviewer.converter.model.sbgnml.SbgnmlXmlConverter": "sbgnml",
    "SBGN-ML": "sbgnml",
    "lcsb.mapviewer.converter.model.celldesigner.CellDesignerXmlParser": "celldesigner",
    "CellDesigner_SBML": "celldesigner",
    "lcsb.mapviewer.converter.model.sbml.SbmlParser": "sbml",
    "SBML": "sbml",
    "lcsb.mapviewer.wikipathway.GpmlParser": "gpml",
    "GPML": "gpml",
    "lcsb.mapviewer.converter.graphics.PngImageGenerator": "png",
    "png": "png",
    "lcsb.mapviewer.converter.graphics.PdfImageGenerator": "pdf",
    "pdf": "pdf",
    "lcsb.mapviewer.converter.graphics.SvgImageGenerator": "svg",
    "svg": "svg",
}

_image_formats = set(["png", "pdf", "svg"])


def get_formats(format_to_image=True, format_to_format=True):
    inputs = set([])
    outputs = set([])
    if format_to_format:
        url = minervapy.utils.join_urls(
            [minervapy.session.get_base_url(), _conversion_url]
        )
        response = requests.get(url)
        json = minervapy.utils.get_json(response)
        for input_formats in json["inputs"]:
            for input_format in input_formats["available_names"]:
                inputs.add(_minerva_format_to_short_format[input_format])
        for output_formats in json["outputs"]:
            for output_format in output_formats["available_names"]:
                outputs.add(_minerva_format_to_short_format[output_format])
    if format_to_image:
        url = minervapy.utils.join_urls(
            [minervapy.session.get_base_url(), _conversion_image_url]
        )
        response = requests.get(url)
        json = minervapy.utils.get_json(response)
        for input_formats in json["inputs"]:
            for input_format in input_formats["available_names"]:
                inputs.add(_minerva_format_to_short_format[input_format])
        for output_formats in json["outputs"]:
            for output_format in output_formats["available_names"]:
                outputs.add(_minerva_format_to_short_format[output_format])
    return inputs, outputs


def convert(
    input_file_path, input_format, output_file_path, output_format, unzip=True
):
    if output_format in _image_formats:
        conversion_url = _conversion_image_url
    else:
        conversion_url = _conversion_url
    input_minerva_format = _short_format_to_minerva_default_format[input_format]
    output_minerva_format = _short_format_to_minerva_default_format[
        output_format
    ]
    url_suffix = f"{input_minerva_format}:{output_minerva_format}"
    url = minervapy.utils.join_urls(
        [
            minervapy.session.get_base_url(),
            conversion_url,
            url_suffix,
        ]
    )
    with open(input_file_path, "rb") as input_file:
        input_data = input_file.read()
    response = requests.post(
        url=url,
        data=input_data,
        headers={"Content-Type": "application/octet-stream"},
    )
    content = response.content
    if unzip and response.headers["Content-Type"] == "application/zip":
        z = zipfile.ZipFile(io.BytesIO(content))
        zip_infos = z.infolist()
        content = z.read(zip_infos[0])
    with open(output_file_path, "wb") as output_file:
        output_file.write(content)
