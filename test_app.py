from flask import Flask, render_template_string, request
from faker import Faker
import pandas as pd

from flask_dashboard import get_template
from flask_dashboard.components.inputs import InputDropdown, TextInput
from flask_dashboard.components.outputs import OutputText, OutputTable, OutputImage


fake = Faker()
product_list = ['Apple', 'Banana', 'Cherry', 'Date', 'Fig', 'Grape']
category_list = ['Fruit', 'Vegetable', 'Dairy', 'Meat', 'Beverage', 'Snack']
df = pd.DataFrame({
    'Product': [fake.word(ext_word_list=product_list) for _ in range(100)],
    'Category': [fake.word(ext_word_list=category_list) for _ in range(100)],
    'Costs': [fake.pydecimal(left_digits=2, right_digits=2, positive=True) for _ in range(100)],
})


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():


    ##########################################################################################################################
    ##########################################################################################################################
    ### Example 1: Simple text input: you need to create one variable for the component and one variable to capture the input
    input1_text = TextInput('user_name', 'Enter your name please...').render()
    input1_text_capture = request.form.get('user_name', '')

    ### Example 2: Dropdown input: you need to create one variable for the component and one variable to capture the input
    input2_dropdown_capture = request.form.get('product_selection', '')
    intput2_dropdown = InputDropdown('product_selection', 'Select a product:', (df, 'Product'), action_url='/', selected_value=input2_dropdown_capture).render()

    ### Example 3: Dropdown input: you need to create one variable for the component and one variable to capture the input
    input3_dropdown_capture = request.form.get('color_choice', 'Red')
    input3_dropdown = InputDropdown('color_choice', 'Select a color:', ['Red', 'Green', 'Yellow'], action_url='/', selected_value=input3_dropdown_capture).render()

    ## Client-side rendering
    ## Input components
    input_components = [
        input1_text,
        intput2_dropdown,
        input3_dropdown
    ]
    ##########################################################################################################################
    ##########################################################################################################################




    ##########################################################################################################################
    #############################################################
    ## Server-side processing
    # Process the form data to produce the output
    if input2_dropdown_capture:
        output_df = df[df['Product'] == input2_dropdown_capture]
    else:
        output_df = df
    #############################################################

    ## Output components
    output_components = [
        OutputText(f"The name that you entered is: {input1_text_capture}").render(),
        OutputText(f"The color that you selected is: {input3_dropdown_capture}").render(),
        OutputTable(output_df.to_dict(orient='records')).render(),
        OutputImage("https://via.placeholder.com/150").render()
    ]

    ## Choose a template type that you want to use: 
    template_content = get_template('base.html')
    #############################################################
    ##########################################################################################################################


    ## Render the template along with the components
    return render_template_string(
                    template_content, 
                    input_components=input_components, 
                    output_components=output_components)

if __name__ == '__main__':
    app.run(debug=True)
