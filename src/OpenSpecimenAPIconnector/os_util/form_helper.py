import re
import json

class form_helper:

    def __init__(self, form_id=-1):
        self.form_id = form_id

    
    def get_fresh_structure(self, caption, variable=None):
        if variable is None:
            variable = caption

        name = self._clear_variable_name(variable)

        form = {"$saved": True,
                "name": name,
                "caption": caption,
                "id": self.form_id,
                "layouts": [],
                "rows": []}

        return form


    def create_headline(self, text, variable=None, font_size=20):
        if variable is None:
            variable = text

        name = self._clear_variable_name(variable)

        row = {
            "$saved": True,
            "type": "label",
            "$sameRowAsLastField": False,
            "note": True,
            "caption": f"<span style=\"font-size:{font_size}px;\"><strong>{text}</strong></span>",
            "udn": name,
            "name": name
        }

        return [row]
    

    def create_textfield(self, caption, variable=None, mandatory=False, same_row_as_last_field=False):
        if variable is None:
            variable = caption

        name = self._clear_variable_name(variable)

        row = {
            "defaultValue": "",
            "caption": caption,
            "type": "stringTextField",
            "mandatory": mandatory,
            "labelPosition": "LEFT_SIDE",
            "showInGrid": False,
            "name": name,
            "udn": name,
            "$sameRowAsLastField": same_row_as_last_field,
            "$unused": ""
        }

        return [row]    


    def create_checkbox(self, caption, options, default_idx, variable=None, same_row_as_last_field=False):
        if variable is None:
            variable = caption

        name = self._clear_variable_name(variable)

        pvs = []
        for pv in options:
            tmp = {
                "optionName": pv,
                "value": pv
            }
            pvs.append(tmp)

        row = {
                "defaultValue": {
                    "optionName": options[default_idx],
                    "value": options[default_idx]
                },
                "pvs": pvs,
                "caption": caption,
                "type": "checkbox",
                "mandatory": False,
                "optionsPerRow": len(options),
                "labelPosition": "LEFT_SIDE",
                "showInGrid": False,
                "dataType": "STRING",
                "toolTip": "",
                "name": name,
                "udn": name,
                "$sameRowAsLastField": same_row_as_last_field,
                "$sfField": False,
                "$unused": [
                    options[default_idx]
                ]
                }

        return [row]


    def create_dropdown(self, caption, options, default_idx=-1, variable=None, mandatory=False, same_row_as_last_field=False):
        if variable is None:
            variable = caption

        name = self._clear_variable_name(variable)

        pvs = []
        for pv in options:
            tmp = {
                "optionName": pv,
                "value": pv
            }
            pvs.append(tmp)

        row = {
            "caption": caption,
            "type": "combobox",
            "mandatory": mandatory,
            "labelPosition": "LEFT_SIDE",
            "showInGrid": False,
            "pvOrdering": "NONE",
            "pvs": pvs,
            "dataType": "STRING",
            "toolTip": "",
            "name": name,
            "udn": name,
            "$sameRowAsLastField": same_row_as_last_field,
        }
        if default_idx != -1:
            row["defaultValue"] = {"value": options[default_idx]}

        return [row]


    def create_final_form(self, form, fields):

        row_idx = 0
        for field in fields:

            if field[0]["$sameRowAsLastField"] == True:
                row_idx -= 1
                field[0]["$rowIdx"] = row_idx

                form["rows"][-1].append(field[0])
            else:
                field[0]["$rowIdx"] = row_idx
                field[0]["pageRow"] = row_idx + 1
                field[0]["rowColumn"] = 1

                form["rows"].append(field)

            row_idx += 1
        
        return json.dumps(form)


    def _clear_variable_name(self, variable_name):

        # replace escape sequence
        variable_name = variable_name.encode().decode("unicode-escape")

        # Remove umlauts
        umlaut_map = {
            "ä": "ae",
            "ö": "oe",
            "ü": "ue",
            "Ä": "Ae",
            "Ö": "Oe",
            "Ü": "Ue",
            "ß": "ss"
            }

        for umlaut, replacement in umlaut_map.items():
            variable_name = variable_name.replace(umlaut, replacement)

        # Replace special characters with underscores
        variable_name = re.sub(r'[^a-zA-Z0-9]', '_', variable_name)

        return variable_name.lower()
