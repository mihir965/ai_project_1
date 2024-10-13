# # # from environment_utils import *
# # from env_utils import *
# # import sys
# # import os
# # from Bot import *
# # import numpy as np
# # import random

# # n = 40
# # q = 0.55

# # seed_value = random.randrange(1, 1000)
# # # seed_value = 999
# # # seed_value = 176
# # # seed_value = 616
# # # seed_value = 29
# # # seed_value = 604
# # # seed_value = 195
# # # seed_value = 964
# # print(seed_value)
# # random.seed(seed_value)
# # np.random.seed(seed_value)

# # grid = grid_init(n)
# # button_pos = button_init(grid, n, 3)
# # bot_pos = bot_init(grid, n, 4)
# # fire_init = fire_init_fn(grid, n, 2)

# # frames_bot1 = []
# # frames_bot2 = []
# # frames_bot3 = []
# # frames_bot4 = []

# # print("Bot 1")
# # random.seed(seed_value)
# # np.random.seed(seed_value)
# # time_lapse_fn_bot_1(grid.copy(), q, n, frames_bot1, bot_pos, button_pos, fire_init, seed_value)

# # print("Bot 2")
# # random.seed(seed_value)
# # np.random.seed(seed_value)
# # time_lapse_fn_bot2(grid.copy(), q, n, frames_bot2, bot_pos, button_pos, fire_init, seed_value)

# # print("Bot 3")
# # random.seed(seed_value)
# # np.random.seed(seed_value)
# # time_lapse_fn_bot3(grid.copy(), q, n, frames_bot3, bot_pos, button_pos, fire_init, seed_value)

# # # print("Bot 4")
# # # random.seed(seed_value)
# # # np.random.seed(seed_value)
# # # time_lapse_fn_bot4(grid.copy(), q, n, frames_bot4, bot_pos, button_pos, fire_init, seed_value)

# # print("Bot 4")
# # random.seed(seed_value)
# # np.random.seed(seed_value)
# # time_lapse_fn_bot4_new(grid.copy(), q, n, frames_bot4, bot_pos, button_pos, fire_init, seed_value)



# from env_utils import *
# from Bot import *
# import numpy as np
# import pandas as pd
# import random
# import os

# # Function to check the success of a bot in the latest log entry
# def check_success_from_log(bot_type):
#     log_file_path = 'C:/Users/shaiv/Downloads/ai_project_1-main/simulation_results.csv'  # Path to the log file
#     df = pd.read_csv(log_file_path)  # Load CSV with headers (no need for header=None)
    
#     # Filter rows for the given bot type
#     bot_logs = df[df['bot_type'] == bot_type]
    
#     if bot_logs.empty:
#         return False  # If there are no logs for this bot, return False
    
#     # Check if the last log entry for this bot contains 'Success' in the 'result' column
#     return 'Success' in bot_logs.iloc[-1]['result']

# def run_simulation(seed_value):
#     n = 40
#     q = 0.4

#     random.seed(seed_value)
#     np.random.seed(seed_value)

#     grid = grid_init(n)
#     button_pos = button_init(grid, n, 3)
#     bot_pos = bot_init(grid, n, 4)
#     fire_init = fire_init_fn(grid, n, 2)

#     frames_bot1, frames_bot2, frames_bot3 = [], [], []

#     # Suppress output from bot functions
#     time_lapse_fn_bot_1(
#         grid.copy(), q, n, frames_bot1, bot_pos, button_pos, fire_init, seed_value
#     )
#     time_lapse_fn_bot2(
#         grid.copy(), q, n, frames_bot2, bot_pos, button_pos, fire_init, seed_value
#     )
#     time_lapse_fn_bot3(
#         grid.copy(), q, n, frames_bot3, bot_pos, button_pos, fire_init, seed_value
#     )

#     # Check the log for success results
#     bot1_success = check_success_from_log('Bot 1')
#     bot2_success = check_success_from_log('Bot 2')
#     bot3_success = check_success_from_log('Bot 3')

