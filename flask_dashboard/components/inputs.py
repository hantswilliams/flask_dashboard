# components/inputs.py

from flask import render_template_string

class BaseInput:
    def __init__(self, name, default_value=""):
        self.name = name
        self.default_value = default_value

    def capture(self, request):
        self.value = request.form.get(self.name, self.default_value)

class InputDropdown(BaseInput):
    def __init__(self, name, label, values, action_url="/", selected_value="Select All"):
        # Initialize the base attributes
        super().__init__(name, selected_value)
        
        self.label = label
        if isinstance(values, tuple) and len(values) == 2 and hasattr(values[0], 'loc'):
            # If values is a tuple and the first item is a DataFrame, extract unique values from the given column
            self.values = ["Select All"] + values[0][values[1]].unique().tolist()
        elif isinstance(values, list):
            # If values is a list, add "Select All" at the beginning
            self.values = ["Select All"] + values
        else:
            raise ValueError("Invalid values provided. It should be either a list or a tuple with DataFrame and column name.")
        
        self.action_url = action_url
        self.selected_value = selected_value

    def capture(self, request):
        self.value = request.form.get(self.name)

        print(f"Captured value for {self.name}: {self.value}")  # debugging print statement
        
        if not self.value:
            # Default to the 'Select All' option
            self.value = "Select All"
        
        # Update the selected_value to the captured value for rendering purposes
        self.selected_value = self.value

    def render(self):
        print("....Rendering dropdown....") 
        template = '''
        <div class="overflow-hidden">
            <label for="{{ name }}" class="overflow-hidden block text-sm font-medium text-red-700">{{ label }}</label>
            <select name="{{ name }}" class="overflow-hidden">
                {% for value in values %}
                    <option value="{{ value }}" {% if value == selected_value %}selected{% endif %}>{{ value }}</option>
                {% endfor %}
            </select>
        </div>
        '''
        return render_template_string(template, name=self.name, label=self.label, values=self.values, selected_value=self.selected_value)
class TextInput(BaseInput):
    def __init__(self, name, label, default_value=""):
        # Initialize the base attributes
        super().__init__(name, default_value)
        
        self.label = label

    def render(self):
        template = '''
        <label for="{{ name }}">{{ label }}</label>
        <input type="text" id="{{ name }}" name="{{ name }}" value="{{ default_value }}">
        '''
        return render_template_string(template, name=self.name, label=self.label, default_value=self.default_value)

