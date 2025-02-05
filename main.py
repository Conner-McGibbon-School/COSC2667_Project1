from job import ReadyJobs, Producer, Scheduler1, Scheduler2
import threading
import pandas as pd

JOB_AMOUNT = 100 # Number of jobs to generate
QUANTUM = 10 / 1000 # Quantum time for the Round Robin scheduler
FILE1 = "output1.txt"
FILE2 = "output2.txt"

def main():
    clean_file(FILE1)
    clean_file(FILE2)

    print("=====Scheduler 1 First Come First Serve=====")
    # Create the queue and threads for the first scheduler
    queue1 = ReadyJobs()
    prodcer_thread1 = threading.Thread(target=Producer, args=(queue1, FILE1, JOB_AMOUNT))
    scheduler_thread1 = threading.Thread(target=Scheduler1, args=(queue1,))

    prodcer_thread1.start()
    scheduler_thread1.start()
    prodcer_thread1.join()
    scheduler_thread1.join()

    print("\n=====Scheduler 2 Round Robin=====")
    # Create the queue and threads for the second scheduler
    queue2 = ReadyJobs()
    prodcer_thread2 = threading.Thread(target=Producer, args=(queue2, FILE2, JOB_AMOUNT))
    scheduler_thread2 = threading.Thread(target=Scheduler2, args=(queue2, QUANTUM))

    prodcer_thread2.start()
    scheduler_thread2.start()
    prodcer_thread2.join()
    scheduler_thread2.join()

    generate_tables(FILE1, FILE2)


# Clean the output files
def clean_file(file_path):
    with open(file_path, "w") as f:
        f.write("Job Number,Burst Time,Turnaround Time,Response Time,Wait Time\n")

def generate_tables(file1, file2):
    # Read the output files into DataFrames
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    # Calculate the rate of waiting time to burst time
    df1['Wait/Burst Ratio'] = df1['Wait Time'] / df1['Burst Time']
    df2['Wait/Burst Ratio'] = df2['Wait Time'] / df2['Burst Time']

    # Print the tables with the new column
    print("\n=====Scheduler 1 Table=====")
    print(df1.to_string(index=False))
    print("\n=====Scheduler 2 Table=====")
    print(df2.to_string(index=False))

    # Calculate the comparison metrics
    comparison = {
        'Metric': ['Average Turnaround Time', 'Max Turnaround Time',
                   'Min Turnaround Time', 'Average Response Time',
                   'Max Response Time', 'Min Response Time',
                   'Average Wait Time', 'Max Wait Time', 'Min Wait Time'],
        'Scheduler 1': [
            df1['Turnaround Time'].mean(),
            df1['Turnaround Time'].max(),
            df1['Turnaround Time'].min(),
            df1['Response Time'].mean(),
            df1['Response Time'].max(),
            df1['Response Time'].min(),
            df1['Wait Time'].mean(),
            df1['Wait Time'].max(),
            df1['Wait Time'].min()
        ],
        'Scheduler 2': [
            df2['Turnaround Time'].mean(),
            df2['Turnaround Time'].max(),
            df2['Turnaround Time'].min(),
            df2['Response Time'].mean(),
            df2['Response Time'].max(),
            df2['Response Time'].min(),
            df2['Wait Time'].mean(),
            df2['Wait Time'].max(),
            df2['Wait Time'].min()
        ]
    }

    # Create a DataFrame for the comparison
    comparison_df = pd.DataFrame(comparison)
    # Print the comparison table
    print("\n=====Comparison Table=====")
    print(comparison_df.to_string(index=False))

if __name__ == "__main__":
    main()
