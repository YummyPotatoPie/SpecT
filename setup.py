import os

def write_config(write_mode):
    with open('config.ini', write_mode) as config:
        config.write("[Telegram]\n")
        config.write("api_id = " + str(input("Please input api_id: ") + "\n"))
        config.write("api_hash = " + str(input("Please input api_hash: ") + "\n"))
        config.write("username = " + str(input("Please input your username: ")))

try:
    if os.path.exists('config.ini'):
        request = input("Rewrite data? Input y (yes) or n (no): ")
        if request == 'y':
            write_config("w")
        else:
            input("Enter any button to exit: ")
    else:
        write_config("x")
        if os.path.exists('csv_data'):
            pass
        else:
            os.mkdir('csv_data')
except Exception:
    print("Something went wrong")

input("Press any key to exit")