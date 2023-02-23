import os

cmd = 'apt-get'

# check if current user and system-bit
# if os.getuid != 0:
#     print("pls use root user to run the script")
#     exit
        
# if os.uname.machine != 'x86_64':
#     print("Invalid system bit")
#     exit


# if not os.path.is_file('/usr/local/bin/v2ray/v2ray'): 
#     print("V2ray bin not installed")
#     exit

# main menu selection
def v2ray_chan_menu():
    print("1. check v2ray configuration")
    opt = input("Pls input your choose:")
    if opt == '1':
        view_v2ray_config_info()
        

# checking v2ray configuration information        
def view_v2ray_config_info():
    address = "127.0.0.1"
    port = 443
    v2ray_id = 'beam'
    print("---------v2ray configuration--------\n")
    print(f"Address = {address}\nPort = {port}\nUUID = {v2ray_id}\nAlter ID = {alterid}")
    print(f"Network Protocol = {net}\nDisguise Type = {header}\nHost = {host}\nPath = {path}")
    

# downloading v2ray client configuration file
def download_v2ray_client_config():
    print("Downloading v2ray client config file")

    
        


if __name__ == "__main__":
    v2ray_chan_menu()