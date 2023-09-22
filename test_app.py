from flask import Flask, render_template_string, request

from flask_dashboard import get_template
from flask_dashboard.components.inputs import InputDropdown, TextInput
from flask_dashboard.components.outputs import OutputText, OutputChart_Matplotlib, OutputTable_HTML, OutputImage
from flask_dashboard.components.managers import ComponentManager

from fake_data.fake_df import fake_df as df

import matplotlib
matplotlib.use('Agg') # required for local development and g-shell
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():

    # Step 1: Initialize the component manager for this request/endpoint
    manager = ComponentManager(request)

    # Step 2: Registering and capturing inputs for this request
    manager.register_input(TextInput('input_freetext', 'Free text input example:', default_value=''))
    input2_dropdown = manager.register_input(InputDropdown(name= 'product_selection', label = 'Select a product:', values = (df, 'Product'), action_url='/'))
    input3_dropdown = manager.register_input(InputDropdown(name = 'descriptive_statistic', label = 'Select a statistic:', values = ['Mean', 'Median', 'Mode']))







    ############### NORMAL PYTHON CODE GOES HERE FOR DATA MANIPULATION/CREATION ###############
    # Step 3: Do any additional processing of the data based on the inputs
    if input2_dropdown.value:
        output_df = df[df['Product'] == input2_dropdown.value]
    else:
        output_df = df

    # Based on the selected column [Product], calculate the mean, median, or mode of the selected column [Costs]
    if input3_dropdown.value == 'Mean':
        stat_output = output_df.groupby('Product').mean().reset_index()
    elif input3_dropdown.value == 'Median':
        stat_output = output_df.groupby('Product').median().reset_index()
    elif input3_dropdown.value == 'Mode':
        stat_output = output_df.groupby('Product').agg(lambda x:x.value_counts().index[0]).reset_index()

    # Based on output_df, create a matplotlib chart, where the x-axis is the product and the y-axis is the cost, 
    # and the selected column [Product] is then highlighted in the chart with a different color
    plt.figure(figsize=(8, 6))
    plt.bar(df['Product'], df['Costs'])
    plt.bar(output_df['Product'], output_df['Costs'], color='red')
    plt.xticks(rotation=45)
    plt.title('Product Cost')
    plt.xlabel('Product')
    plt.ylabel('Cost')
    plt.tight_layout()

    ################################################################################################








    # Step 4: Register output components to be rendered
    manager.register_output(OutputImage("https://www.stonybrook.edu/far-beyond/img/branding/logo/sbu/primary/300/stony-brook-university-logo-horizontal-300.png"))
    manager.register_output(OutputChart_Matplotlib(plt))
    manager.register_output(OutputText(f"The type of descriptive statistic selected: {input3_dropdown.value}, and the product selected: {input2_dropdown.value}. The {input3_dropdown.value} of the {input2_dropdown.value} is {stat_output['Costs'].values[0]}"))
    manager.register_output(OutputTable_HTML(output_df.to_dict(orient='records')))


    # Step 5: Render the template with the inputs and outputs
    return render_template_string(
        get_template('base.html'), # select a template that you want to render for this request page
        input_components=manager.render_inputs(), 
        output_components=manager.render_outputs()
    )

if __name__ == '__main__':
    app.run(debug=True)
