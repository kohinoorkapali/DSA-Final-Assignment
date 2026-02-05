from collections import defaultdict

def max_points_on_line(points):
    max_points = 1

    for i in range(len(points)):
        slopes = defaultdict(int)
        x1, y1 = points[i]

        for j in range(i + 1, len(points)):
            x2, y2 = points[j]

            if x1 == x2:
                slope = 'inf'   # vertical line
            else:
                slope = (y2 - y1) / (x2 - x1)

            slopes[slope] += 1
            max_points = max(max_points, slopes[slope] + 1)

    return max_points


# -------- Example 1 --------
customer_locations = [(1,1), (2,2), (3,3)]
result = max_points_on_line(customer_locations)

print("Example 1 Output:", result)