#     return {
#         'bot1_success': bot1_success,
#         'bot2_success': bot2_success,
#         'bot3_success': bot3_success
#     }

# def run_multiple_simulations(total_simulations=10):
#     success_counts = {'bot1': 0, 'bot2': 0, 'bot3': 0}
#     results = []

#     for iteration in range(total_simulations):
#         seed_value = random.randint(0, 10000)
#         print(f"Starting simulation {iteration + 1} with seed {seed_value}")

#         simulation_result = run_simulation(seed_value)

#         success_counts['bot1'] += int(simulation_result['bot1_success'])
#         success_counts['bot2'] += int(simulation_result['bot2_success'])
#         success_counts['bot3'] += int(simulation_result['bot3_success'])

#         results.append({
#             'iteration': iteration + 1,
#             'seed': seed_value,
#             **simulation_result
#         })

#     # Save results to an Excel file
#     df = pd.DataFrame(results)
#     df.to_excel('simulation_results.xlsx', index=False)

#     print("\nSimulations completed. Results saved to 'simulation_results.xlsx'")
#     print(f"Final success counts: {success_counts}")

# if __name__ == '__main__':
#     run_multiple_simulations()


# from env_utils import *
# from Bot import *
# import numpy as np
# import pandas as pd
# import random
# import os
# import matplotlib.pyplot as plt

# # Function to check the success of a bot in the latest log entry
# def check_success_from_log(bot_type):
#     log_file_path = 'C:/Users/shaiv/Downloads/ai_project_1-main/simulation_results.csv'  # Path to the log file
#     df = pd.read_csv(log_file_path)  # Load CSV with headers (no need for header=None)
    
#     # Filter rows for the given bot type
#     bot_logs = df[df['bot_type'] == bot_type]
    
#     if bot_logs.empty:
#         return False  # If there are no logs for this bot, return False
    
#     # Check if the last log entry for this bot contains 'Success' in the 'result' column
#     return 'Success' in bot_logs.iloc[-1]['result']

# # Function to run a single simulation for a given seed and q-value
# def run_simulation(seed_value, q):
#     n = 40  # Fixed size of the grid

#     random.seed(seed_value)
#     np.random.seed(seed_value)

#     grid = grid_init(n)
#     button_pos = button_init(grid, n, 3)
#     bot_pos = bot_init(grid, n, 4)
#     fire_init = fire_init_fn(grid, n, 2)

#     frames_bot1, frames_bot2, frames_bot3 = [], [], []

#     # Suppress output from bot functions
#     time_lapse_fn_bot_1(
#         grid.copy(), q, n, frames_bot1, bot_pos, button_pos, fire_init, seed_value
#     )
#     time_lapse_fn_bot2(
#         grid.copy(), q, n, frames_bot2, bot_pos, button_pos, fire_init, seed_value
#     )
#     time_lapse_fn_bot3(
#         grid.copy(), q, n, frames_bot3, bot_pos, button_pos, fire_init, seed_value
#     )

#     # Check the log for success results
#     bot1_success = check_success_from_log('Bot 1')
#     bot2_success = check_success_from_log('Bot 2')
#     bot3_success = check_success_from_log('Bot 3')

#     return {
#         'bot1_success': bot1_success,
#         'bot2_success': bot2_success,
#         'bot3_success': bot3_success
#     }

# # Function to run multiple simulations for different q values
# def run_multiple_simulations_q_range(q_values, total_simulations=5):
#     success_rates = {'bot1': [], 'bot2': [], 'bot3': []}  # To store success rates for each q value

#     for q in q_values:
#         print(f"Running simulations for q = {q:.2f}")
#         success_counts = {'bot1': 0, 'bot2': 0, 'bot3': 0}
#         all_results = []

#         for sim in range(total_simulations):
#             seed_value = random.randint(0, 10000)
#             simulation_result = run_simulation(seed_value, q)

