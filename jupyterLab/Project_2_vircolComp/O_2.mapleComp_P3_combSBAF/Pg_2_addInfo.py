## bsub -M 2000 -e /nfs/research/goldman/zihao/code/EBI_INTER/Project_2_vircolComp/2.mapleComp_P3/errorChecking.txt -o /nfs/research/goldman/zihao/code/EBI_INTER/Project_2_vircolComp/2.mapleComp_P3/outputChecking.txt 'python3 /nfs/research/goldman/zihao/code/EBI_INTER/Project_2_vircolComp/2.mapleComp_P3/Pg_2_addInfo.py'

import pandas as pd
# import plotly.graph_objects as go
import os

##########################################
# 1.Import and handle with the data
##########################################
Folder_col = "/nfs/research/goldman/zihao/N_compProject_2_P3/Folder_mapleComp_p3/COL_output_modified.txt"
Folder_vir = "/nfs/research/goldman/zihao/N_compProject_2_P3/Folder_mapleComp_p3/VIR_output_modified.txt"

df_col = pd.read_csv(Folder_col, sep='\t')
df_vir = pd.read_csv(Folder_vir, sep='\t')

df_vir['VIR'] = 1
df_col['COL'] = 1
merged_df = pd.merge(df_vir, df_col, on=['ID','Position'], how='outer')
df_filled = merged_df.fillna(0)
df_filled = df_filled[0:10] ### TEST
# print(df_filled.head())

##########################################
# 3.add info_COV_ANNOT
##########################################


# Set to keep track of IDs for which data is not found
missing_ids = set()

# Function to find values based on ID and Position
def find_values(ID, Position, file_path_template, columns, pos_col_name):
    # Generate file path based on ID
    file_path = file_path_template.format(id=ID)
    # Check if file exists
    if not os.path.exists(file_path):
        missing_ids.add(ID)
        return [None for _ in columns], False
    # Read file
    df = pd.read_csv(file_path, delimiter="\t") 
    # Find data based on Position
    df_matched = df[df[pos_col_name] == Position]
    if df_matched.empty:
        missing_ids.add(ID)
        return [None for _ in columns], False
    else:
        return df_matched.iloc[0][columns].tolist(), True

# Iterate over each row in df_filled to find corresponding data in df_cov_path and df_ann_path
for idx, row in df_filled.iterrows():
    ID = row["ID"]
    Position = row["Position"]
    # Find corresponding data in df_cov_path
    df_filled.loc[idx, "RATIO"], _ = find_values(ID, Position, "/nfs/research/goldman/zihao/Datas/p1/File_5_coverage/Decompress/{id}_coverage.txt", ["RATIO"], "Position")
    # Find corresponding data in df_ann_path
    df_filled.loc[idx, ["AF", "SB"]], _ = find_values(ID, Position, "/nfs/research/goldman/zihao/Datas/p1/File_5_annot/New_Decompress/{id}_annot.txt", ["AF", "SB"], "POS")

File_addInfo = "/nfs/research/goldman/zihao/Datas/p2_compViridian_P3/Folder_addInfo/output_addInfo.txt"
df_filled.to_csv(File_addInfo, sep="\t", index=False)
print("The file after adding the information is saved at: ", File_addInfo)

# Print count of missing IDs
print(f"Number of missing IDs: {len(missing_ids)}")

# Save missing IDs to txt file
missing_ids_path = "/nfs/research/goldman/zihao/Datas/p2_compViridian_P3/Folder_addInfo/missing_ids.txt"
with open(missing_ids_path, "w") as f:
    for ID in missing_ids:
        f.write(f"{ID}\n")

# Print path of txt file where missing IDs are saved
print(f"Missing IDs saved at: {os.path.abspath(missing_ids_path)}")

"""
##########################################
# 2.Count
##########################################
vir = df_filled['VIR'].value_counts()[1]
col = df_filled['COL'].value_counts()[1]
both = ((df_filled['VIR'] == 1) & (df_filled['COL'] == 1)).sum()
print('Only Viridian wrong: ', vir)
print('Only Colman\'s assembly wrong: ', col)
print('Both wrong: ', both)
##########################################
# 3.Plot
##########################################

## Define the data
labels = ['Only Viridian wrong', 'Only Colman\'s assembly wrong', 'Both wrong']
values = [vir, col, both]
bubble_sizes = [vir/5000, col/5000, both/5000]

## Create the bubble chart
fig = go.Figure(data=[go.Scatter(
    x=labels,
    y=values,
    mode='markers',
    marker=dict(
        size=bubble_sizes,
        sizemode='diameter',
        sizeref=0.1,
        color=bubble_sizes,
        colorscale='Viridis',
        showscale=True
    )
)])

## Add axis labels and title
fig.update_layout(
    xaxis_title='Category',
    yaxis_title='Count',
    title='Null now'
)

fig.show()
"""