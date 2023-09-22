from flask import Flask, render_template_string, request

from flask_dashboard import get_template
from flask_dashboard.components.inputs import InputDropdown
from flask_dashboard.components.outputs import OutputText, OutputChart_Matplotlib, OutputTable_HTML, OutputImage, OutputMarkdown
from flask_dashboard.components.managers import ComponentManager

import pandas as pd

import matplotlib
matplotlib.use('Agg') # required for local development and g-shell
import matplotlib.pyplot as plt

app = Flask(__name__)

df = pd.read_csv('fake_data/ny_suffolk_nassau.csv')

@app.route('/', methods=['GET', 'POST'])
def index():

    # Step 1: Initialize the component manager for this request/endpoint
    manager = ComponentManager(request)

    # Step 2: Registering and capturing inputs for this request
    # manager.register_input(TextInput('input_freetext', 'Free text input example:', default_value=''))
    input2_dropdown = manager.register_input(InputDropdown(name= 'hospital_selection', label = 'Select a hospital:', values = (df, 'Hospital Name'), action_url='/'))


















    ############### NORMAL PYTHON CODE GOES HERE FOR DATA MANIPULATION/CREATION ###############
    # Step 3: Do any additional processing of the data based on the inputs
    ## if a value is selected and it is not "Select All", filter the dataframe to only include the selected value
    if input2_dropdown.value and input2_dropdown.value != 'Select All':
        output_df = df[df['Hospital Name'] == input2_dropdown.value]
    else:
        output_df = df

    ## Calculate median net income for all hospitals
    avg_net_income_num = df['Net Income'].median()
    avg_net_income = "{:,}".format(avg_net_income_num).split('.')[0]

    ## Calculate difference between selected hospital and average net income
    if input2_dropdown.value:
        diff_net_income = output_df['Net Income'].values[0] - avg_net_income_num
        diff_net_income = "{:,}".format(diff_net_income).split('.')[0]
    else:
        diff_net_income = 0

    # Based on output_df, create a matplotlib chart, where the x-axis is the product and the y-axis is the cost, 
    # and the selected column [Product] is then highlighted in the chart with a different color
    plt.figure(figsize=(8, 6))
    plt.bar(df['Hospital Name'], df['Net Income'])
    plt.bar(output_df['Hospital Name'], output_df['Net Income'], color='red')
    plt.axhline(y=avg_net_income_num, color='green', linestyle='--', label=f'Median: ${avg_net_income}')
    plt.xticks(rotation=90)
    plt.title('Net Income')
    plt.xlabel('Hospital Name')
    plt.ylabel('Net Income')
    plt.tight_layout()

    ################################################################################################

















    # Step 4: Register output components to be rendered
    manager.register_output(OutputImage("https://www.stonybrook.edu/far-beyond/img/branding/logo/sbu/primary/300/stony-brook-university-logo-horizontal-300.png"))
    manager.register_output(OutputText(f"The median net income across these {len(df)} hospitals is {avg_net_income}."))
    manager.register_output(OutputText(f"The difference between the selected hospital ({input2_dropdown.value.lower()}) and the median net income across these {len(df)} hospitals is {diff_net_income}."))
    manager.register_output(OutputMarkdown("""---"""))
    manager.register_output(OutputChart_Matplotlib(plt))
    manager.register_output(OutputMarkdown("""### Hospital Financial Detail Data"""))
    manager.register_output(OutputTable_HTML(output_df.to_dict(orient='records')))


    # Step 5: Render the template with the inputs and outputs
    return render_template_string(
        get_template('base.html'), # select a template that you want to render for this request page
        input_components=manager.render_inputs(), 
        output_components=manager.render_outputs()
    )

if __name__ == '__main__':
    app.run(debug=True)
