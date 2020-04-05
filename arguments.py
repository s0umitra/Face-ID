f = open("config.cfg", "r")
configs = f.readlines()


def arguments():
    # default values
    method = "cnn"
    upscale = 1
    r_res = 1200
    d_res = 1200
    jitters = 100

    for (i, line) in enumerate(configs):
        try:
            if configs[i][0] not in ('#', ' ', '\n'):
                command = line.split('=')
                comm = command[0].strip()

                if comm == 'method' and (command[1].strip() in ("hog", "cnn")):
                    method = command[1].strip()

                elif comm == 'upscale-factor' and (int(command[1].strip()) <= 5):
                    upscale = int(command[1].strip())

                elif comm == 'img-res' and (int(command[1].strip()) <= 4000):
                    r_res = command[1].strip()

                elif comm == 'face-res' and (int(command[1].strip()) <= 4000):
                    d_res = command[1].strip()

                elif comm == 'jitters' and (int(command[1].strip()) <= 200):
                    jitters = command[1].strip()

                else:
                    print("Could not set new value to : " + comm)

        except:
            print("\nError detected in config.cfg")
            break

    return method, upscale, d_res, r_res, jitters
