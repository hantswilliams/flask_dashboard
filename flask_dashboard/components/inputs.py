# components/inputs.py

from flask import render_template_string

class InputDropdown:
    def __init__(self, name, label, values, action_url="/", selected_value=None):
        self.name = name
        self.label = label
        if isinstance(values, tuple) and len(values) == 2 and hasattr(values[0], 'loc'):
            # If values is a tuple and the first item is a DataFrame, extract unique values from the given column
            self.values = values[0][values[1]].unique().tolist()
        elif isinstance(values, list):
            # If values is a list, use it directly
            self.values = values
        else:
            raise ValueError("Invalid values provided. It should be either a list or a tuple with DataFrame and column name.")
        self.action_url = action_url
        self.selected_value = selected_value

    def render(self):
        template = '''
        <select name="{{ name }}">
        <label for="{{ name }}">{{ label }}</label>
        {% for value in values %}
            <option value="{{ value }}" {% if value == selected_value %}selected{% endif %}>{{ value }}</option>
        {% endfor %}
        </select>
        '''
        return render_template_string(template, name=self.name, label=self.label, values=self.values, selected_value=self.selected_value)




class TextInput:
    def __init__(self, name, label, default_value=""):
        self.name = name
        self.label = label
        self.default_value = default_value

    def render(self):
        template = '''
        <label for="{{ name }}">{{ label }}</label>
        <input type="text" id="{{ name }}" name="{{ name }}" value="{{ default_value }}">
        '''
        return render_template_string(template, name=self.name, label=self.label, default_value=self.default_value)


