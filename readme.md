# Flask Dashboard

*About*: Inspired by Shiny and Streamlit, a flask focused python library to help assist with fast dashboarding. While Streamlit and Shiny are highly opinioned, this approach brings the dashboarding functionality (limited right now) to your flask environment, allowing you the freedom to further create and curate the application as you please. 

---

## Component Manager

The heart of the flask dashboarding library lies in the `ComponentManager`. It serves as a central coordinator for managing both input and output components, ensuring that everything is orchestrated in a seamless manner. Let's dive deeper:

### Role of the Component Manager:

1. **Managing State**: The `ComponentManager` retains the state of all registered components. This allows for the preservation of user inputs, even between page refreshes, enhancing the user experience.

2. **Input Handling**: Every input, whether it be a dropdown, textbox, or a slider, is registered and managed by the `ComponentManager`. This registration aids in the collection of user input data, making it straightforward to access and process.

3. **Output Rendering**: After processing the data, you can register output components that dictate how the processed data should be displayed. Whether you want to show a graph, a table, or just some text, the `ComponentManager` can handle it. It ensures that the outputs are rendered in the order they're registered.

4. **HTML Integration**: Instead of manually curating HTML templates, the `ComponentManager` integrates with pre-defined templates. The registered input and output components are automatically injected into these templates, allowing for a dynamic and adaptive UI experience.

### How to Use the Component Manager:

It's quite simple. At the beginning of your endpoint function:

1. **Initialization**: Start by initializing the `ComponentManager` with the current request.

    ```python
    manager = ComponentManager(request)
    ```

2. **Input Registration**: Create your inputs, encapsulate them into `FormGroups` if necessary, and then register these inputs with the manager.

    ```python
    input2_dropdown = InputDropdown(name='hospital_selection', label='Select a hospital:', values=(df, 'Hospital Name'))
    manager.register_input(input2_dropdown)
    ```

3. **Output Registration**: After processing your data, decide how you want to display it. Create output components and register them with the manager.

    ```python
    manager.register_output(OutputText(f"The median net income is {avg_net_income}."))
    ```

4. **Rendering**: Finally, use the manager's rendering methods to get the HTML representation of the components and inject them into your chosen template.

    ```python
    return render_template_string(
        get_template('base.html'),
        form_groups=manager.render_form_groups(), 
        output_components=manager.render_outputs()
    )
    ```

By using the `ComponentManager`, you can ensure a structured and streamlined approach to dashboarding, all while retaining the flexibility and customizability that Flask offers.

---

# Installation and Walk-through

## Installation 

```bash
pip install ???_flask_dashboard_???
```

## How to: 

1. **LOAD LIBRARY**: First load in the library at the top of you app file. In a basic example, it might look like this:
```python
from flask_dashboard import get_template
from flask_dashboard.components.inputs import InputDropdown
from flask_dashboard.components.outputs import OutputText, OutputChart_Matplotlib, OutputTable_HTML, OutputImage, OutputMarkdown
from flask_dashboard.components.managers import ComponentManager, FormGroup
```

2. **INPUT SECTION**: Create a `FormGroup`. The idea here is that you might want to have multiple sets of filters, that are nested together within a form, all within a single page. If you are familiar with HTML, think about having multiple forms on a single HTML page. In order to achieve this, we have the concept of a `FormGroup`, that can be composed of multiple inputs. In the below example, we are creating a form group with a single input field:

```python
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
```

3. **SERVER SECTION**: Based on the form input, we then do some *normal* python coding, based on the received inputs from the form(s). The rest of thie code is from `test_data_processing.py` file if you want to see what manipulations are happening:

```python
    output_df, avg_net_income, diff_net_income, plt = process_data(df, [input2_dropdown.value, 
                                                                        input2_dropdown2.value, input2_dropdown3.value])
```

4. **OUTPUT SECTION**: In a attempt to again reduce, or completely remove the need to do any HTML/CSS/Javascript, we have wrapped up specific types of *output components* so you do not need to worry about rendering or dealing with HTML. This is heavily inspired by what I see in Streamlit:

In the below example, you register specific output components, like `OutputMark` or `OutputTable_HTML`, based on what you then want to present to the user on that specific page (endpoint). 

```python
    manager.register_output(OutputImage("https://www.stonybrook.edu/far-beyond/img/branding/logo/sbu/primary/300/stony-brook-university-logo-horizontal-300.png"))
    manager.register_output(OutputText(f"The median net income across these {len(df)} hospitals is {avg_net_income}."))
    manager.register_output(OutputText(f"The difference between the selected hospital ({input2_dropdown.value.lower()}) and the median net income across these {len(df)} hospitals is {diff_net_income}."))
    manager.register_output(OutputMarkdown("""---"""))
    manager.register_output(OutputChart_Matplotlib(plt))
    manager.register_output(OutputMarkdown("""### Hospital Financial Detail Data"""))
    manager.register_output(OutputTable_HTML(output_df.to_dict(orient='records')))
    manager.register_output(OutputMarkdown("""<br /> <br /> """))
```

Finally, after this step, you then being together all of the inputs and outputs, and select a specific template. Right now in the module, there is only a `base.html`` template, but in the future, I will add in more that the user can choose between. 

```python
    return render_template_string(
        get_template('base.html'),
        form_groups=manager.render_form_groups(), 
        output_components=manager.render_outputs()
    )
```

----


## To do: 
- [x] Add initial input components
- [x] Add initial output components
- [x] Create at least one basic .html template for the dashboard view 
- [ ] Incorporate statement system 
- [ ] Incorporate loggin 
- [ ] Incorporate user login / RBAC 