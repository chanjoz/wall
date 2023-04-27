import os, json, jsonpath, subprocess
from shutil import copyfile
from tqdm import tqdm
from urllib.request import urlopen, urlretrieve

# main menu selection
def v2ray_chan_menu():
    print("""---------main menu for selection---------
          1.   check v2ray configuration
          2.   change v2ray configuration
          3.   install v2ray
          4.   config and start v2ray after installation
          5.   restart v2ray""")
    
    opt = input("\nPls choose:")
    if opt == '1':
        view_v2ray_config_info()
    elif opt == '2':
        change_v2ray_config()
    elif opt == '3':
        install_v2ray()
    elif opt == '4':
        start_v2ray()
    elif opt == '5':
        restart_v2ray()
    else:
        print("Invalid input")     

# checking v2ray server configuration information        
def view_v2ray_config_info():
    v2ray_server_config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                            'config', 'server',"conf.json")
    
    with open(v2ray_server_config_file) as server_json:
        server_data = json.load(server_json)
        address = "127.0.0.1"
        port = jsonpath.jsonpath(server_data, '$..port')[0]   
        v2ray_id = jsonpath.jsonpath(server_data, '$..id')[0]
        alterid = jsonpath.jsonpath(server_data, '$..alterId')[0]
        tmpath = jsonpath.jsonpath(server_data, '$..network') 
        if not tmpath:
            network = "tcp"
        else:
            network = tmpath[0]
        
        print("---------v2ray configuration---------\n")
        print(f"Address = {address}\nPort = {port}\nUUID = {v2ray_id}\nAlter ID = {alterid}")
        print(f"Network Protocol = {network }")

# change v2ray server side configuration and update client side config accordingly        
def change_v2ray_config():
    print("""----------v2ray configuration update selection---------
          1.    change v2ray port
          2.    change v2ray transport""")
    
    opt = input("\nPls choose:")
    if opt == '1':
        change_v2ray_ip()
    elif opt == '2':
        change_v2ray_transport()
    else:
        print("Invalid input")
    

def change_v2ray_ip():
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    v2ray_server_config = os.path.join(cur_dir, 'config', 'server', 'conf.json')
    v2ray_client_config = os.path.join(cur_dir, 'config', 'client', 'conf.json')
    
    with open (v2ray_server_config, 'r') as server_json:
        server_data = json.load(server_json)
        old_port = jsonpath.jsonpath(server_data, '$..port')[0]   
        new_port = input("pls input new port number:")
        
    if old_port == new_port:
        print("the input is same as old port number!")
    else:
        # update v2ray server inbounds port
        server_data["inbounds"]["port"] = new_port
        with open (v2ray_server_config, 'w') as server_json:
            json.dump(server_data, server_json, indent=4, sort_keys=True)
        # update v2ray client outbounds port
        with open(v2ray_client_config, 'r') as client_json:
            client_data = json.load(client_json) 
            client_data["outbounds"][0]["settings"]["vnext"][0]["port"] = new_port
        with open (v2ray_client_config, 'w') as client_json:
            json.dump(client_data, client_json, indent=4, sort_keys=True)
        
        # replace v2ray configuration file under /usr/local/etc/v2ray
        etc_config = "/usr/local/etc/v2ray"
        os.mkdir(etc_config)
        copyfile(v2ray_server_config, os.path.join(etc_config, "conf,json"))
        
        restart_v2ray()    
        
# change v2ray transport from TCP to Websocket+TLS+Web
def change_v2ray_transport():
    # install nginx
    subprocess.run("apt-get install nginx", shell=True,
                   stdout=subprocess.PIPE,
                   sterr=subprocess.STDOUT)  
    # setup TLS         
    
# downloading v2ray client configuration file
def download_v2ray_client_config():
    print("Downloading v2ray client config file")
    
# v2ray restart    
def restart_v2ray():
    cmds = ["systemctl restart v2ray"]
    for command in cmds:    
        r = subprocess.run(command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
        )

# bar progress func
def progress_update(pbar, blocknum, blocksize):
    pbar.update(blocksize)

# v2ray new install    
def install_v2ray():
    # get latest version by github repo api
    api_url = "https://api.github.com/repos/v2ray/v2ray-core/releases/latest"
    with urlopen(api_url) as response:
        body = response.read()
        body_json = json.loads(body)
        latest_ver = body_json["tag_name"]  
        download_link = "https://github.com/v2fly/v2ray-core/releases/download/" + latest_ver + "/v2ray-linux-64.zip" 
        file_name = "v2ray_linux64.zip"

    # acquire file size
    u = urlopen(download_link)
    file_size = int(u.headers["Content-Length"])

    # download file and show bar progress
    with tqdm(total=file_size, unit='B', unit_scale=True, desc=file_name) as pbar:
        urlretrieve(download_link, filename=file_name, reporthook=lambda blocknum, blocksize, totalsize: progress_update(pbar, blocknum, blocksize))

    command = "unzip -o -d /usr/local/bin/v2ray v2ray_linux64.zip"

    r = subprocess.run(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
        )
    v2ray_systemd_unit = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'v2ray.service')
    v2ray_system_service = "/usr/local/lib/systemd/system"
    copyfile(v2ray_systemd_unit, v2ray_system_service)
    
# configure and start v2ray server node after installation
def start_v2ray():
    opt = input("Pls choose v2ray transport 'tcp/ws':")

    cur_dir = os.path.dirname(os.path.abspath(__file__))
    v2ray_server_config = os.path.join(cur_dir, 'config', 'server', 'conf.json')
    v2ray_client_config = os.path.join(cur_dir, 'config', 'client', 'conf.json')
    v2ray_server_template = os.path.join(cur_dir, 'template', 'server', opt + '.json')
    v2ray_client_template = os.path.join(cur_dir, 'template', 'client', opt + '.json') 
    
    

if __name__ == "__main__":
    
    cmd = 'apt-get'

    # check if current user and system-bit
    if os.getuid != 0:
        print("pls use root user to run the script")
        exit
            
    if os.uname().machine != 'x86_64':
        print("Invalid system bit")
        exit

    if not os.path.isfile('/usr/local/bin/v2ray/v2ray'): 
        print("V2ray bin not installed")
        exit
    
    v2ray_chan_menu()