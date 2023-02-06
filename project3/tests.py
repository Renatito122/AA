from collections import defaultdict
from lossy_count import LossyCounter
from exact_counter import ExactCounter
from fixed_probability_counter import FixedProbCounter
import time
from math import sqrt
from tabulate import tabulate
from utils import *
import matplotlib.pyplot as plt


class Test():
    def __init__(self, fname="datasets/AssociationFootball.txt", rep=1000, k=10, epsilon=5e-3):
        self.fname = fname
        self.rep = rep
        self.k = k
        self.epsilon = epsilon

        self.run_test()


    def run_test(self):
        exact_counter, fixed_prob_counter, lossy_count =\
            ExactCounter(self.fname), FixedProbCounter(self.fname), LossyCounter(self.fname, self.epsilon)

        self.get_stats(exact_counter, exact_counter=True)
        self.get_stats(fixed_prob_counter)
        self.get_lossy_stats(lossy_count)


    def get_stats(self, counter, exact_counter=False):
        print(f"{counter}\n")

        total_time, total_means, total_countings, total_estimated_events,\
            total_alp_size, total_min_events, total_max_events =\
                0, 0, 0, 0, 0, 0, 0,
        total_letter_occur = defaultdict(lambda: [])
        plot_data = [[], [], []]

        for i in range(self.rep):
            tic = time.time()
            counter.count()
            total_time += time.time() - tic

            if not exact_counter:
                counter.estimate_events()
                total_countings += sum(counter.letter_occur.values())
                total_alp_size += len(counter.letter_occur)
                total_estimated_events += sum(counter.estimated_letter_occur.values())
                total_min_events += min(counter.estimated_letter_occur.values())
                total_max_events += max(counter.estimated_letter_occur.values())
                total_means += calc_mean(counter.estimated_letter_occur.values())

                merge_dicts(total_letter_occur, counter.estimated_letter_occur)

                rep = i + 1
                plot_data[0].append(rep)
                plot_data[1].append(abs(self.total_events - (total_estimated_events / rep)) / self.total_events * 100)
                rel_errors = [abs(sum(occur) / rep - self.exact_letter_occur[letter]) for letter, occur in total_letter_occur.items()]
                avg_rel_errors = sum(rel_errors) / len(rel_errors)
                plot_data[2].append(avg_rel_errors)

        avg_time = round(total_time / self.rep, 3)
        data = [["Counting Time (s)", avg_time], ["Alphabet Size"], ["Events"], ["Mean"], ["Minimum"], ["Maximum"]]
        headers = ["Measure", "Value"]

        if exact_counter:
            self.exact_letter_occur = counter.letter_occur
            self.exact_top_k_letters = counter.top_k_letters(self.k)
            self.k = len(self.exact_top_k_letters)
            self.alphabet_size = len(counter.letter_occur)
            self.total_events = total_countings = sum(counter.letter_occur.values())
            self.mean = mean = calc_mean(counter.letter_occur.values())
            self.min_events = min_events = min(counter.letter_occur.values())
            self.max_events = max_events = max(counter.letter_occur.values())
            data[1].append(self.alphabet_size)
            data[2].append(round(self.total_events, 2))
            data[3].append(round(self.mean, 2))
            data[4].append(round(self.min_events, 2))
            data[5].append(round(self.max_events, 2))
        else:
            headers.extend(["Absolute Error", "Relative Error (%)"])
            headers.extend([["Absolute Error"], ["Relative Error (%)"]])
            total_alp_size = round(total_alp_size / self.rep, 2)
            total_countings = round(total_countings / self.rep, 2)
            total_events = round(total_estimated_events / self.rep, 2)
            mean = round(total_means / self.rep, 2)
            min_events = round(total_min_events / self.rep, 2)
            max_events = round(total_max_events / self.rep, 2)
            common_top_k_letters = most_frequent(total_letter_occur, self.k)

            data[0].extend(['-', '-'])
            data[1].extend([total_alp_size, round(abs(self.alphabet_size - total_alp_size), 2),
                round(abs(self.alphabet_size - total_alp_size) / self.alphabet_size * 100, 2)])
            data[2].extend([total_events, round(abs(self.total_events - total_events), 2),
                round(abs(self.total_events - total_events) / self.total_events * 100, 2)])
            data[3].extend([mean, round(abs(self.mean - mean), 2),
                round(abs(self.mean - mean) / self.mean * 100, 2)])
            data[4].extend([min_events, round(abs(self.min_events - min_events), 2),
                round(abs(self.min_events - min_events) / self.min_events * 100, 2)])
            data[5].extend([max_events, round(abs(self.max_events - max_events), 2),
                round(abs(self.max_events - max_events) / self.max_events * 100, 2)])

        print(f"Results for {self.rep} repetition{'s' if self.rep != 1 else ''}:")
        print(f"Total Elapsed Time: {round(total_time, 3)} s\nTotal Events Counted: {total_countings}")
        print("\nAverage Values for a Repetition:")
        print(tabulate(data, headers=headers))

        print(f"\nTop {self.k} Most Frequent Letters:")
        if exact_counter:
            print(tabulate(self.exact_top_k_letters.items(), headers=["Letter", "Exact Events"]))
        else:
            relative_precision, right_position_letters = 0, 0
            exact_top_k_letters = list(self.exact_top_k_letters.keys())

            headers = ["Letter", "Min", "Max", "Mean", "Mean Absolute Error", "Mean Relative Error (%)"]
            data = []
            for i, letter_occur in enumerate(common_top_k_letters.items()):
                letter, occur = letter_occur
                mean_occur = calc_mean(occur)
                abs_error = abs(self.exact_letter_occur[letter] - mean_occur)
                rel_error = round(abs_error / self.exact_letter_occur[letter] * 100, 2)
                if self.rep > 1:
                    variance = calc_variance(occur, mean=mean_occur)
                    std_dvt = sqrt(variance)
                    headers.extend(["Variance", "Standard Deviation"])
                    data.append([letter, min(occur), max(occur), mean_occur, abs_error, rel_error, variance, std_dvt])
                else:
                    data.append([letter, min(occur), max(occur), mean_occur, abs_error, rel_error])
                if letter == exact_top_k_letters[i]:
                    right_position_letters += 1
                    relative_precision += right_position_letters / (i + 1)

            print(tabulate(data, headers=headers))
            
            avg_relative_precision = relative_precision / self.k * 100
            TP = len([letter for letter in common_top_k_letters.keys() if letter in self.exact_top_k_letters.keys()])
            FP = self.k - TP
            TN = self.alphabet_size - self.k - FP
            precision = TP / self.k * 100
            accuracy = (TP + TN) / self.alphabet_size * 100

            # recall not appropriate since it is evaluated top n most frequent letters
            print(f"Accuracy: {accuracy:.2f} %")
            print(f"Precision: {precision:.2f} %")
            print(f"Average Precision (relative order): {avg_relative_precision:.2f} %")
            
            if self.rep > 1:
                plt.plot(plot_data[0], plot_data[1], label="Total Events Relative Error")
                plt.ylabel("Relative Error (%)")
                plt.xlabel("Repetition")
                plt.title(counter)
                plt.legend()
                plt.show()

                plt.plot(plot_data[0], plot_data[2], label="Mean Relative Error")
                plt.ylabel("Relative Error (%)")
                plt.xlabel("Repetition")
                plt.title(counter)
                plt.legend()
                plt.show()

        print("\n")


    def get_lossy_stats(self, counter):
        print(f"{counter}\n")

        exact_counter = ExactCounter(self.fname)
        exact_count = exact_counter.top_letters()
        lossy_count = counter.count()

        for letter in lossy_count:
            exact_value = exact_count[letter]
            lossy_value = lossy_count[letter]
            acc = round(lossy_value / exact_value * 100, 2)
            print("{:<20} -- Exact: {:<5} | Lossy: {:<5} -- Acc: {:<4}".format(letter, exact_value, lossy_value, acc))
