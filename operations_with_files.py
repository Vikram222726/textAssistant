import os
import shutil
import pandas as pd
import re
from datetime import datetime
from utils import display_prompt, select_multiple_prompt_options
from possible_text_options import (
    possible_file_extension_map,
    possible_file_filters,
    possible_aggregate_operations
)

search_file_prompt_list = [
    "Search by exact name",
    "Search by name",
]


def search_files_in_os(file_path, search_type="exact"):
    base_path_list = ["/Users/vikramkumar/Movies", "/Users/vikramkumar/Music", "/Users/vikramkumar/Desktop", "/Users/vikramkumar/Pictures", "/Users/vikramkumar/Documents", "/Users/vikramkumar/Downloads"]

    try:
        matched_file_path_list = []
        for base_path in base_path_list:
            for root, dirs, files in os.walk(base_path):
                for file in files:
                    complete_file_path = os.path.join(root, file)
                    file_path_end_comp = complete_file_path.split("/")[-1]
                    if search_type == "exact":
                        if file_path_end_comp == file_path:
                            return complete_file_path
                    else:
                        file_name = file_path_end_comp.replace("_", " ").replace("- ", " ").replace("-", " ").split(".")[0]
                        file_name = file_name.lower()
                        if file_path in file_name:
                            matched_file_path_list.append(complete_file_path)
        return None if search_type == "exact" else matched_file_path_list
    except Exception as e:
        raise e


def get_exact_matched_file():
    max_num_tries = 0
    while max_num_tries < 2:
        try:
            max_num_tries += 1
            file_name = input("Please enter the exact file name\n")
            file_extension = input("Please enter the file extension\n")
            complete_file_path = f"{file_name}.{possible_file_extension_map[file_extension]}"

            print(f"Started searching file: {complete_file_path}")
            searched_file_path = search_files_in_os(complete_file_path)

            if searched_file_path is None:
                file_not_found_msg = "404: File Not Found"
                file_not_found_msg = f"{file_not_found_msg}, please try again" if max_num_tries < 2 else file_not_found_msg
                print(file_not_found_msg)
            else:
                print("x"*130)
                print(f"File Path => {searched_file_path}")
                print("x"*130)
                return
        except Exception as e:
            print(f"Got error while searching exact file by name with error: {e}")


def get_matched_files():
    while True:
        try:
            file_name = input("Please enter the file name\n")

            search_files_path_list = search_files_in_os(file_name, search_type="all")

            if search_files_path_list is None or len(search_files_path_list) == 0:
                print("404: Files not Found")
                retry_search = input("Do you want to retry search operation again? Yes or No \n")
                if retry_search in ["Yes", "yes", "y"]:
                    print("Please retry again")
                else:
                    return
            else:
                print("x"*130)
                for file_path in search_files_path_list:
                    print("File Path => ", file_path)
                print("x"*130)
                return
        except Exception as e:
            print(f"Got error while searching matched files with error: {e}")
            print("Please retry again")


def search_file():
    option_to_functionality_map = {
        "Search by exact name": get_exact_matched_file,
        "Search by name": get_matched_files
    }

    option_to_functionality_map[display_prompt(search_file_prompt_list)]()


def __generate_file_destination_path(file_source_path_list):
    base_path = "/Users/vikramkumar"
    while True:
        directory_list = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d)) and d[0] != '.']
        folder_location = display_prompt(directory_list)

        confirm_folder_storage = input(f"Do you want to store data on top level in {folder_location} folder? Yes or No\n")
        if confirm_folder_storage in ["Yes", "yes", "y"]:
            file_destination_path_list = []
            for file_source_path in file_source_path_list:
                file_destination_path_list.append(
                    f"{base_path}/{folder_location}/{file_source_path.split('/')[-1]}"
                )
            return file_destination_path_list
        else:
            base_path += f"/{folder_location}"


def transfer_file():
    while True:
        try:
            file_name = input("Please enter the file name:\n")

            all_related_files_list = search_files_in_os(file_name, search_type="all")
            file_source_path_list = select_multiple_prompt_options(all_related_files_list)

            file_destination_path_list = __generate_file_destination_path(file_source_path_list)

            for file_idx in range(len(file_source_path_list)):
                shutil.move(file_source_path_list[file_idx], file_destination_path_list[file_idx])

                print(f"Successfully transferred file from {file_source_path_list[file_idx]} => {file_destination_path_list[file_idx]}")
            return
        except Exception as e:
            print(f"Got an error while transferring file: {e}")


