import pandas as pd

# Load the data from the CSV file
file_path = 'final_output_table.csv'
df = pd.read_csv(file_path)

# Initialize the new DataFrame with the desired structure
final_df = pd.DataFrame(columns=['SID', 'Group', 'Scenario', 'C++', 'Vul', 'Accuracy', 'Time', 'Confidence'])

# Populate the new DataFrame
for i in range(len(df)):
    for case_num in range(1, 7):  
        new_row = {
            'SID': i + 1,
            'Group': '',  # Blank as per instruction
            'Scenario': '',  # Blank as per instruction
            'C++': df.loc[i, 'C++'],  # The data from the "C++" column
            'Vul': df.loc[i, 'Vul'],  # The data from the "Vul" column
            'Accuracy': '',  # Blank as per instruction
            'Time': df.loc[i, f'Case{case_num}_duration'],  # Duration for each case
            'Confidence': df.loc[i, f'Case{case_num}_confidence']  # Confidence for each case
        }
        final_df = final_df._append(new_row, ignore_index=True)

# Now final_df has the required format with 25*6 rows
# If you need to save this DataFrame to a new CSV file:
final_df.to_csv('transformed_final_table.csv', index=False)
