import os
import pandas as pd
import csv

# Define input and output folders
input_folder = "C:/Users/Abhimanyu/PycharmProjects/pythonProject11/File-Processor/interview_task/myfiles"
output_folder = "C:/Users/Abhimanyu/PycharmProjects/pythonProject11/File-Processor/interview_task/myoutput"


def read_files(input_folder):
    all_data = []
    file_names = []
    if not os.path.exists(input_folder):
        raise FileNotFoundError(f"The input folder '{input_folder}' does not exist.")

    for file_name in os.listdir(input_folder):
        if file_name.endswith(".dat"):
            file_path = os.path.join(input_folder, file_name)
            try:
                data = pd.read_csv(file_path)
                all_data.append(data)
                file_names.append(file_name)
            except Exception as e:
                print(f"Error reading {file_path}: {e}")

    if all_data:
        combined_data = pd.concat(all_data, ignore_index=True)
        return combined_data, file_names
    else:
        return pd.DataFrame(), file_names  # Return an empty DataFrame if no data was read



def remove_duplicates(data):
    return data.drop_duplicates()


def calculate_footer(data):
    if 'salary' not in data.columns:
        raise KeyError("The required column 'basic_salary' is not present in the data.")

    salaries = data['basic_salary'].astype(float)
    second_highest_salary = salaries.nlargest(2).iloc[-1]
    average_salary = salaries.mean()
    return second_highest_salary, average_salary


def write_csv(data, file_names, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    second_highest_salary, average_salary = calculate_footer(data)

    # Write each input file's processed data to a separate output CSV file
    for file_name in file_names:
        base_name = os.path.splitext(file_name)[0]
        output_file = os.path.join(output_folder, f"{base_name}_result.csv")
        data.to_csv(output_file, index=False)

        # Append the footer with second highest and average salary using CSV writer
        with open(output_file, "a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow([])  # Blank line for separation
            writer.writerow(["Second Highest Salary", second_highest_salary])
            writer.writerow(["Average Salary", average_salary])


def main():
    data, file_names = read_files(input_folder)
    if data.empty:
        print("No data found in the input files.")
        return

    clean_data = remove_duplicates(data)
    write_csv(clean_data, file_names, output_folder)


if __name__ == "__main__":
    main()