def __generate_filter_on_files(df):
    try:
        column_name_list = df.columns.tolist()

        file_filter_list, filter_column_map = [], dict()
        while True:
            column_name = input("Please enter the column name\n")
            if len(column_name.split(" ")) > 1:
                column_name = column_name.replace(" ", "_")

            if column_name not in column_name_list:
                print(f"provided column: {column_name} not present in file, please retry telling column name")
                continue

            filter_option_selected = display_prompt(possible_file_filters)

            print(f"Filtered option selected: {filter_option_selected}")
            if str(column_name + filter_option_selected) in filter_column_map:
                print(f"column: {column_name} already added for {filter_option_selected} filter")
            else:
                filter_column_map[str(column_name + filter_option_selected)] = 1
                if filter_option_selected == "group by":
                    file_filter_list.append({
                        "col_name": column_name,
                        "col_filter_type": filter_option_selected
                    })
                elif filter_option_selected == "aggregate":
                    if str(column_name + "group by") in filter_column_map.keys():
                        print("Group by and aggregate operation cannot be performed on same column, please retry!")
                        continue
                    aggregate_option_selected = display_prompt(possible_aggregate_operations)

                    file_filter_list.append({
                        "agg_col_name": column_name,
                        "agg_operation": aggregate_option_selected,
                        "col_filter_type": filter_option_selected
                    })
                else:
                    column_filter_value = input(f"Please enter column value should be {filter_option_selected}\n")
                    try:
                        column_type = df[column_name].dtype

                        if column_type in [int, "uint64", "int64"]:
                            column_filter_value = int(column_filter_value)
                        elif column_type in [float, "float64", "float32"]:
                            column_filter_value = float(column_filter_value)
                        else:
                            column_filter_value = str(column_filter_value)
                    except Exception as err:
                        print(f"Got error while converting filtered column value: {err}")
                        print("Please retry again")
                        continue

                    file_filter_list.append({
                        "col_name": column_name,
                        "col_filter_value": column_filter_value,
                        "col_filter_type": filter_option_selected
                    })

                add_more_filter = input("Do you want to add more filters? Yes or No\n")
                if add_more_filter in ["Yes", "yes", "y"]:
                    continue
                else:
                    break
        print(f"Final filtered list: {file_filter_list}")
        return file_filter_list
    except Exception as exc:
        print(f"Failed while generating filter on df with error: {exc}")
        raise exc


def __apply_filters_on_df(df_main, applied_filter_list):
    df = df_main.copy()

    filter_option_list = [data for data in applied_filter_list if data["col_filter_type"] not in ["group by", "aggregate"]]
    group_by_option_list = [data["col_name"] for data in applied_filter_list if data["col_filter_type"] == "group by"]
    aggregate_option_items = {data["agg_col_name"]: data["agg_operation"] for data in applied_filter_list if data["col_filter_type"] == "aggregate"}

    for filter_option in filter_option_list:
        if filter_option["col_filter_type"] == "greater than":
            df = df[df[filter_option["col_name"]] > filter_option["col_filter_value"]]
        if filter_option["col_filter_type"] == "greater than equal to":
            df = df[df[filter_option["col_name"]] >= filter_option["col_filter_value"]]
        if filter_option["col_filter_type"] == "less than":
            df = df[df[filter_option["col_name"]] < filter_option["col_filter_value"]]
        if filter_option["col_filter_type"] == "less than equal to":
            df = df[df[filter_option["col_name"]] <= filter_option["col_filter_value"]]
        if filter_option["col_filter_type"] == "equal to":
            df = df[df[filter_option["col_name"]] == filter_option["col_filter_value"]]
        if filter_option["col_filter_type"] == "not equal to":
            df = df[df[filter_option["col_name"]] != filter_option["col_filter_value"]]

    if len(group_by_option_list) > 0:
        df = df.groupby(group_by_option_list).agg(aggregate_option_items).reset_index()
    return df


def filter_file():
    while True:
        file_name = input("Please input the file name you want to filter data from\n")
        matched_files_path_list = search_files_in_os(file_name, search_type="all")
        if len(matched_files_path_list) == 0:
            print("No file found with this name, please retry")
            continue

        file_selected = display_prompt(matched_files_path_list)
        if file_selected.split(".")[-1] not in ["csv", "xlsx"]:
            print("File should be of either csv or excel type")
            continue

        file_type = file_selected.split(".")[-1]

        df = pd.read_csv(file_selected) if file_type == "csv" else pd.read_excel(file_selected)
        try:
            df.columns = [re.sub(r"(?<!^)(?=[A-Z])", "_", x).replace(" ", "_").replace("-", "_").lower() for x in df.columns]
        except Exception as err:
            print("Found some issue in table columns, please check and retry")
            raise err

        applied_filter_list = __generate_filter_on_files(df)

        df = __apply_filters_on_df(df, applied_filter_list)

        file_split_source_path = file_selected.split("/")
        file_destination_path = "/".join(file_split_source_path[:-1]) + "/" + file_split_source_path[-1].split(".")[0] + "_" + datetime.now().strftime('%Y-%m-%dT%H:%M:%S') + "." + file_type

        if file_type == "csv":
            df.to_csv(file_destination_path)
        elif file_type == "xlsx":
            df.to_excel(file_destination_path)

        print("Successfully stored filtered file on destination location => ", file_destination_path)
        return
