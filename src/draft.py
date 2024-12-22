def get_deadline(x):
    # Calculate the deadline for reaching a cell based on its position (x) and constant K.
    return (abs(x) + 1) * K


# Constant K determines the maximum allowed steps per cell area.
K = 9
# S_max defines the maximum coordinate range.
S_max = 10 ** 6
# Initialize boundaries of visited cells. left is equivalent to the point (0, 1), right is equivalent to the point (1, 0)
left = -1
right = 1
# Our current position. 0 is equivalent to the point (0, 0)
current = 0
# The number of taken steps.
steps = 0
while left >= -S_max or right <= S_max:
    if current + 1 == right:
        # Determine if we need to switch direction or expand further to the right.
        if current + 1 + abs(left) + steps + 1 > get_deadline(left) or right == S_max + 1:
            steps += current + abs(left)
            current = left
            left -= 1
        else:
            steps += 1
            right += 1
            current += 1
    else:
        # Determine if we need to switch direction or expand further upwards.
        if abs(current - 1) + right + steps + 1 > get_deadline(right) or left == -S_max - 1:
            steps += abs(current) + right
            current = right
            right += 1
        else:
            current -= 1
            steps += 1
            left -= 1
    # Check if the deadline is met.
    if get_deadline(current) < steps:
        print("K is too small")
        exit(0)
