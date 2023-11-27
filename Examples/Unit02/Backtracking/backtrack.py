def combination_sum(numbers, sum, lowest = -1, print_results = True):
    if sum == 0:
        return []
    results = []
    for i in range(len(numbers)):
        if numbers[i] <= sum and (lowest == -1 or numbers[i] <= lowest):
            ans = combination_sum(numbers, sum-numbers[i], numbers[i], False)
            if len(ans) == 0:
                results += [[numbers[i]]]
            else:
                results += [[numbers[i]]+j for j in ans]
    if print_results:
        for i in results:
            print(i)
    return results

combination_sum([2,4,6,8], 8)

def place_1s(numbers, print_result = True):
    result = [numbers]
    if len(numbers) <= 1:
        if print_result:
            print(numbers)
        return result
    for i in range(1, len(numbers)):
        #insert a 1 at index i, split the list there and run place_1s on each half
        ans_left = [numbers[:i]]
        ans_right = place_1s(numbers[i:], False)
        for a in ans_left:
            for b in ans_right:
                result += [a + [1] + b]
    if print_result:
        for i in result:
            print(i)
    return result

place_1s([2,3,4])