import matplotlib.pyplot as plt

class graph:

    def __init__(self, y_coords):

        plt.figure()

        # Create an array of x-values (just indices of the list)
        x_coords = list(range(len(y_coords)))

        # Create a plot
        plt.plot(x_coords, y_coords, marker='o', linestyle='-', color='b')

        # Add labels and title
        plt.xlabel('Time')
        plt.ylabel('Value')
        plt.title('Data')

        # Display the plot
        plt.show()