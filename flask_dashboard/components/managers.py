## Havn't added this in yet....for future use

class ComponentManager:
    def __init__(self, request):
        self.request = request
        self.inputs = []

    def register_input(self, input_component):
        input_component.capture(self.request)
        self.inputs.append(input_component)
        return input_component

    def render_inputs(self):
        return [input_component.render() for input_component in self.inputs]
