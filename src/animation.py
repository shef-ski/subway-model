import os
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from src.constants import TrainState, TRAVEL_TIME_BETWEEN_STATIONS
from src.simulation import Simulation


def animate_simulation(sim: Simulation,
                       duration_seconds: int,
                       animation_interval_ms: int,
                       save_video: bool = False,
                       output_dir: str = "."):

    line = sim.lines[0]  # Only visualize first line for now

    # --- Plot setup ---
    fig, ax = plt.subplots(figsize=(12, 3))
    ax.set_yticks([])
    ax.set_xlim(0.5, len(line.stations) + 0.5)
    ax.set_ylim(-2.5, 3.0)  # Increased ylim slightly for legend
    ax.set_xticks([s.id for s in line.stations])
    ax.plot([s.id for s in line.stations], [0] * len(line.stations),
            '-o', color='grey', markersize=8, label='Line')
    time_text = ax.text(0.01, 0.90, f'Time: {sim.current_time} s', transform=ax.transAxes)

    # Initialize plot elements for trains and stations using placeholder data (0,0)
    train_markers = [ax.plot(0, 0, 's', markersize=10)[0] for t in line.trains]
    # train_texts = [ax.text(0, 0, f'{t.id}', va='center', fontsize=9) for t in line.trains]
    train_psg = [ax.text(0, 0, f'{t.n_psg}', va='center', fontsize=9) for t in line.trains]
    station_n_psg_up = [ax.text(s.id, -0.3, f'{s.psg_waiting_up}', va='center', fontsize=9, color="red")
                        for s in line.stations]

    station_n_psg_down = [ax.text(s.id, 0.3, f'{s.psg_waiting_down}', va='center', fontsize=9, color="red")
                          for s in line.stations]

    # --- Update function ---
    def update(frames):
        """Update function called by FuncAnimation for each frame.

        Uses matplotlib variables from the outer scope.
        """

        sim.step()
        updates = []  # Artists to be redrawn

        # Add empty train markers if new train was added
        if len(train_markers) < len(line.trains):
            new_t = line.trains[-1]
            train_markers.append(ax.plot(0, 0, 's', markersize=10)[0])
            train_psg.append(ax.text(0, 0, f'{new_t.n_psg}', va='center', fontsize=9))

        # Update train markers and text labels
        for i, train in enumerate(line.trains):
            x_pos = None
            # y position with some space for individual trains and based on right-side traffic
            y_pos = 0.3 * train.id * train.direction * -1 + (0.3 * train.direction * -1)

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
                # train_texts[i].set_position((x_pos+0.04, y_pos))  # Position text next to marker
                train_psg[i].set_position((x_pos+0.04, y_pos))  # Position text next to marker
                train_psg[i].set_text(f"{train.n_psg}")
                updates.append(train_markers[i])
                #updates.append(train_texts[i])
                updates.append(train_psg[i])

        for i, station in enumerate(line.stations):
            station_n_psg_up[i].set_text(f"{station.psg_waiting_up}")
            station_n_psg_down[i].set_text(f"{station.psg_waiting_down}")
            updates.append(station_n_psg_up[i])
            updates.append(station_n_psg_down[i])

        # Update time text
        time_text.set_text(f'Time: {sim.current_time - 1} s')  # Display time at end of step
        updates.append(time_text)

        return updates  # Return list of modified artists for blitting

    # --- Create and Run Animation ---
    ani = animation.FuncAnimation(fig, update,
                                  frames=duration_seconds,  # duration drives frame count
                                  interval=animation_interval_ms,  # controls playback speed
                                  blit=True,  # smoother animation
                                  repeat=False)

    # --- Save or Show animation ---
    if save_video:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)  # Create output directory if it doesn't exist

        # Define filenames
        output_filename_mp4 = os.path.join(output_dir, "subway_simulation.mp4")
        # output_filename_gif = os.path.join(output_dir, "subway_simulation.gif")

        # --- Try saving as MP4 using ffmpeg ---
        save_fps_video = 30  # Adjust FPS for the saved video (e.g., 30)
        save_dpi = 150  # Adjust DPI for resolution/quality
        try:
            print(f"Attempting to save animation to {output_filename_mp4}...")
            print(f"(Using writer='ffmpeg', fps={save_fps_video}, dpi={save_dpi})")
            # You might need to specify writer='ffmpeg_file' on some systems
            ani.save(output_filename_mp4, writer='ffmpeg', fps=save_fps_video, dpi=save_dpi)
            print(f"Successfully saved MP4: {output_filename_mp4}")
        except FileNotFoundError:
            print("\nERROR: 'ffmpeg' writer not found.")
            print("Please install FFmpeg and ensure it's in your system's PATH.")
            print("See FFmpeg website for installation instructions.\n")
        except Exception as e:
            print(f"\nERROR saving MP4: {e}\n")
    else:
        ax.legend(loc='upper right')
        plt.tight_layout()
        plt.show()
