from flask import Flask, render_template_string, request

from flask_dashboard import get_template
from flask_dashboard.components.inputs import InputDropdown
from flask_dashboard.components.outputs import OutputText, OutputChart_Matplotlib, OutputTable_HTML, OutputImage, OutputMarkdown
from flask_dashboard.components.managers import ComponentManager, FormGroup

import pandas as pd

import matplotlib
matplotlib.use('Agg') # required for local development and g-shell
import matplotlib.pyplot as plt

from test_data_processing import process_data

app = Flask(__name__)

df = pd.read_csv('fake_data/ny_suffolk_nassau.csv')

@app.route('/', methods=['GET', 'POST'])
def index():

    # Step 1: Initialize the component manager for this request/endpoint
    manager = ComponentManager(request)

    # Step 2: Registering and capturing inputs for this request
    # We can separate these into distinct groups, so here is the first group: 
    hospital_form_group = FormGroup(action_url='/', markdown="""### Hospital Selection""", markdown_position='top')
    input2_dropdown = InputDropdown(name='hospital_selection', label='Select a hospital:', values=(df, 'Hospital Name'))
    hospital_form_group.add_input(input2_dropdown)
    manager.register_input(input2_dropdown)
    manager.register_form_group(hospital_form_group)

    # Step 2b: Lets now create a second group of inputs
    # This one will have a dropdown based on the Number of Beds, where we have a list of <100, or >100
    hospital_form_group2 = FormGroup(action_url='/', markdown="""### Hospital Bed Selection""", markdown_position='top')
    input2_dropdown2 = InputDropdown(name='bed_selection', label='Select a number of beds:', values=['<100', '>100'])
    hospital_form_group2.add_input(input2_dropdown2)
    manager.register_input(input2_dropdown2)
    manager.register_form_group(hospital_form_group2)

    # Step 2c: Lets create a dropdown that can filter if the net income is positive or negative
    hospital_form_group3 = FormGroup(action_url='/', markdown="""### Hospital Net Income Selection""", markdown_position='top')
    input2_dropdown3 = InputDropdown(name='net_income_selection', label='Select a net income:', values=['Positive', 'Negative'])
    hospital_form_group3.add_input(input2_dropdown3)
    manager.register_input(input2_dropdown3)
    manager.register_form_group(hospital_form_group3)
    
    ################################################################################################
    # Step 3: 
    ### Do the normal python processing stuff of your data: 
    output_df, plt = process_data(df, [input2_dropdown.value, input2_dropdown2.value, input2_dropdown3.value])
    ################################################################################################

    ################################################################################################
    # Step 4: Register output components to be rendered
    manager.register_output(OutputImage("https://www.stonybrook.edu/far-beyond/img/branding/logo/sbu/primary/300/stony-brook-university-logo-horizontal-300.png"))
    manager.register_output(OutputMarkdown("""---"""))
    manager.register_output(OutputChart_Matplotlib(plt))
    manager.register_output(OutputMarkdown("""### Hospital Financial Detail Data"""))
    manager.register_output(OutputTable_HTML(output_df.to_dict(orient='records')))
    manager.register_output(OutputMarkdown("""<br /> <br /> """))

    ################################################################################################

    # Step 5: Render the template with the inputs and outputs
    return render_template_string(
        get_template('base.html'),
        form_groups=manager.render_form_groups(), 
        output_components=manager.render_outputs()
    )

if __name__ == '__main__':
    app.run(debug=True)