#             success_counts['bot1'] += int(simulation_result['bot1_success'])
#             success_counts['bot2'] += int(simulation_result['bot2_success'])
#             success_counts['bot3'] += int(simulation_result['bot3_success'])

#             all_results.append({
#                 'q_value': q,
#                 'simulation': sim + 1,
#                 'seed_value': seed_value,
#                 'bot1_success': simulation_result['bot1_success'],
#                 'bot2_success': simulation_result['bot2_success'],
#                 'bot3_success': simulation_result['bot3_success']
#             })

#         # Calculate average success rate for each bot
#         success_rates['bot1'].append(success_counts['bot1'] / total_simulations)
#         success_rates['bot2'].append(success_counts['bot2'] / total_simulations)
#         success_rates['bot3'].append(success_counts['bot3'] / total_simulations)

#     # Save the detailed results to an Excel file
#     df_results = pd.DataFrame(all_results)
#     df_results.to_excel('simulation_details.xlsx', index=False)
#     print("Detailed simulation results saved to 'simulation_details.xlsx'")
    
#     return success_rates

# # Function to plot the results
# def plot_success_rates(q_values, success_rates):
#     plt.figure(figsize=(10, 6))
    
#     # Plot success rates for each bot
#     plt.plot(q_values, success_rates['bot1'], label='Bot 1', marker='o')
#     plt.plot(q_values, success_rates['bot2'], label='Bot 2', marker='x')
#     plt.plot(q_values, success_rates['bot3'], label='Bot 3', marker='s')
    
#     plt.xlabel('q value (probability)')
#     plt.ylabel('Success Rate')
#     plt.title('Success Rate of Bots vs q Value')
#     plt.legend()
#     plt.grid(True)

#     plt.savefig('success_rate_plot.png')
#     print("Graph saved as 'success_rate_plot.png'")

#     plt.show()

# if __name__ == '__main__':
#     # Define a range of q values from 0 to 1 with step size 0.5
#     q_values = np.arange(0.0, 1.01, 0.05)  # Step size of 0.5

#     # Run simulations for each q value
#     total_simulations = 3  # Number of simulations per q value
#     success_rates = run_multiple_simulations_q_range(q_values, total_simulations)

#     # Plot the success rates
#     plot_success_rates(q_values, success_rates)


# from env_utils import *
# from Bot import *
# import numpy as np
# import pandas as pd
# import random
# import os
# import matplotlib.pyplot as plt

# # Function to check the success of a bot in the latest log entry
# def check_success_from_log(bot_type):
#     log_file_path = 'C:/Users/shaiv/Downloads/ai_project_1-main/simulation_results.csv'  # Path to the log file
#     df = pd.read_csv(log_file_path)  # Load CSV with headers (no need for header=None)
    
#     # Filter rows for the given bot type
#     bot_logs = df[df['bot_type'] == bot_type]
    
#     if bot_logs.empty:
#         return False  # If there are no logs for this bot, return False
    
#     # Check if the last log entry for this bot contains 'Success' in the 'result' column
#     return 'Success' in bot_logs.iloc[-1]['result']

# # Function to run a single simulation for a given seed and q-value
# def run_simulation(seed_value, q):
#     n = 40  # Fixed size of the grid

#     random.seed(seed_value)
#     np.random.seed(seed_value)

#     grid = grid_init(n)
#     button_pos = button_init(grid, n, 3)
#     bot_pos = bot_init(grid, n, 4)
#     fire_init = fire_init_fn(grid, n, 2)

#     frames_bot1, frames_bot2, frames_bot3, frames_bot4 = [], [], [], []

