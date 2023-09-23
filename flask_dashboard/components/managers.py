## Havn't added this in yet....for future use

# components/managers.py

from flask import render_template_string
from markdown import markdown


FORM_GROUP_TEMPLATE = """
<form method="post" action="{{ action_url }}">
    {% if markdown_top %}
        <div class="markdown-body">{{ markdown_top|safe }}</div>
    {% endif %}
    
    {% for input_component in inputs %}
        <div class="mb-4">{{ input_component|safe }}</div>
    {% endfor %}

    {% if markdown_bottom %}
        <div class="markdown-body mb-2">{{ markdown_bottom|safe }}</div>
    {% endif %}
    
    <button type="submit" class="rounded bg-white px-2 py-1 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50">Submit</button>


    
    </form>
"""



class ComponentManager:
    def __init__(self, request):
        """
        Initialize the ComponentManager with a request object to handle input components.
        
        Args:
        - request (flask.Request): The current Flask request object.
        """
        self.request = request
        self.inputs = []
        self.form_groups = []   # list to store registered form groups
        self.outputs = []

    def register_input(self, input_component):
        """
        Register an input component, capture its value from the request, and append it to the inputs list.
        
        Args:
        - input_component (BaseInput): The input component to register.

        Returns:
        - BaseInput: The registered input component.
        """
        input_component.capture(self.request)
        self.inputs.append(input_component)
        return input_component
    
    def register_form_group(self, form_group):
        """
        Register a form group and append it to the form_groups list.
        
        Args:
        - form_group (FormGroupManager): The form group to register.

        Returns:
        - FormGroupManager: The registered form group.
        """
        self.form_groups.append(form_group)
        return form_group

    def render_inputs(self):
        """
        Render all the registered input components.
        
        Returns:
        - list: List of rendered input components.
        """
        return [input_component.render() for input_component in self.inputs]

    def register_output(self, output_component):
        """
        Register an output component and append it to the outputs list.
        
        Args:
        - output_component (BaseOutput): The output component to register.

        Returns:
        - BaseOutput: The registered output component.
        """
        self.outputs.append(output_component)
        return output_component
    
    def render_form_groups(self):
        rendered_form_groups = []
        for form_group in self.form_groups:
            inputs = [input_component.render() for input_component in form_group.inputs]
            rendered_form_group = render_template_string(
                FORM_GROUP_TEMPLATE, 
                action_url=form_group.action_url, 
                inputs=inputs,
                markdown_top=markdown(form_group.markdown_top),
                markdown_bottom=markdown(form_group.markdown_bottom)
            )
            rendered_form_groups.append(rendered_form_group)
        return rendered_form_groups
    
    def render_outputs(self):
        """
        Render all the registered output components.
        
        Returns:
        - list: List of rendered output components.
        """
        return [output_component.render() for output_component in self.outputs]
    



class FormGroup:
    def __init__(self, action_url='/', markdown_top=None, markdown_bottom=None):
        """
        :param action_url: URL to which the form data should be posted.
        :param markdown_top: Optional markdown content to be displayed at the top of the section.
        :param markdown_bottom: Optional markdown content to be displayed at the bottom of the section.
        """
        self.action_url = action_url
        self.inputs = []
        self.markdown_top = markdown_top
        self.markdown_bottom = markdown_bottom

    def add_input(self, input_component):
        print(f"Adding input: {input_component.name}")  # Debugging statement
        self.inputs.append(input_component)