import pandas as pd
import matplotlib.pyplot as plt

def process_data(df, input_values):
    hospital_name, bed_value, income_value = input_values

    if hospital_name and hospital_name != 'Select All':
        output_df = df[df['Hospital Name'] == hospital_name]
    else:
        output_df = df

    if bed_value and bed_value != 'Select All':
        condition = output_df['Number of Beds'] < 100 if bed_value == '<100' else output_df['Number of Beds'] > 100
        output_df = output_df[condition]

    if income_value and income_value != 'Select All':
        condition = output_df['Net Income'] > 0 if income_value == 'Positive' else output_df['Net Income'] < 0
        output_df = output_df[condition]

    avg_net_income_num = df['Net Income'].median()
    avg_net_income = "{:,}".format(avg_net_income_num).split('.')[0]

    diff_net_income = output_df['Net Income'].values[0] - avg_net_income_num if hospital_name else 0
    diff_net_income = "{:,}".format(diff_net_income).split('.')[0]

    plt.figure(figsize=(8, 6))
    plt.bar(df['Hospital Name'], df['Net Income'])
    plt.bar(output_df['Hospital Name'], output_df['Net Income'], color='red')
    plt.axhline(y=avg_net_income_num, color='green', linestyle='--', label=f'Median: ${avg_net_income}')
    plt.xticks(rotation=90)
    plt.title('Net Income')
    plt.xlabel('Hospital Name')
    plt.ylabel('Net Income')
    plt.tight_layout()

    columns_to_format = ['Net Income', 'Number of Beds', 'Outpatient Revenue', 'Inpatient Revenue', 'Medicaid Charges']
    for column in columns_to_format:
        output_df[column] = output_df[column].apply(lambda x: "{:,}".format(x).split('.')[0])

    return output_df, avg_net_income, diff_net_income, plt