#     # Suppress output from bot functions
#     time_lapse_fn_bot_1(
#         grid.copy(), q, n, frames_bot1, bot_pos, button_pos, fire_init, seed_value
#     )
#     time_lapse_fn_bot2(
#         grid.copy(), q, n, frames_bot2, bot_pos, button_pos, fire_init, seed_value
#     )
#     time_lapse_fn_bot3(
#         grid.copy(), q, n, frames_bot3, bot_pos, button_pos, fire_init, seed_value
#     )
#     time_lapse_fn_bot4_prob_safe(
#         grid.copy(), q, n, frames_bot3, bot_pos, button_pos, fire_init, seed_value
#     )

#     # Check the log for success results
#     bot1_success = check_success_from_log('Bot 1')
#     bot2_success = check_success_from_log('Bot 2')
#     bot3_success = check_success_from_log('Bot 3')
#     bot4_success = check_success_from_log('Bot 4')

#     # If any bot succeeded, assume success was possible
#     success_possible = bot1_success or bot2_success or bot3_success

#     return {
#         'bot1_success': bot1_success,
#         'bot2_success': bot2_success,
#         'bot3_success': bot3_success,
#         'bot4_success': bot4_success,
#         'success_possible': success_possible  # Whether any bot succeeded
#     }

# # Function to run multiple simulations for different q values
# def run_multiple_simulations_q_range(q_values, total_simulations=10):
#     success_rates = {'bot1': [], 'bot2': [], 'bot3': [], 'bot4': []}  # To store raw success rates for each q value
#     possible_success_rates = {'bot1': [], 'bot2': [], 'bot3': [], 'bot4': []}  # Success rates for possible successes
#     all_results = []  # To store detailed results for saving to Excel

#     for q in q_values:
#         print(f"Running simulations for q = {q:.2f}")
#         success_counts = {'bot1': 0, 'bot2': 0, 'bot3': 0, 'bot4':0}
#         possible_success_counts = {'bot1': 0, 'bot2': 0, 'bot3': 0, 'bot4': 0}
#         total_possible_success = 0  # Count how many simulations had possible success

#         for sim in range(total_simulations):
#             seed_value = random.randint(0, 10000)
#             simulation_result = run_simulation(seed_value, q)

#             success_counts['bot1'] += int(simulation_result['bot1_success'])
#             success_counts['bot2'] += int(simulation_result['bot2_success'])
#             success_counts['bot3'] += int(simulation_result['bot3_success'])
#             success_counts['bot4'] += int(simulation_result['bot4_success'])

#             if simulation_result['success_possible']:
#                 total_possible_success += 1  # Increment count of scenarios where success was possible
#                 possible_success_counts['bot1'] += int(simulation_result['bot1_success'])
#                 possible_success_counts['bot2'] += int(simulation_result['bot2_success'])
#                 possible_success_counts['bot3'] += int(simulation_result['bot3_success'])
#                 possible_success_counts['bot4'] += int(simulation_result['bot4_success'])


#             # Append simulation result for each q value
#             all_results.append({
#                 'q_value': q,
#                 'simulation': sim + 1,
#                 'seed_value': seed_value,
#                 'bot1_success': simulation_result['bot1_success'],
#                 'bot2_success': simulation_result['bot2_success'],
#                 'bot3_success': simulation_result['bot3_success'],
#                 'bot4_success': simulation_result['bot4_success'],
#                 'success_possible': simulation_result['success_possible']
#             })

#         # Calculate raw success rates (out of all simulations)
#         success_rates['bot1'].append(success_counts['bot1'] / total_simulations)
#         success_rates['bot2'].append(success_counts['bot2'] / total_simulations)
#         success_rates['bot3'].append(success_counts['bot3'] / total_simulations)
#         success_rates['bot4'].append(success_counts['bot4'] / total_simulations)

#         # Calculate possible success rates (out of simulations where success was possible)
#         possible_success_rates['bot1'].append(possible_success_counts['bot1'] / total_possible_success if total_possible_success > 0 else 0)
#         possible_success_rates['bot2'].append(possible_success_counts['bot2'] / total_possible_success if total_possible_success > 0 else 0)
#         possible_success_rates['bot3'].append(possible_success_counts['bot3'] / total_possible_success if total_possible_success > 0 else 0)
#         possible_success_rates['bot4'].append(possible_success_counts['bot4'] / total_possible_success if total_possible_success > 0 else 0)


