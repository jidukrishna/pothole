import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

def generate_pothole_simulation(grid_size=100, num_potholes=5, scale_factor=0.95):
    # Create the grid
    x = np.linspace(-5, 5, grid_size)
    y = np.linspace(-5, 5, grid_size)
    X, Y = np.meshgrid(x, y)

    # Function to create multiple potholes
    def multi_pothole(X, Y, centers, depths, widths):
        Z_multi = np.zeros_like(X)
        for (cx, cy, depth, width) in zip(centers[:, 0], centers[:, 1], depths, widths):
            Z_multi += -np.exp(-((X - cx)**2 + (Y - cy)**2) / (2 * width**2)) * depth
        return Z_multi

    # Define random pothole centers, depths, and widths
    np.random.seed(None)  # Use system time for randomness
    centers = np.random.uniform(-3, 3, (num_potholes, 2))  # Random locations
    depths = np.random.uniform(1.5, 3.5, num_potholes)  # Random depths
    widths = np.random.uniform(0.8, 1.5, num_potholes)  # Random width variations

    # Generate multiple potholes
    Z_multi_uneven = multi_pothole(X, Y, centers, depths, widths)

    # Add depth-only noise for an uneven bottom
    depth_noise_multi = (np.random.rand(*X.shape) - 0.5) * 0.8
    Z_multi_uneven += depth_noise_multi * np.exp(-0.5 * (X**2 + Y**2))

    # Ensure the road surface remains flat at the top
    Z_multi_uneven = np.minimum(0, Z_multi_uneven)

    # Apply Gaussian smoothing to the pothole bottoms
    Z_multi_smoothed = gaussian_filter(Z_multi_uneven, sigma=2)

    # Find the max dimensions
    max_length = np.max(X) - np.min(X)  # X-axis range
    max_height = np.max(Y) - np.min(Y)  # Y-axis range
    max_depth = np.abs(np.min(Z_multi_smoothed))  # Max depth

    # Scale down
    scaled_length = max_length * scale_factor
    scaled_height = max_height * scale_factor
    scaled_depth = max_depth * scale_factor

    # Scale down the X and Y coordinates
    x_scaled = np.linspace(-scaled_length / 2, scaled_length / 2, grid_size)
    y_scaled = np.linspace(-scaled_height / 2, scaled_height / 2, grid_size)
    X_scaled, Y_scaled = np.meshgrid(x_scaled, y_scaled)

    # Scale down the pothole depths
    Z_scaled = Z_multi_smoothed * (scaled_depth / max_depth)

    # Calculate volumes
    dx_original = np.abs(x[1] - x[0])
    dy_original = np.abs(y[1] - y[0])
    volume_original = np.sum(np.abs(Z_multi_uneven) * dx_original * dy_original)

    dx_scaled = np.abs(x_scaled[1] - x_scaled[0])
    dy_scaled = np.abs(y_scaled[1] - y_scaled[0])
    volume_scaled = np.sum(np.abs(Z_scaled) * dx_scaled * dy_scaled)

    # Create a side-by-side comparison plot
    fig, axes = plt.subplots(1, 2, figsize=(12, 5), subplot_kw={"projection": "3d"})

    # Plot Original Rough Pothole Surface
    ax1 = axes[0]
    ax1.plot_surface(X, Y, Z_multi_uneven, cmap='gray', edgecolor='k')
    ax1.set_title(f"Original Rough Potholes\nLength: {max_length:.2f}, Height: {max_height:.2f}, Depth: {max_depth:.2f}\nVolume: {volume_original:.2f} cubic units")
    ax1.set_xlabel("X-axis")
    ax1.set_ylabel("Y-axis")
    ax1.set_zlabel("Depth")

    # Plot Scaled-Down Smoothed Pothole Surface
    ax2 = axes[1]
    ax2.plot_surface(X_scaled, Y_scaled, Z_scaled, cmap='gray', edgecolor='k')
    ax2.set_title(f"Scaled-Down ({scale_factor*100:.0f}%) Smoothed Potholes\nLength: {scaled_length:.2f}, Height: {scaled_height:.2f}, Depth: {scaled_depth:.2f}\nVolume: {volume_scaled:.2f} cubic units")
    ax2.set_xlabel("X-axis")
    ax2.set_ylabel("Y-axis")
    ax2.set_zlabel("Depth")

    # Show the plots
    plt.tight_layout()
    plt.show()

    # Output the volumes
    print(f"Volume of the original rough pothole surface: {volume_original:.2f} cubic units")
    print(f"Volume of the smoothed {scale_factor*100:.0f}% pothole surface: {volume_scaled:.2f} cubic units")
    cuboid = round(scaled_depth * scaled_height * scaled_length, 4)
    print(f"{round(((cuboid - volume_scaled) / cuboid) * 100,2)}%")
    data=[round(volume_original,2), round(volume_scaled,2), round(cuboid,2),round(((cuboid - volume_scaled) / cuboid) * 100,2)]


# Run the function with default parameters
generate_pothole_simulation(60,100,0.95)
