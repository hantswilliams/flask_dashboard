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
    hospital_form_group = FormGroup(action_url='/', markdown_top="""### Hospital Selection""", markdown_bottom="""*Use this section to filter by a specific hospital.*""")
    input2_dropdown = InputDropdown(name='hospital_selection', label='Select a hospital:', values=(df, 'Hospital Name'))
    hospital_form_group.add_input(input2_dropdown)
    manager.register_input(input2_dropdown)
    manager.register_form_group(hospital_form_group)

    # Step 2b: Lets now create a second group of inputs
    # This one will have a dropdown based on the Number of Beds, where we have a list of <100, or >100
    hospital_form_group2 = FormGroup(action_url='/', markdown_top="""### Hospital Bed Selection""", markdown_bottom="""*Use this section to filter by a number of beds.*""")
    input2_dropdown2 = InputDropdown(name='bed_selection', label='Select a number of beds:', values=[
        'hospital < 100', 
        '100 >= hospital < 300', 
        'hospital >= 300'])
    hospital_form_group2.add_input(input2_dropdown2)
    manager.register_input(input2_dropdown2)
    manager.register_form_group(hospital_form_group2)

    # Step 2c: Lets create a dropdown that can filter if the net income is positive or negative
    hospital_form_group3 = FormGroup(action_url='/', markdown_top="""### Hospital Net Income Selection""", markdown_bottom="""*Use this section to filter by a net income.*""")
    input2_dropdown3 = InputDropdown(name='net_income_selection', label='Select a net income:', values=['Positive', 'Negative'])
    hospital_form_group3.add_input(input2_dropdown3)
    manager.register_input(input2_dropdown3)
    manager.register_form_group(hospital_form_group3)
    
    ################################################################################################
    # Step 3: 
    ### Do the normal python processing stuff of your data: 
    output_df, sum_stats_df, fig1 = process_data(df, [input2_dropdown.value, input2_dropdown2.value, input2_dropdown3.value])
    ################################################################################################

    ################################################################################################
    # Step 4: Register output components to be rendered
    manager.register_output(OutputMarkdown("""*Powered by [School of Health Professions - Applied Health Informatics](https://healthprofessions.stonybrookmedicine.edu/programs/ahi) at*"""))
    manager.register_output(OutputImage("https://www.stonybrook.edu/far-beyond/img/branding/logo/sbu/primary/300/stony-brook-university-logo-horizontal-300.png"))
    manager.register_output(OutputMarkdown("""---"""))
    manager.register_output(OutputMarkdown("""# Hospital Comparison: Suffolk and Nassau County Hospital Data by CMS 2019"""))
    manager.register_output(OutputMarkdown("""The following data originates from [data.cms.gov](https://data.cms.gov/provider-compliance/cost-report/hospital-provider-cost-report),
                                           and is a subset of the data for Suffolk and Nassau County. The data is from 2019 and is the most recent data available. 
                                           This data is gathered from the hospital annual cost report information maintained in the Healthcare Provider Cost 
                                           Reporting Information System (HCRIS). The data does not contain all measures reported in the HCRIS, but rather includes 
                                           a subset of commonly used measures."""))
    manager.register_output(OutputMarkdown("""In this example, we show how visualization can be a powerful tool when exploring data. The government provides a lot of data, 
                                           but it can be difficult to understand and interpret. By using visualization, we can quickly see the distribution of the data. Using 
                                           the dropdowns below, you can filter the data by hospital, number of beds, and net income. The bar chart will update to show the
                                           filtered data. The table below the chart will show the filtered data as well. The table can be sorted by clicking on the column headers."""))
    manager.register_output(OutputMarkdown("""Please be aware that this data is for 2019 (pre-covid). Since we focus on net income, it is calculated by: subtracting Total Other Expenses (G3-Line-28-Column-1) from 
                                           Total Income (G3-Line-26-Column-1) reported on the Statement of Revenues and Expenses (Worksheet-G-3).
                                           The complete data dictionary can be found [here](https://data.cms.gov/resources/hospital-provider-cost-report-data-dictionary)."""))
    manager.register_output(OutputMarkdown("""---"""))
    manager.register_output(OutputMarkdown("""### Hospital Financial Summary Data"""))
    manager.register_output(OutputMarkdown("""Filters Active: Hospital: **{input2_dropdown.value}** // Beds: **{input2_dropdown2.value}** // Net Income: **{input2_dropdown3.value}**""".format(input2_dropdown=input2_dropdown, input2_dropdown2=input2_dropdown2, input2_dropdown3=input2_dropdown3)))
    manager.register_output(OutputMarkdown("""---"""))
    manager.register_output(OutputChart_Matplotlib(fig1))
    manager.register_output(OutputMarkdown("""---"""))
    manager.register_output(OutputText(f"Percent of Total Beds in Suffolk + Nassau County: {(sum_stats_df['Percent of Total Beds'].values[0] * 100).round(2)}%"))
    manager.register_output(OutputText(f"Percent of Total Hospitals in Suffolk + Nassau County: {(sum_stats_df['Percent of Total Hospitals'].values[0] * 100).round(2)}%"))
    manager.register_output(OutputText(f"Percent of Total Outpatient Revenue in Suffolk + Nassau County: {(sum_stats_df['Percent of Total Outpatient Revenue'].values[0] * 100).round(2)}%"))
    manager.register_output(OutputText(f"Percent of Total Inpatient Revenue in Suffolk + Nassau County: {(sum_stats_df['Percent of Total Inpatient Revenue'].values[0] * 100).round(2)}%"))
    manager.register_output(OutputText(f"Percent of Total Medicaid Charges in Suffolk + Nassau County: {(sum_stats_df['Percent of Total Medicaid Charges'].values[0] * 100).round(2)}%"))
    manager.register_output(OutputText(f"Percent of Total Net Income in Suffolk + Nassau County: {(sum_stats_df['Percent of Total Net Income'].values[0] * 100).round(2)}%"))
    manager.register_output(OutputMarkdown("""---"""))
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
