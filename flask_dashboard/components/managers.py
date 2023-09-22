## Havn't added this in yet....for future use

# components/managers.py

class ComponentManager:
    def __init__(self, request):
        """
        Initialize the ComponentManager with a request object to handle input components.
        
        Args:
        - request (flask.Request): The current Flask request object.
        """
        self.request = request
        self.inputs = []
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
    
    def render_outputs(self):
        """
        Render all the registered output components.
        
        Returns:
        - list: List of rendered output components.
        """
        return [output_component.render() for output_component in self.outputs]