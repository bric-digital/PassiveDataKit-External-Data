# pylint: disable=line-too-long

import langdetect

def annotate(content, field_name=None):
    annotations = {}

    annotation_field = 'pdk_language'

    if field_name is not None:
        annotation_field = 'pdk_language_' + field_name

    language = langdetect.detect(content)

    annotations[annotation_field] = language

    scores = langdetect.detect_langs(content)

    annotation_field = 'pdk_language_confidence'

    if field_name is not None:
        annotation_field = 'pdk_language_confidence_' + field_name

    annotations[annotation_field] = None

    for score in scores:
        if score.lang == language:
            annotations[annotation_field] = score.prob

    return annotations

def fetch_annotation_fields():
    return ['pdk_language', 'pdk_language_confidence']


def fetch_annotations(properties):
    if properties is None or isinstance(properties, dict) is False:
        return {}

    annotations = {
        'pdk_language': None,
        'pdk_language_confidence': None,
    }

    if 'pdk_language' in properties:
        annotations['pdk_language'] = properties['pdk_language']
    else:
        for key in properties:
            if key.startswith('pdk_language_') and ('url' in key.lower()) is False:
                annotations['pdk_language']  = properties[key]
            else:
                value = properties[key]

                if isinstance(value, dict):
                    dict_language = fetch_annotations(value)

                    if dict_language is not None and 'pdk_language' in dict_language:
                        annotations['pdk_language']  = dict_language['pdk_language']
                elif isinstance(value, list):
                    for item in value:
                        list_language = fetch_annotations(item)

                        if list_language is not None and 'pdk_language' in list_language:
                            annotations['pdk_language']  = list_language['pdk_language']

    if 'pdk_language_confidence' in properties:
        annotations['pdk_language_confidence'] = properties['pdk_language_confidence']
    else:
        for key in properties:
            if key.startswith('pdk_language_confidence_') and ('url' in key.lower()) is False:
                annotations['pdk_language_confidence']  = properties[key]
            else:
                value = properties[key]

                if isinstance(value, dict):
                    dict_language = fetch_annotations(value)

                    if dict_language is not None and 'pdk_language_confidence' in dict_language:
                        annotations['pdk_language_confidence']  = dict_language['pdk_language_confidence']
                elif isinstance(value, list):
                    for item in value:
                        list_language = fetch_annotations(item)

                        if list_language is not None and 'pdk_language_confidence' in list_language:
                            annotations['pdk_language_confidence']  = list_language['pdk_language_confidence']

    return annotations

def update_data_type_definition(definition):
    for key in definition.keys():
        if 'pdk_language_' in key:
            definition[key]['pdk_variable_name'] = 'Detected Language'
            definition[key]['pdk_variable_description'] = 'Most likely language of the provided content.'

        if 'pdk_language_confidence_' in key:
            definition[key]['pdk_variable_name'] = 'Detected Language Confidence'
            definition[key]['pdk_variable_description'] = 'Confidence of language prediction (0 to 1).'
