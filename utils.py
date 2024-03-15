import numpy as np
import pandas as pd
import os
from tabulate import tabulate

def parse_pipeline_results(text):
    results = []
    branches = set()
    dataset = None
    for line in text.split("\n"):
        if line.startswith("ML") or line.startswith("Project name"):
            continue
        elif any(list(map(line.startswith, ["ALL", "TEST", "TRAIN", "VALIDATE"]))):
            dataset = line.split()[0].capitalize()
        else:
            splits = line.split("\t")
            if len(splits) > 1:
                project = splits[0].split("...")[0]
                branch = splits[0].split("...")[1]
                greatness = float(splits[1].replace("%", ""))

                if (
                    len(results)
                    and results[-1]["project"] == project
                    and results[-1]["dataset"] == dataset
                ):
                    results[-1].update({f"{branch}/greatness": greatness})
                else:
                    results.append(
                        {
                            "project": project,
                            "dataset": dataset,
                            f"{branch}/greatness": greatness,
                        }
                    )
                    
                if branch != "master" or branch != "engine_baseline":
                    branches.add(branch)

    return pd.DataFrame(results), list(branches)


def parse_and_export_excel(text, out_filename):
    # Parse the results as a DataFrame
    df, branches = parse_pipeline_results(text)
    # print(df.columns)
    # print(tabulate(df))
    # print(branches)
    custom_branch = branches[0]

    # Filter columns
    branch_metric_names = []
    for col in df.columns:
        if "greatness" in col and not "master" in col:
            branch_metric_names.append(col)
            # break

    print("Branch metric names:")
    print(branch_metric_names)
    
    compare_branch = None
    if "master/greatness" in df.columns:
        compare_branch = "master/greatness"
    elif "engine_baseline/greatness":
        compare_branch = "engine_baseline/greatness"

    df = df[["project", "dataset", *branch_metric_names, compare_branch]]

    df = df.sort_values(by=["project", "dataset"])
    try:
        df["delta/greatness"] = df[f"{custom_branch}/greatness"] - df[compare_branch]
        df["delta/bool"] = df["delta/greatness"] > 0
    except:
        pass

    df = df.drop_duplicates()

    # Formatting numbers
    # for col in df.columns:
    #     if "greatness" in col:
    #         df[col] = df[col].apply(lambda x: f"{np.round(x, 2)} %")

    # Export to excel
    print(tabulate(df))
    # df.to_excel(out_filename, index=False)

    writer = pd.ExcelWriter(out_filename) 
    df.to_excel(writer, sheet_name='sheetName', index=False, na_rep='NaN')

    for column in df:
        column_length = max(df[column].astype(str).apply(len).max(), len(column)) + 5
        # col_idx = df.columns.get_loc(column)
        # writer.sheets['sheetName'].set_column(col_idx, col_idx, column_length)
        writer.sheets['sheetName'].column_dimensions[column].width = column_length

    writer.save()

def clear_directory(dir):
    for f in os.listdir(dir):
        filename = os.path.join(dir, f)
        if os.path.isfile(filename):
            os.remove(filename)