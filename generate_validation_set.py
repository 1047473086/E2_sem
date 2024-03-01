import pandas as pd
# Mapping of scenarios to their actual vulnerable lines
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
vulnerable_lines_mapping = {
    '1': list(range(1, 15)),  # all lines are vulnerable
    '2': list(range(1, 25)), # all lines are vulnerable
    '3': [16, 18, 22, 26, 27],
    '4': [1, 18, 19, 20, 21, 22],
    '5': [],  # No vulnerable lines
    '6': [],  # No vulnerable lines
}

rows = []
for group, cases in group_case_beginnings.items():
    for case_num, case_info in cases.items():
        scenario_id = case_info.split(' ')[2]  # Extract scenario number
        # Use scenario_id to get the corresponding vulnerable lines list from the mapping
        vulnerable_lines = vulnerable_lines_mapping[scenario_id[1]]
        # Prepare row for DataFrame
        row = {
            'Group': group,
            'Case Number': case_num,
            'Scenario ID': scenario_id[0],
            'Vulnerable Lines': str(vulnerable_lines)  # Convert list to string for CSV representation
        }
        rows.append(row)

# Create DataFrame
df = pd.DataFrame(rows)

# Define CSV output path, adjust the path as needed for your environment
csv_output_path = 'validation_set.csv'

# Save DataFrame to CSV
df.to_csv(csv_output_path, index=False)

print(f'Updated mapping has been saved to {csv_output_path}')