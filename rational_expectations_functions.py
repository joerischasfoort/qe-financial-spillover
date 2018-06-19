import  pickle
import os.path



def check_file_availability(local_dir, obj_label, time_range, seed_range):
    time_count = 0

    for seed in seed_range:
        seed_label = "_seed_" + str(seed) + "_"
        # wait until all files that are needed are available
        while time_count != len(time_range):
            time_count = 0
            for day in time_range:
                filename = local_dir + "objects_day_" + str(day) + seed_label + obj_label + ".pkl"
                time_count += os.path.isfile(filename)

    print("done")