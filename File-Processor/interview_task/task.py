import os
import pandas as pd
import csv

#  read data from the multiple files which are located in particular folder.
input_folder = "C:/Users/Abhimanyu/PycharmProjects/pythonProject11/File-Processor/interview_task/myfiles"

output_folder = "C:/Users/Abhimanyu/PycharmProjects/pythonProject11/File-Processor/interview_task/myoutput"



# get list of files in input_folder
files = os.listdir(input_folder)

for file_name in files:
    base_name = os.path.splitext(file_name)[0]
    output_file = os.path.join(output_folder, f"{base_name}_result.csv")
    file_path = os.path.join(input_folder, file_name)
    with open(file_path, 'r') as file:
        data = pd.read_csv(file, delimiter="\t")

        # remove duplicates
        cleaned_data = data.drop_duplicates()

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # store cleaned data into output file
        cleaned_data.to_csv(output_file, index=False)

        # get second-highest salary and average salary from cleaned data
        salaries = cleaned_data['basic_salary'].astype(float)
        second_highest_salary = salaries.nlargest(2).iloc[-1]
        average_salary = salaries.mean()

        with open(output_file, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([])  # Blank line for separation
            writer.writerow(["second-highest salary", second_highest_salary])
            writer.writerow(["average salary", average_salary])

