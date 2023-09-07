import pandas as pd
import os

def combine_assemblies(folder_col, folder_vir, folder_data, output_dir, not_found_ids_file):

    # 1.Combine the Colman's Assembly and Viridian Assembly
    df_col = pd.read_csv(folder_col, sep='\t')
    df_vir = pd.read_csv(folder_vir, sep='\t')

    df_vir['VIR'] = 1
    df_col['COL'] = 1
    merged_df = pd.merge(df_vir, df_col, on=['ID','Position'], how='outer')
    df_filled = merged_df.fillna(0)

    df_filled['COL'] = pd.to_numeric(df_filled['COL'], errors='coerce').astype(int)
    df_filled['VIR'] = pd.to_numeric(df_filled['VIR'], errors='coerce').astype(int)

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Store not found IDs
    not_found_ids = []

    for index, row in df_filled.iterrows():
        file_path = f'{folder_data}/{row["ID"]}.txt'
        if os.path.exists(file_path):
            df = pd.read_csv(file_path, sep='\t')[['position', 'nucleotide_martin', 'nucleotide_origin', 'label_mar', 'label_ori']]
            if row['Position'] in df['position'].values:
                df.loc[df['position'] == row['Position'], 'VIR'] = row['VIR']
                df.loc[df['position'] == row['Position'], 'COL'] = row['COL']
                df.to_csv(os.path.join(output_dir, f'{row["ID"]}.txt'), index=False, sep='\t')
            else:
                not_found_ids.append(row["ID"])
        else:
            not_found_ids.append(row["ID"])

    # Check if parent folder of not_found_ids_file exists and create if it does not
    if not os.path.exists(os.path.dirname(not_found_ids_file)):
        os.makedirs(os.path.dirname(not_found_ids_file))

    # Save not found IDs to a file
    with open(not_found_ids_file, 'w') as f:
        for item in not_found_ids:
            f.write("%s\n" % item)

    # Print the location of not_found_ids_file
    print(f"The not found IDs file has been saved to: {not_found_ids_file}")

    # Print the number of not found IDs
    print(f"The number of not found IDs: {len(not_found_ids)}")

    # Iterate over all files in the folder_data directory
    for filename in os.listdir(folder_data):
        file_id = filename.split('.')[0]  # Get the ID from the filename
        if file_id not in df_filled['ID'].values:  # If ID is not in df_filled
            df = pd.read_csv(f'{folder_data}/{filename}', sep='\t')
            df['COL'] = np.nan  # Add 'COL' column with NaN
            df['VIR'] = np.nan  # Add 'VIR' column with NaN
            df.to_csv(os.path.join(output_dir, filename), index=False, sep='\t')  # Save to output_dir

folder_col = '/nfs/research/goldman/zihao/Datas/p2_compViridian_P3/Folder_mapleOutput/COL_output_modified.txt'
folder_vir = '/nfs/research/goldman/zihao/Datas/p2_compViridian_P3/Folder_mapleOutput/VIR_output_modified.txt'
folder_data = '/nfs/research/goldman/zihao/Datas/p2_compViridian_P2/Folder_2_combination/folderData_combination'
output_dir = '/nfs/research/goldman/zihao/Datas/p2_compViridian_P3/folderData_addError'
not_found_ids_file = '/nfs/research/goldman/zihao/Datas/p2_compViridian_P3/notFound_idsError.txt'

combine_assemblies(folder_col, folder_vir, folder_data, output_dir, not_found_ids_file)