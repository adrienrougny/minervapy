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

    def _get_formats_from_url(url):
        inputs = set([])
        outputs = set([])
        response = requests.get(url)
        minervapy.utils.check_response(response)
        json = response.json()
        for input_formats in json["inputs"]:
            for input_format in input_formats["available_names"]:
                inputs.add(_minerva_format_to_short_format[input_format])
        for output_formats in json["outputs"]:
            for output_format in output_formats["available_names"]:
                outputs.add(_minerva_format_to_short_format[output_format])
        return inputs, outputs

    inputs = set([])
    outputs = set([])
    if format_to_format:
        url = minervapy.utils.join_urls(
            [minervapy.session.get_base_url(), _conversion_url]
        )
        format_inputs, format_outputs = _get_formats_from_url(url)
        inputs.update(format_inputs)
        outputs.update(format_outputs)
    if format_to_image:
        url = minervapy.utils.join_urls(
            [minervapy.session.get_base_url(), _conversion_image_url]
        )
        image_inputs, image_outputs = _get_formats_from_url(url)
        inputs.update(image_inputs)
        outputs.update(image_outputs)
    return inputs, outputs


def convert(
    input_file_path_or_input_data,
    input_format,
    output_format,
    output_file_path=None,
    unzip=True,
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
    if isinstance(input_file_path_or_input_data, bytes):
        input_data = input_file_path_or_input_data
    else:
        with open(input_file_path_or_input_data, "rb") as input_file:
            input_data = input_file.read()
    data = minervapy.utils.request_to_data(
        url,
        method="POST",
        data=input_data,
        headers={"Content-Type": "application/octet-stream"},
        unzip=unzip,
    )
    if output_file_path is not None:
        minervapy.utils.data_to_file(data, output_file_path)
    return data
