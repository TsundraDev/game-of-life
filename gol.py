import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Terrain parameters
terrain_width  = 200
terrain_height = 200
max_tick = 200

# Animation parameters
frequency  = 10         # Frequency in Hz
output_filename = f"gol-{terrain_width}x{terrain_height}.mp4"

# Main algorithm for game of life
def gol(terrain):
    new_terrain = np.zeros(terrain.shape)

    x, y = terrain.shape
    for i in range(x):
        for j in range(y):
            # Calculate neighbours
            neighbours  = terrain[(i-1)%x, (j-1)%y] + terrain[(i-1)%x,  j] + terrain[(i-1)%x, (j+1)%y]
            neighbours += terrain[i, (j-1)%y] + terrain[i, (j+1)%y]
            neighbours += terrain[(i+1)%x, (j-1)%y] + terrain[(i+1)%x,  j] + terrain[(i+1)%x, (j+1)%y]

            # Update tile
            new_terrain[i, j] = 1 if neighbours == 3 else 0

    return new_terrain

# Generate terrain
def generate_terrain_history(width, height, max_tick):
    # Create initial terrain
    terrain_history  = [np.random.randint(0, 2, (width, height))]
    terrain_history += [gol(terrain_history[0])]

    stop_tick = max_tick
    for tick in range(2, max_tick):
        # Update terrain
        terrain_history += [gol(terrain_history[-1])]
        if tick % 10 == 0:
            print(f"Generated tick : {tick}")

        # Stop once terrain has stabilised
        if np.array_equal(terrain_history[-1], terrain_history[-2]):
            return terrain_history, len(terrain_history)

        # Send stop signal when terrain has a repeating pattern %2
        # Other repeating pattern do not appear as frequently if at all
        if stop_tick == max_tick and np.array_equal(terrain_history[-1], terrain_history[-3]):
            # Generate 2 second worth of ticks to display repeating pattern
            stop_tick = min(max_tick, tick + 2 * frequency)

        # Stop generation on stop signal
        if tick == stop_tick:
            return terrain_history, len(terrain_history)

    return terrain_history, len(terrain_history)

# Create animation
def update_frame(frame, ax):
    # Clear frame
    ax.clear()
    ax.axis("off")

    # Draw current frame
    ax.imshow(terrain_history[frame])
    if frame != 0 and frame % 10 == 0:
        print(f"Drawn frame {frame}/{num_frames}")


# Generate terrain
terrain_history, num_frames = generate_terrain_history(terrain_width, terrain_height, max_tick)
print(f"Generated terrain with {num_frames} ticks")

# Draw animation
fig, ax = plt.subplots()
anim = FuncAnimation(fig, update_frame, frames=num_frames, fargs=(ax,), interval=1000/frequency)
anim.save(output_filename, writer='ffmpeg')
print(f"Drawn animation with {num_frames} frames")