#     # Save the detailed results to an Excel file
#     df_results = pd.DataFrame(all_results)
#     df_results.to_excel('simulation_details_success_possible.xlsx', index=False)
#     print("Detailed simulation results saved to 'simulation_details_success_possible.xlsx'")

#     return success_rates, possible_success_rates

# # Function to plot the success rates (raw and possible)
# def plot_success_rates(q_values, success_rates, possible_success_rates):
#     plt.figure(figsize=(12, 8))

#     # Plot raw success rates for each bot
#     plt.subplot(2, 1, 1)
#     plt.plot(q_values, success_rates['bot1'], label='Bot 1 (Raw)', marker='o')
#     plt.plot(q_values, success_rates['bot2'], label='Bot 2 (Raw)', marker='x')
#     plt.plot(q_values, success_rates['bot3'], label='Bot 3 (Raw)', marker='s')
#     plt.plot(q_values, success_rates['bot4'], label='Bot 4 (Raw)', marker='*')
#     plt.xlabel('q value')
#     plt.ylabel('Raw Success Rate')
#     plt.title('Raw Success Rates of Bots vs q Value')
#     plt.legend()
#     plt.grid(True)

#     # Plot possible success rates for each bot
#     plt.subplot(2, 1, 2)
#     plt.plot(q_values, possible_success_rates['bot1'], label='Bot 1 (Possible)', marker='o')
#     plt.plot(q_values, possible_success_rates['bot2'], label='Bot 2 (Possible)', marker='x')
#     plt.plot(q_values, possible_success_rates['bot3'], label='Bot 3 (Possible)', marker='s')
#     plt.plot(q_values, possible_success_rates['bot4'], label='Bot 4 (Possible)', marker='*')
#     plt.xlabel('q value')
#     plt.ylabel('Success Rate (Where Possible)')
#     plt.title('Success Rates of Bots (Where Success Possible) vs q Value')
#     plt.legend()
#     plt.grid(True)

#     plt.tight_layout()
#     plt.savefig('bot_success_rates.png')
#     plt.show()

# if __name__ == '__main__':
#     # Define a range of q values from 0 to 1 with step size 0.5
#     q_values = np.arange(0.0, 1.01, 0.05)  # Step size of 0.5

#     # Run simulations for each q value
#     total_simulations = 5  # Number of simulations per q value
#     success_rates, possible_success_rates = run_multiple_simulations_q_range(q_values, total_simulations)

#     # Plot the success rates
#     plot_success_rates(q_values, success_rates, possible_success_rates)

from env_utils import *
from Bot import *
import numpy as np
import pandas as pd
import random
import os
import matplotlib.pyplot as plt

# Function to check the success of a bot in the latest log entry
def check_success_from_log(bot_type):
    log_file_path = 'C:/Users/shaiv/Downloads/ai_project_1-main/simulation_results.csv'  # Path to the log file
    df = pd.read_csv(log_file_path)  # Load CSV with headers (no need for header=None)
    
    # Filter rows for the given bot type
    bot_logs = df[df['bot_type'] == bot_type]
    
    if bot_logs.empty:
        return False  # If there are no logs for this bot, return False
    
    # Check if the last log entry for this bot contains 'Success' in the 'result' column
    return 'Success' in bot_logs.iloc[-1]['result']

