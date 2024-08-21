# def get_digit_count(number):
#     temp = "".join(c for c in str(number) if c.isdigit())
#     return len(temp)
#
#
# def get_digit(num, pos):
#     return (num % 10 ** (pos + 1)) // (10 ** pos)
#
#
# def ascending(num_array):
#     works = True if num_array == sorted(num_array) else False
#     return works
#
#
# def single_swap_ascending(num_array):
#     for i, x in enumerate(num_array):
#         x_length = get_digit_count(x)
#         print(f"Length of Number A: {x_length}")
#         for j in range(0, x_length - 1):
#             x_temp = str(abs(x))[j]
#             print(f"Digit to swap 1: {x_temp}")
#             for k, y in enumerate(num_array):
#                 y_length = get_digit_count(y)
#                 print(f"Length of Number B: {y_length}")
#                 for l in range(0, y_length - 1):
#                     y_temp = str(abs(y))[l]
#                     print(f"Digit to swap 2: {y_temp}")
#                     if x < 0:
#                         new_x = x + (10 ** (j) * int(x_temp)) - (10 ** (j) * int(y_temp))
#                         new_y = y + (10 ** (l) * int(y_temp)) - (10 ** (l) * int(x_temp))
#                     else:
#                         new_x = x - (10**(j) * int(x_temp)) + (10**(j) * int(y_temp))
#                         new_y = y - (10**(l) * int(y_temp)) + (10**(l) * int(x_temp))
#                     new_numbers = num_array
#                     new_numbers[i] = int(new_x)
#                     new_numbers[k] = int(new_y)
#                     print(new_numbers)
#                     if new_numbers == sorted(new_numbers):
#                         return True
#     return False
#
#
# numbers = [-8, 5, 6, 16, 5]
# result = single_swap_ascending(numbers)
# print(result)


def solution(arr):
    max_length = 0
    for word in arr:
        max_length = len(word) if len(word) > max_length else max_length

    final_string = ""
    for i in range(0, max_length):
        for word in arr:
            if i < len(word):
                final_string = final_string + word[i]

    return final_string


arr = ["Daisy", "Rose", "Hyacinth", "Poppy"]
final_word = solution(arr)
print(final_word == "DRHPaoyoisapsecpyiynth")
print(final_word)