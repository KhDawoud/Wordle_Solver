from itertools import product
from math import log2
import multiprocessing

with open(r'words.txt', 'r') as file:
    words = [line.strip()[:5] for line in file if line.strip()]

all_possible_combinations = list(product([0, 1, 2], repeat=5))


def generate_filtered_list(word, combination, word_list):
    filtered_list = word_list
    for i, (letter, colour) in enumerate(zip(word, combination)):
        match colour:
            case 0:
                filtered_list = [word for word in filtered_list if letter not in word]
            case 1:
                filtered_list = [word for word in filtered_list if letter in word]
                filtered_list = [word for word in filtered_list if word[i] != letter]
            case 2:
                filtered_list = [word for word in filtered_list if letter in word]
                filtered_list = [word for word in filtered_list if word[i] == letter]

    return list(filtered_list)


def calculate_cweighting(word, combination, word_list):
    length_remaining_words = len(generate_filtered_list(word, combination, word_list))
    probability = length_remaining_words / len(word_list)
    information_gain = log2(len(word_list) / length_remaining_words) if length_remaining_words != 0 else 0
    score = probability * information_gain
    return score


def calculate_fweighting(word, word_list):
    f_weighting = 0
    for combination in all_possible_combinations:
        f_weighting += calculate_cweighting(word, combination, word_list)
    return f_weighting


def evaluate_words(word_list, results, possible):
    for word in word_list:
        calculation = calculate_fweighting(word, possible)
        print(word, calculation)
        results.append((word, calculation))


# def split_list(lst, num_parts):
#     if num_parts <= 0:
#         raise ValueError("Number of parts should be greater than zero.")
#
#     avg_length = len(lst) // num_parts
#     remainder = len(lst) % num_parts
#
#     sublists = []
#     start_idx = 0
#
#     for i in range(num_parts):
#         sublist_length = avg_length + (1 if i < remainder else 0)
#         end_idx = start_idx + sublist_length
#         sublists.append(lst[start_idx:end_idx])
#         start_idx = end_idx
#
#     return sublists


if __name__ == "__main__":
    filtered_words = words
    for i in range(5):
        guess = input("Enter your guess ")
        colors = input("Enter the colors ").split(',')
        colors = map(int, colors)
        filtered_words = generate_filtered_list(guess, colors, filtered_words)
        if len(filtered_words) == 1:
            print(filtered_words[0])
            break
        # processes = []
        # manager = multiprocessing.Manager()
        # results = manager.list()
        # batches = split_list(words, 6)
        #
        # for batch in batches:
        #     p = multiprocessing.Process(target=evaluate_words, args=(batch, results, filtered_words))
        #     processes.append(p)
        #     p.start()
        #
        # for p in processes:
        #     p.join()

        word_weightings = []
        evaluate_words(words, word_weightings, filtered_words)
        sorted_word_weightings = sorted(word_weightings, key=lambda x: x[1])

        for word, calculation in sorted_word_weightings:
            print(f"Word: {word}, Calculation: {calculation}")

