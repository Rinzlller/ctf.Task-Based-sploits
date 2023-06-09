#!/usr/bin/env python3

import math

def main():
	amplitude = 2.5
	noise_variance = 0.8
	p_transmit_one = 0.6
	p_transmit_zero = 0.4

	threshold = likelihood_ratio_threshold(amplitude, noise_variance, p_transmit_one, p_transmit_zero)
	ratio = likelihood_ratio_ratio(amplitude, noise_variance, p_transmit_one, p_transmit_zero)
	error_prob_dfm = average_error_probability_dfm(amplitude, noise_variance, p_transmit_one, p_transmit_zero)
	error_prob_optimal = average_error_probability_optimal(amplitude, noise_variance, p_transmit_one, p_transmit_zero)
	error_prob_accumulation = error_probability_accumulation(amplitude, noise_variance, p_transmit_one, p_transmit_zero)

	print("Пороговое отношение правдоподобия:", threshold)
	print("Отношение правдоподобия:", ratio)
	print("Средняя вероятность ошибки при ДФМ:", error_prob_dfm)
	print("Средняя вероятность ошибки при оптимальном приёме:", error_prob_optimal)
	print("Вероятность ошибки при методе синхронного накопления:", error_prob_accumulation)


def likelihood_ratio_threshold(amplitude, noise_variance, p_transmit_one, p_transmit_zero):
    threshold = math.log(p_transmit_one / p_transmit_zero) * (amplitude**2) / (2 * noise_variance)
    return threshold


def likelihood_ratio_ratio(amplitude, noise_variance, p_transmit_one, p_transmit_zero):
    ratio = (p_transmit_one / p_transmit_zero) * math.exp((amplitude**2) / (2 * noise_variance))
    return ratio


def average_error_probability_dfm(amplitude, noise_variance, p_transmit_one, p_transmit_zero):
    threshold = likelihood_ratio_threshold(amplitude, noise_variance, p_transmit_one, p_transmit_zero)
    error_probability = 0.5 * math.erfc(math.sqrt(threshold / 2))
    return error_probability


def average_error_probability_optimal(amplitude, noise_variance, p_transmit_one, p_transmit_zero):
    ratio = likelihood_ratio_ratio(amplitude, noise_variance, p_transmit_one, p_transmit_zero)
    error_probability = 0.5 * (1 - math.sqrt(ratio / (1 + ratio)))
    return error_probability


def error_probability_accumulation(amplitude, noise_variance, p_transmit_one, p_transmit_zero):
    threshold = likelihood_ratio_threshold(amplitude, noise_variance, p_transmit_one, p_transmit_zero)
    error_probability = 0.5 * math.exp(-threshold / 2)
    return error_probability


if __name__ == "__main__":
	main()