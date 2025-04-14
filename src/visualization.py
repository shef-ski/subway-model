import matplotlib.pyplot as plt
import matplotlib.animation as animation

from src.constants import TrainState, TRAVEL_TIME_BETWEEN_STATIONS
from src.simulation import Simulation


def animate_simulation(sim: Simulation,
                       duration_seconds: int,
                       animation_interval_ms: int):

    line = sim.lines[0]  # Only visualize first line for now

    # --- Plot setup ---
    fig, ax = plt.subplots(figsize=(12, 3))
    ax.set_yticks([])
    ax.set_xlim(0.5, len(line.stations) + 0.5)
    ax.set_ylim(-0.5, 1.0)  # Increased ylim slightly for legend
    ax.set_xticks([s.id for s in line.stations])
    ax.plot([s.id for s in line.stations], [0] * len(line.stations),
            '-o', color='grey', markersize=8, label='Line')
    time_text = ax.text(0.01, 0.90, f'Time: {sim.current_time} s', transform=ax.transAxes)
    # Initialize plot elements for trains using placeholder data (0,0)
    train_markers = [ax.plot(0, 0, 's', markersize=10, label=f'{t.id}')[0] for t in line.trains]
    train_texts = [ax.text(0, 0, f' {t.id}', va='center', fontsize=9) for t in line.trains]

    # --- Update function ---
    def update(frames):
        """Update function called by FuncAnimation for each frame.

        Uses matplotlib variables from the outer scope.
        """

        sim.step()
        updates = []  # Artists to be redrawn

        # Update train markers and text labels
        for i, train in enumerate(line.trains):
            x_pos = None
            # y position with some space for individual trains and based on right-side traffic
            y_pos = 0.06 * train * train.direction * -1

            if train.state == TrainState.AT_STATION:
                x_pos = train.current_station.id
            elif train.state == TrainState.EN_ROUTE:
                # Interpolate position based on time elapsed since departure
                time_since_departure = sim.current_time - train.previous_departure_time
                travel_progress = min(1.0, time_since_departure / TRAVEL_TIME_BETWEEN_STATIONS)  # Clamp to max 1.0
                start_station_pos = train.prev_station.id
                end_station_pos = train.next_station.id
                x_pos = start_station_pos + (end_station_pos - start_station_pos) * travel_progress
            if x_pos is not None:
                train_markers[i].set_data([x_pos], [y_pos])
                train_texts[i].set_position((x_pos+0.02, y_pos))  # Position text next to marker
                updates.append(train_markers[i])
                updates.append(train_texts[i])

        # Update time text
        time_text.set_text(f'Time: {sim.current_time - 1} s')  # Display time at end of step
        updates.append(time_text)

        return updates  # Return list of modified artists for blitting

    # --- Create and Run Animation ---
    ani = animation.FuncAnimation(fig, update,
                                  frames=duration_seconds,  # Duration drives frame count
                                  interval=animation_interval_ms,  # Controls playback speed
                                  blit=True,
                                  repeat=False)

    ax.legend(loc='upper right')
    plt.tight_layout()
    plt.show()

    # todo add code to save the visualization as mp4 or similar format
