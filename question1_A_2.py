from collections import defaultdict

def max_points_on_line(points):
    max_points = 1

    for i in range(len(points)):
        slopes = defaultdict(int)
        x1, y1 = points[i]

        for j in range(i + 1, len(points)):
            x2, y2 = points[j]

            if x1 == x2:
                slope = 'inf'  
            else:
                slope = (y2 - y1) / (x2 - x1)

            slopes[slope] += 1
            max_points = max(max_points, slopes[slope] + 1)

    return max_points

customer_locations = [(1,1), (3,2), (5,3), (4,1), (2,3), (1,4)]
result = max_points_on_line(customer_locations)

print("Example 2 Output:", result)
