import pandas as pd

# Define the Excel file path
file_path = '1.xlsx'  # Make sure to update this with the correct file path

# Define the sheet names for groups A to C (extend this list for more groups as needed)
sheet_names = ['A', 'B', 'C', 'D', 'E', 'F']

# Define a dictionary to hold the case beginnings for each group
group_case_beginnings = {
    'A': {
        1: "GroupA Case1 L1 Q2_",
        2: "GroupA Case2 C2 Q2_",
        3: "GroupA Case3 C5 Q2_",
        4: "GroupA Case4 C6 Q2_",
        5: "GroupA Case5 C3 Q2_", 
        6: "GroupA Case6 L4 Q2_",
    },
    'B': {
        1: "GroupB Case1 L2 Q2_",
        2: "GroupB Case2 C5 Q2_",
        3: "GroupB Case3 C1 Q2_",
        4: "GroupB Case4 C4 Q2_",
        5: "GroupB Case5 L6 Q2_",
        6: "GroupB Case6 L3 Q2_",
    },
    'C': { 
        1: "GroupC Case1 L5 Q2_",
        2: "GroupC Case2 L1 Q2_",
        3: "GroupC Case3 C2 Q2_",
        4: "GroupC Case4 C3 Q2_",
        5: "GroupC Case5 L4 Q2_",
        6: "GroupC Case6 C6 Q2_",
    },
    'D': {
        1: "GroupD Case1 C6 Q2_",
        2: "GroupD Case2 C4 Q2_",
        3: "GroupD Case3 L3 Q2_",
        4: "GroupD Case4 L2 Q2_",
        5: "GroupD Case5 C1 Q2_",
        6: "GroupD Case6 L5 Q2_",
    },
    'E': { 
        1: "GroupE Case1 C3 Q2_",
        2: "GroupE Case2 L6 Q2_",
        3: "GroupE Case3 L4 Q2_",
        4: "GroupE Case4 L1 Q2_",
        5: "GroupE Case5 C5 Q2_",
        6: "GroupE Case6 C2 Q2_",
    },
    'F': {
        1: "GroupF Case1 C4 Q2_",
        2: "GroupF Case2 L3 Q2_",
        3: "GroupF Case3 L6 Q2_",
        4: "GroupF Case4 L5 Q2_",
        5: "GroupF Case5 L2 Q2_",
        6: "GroupF Case6 C1 Q2_",
    },
}

# Initialize an empty DataFrame to store aggregated results from all groups
all_groups_data = pd.DataFrame()

# Process data for each group
for sheet_name in sheet_names:
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    case_beginnings = group_case_beginnings.get(sheet_name, {})

    # Initialize an empty DataFrame for this group
    group_data = pd.DataFrame()

    # Process data for each case using the specific case beginnings for the current group
    for case_number, beginning_string in case_beginnings.items():
        relevant_columns = [col for col in df.columns if col.startswith(beginning_string)]
        confidence_column = f"{beginning_string[:-1]}.1_1"  # Updated to fetch confidence level
        time_start_column = f"{beginning_string[:-7]} Timing1_First Click"
        time_end_column = f"{beginning_string[:-7]} Timing1_Last Click"
        # print(time_start_column)  
        case_data = df[relevant_columns + [confidence_column] + [time_start_column] + [time_end_column]]  # Include confidence column in the case data
        # print(confidence_column)
        # Simplify the column names
        simplified_columns = {col: f"{i+1}" for i, col in enumerate(relevant_columns)}
        case_data = case_data.rename(columns=simplified_columns)

        # Identify the exact columns marked as "On" and "Off" for each participant in this case
        for i in range(1, case_data.shape[0]):  # Assuming first row is header/description
            on_columns = [col for col, value in case_data.iloc[i].items() if value == "On"]
            off_columns = [col for col, value in case_data.iloc[i].items() if value == "Off"]
            confidence_level = df.loc[i, confidence_column]
            time_start = df.loc[i, time_start_column]
            time_end = df.loc[i, time_end_column]
            duration = df.loc[i, time_end_column] - df.loc[i, time_start_column]

            # Storing the column numbers as a string
            group_data.loc[i, f'Case{case_number}_on_cols'] = ', '.join(on_columns)
            group_data.loc[i, f'Case{case_number}_off_cols'] = ', '.join(off_columns)
            group_data.loc[i, f'Case{case_number}_confidence'] = confidence_level
            group_data.loc[i, f'Case{case_number}_duration'] = duration
            # group_data.loc[i, f'Case{case_number}_time_start'] = time_start
            # group_data.loc[i, f'Case{case_number}_time_end'] = time_end
    # Add a column to distinguish the group
    group_data['Group'] = sheet_name
    group_data['C++'] = df["Q5_1"]
    group_data['Vul'] = df["Q8_1"]

    # Append the group's data to the all_groups_data DataFrame
    all_groups_data = pd.concat([all_groups_data, group_data], ignore_index=True)

# Reset index to represent participant IDs more clearly
all_groups_data.index.name = 'Participant'
all_groups_data.reset_index(inplace=True)
all_groups_data['Participant'] = all_groups_data['Participant'].apply(lambda x: f'Participant {x}')

# Save the all_groups_data DataFrame to a CSV file
csv_output_path = 'final_output_table.csv'  # Define your desired output file path
all_groups_data.to_csv(csv_output_path, index=False)

print(f'The output table has been saved to {csv_output_path}')
