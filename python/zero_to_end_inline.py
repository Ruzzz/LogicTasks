from typing import List

# https://leetcode.com/problems/move-zeroes/


def zero_to_end_inline(arr: List[int]) -> List[int]:
    j = 0  # указатель для "копирования"
    for i, n in enumerate(arr):
        if n != 0:
            if j != i:  # маленькая оптимизация, копируем только если ранее встретились нули
                arr[j] = n
            j += 1   # изменяем только если текущий элемент не ноль, т.е. произвели копирование

    for i in range(j, len(arr)):  # заполняем нулями "хвост"
        arr[i] = 0

    return arr


assert zero_to_end_inline([1, 0, 0, 2, 0, 0]) == [1, 2, 0, 0, 0, 0]
assert zero_to_end_inline([0, 0, 1, 2, 0, 0]) == [1, 2, 0, 0, 0, 0]
assert zero_to_end_inline([0, 0, 0, 0, 1, 2]) == [1, 2, 0, 0, 0, 0]
