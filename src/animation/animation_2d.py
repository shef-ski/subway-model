import os
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from src.constants import TrainState
from src.data.nyc_map import NycMap
from src.simulation import Simulation
from src.utils import format_time


def animate_simulation_2d(sim: Simulation,
                          map: NycMap,
                          duration_seconds: int,
                          animation_interval_ms: int,
                          save_video: bool = False,
                          trim_to_square: bool = True,
                          output_dir: str = "."):

    line = sim.lines[0]  # Only visualize first line for now

    # --- Plot setup ---
    fig, ax = plt.subplots(1, 1, figsize=(14, 14))

    if trim_to_square:
        print("Warning: this setting is bugged and currently only used to" \
        "view the whole NYC Map")
        map.trim_map_to_stations_square()
        min_plot_lon, max_plot_lon, min_plot_lat, max_plot_lat = map.square_bounds
        ax.set_xlim(min_plot_lon, max_plot_lon)
        ax.set_ylim(min_plot_lat, max_plot_lat)

    map.geo_df.plot(ax=ax, color='lightgray', edgecolor='white')
    # Set the background color of the axis (plot area)
    ax.set_facecolor('skyblue')
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")

    ax.set_aspect(aspect=0.9, adjustable='box') # aspect = 1 for square

    ax.plot(map.stations_lon, 
            map.stations_lat, 
            '-o',                 
            color='black',          
            markersize=10,     
            linewidth=1,
            label='Subway Line') 

    time_text = ax.text(0.01, 0.90, f'Time: {sim.current_time} s',
                        transform=ax.transAxes)
    
    ax.text(0.01, 0.96, f'Line: {line.name}', transform=ax.transAxes)
    
    train_markers = [ax.plot(0, 0, 's', markersize=10, color='lightgreen')[0]
                     for t in line.get_trains()]
    train_psg = [ax.text(0, 0, f'{len(t.passengers)}', va='center', fontsize=9)
                 for t in line.get_trains()]
    station_n_psg_up = [ax.text(s.lon, s.lat+0.0015, f'{len(s.get_waiting_psg_up())}',
                                va='center', fontsize=9, color="red")
                                for s in line.get_stations()]

    station_n_psg_down = [ax.text(s.lon, s.lat-0.0015,
                                  f'{len(s.get_waiting_psg_down())}',
                                  va='center', fontsize=9, color="blue")
                                  for s in line.get_stations()]

    plt.tight_layout()


    # --- Update function ---
    def update(frames):
        """Update function called by FuncAnimation for each frame.

        Uses matplotlib variables from the outer scope.
        """

        sim.step()
        updates = []  # Artists to be redrawn

        # Add empty train markers if new train was added
        if len(train_markers) < len(line.get_trains()):
            new_t = line.get_trains()[-1]
            train_markers.append(ax.plot(0, 0, 's', markersize=10)[0])
            train_psg.append(ax.text(0, 0, f'{len(new_t.passengers)}', va='center',
                                     fontsize=9))

        # Update train markers and text labels
        for i, train in enumerate(line.get_trains()):
            x_pos = None

            if train.state == TrainState.AT_STATION:
                x_pos = train.current_station.lon
                y_pos = train.current_station.lat
            elif train.state == TrainState.EN_ROUTE:
                # Interpolate position based on time elapsed since departure
                time_since_departure = sim.current_time - train.previous_departure_time
                travel_progress = min(1.0, time_since_departure.total_seconds() /
                                      train.get_travel_time())
                
                start_x = train.prev_station.lon
                start_y = train.prev_station.lat

                next_x = train.next_station.lon
                next_y = train.next_station.lat

                x_pos = start_x + (next_x - start_x) * travel_progress
                y_pos = start_y + (next_y - start_y) * travel_progress

            if x_pos is not None:
                train_markers[i].set_data([x_pos], [y_pos])
                if train.direction == 1:
                    train_markers[i].set_color('red')
                else:
                    train_markers[i].set_color('blue')
                train_psg[i].set_position((x_pos, y_pos))
                train_psg[i].set_text(f"{len(train.passengers)}")
                updates.append(train_markers[i])
                #updates.append(train_texts[i])
                updates.append(train_psg[i])

        for i, station in enumerate(line.get_stations()):
            station_n_psg_up[i].set_text(f"{len(station.get_waiting_psg_up())}")
            station_n_psg_down[i].set_text(f"{len(station.get_waiting_psg_down())}")
            updates.append(station_n_psg_up[i])
            updates.append(station_n_psg_down[i])

        # Update time text
        time_text.set_text(f'Time: {format_time(sim.current_time) }')  # Display time at end of step
        updates.append(time_text)

        return updates  # Return list of modified artists for blitting

    # --- Create and Run Animation ---
    ani = animation.FuncAnimation(fig, update,
                                  frames=duration_seconds,  # duration drives frame count
                                  interval=animation_interval_ms,  # controls playback speed
                                  blit=True,  # smoother animation
                                  repeat=False)

    # --- Save xor Show animation ---
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