# Function to run a single simulation for a given seed and q-value
def run_simulation(seed_value, q):
    n = 40  # Fixed size of the grid

    random.seed(seed_value)
    np.random.seed(seed_value)

    grid = grid_init(n)
    button_pos = button_init(grid, n, 3)
    bot_pos = bot_init(grid, n, 4)
    fire_init = fire_init_fn(grid, n, 2)

    frames_bot1, frames_bot2, frames_bot3, frames_bot4 = [], [], [], []

    # Suppress output from bot functions
    time_lapse_fn_bot_1(
        grid.copy(), q, n, frames_bot1, bot_pos, button_pos, fire_init, seed_value
    )
    time_lapse_fn_bot2(
        grid.copy(), q, n, frames_bot2, bot_pos, button_pos, fire_init, seed_value
    )
    time_lapse_fn_bot3(
        grid.copy(), q, n, frames_bot3, bot_pos, button_pos, fire_init, seed_value
    )
    time_lapse_fn_bot4_prob_safe(
        grid.copy(), q, n, frames_bot3, bot_pos, button_pos, fire_init, seed_value
    )

    # Check the log for success results
    bot1_success = check_success_from_log('Bot 1')
    bot2_success = check_success_from_log('Bot 2')
    bot3_success = check_success_from_log('Bot 3')
    bot4_success = check_success_from_log('Bot 4')

    # If any bot succeeded, assume success was possible
    success_possible = bot1_success or bot2_success or bot3_success

    return {
        'bot1_success': bot1_success,
        'bot2_success': bot2_success,
        'bot3_success': bot3_success,
        'bot4_success': bot4_success,
        'success_possible': success_possible  # Whether any bot succeeded
    }

# Function to run multiple simulations for different q values
def run_multiple_simulations_q_range(q_values, total_simulations=10):
    success_rates = {'bot1': [], 'bot2': [], 'bot3': [], 'bot4': []}  # To store raw success rates for each q value
    possible_success_rates = {'bot1': [], 'bot2': [], 'bot3': [], 'bot4': []}  # Success rates for possible successes
    all_results = []  # To store detailed results for saving to Excel

    # Initialize total success counts for overall accuracy
    overall_success_counts = {'bot1': 0, 'bot2': 0, 'bot3': 0, 'bot4': 0}
    total_simulations_overall = 0  # Total number of simulations over all q values

    for q in q_values:
        print(f"Running simulations for q = {q:.2f}")
        success_counts = {'bot1': 0, 'bot2': 0, 'bot3': 0, 'bot4': 0}
        possible_success_counts = {'bot1': 0, 'bot2': 0, 'bot3': 0, 'bot4': 0}
        total_possible_success = 0  # Count how many simulations had possible success

        for sim in range(total_simulations):
            seed_value = random.randint(0, 10000)
            simulation_result = run_simulation(seed_value, q)

            success_counts['bot1'] += int(simulation_result['bot1_success'])
            success_counts['bot2'] += int(simulation_result['bot2_success'])
            success_counts['bot3'] += int(simulation_result['bot3_success'])
            success_counts['bot4'] += int(simulation_result['bot4_success'])

            if simulation_result['success_possible']:
                total_possible_success += 1  # Increment count of scenarios where success was possible
                possible_success_counts['bot1'] += int(simulation_result['bot1_success'])
                possible_success_counts['bot2'] += int(simulation_result['bot2_success'])
                possible_success_counts['bot3'] += int(simulation_result['bot3_success'])
                possible_success_counts['bot4'] += int(simulation_result['bot4_success'])

            # Append simulation result for each q value
            all_results.append({
                'q_value': q,
                'simulation': sim + 1,
                'seed_value': seed_value,
                'bot1_success': simulation_result['bot1_success'],
                'bot2_success': simulation_result['bot2_success'],
                'bot3_success': simulation_result['bot3_success'],
                'bot4_success': simulation_result['bot4_success'],
                'success_possible': simulation_result['success_possible']
            })

        # Update overall success counts and total simulations
        overall_success_counts['bot1'] += success_counts['bot1']
        overall_success_counts['bot2'] += success_counts['bot2']
        overall_success_counts['bot3'] += success_counts['bot3']
        overall_success_counts['bot4'] += success_counts['bot4']
        total_simulations_overall += total_simulations

        # Calculate raw success rates (out of all simulations)
        success_rates['bot1'].append(success_counts['bot1'] / total_simulations)
        success_rates['bot2'].append(success_counts['bot2'] / total_simulations)
        success_rates['bot3'].append(success_counts['bot3'] / total_simulations)
        success_rates['bot4'].append(success_counts['bot4'] / total_simulations)

        # Calculate possible success rates (out of simulations where success was possible)
        possible_success_rates['bot1'].append(possible_success_counts['bot1'] / total_possible_success if total_possible_success > 0 else 0)
        possible_success_rates['bot2'].append(possible_success_counts['bot2'] / total_possible_success if total_possible_success > 0 else 0)
        possible_success_rates['bot3'].append(possible_success_counts['bot3'] / total_possible_success if total_possible_success > 0 else 0)
        possible_success_rates['bot4'].append(possible_success_counts['bot4'] / total_possible_success if total_possible_success > 0 else 0)

    # Save the detailed results to an Excel file
    df_results = pd.DataFrame(all_results)
    df_results.to_excel('simulation_details_success_possible.xlsx', index=False)
    print("Detailed simulation results saved to 'simulation_details_success_possible.xlsx'")

    # Print overall accuracy for each bot after all simulations
    print("\nOverall Accuracy of each bot:")
    print(f"Bot 1 Overall Accuracy: {(overall_success_counts['bot1'] / total_simulations_overall) * 100:.2f}%")
    print(f"Bot 2 Overall Accuracy: {(overall_success_counts['bot2'] / total_simulations_overall) * 100:.2f}%")
    print(f"Bot 3 Overall Accuracy: {(overall_success_counts['bot3'] / total_simulations_overall) * 100:.2f}%")
    print(f"Bot 4 Overall Accuracy: {(overall_success_counts['bot4'] / total_simulations_overall) * 100:.2f}%")

    return success_rates, possible_success_rates  # Return only the success rates

