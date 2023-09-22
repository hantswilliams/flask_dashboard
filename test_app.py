from flask import Flask, render_template_string, request

from flask_dashboard import get_template
from flask_dashboard.components.inputs import InputDropdown
from flask_dashboard.components.outputs import OutputText, OutputChart_Matplotlib, OutputTable_HTML, OutputImage, OutputMarkdown
from flask_dashboard.components.managers import ComponentManager, FormGroup

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
    # We can separate these into distinct groups, so here is the first group: 
    hospital_form_group = FormGroup(action_url='/')
    input2_dropdown = InputDropdown(name='hospital_selection', label='Select a hospital:', values=(df, 'Hospital Name'))
    hospital_form_group.add_input(input2_dropdown)
    manager.register_input(input2_dropdown)
    manager.register_form_group(hospital_form_group)

    # Step 2b: Lets now create a second group of inputs
    # This one will have a dropdown based on the Number of Beds, where we have a list of <100, or >100
    hospital_form_group2 = FormGroup(action_url='/')
    input2_dropdown2 = InputDropdown(name='bed_selection', label='Select a number of beds:', values=['<100', '>100'])
    hospital_form_group2.add_input(input2_dropdown2)
    manager.register_input(input2_dropdown2)
    manager.register_form_group(hospital_form_group2)

    # Step 2b: Lets create a dropdown that can filter if the net income is positive or negative
    hospital_form_group3 = FormGroup(action_url='/')
    input2_dropdown3 = InputDropdown(name='net_income_selection', label='Select a net income:', values=['Positive', 'Negative'])
    hospital_form_group3.add_input(input2_dropdown3)
    manager.register_input(input2_dropdown3)
    manager.register_form_group(hospital_form_group3)
    
    
    
    

    
    
    
    

    
    
    
    

    
    ############### NORMAL PYTHON CODE GOES HERE FOR DATA MANIPULATION/CREATION ###############
    # Step 3: Do any additional processing of the data based on the inputs
    ## if a value is selected and it is not "Select All", filter the dataframe to only include the selected value

    if input2_dropdown.value and input2_dropdown.value != 'Select All':
        output_df = df[df['Hospital Name'] == input2_dropdown.value]
    else:
        output_df = df

    if input2_dropdown2.value and input2_dropdown2.value != 'Select All':
        if input2_dropdown2.value == '<100':
            output_df = output_df[output_df['Number of Beds'] < 100]
        else:
            output_df = output_df[output_df['Number of Beds'] > 100]
    
    if input2_dropdown3.value and input2_dropdown3.value != 'Select All':
        if input2_dropdown3.value == 'Positive':
            output_df = output_df[output_df['Net Income'] > 0]
        else:
            output_df = output_df[output_df['Net Income'] < 0]


    ## Calculate median net income for all hospitals
    df_median = df.copy()
    avg_net_income_num = df_median['Net Income'].median()
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

    ## Modify the output_df to include commas in the numbers: Number of Beds, Outpatient Revenue, Inpatient Revenue, Net Income, Medicaid Charges
    output_df['Net Income'] = output_df['Net Income'].apply(lambda x: "{:,}".format(x).split('.')[0])
    output_df['Number of Beds'] = output_df['Number of Beds'].apply(lambda x: "{:,}".format(x).split('.')[0])
    output_df['Outpatient Revenue'] = output_df['Outpatient Revenue'].apply(lambda x: "{:,}".format(x).split('.')[0])
    output_df['Inpatient Revenue'] = output_df['Inpatient Revenue'].apply(lambda x: "{:,}".format(x).split('.')[0])
    output_df['Medicaid Charges'] = output_df['Medicaid Charges'].apply(lambda x: "{:,}".format(x).split('.')[0])

    ################################################################################################

    
    
    

    
    
    
    

    
    
    
    

    
    ################################################################################################
    # Step 4: Register output components to be rendered
    manager.register_output(OutputImage("https://www.stonybrook.edu/far-beyond/img/branding/logo/sbu/primary/300/stony-brook-university-logo-horizontal-300.png"))
    manager.register_output(OutputText(f"The median net income across these {len(df)} hospitals is {avg_net_income}."))
    manager.register_output(OutputText(f"The difference between the selected hospital ({input2_dropdown.value.lower()}) and the median net income across these {len(df)} hospitals is {diff_net_income}."))
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
