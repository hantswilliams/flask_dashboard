import pandas as pd
import matplotlib.pyplot as plt

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

    ### create a new dataframe with the sum stats
    sum_stats = {
                'Percent of Total Beds': percent_of_total_beds,
                'Percent of Total Outpatient Revenue': percent_of_total_outpatient_revenue,
                'Percent of Total Inpatient Revenue': percent_of_total_inpatient_revenue,
                'Percent of Total Medicaid Charges': percent_of_total_medicaid_charges,
                'Percent of Total Net Income': percent_of_total_net_income
                }
    
    sum_stats_df = pd.DataFrame(sum_stats, index=[0])
    
    def main_barchart():
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.bar(df['Hospital Name'], df['Net Income'])
        ax.bar(output_df['Hospital Name'], output_df['Net Income'], color='red')
        ax.axhline(y=median_net_income_num, color='green', linestyle='--', label=f'Median: ${median_net_income_num}')
        ax.set_xticklabels(df['Hospital Name'], rotation=90)
        ax.set_title('Net Income')
        ax.set_xlabel('Hospital Name')
        ax.set_ylabel('Net Income')
        plt.tight_layout()
        return fig  # Return the figure object

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
