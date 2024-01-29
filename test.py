two_dim_list = [[2, 1], [3, 4], [5, 6]]
indices = list(range(len(two_dim_list)))
indices.sort(key=lambda i: two_dim_list[i][0])
sorted_two_dim_list = [two_dim_list[i] for i in indices]
print(sorted_two_dim_list)
