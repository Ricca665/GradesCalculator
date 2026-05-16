import subprocess, time
def hard_reset(is_transfermode=True):
    if is_transfermode:
        print("Removing transfer mode flag...")
        subprocess.run(["mpremote", "reset"], capture_output=True, text=False)
        time.sleep(1)
        subprocess.run(["mpremote", "rm", "-rv", ":connection"], capture_output=True, text=True)

    print("Resetting device...")
    subprocess.run(["mpremote", "reset"], capture_output=True, text=True)
    print("Exiting...")
    exit()
