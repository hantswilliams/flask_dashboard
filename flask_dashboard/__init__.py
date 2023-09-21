def get_template(template_name):
    with open(f'flask_dashboard/templates/{template_name}', 'r') as file:
        return file.read()
