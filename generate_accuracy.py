import pandas as pd

# Load the data
final_output_df = pd.read_csv('final_output_table.csv')
validation_df = pd.read_csv('validation_set.csv')

# Prepare a dictionary from the validation set for easier access
validation_dict = {}
for _, row in validation_df.iterrows():
    key = (row['Group'], row['Case Number'])
    validation_dict[key] = [int(x) for x in row['Vulnerable Lines'].strip('[]').split(',') if x]

# Function to calculate accuracy
def calculate_accuracy(selected_lines, actual_vulnerable):
    if not actual_vulnerable:  # Handle cases with no vulnerabilities
        return 1.0 if not selected_lines else 0.0
    TP = len(set(selected_lines).intersection(actual_vulnerable))
    FP = len(set(selected_lines).difference(actual_vulnerable))
    FN = len(set(actual_vulnerable).difference(selected_lines))
    TN = len(actual_vulnerable) - TP  # Simplification, might need adjustment based on total lines
    return (TP + TN) / (TP + TN + FP + FN)

# Iterate over the final_output_df to calculate accuracy
results = []
for _, row in final_output_df.iterrows():
    group = row['Group']
    for case in range(1, 7):  # Assuming cases 1 to 6
        case_col = f'Case{case}_on_cols'
        if case_col in row:
            selected_lines = [int(x) for x in str(row[case_col]).split(', ') if x.isdigit()]
            actual_vulnerable = validation_dict.get((group, case), [])
            accuracy = calculate_accuracy(selected_lines, actual_vulnerable)
            results.append({'Participant': row['Participant'], 'Group': group, 'Case': case, 'Accuracy': accuracy})

# Convert results to DataFrame and save
results_df = pd.DataFrame(results)
results_df.to_csv('accuracy_results.csv', index=False)
print('Accuracy results saved to accuracy_results.csv.')
