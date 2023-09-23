import pandas as pd
import matplotlib.pyplot as plt

# Use a stylesheet for a modern look
plt.style.use('seaborn-whitegrid')

def process_data(df, input_values):
    hospital_name, bed_value, income_value = input_values

    if hospital_name and hospital_name != 'Select All':
        output_df = df[df['Hospital Name'] == hospital_name]
    else:
        output_df = df

    if bed_value and bed_value != 'Select All':
        if bed_value == 'hospital < 100':
            condition = output_df['Number of Beds'] < 100
        elif bed_value == '100 >= hospital < 300':
            condition = (output_df['Number of Beds'] >= 100) & (output_df['Number of Beds'] < 300)
        elif bed_value == 'hospital >= 300':
            condition = output_df['Number of Beds'] >= 300
        output_df = output_df[condition]

    if income_value and income_value != 'Select All':
        condition = output_df['Net Income'] > 0 if income_value == 'Positive' else output_df['Net Income'] < 0
        output_df = output_df[condition]


    ### create descriptive sum stats
    number_of_hospital = len(output_df)
    number_beds_sum = output_df['Number of Beds'].sum()
    total_outpatient_revenue = output_df['Outpatient Revenue'].sum()
    total_inpatient_revenue = output_df['Inpatient Revenue'].sum()
    total_medicaid_charges = output_df['Medicaid Charges'].sum()
    total_net_income = output_df['Net Income'].sum()
    median_net_income_num = df['Net Income'].median()

    ### calculate the percent of total for the selected hospital
    percent_of_total_beds = number_beds_sum / df['Number of Beds'].sum()
    percent_of_total_outpatient_revenue = total_outpatient_revenue / df['Outpatient Revenue'].sum()
    percent_of_total_inpatient_revenue = total_inpatient_revenue / df['Inpatient Revenue'].sum()
    percent_of_total_medicaid_charges = total_medicaid_charges / df['Medicaid Charges'].sum()
    percent_of_total_net_income = total_net_income / df['Net Income'].sum()
    percent_of_total_hospitals = number_of_hospital / len(df)

    ### create a new dataframe with the sum stats
    sum_stats = {
                'Percent of Total Beds': percent_of_total_beds,
                'Percent of Total Outpatient Revenue': percent_of_total_outpatient_revenue,
                'Percent of Total Inpatient Revenue': percent_of_total_inpatient_revenue,
                'Percent of Total Medicaid Charges': percent_of_total_medicaid_charges,
                'Percent of Total Net Income': percent_of_total_net_income,
                'Percent of Total Hospitals': percent_of_total_hospitals,
                }
    
    sum_stats_df = pd.DataFrame(sum_stats, index=[0])
    
    def main_barchart():
        fig, ax = plt.subplots(figsize=(10, 7))
        
        # Bar colors
        main_color = '#1f75fe'  # A modern blue
        highlight_color = '#ee204d'  # A modern orange
        
        ax.bar(df['Hospital Name'], df['Net Income'], color=main_color, alpha=0.7, label='All Hospitals')
        ax.bar(output_df['Hospital Name'], output_df['Net Income'], color=highlight_color, alpha=0.9, label='Selected Hospital')
        ## round and format the median net income, adding commas and dollar sign for median 
        ax.axhline(y=median_net_income_num, color='green', linestyle='--', label=f'Median: ${(median_net_income_num).round(2):,}')
        ## round and format the mean net income, adding commas and dollar sign for mean
        ax.axhline(y=df['Net Income'].mean(), color='red', linestyle='--', label=f'Mean: ${(df["Net Income"].mean()).round(2):,}')
        
        # Adjust the spines (borders)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        # Fonts and rotations for labels
        ax.set_xticklabels(df['Hospital Name'], rotation=80, ha='right', fontsize=10)
        ax.set_title('Hospital Net Income', fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Hospital Name', fontsize=14, labelpad=15)
        ax.set_ylabel('Net Income', fontsize=14, labelpad=15)

        # Set the y-axis scale to be in millions
        ax.set_yticklabels(['${:,.0f} million'.format(x) for x in ax.get_yticks()/1000000])

        # add in standard deviation to the plot
        ax.axhspan(df['Net Income'].mean() - df['Net Income'].std(), df['Net Income'].mean() + df['Net Income'].std(), alpha=0.2, color='yellow', label='Standard Deviation')

        # add standard deviation to the legend
        ax.legend(frameon=True, loc='upper right')
        
        plt.tight_layout()
        return fig

    fig1 = main_barchart()

    # def example_pie_chart():
    #     labels = output_df['Hospital Name'].tolist()
    #     sizes = output_df['Net Income'].tolist()
    #     total = sum(sizes)
    #     sizes = [size / total for size in sizes]
    #     sizes = [abs(size) for size in sizes]
    #     fig, ax = plt.subplots()
    #     ax.pie(sizes)
    #     ax.legend(labels, loc='upper left', bbox_to_anchor=(0.85, 0.5))
    #     plt.setp(ax.get_legend().get_texts(), fontsize='small')
    #     return fig  # Return the figure object
    
    # fig2 = example_pie_chart()

    
    output_table_formated = output_df.copy()
    columns_to_format = ['Net Income', 'Number of Beds', 'Outpatient Revenue', 'Inpatient Revenue', 'Medicaid Charges']
    for column in columns_to_format:
        output_table_formated[column] = output_table_formated[column].apply(lambda x: "{:,}".format(x).split('.')[0])

    return output_table_formated, sum_stats_df, fig1
