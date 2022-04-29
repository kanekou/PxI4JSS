import re
import pandas as pd

def extract_variable(s):
    literal = re.split('[\[\]]', s)
    while '' in literal:
        literal.remove('')
    return literal

def calculate_processing_time(low_time, decoded_solution_sample, pt):
    if not decoded_solution_sample:
        return -1, -1

    start_time = low_time - 1
    solution_dict = format_solution_to_2Ddict(decoded_solution_sample)
    solution_df = pd.DataFrame(solution_dict).T

    # If the time size of solution_df and start_time do not match
    solution_df_last_column = len(solution_df.columns)-1
    if (solution_df[solution_df_last_column] == 0).all():
        for ci in range(solution_df_last_column, -1, -1):
            # check if a column is all zeroes
            if (solution_df[ci] == 0).all():
                solution_df.drop(columns=ci, inplace=True)
                start_time -= 1
            else:
                break

    max_start_time_transitions = solution_df[solution_df[start_time]
                                                == 1].index.values
    end_time = 0
    for t in max_start_time_transitions:
        end_time = max(start_time + (pt['t{}'.format(t)]), end_time)

    return start_time, end_time

def format_solution_to_2Ddict(solution):
    if not solution:
        return {}

    formated_solution = {}
    for k, v in solution.items():
        literal = extract_variable(k)
        time = int(literal[2])
        trans = int(literal[1])

        if not (trans in formated_solution):
            formated_solution[trans] = {}
        formated_solution[trans].update({time: v})

    # {0: {0: 1, 1: 0, 2: 0, 3: 0, 4: 0},
    #  1: {0: 0, 1: 0, 2: 1, 3: 0, 4: 0},
    #  2: {0: 0, 1: 0, 2: 0, 3: 0, 4: 1},
    #  3: {0: 1, 1: 0, 2: 0, 3: 0, 4: 0},
    #  4: {0: 0, 1: 0, 2: 0, 3: 1, 4: 0},
    #  5: {0: 0, 1: 0, 2: 0, 3: 0, 4: 1}}
    return formated_solution