# Function to plot the success rates (raw and possible)
def plot_success_rates(q_values, success_rates, possible_success_rates):
    plt.figure(figsize=(12, 8))

    # Plot raw success rates for each bot
    plt.subplot(2, 1, 1)
    plt.plot(q_values, success_rates['bot1'], label='Bot 1 (Raw)', marker='o')
    plt.plot(q_values, success_rates['bot2'], label='Bot 2 (Raw)', marker='x')
    plt.plot(q_values, success_rates['bot3'], label='Bot 3 (Raw)', marker='s')
    plt.plot(q_values, success_rates['bot4'], label='Bot 4 (Raw)', marker='*')
    plt.xlabel('q value')
    plt.ylabel('Raw Success Rate')
    plt.title('Raw Success Rates of Bots vs q Value')
    plt.legend()
    plt.grid(True)

    # Plot possible success rates for each bot
    plt.subplot(2, 1, 2)
    plt.plot(q_values, possible_success_rates['bot1'], label='Bot 1 (Possible)', marker='o')
    plt.plot(q_values, possible_success_rates['bot2'], label='Bot 2 (Possible)', marker='x')
    plt.plot(q_values, possible_success_rates['bot3'], label='Bot 3 (Possible)', marker='s')
    plt.plot(q_values, possible_success_rates['bot4'], label='Bot 4 (Possible)', marker='*')
    plt.xlabel('q value')
    plt.ylabel('Success Rate (Where Possible)')
    plt.title('Success Rates of Bots (Where Success Possible) vs q Value')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig('bot_success_rates.png')
    plt.show()

if __name__ == '__main__':
    # Define a range of q values from 0 to 1 with step size 0.05
    q_values = np.arange(0.0, 1.01, 0.05)  # Step size of 0.05

    # Run simulations for each q value
    total_simulations = 10  # Number of simulations per q value
    success_rates, possible_success_rates = run_multiple_simulations_q_range(q_values, total_simulations)

    # Plot the success rates
    plot_success_rates(q_values, success_rates, possible_success_rates)

