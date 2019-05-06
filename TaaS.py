import paramiko
import time

f1 = open('tenantinput.txt','r')
f2 = open('scripts/connectivitymat.txt','r')
mgmt_ip = {}
# find the management IP of each node
for line2 in f2:
    nodes = line2.split()
    for node in nodes:
        mgmt_ip[node] = '172.17.0.'+str(nodes.index(node)+2)
    break
print("mgmt IP:", mgmt_ip)
# to create tunnels, bridges, add interfaces to bridges in leaf routers
leaf_d ={}
tenants_set = set()
for line in f1:
    leaf = line[1:line.find("}")]
    x = line.split(" ")
    tenant_host_dic ={}
    leaf_host =[]
    for i in range(1,len(x)):
        hosts = x[i][x[i].find('{')+1:x[i].find('}')].split(',')
        print("Hosts:",hosts)
        for hst in hosts:
            leaf_host.append(hst)
        tenant_host_dic[x[i][:x[i].find('-')]]=hosts
        tenants_set.add(x[i][:x[i].find('-')])

    remoteIP = mgmt_ip[leaf]
    username = 'root'
    password = 'root'
    handler = paramiko.SSHClient()
    handler.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    handler.connect(remoteIP, username = username, password = password, look_for_keys = False, allow_agent = False)
    time.sleep(2)
    shell = handler.invoke_shell()
    output = shell.recv(1000)
    shell.send("apt-get install bridge-utils\n") #install bridge utils
    time.sleep(5)
    eth_interface = {}
    print("leaf_host:", leaf_host)
    print('nodes:', nodes)
    # delete the ip of the interface connecting to servers/hosts
    for host in leaf_host:
        print('host:',host)
        eth_interface[host] = 'eth'+str(nodes.index(host)+1)+'1'
        shell.send('ip a show dev eth'+str(nodes.index(host)+1)+'1\n')
        time.sleep(5)
        data = shell.recv(10000)
        pos = data.find('192.168.')
        ip_addr = data[pos:data.find(" ",pos)]
        shell.send('ip add del '+str(ip_addr)+ ' dev eth'+str(nodes.index(host)+1)+'1\n')
        time.sleep(2)
    print(eth_interface)
    # configuration of tenant bridges and adding the intefaces to respective bridges
    # configuration of tenant tunnels
    for tenant in tenant_host_dic:
        #print(tenant, " ", leaf)
        #print('ip link add vxlan'+tenant[6:]+' type vxlan id '+ tenant[6:]+' dstport 4789 local 3.3.3.'+leaf[1:]+' nolearning\n')
        shell.send('brctl addbr '+tenant+'\n')
        time.sleep(2)
        shell.send('ip link add vxlan'+tenant[6:]+' type vxlan id '+ tenant[6:]+' dstport 4789 local 3.3.3.'+leaf[1:]+' nolearning\n')
        time.sleep(2)
        shell.send('ip link set up dev vxlan'+tenant[6:]+'\n')
        time.sleep(2)
        shell.send('ip link set up dev '+tenant+'\n')
        time.sleep(2)
        shell.send('brctl addif '+tenant +' vxlan'+tenant[6:]+'\n')
        time.sleep(2)
        for host in tenant_host_dic[tenant]:
            shell.send('brctl addif '+tenant+' ' + eth_interface[host]+'\n')
    # Configure tenant server's IP address
    for tenant in tenant_host_dic:
        for host in tenant_host_dic[tenant]:
            remoteIP = mgmt_ip[host]
            username = 'root'
            password = 'root'
            handler = paramiko.SSHClient()
            handler.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            handler.connect(remoteIP, username = username, password = password, look_for_keys = False, allow_agent = False)
            time.sleep(2)
            shell = handler.invoke_shell()
            output = shell.recv(1000)
            shell.send('ip a show dev eth'+str(nodes.index(leaf)+1)+'1\n')
            time.sleep(5)
            data = shell.recv(1000)
            pos1 = data.find('192.168.')
            ip_addr1 = data[pos1:data.find(" ",pos1)]
            shell.send('ip add del '+str(ip_addr1)+ ' dev eth'+str(nodes.index(leaf)+1)+'1\n')
            time.sleep(2)
            shell.send('ip add add '+tenant[6:]+'0.'+tenant[6:]+'0.'+tenant[6:]+'0.'+host[1:]+'/24 dev eth'+str(nodes.index(leaf)+1)+'1\n')
            time.sleep(2)
            shell.send('ip a show dev eth'+str(nodes.index(leaf)+1)+'1\n')
            time.sleep(2)
            data = shell.recv(10000)
            print(data)
# configure tenants, tunnels, bridges in Core router
remoteIP = '172.17.0.2';
username = 'root';
password = 'root';
handler = paramiko.SSHClient();
handler.set_missing_host_key_policy(paramiko.AutoAddPolicy());
handler.connect(remoteIP, username = username, password = password, look_for_keys = False, allow_agent = False);
time.sleep(2);
shell = handler.invoke_shell();
output = shell.recv(1000);
shell.send("apt-get install bridge-utils\n");
time.sleep(5);
for tenant in tenants_set:
    shell.send('brctl addbr '+tenant+'\n')
    time.sleep(2)
    shell.send('ip link add vxlan'+tenant[6:]+' type vxlan id '+ tenant[6:]+' dstport 4789 local 1.1.1.1 nolearning\n')
    time.sleep(2)
    shell.send('ip link set up dev vxlan'+tenant[6:]+'\n')
    time.sleep(2)
    shell.send('ip link set up dev '+tenant+'\n')
    time.sleep(2)
    shell.send('brctl addif '+tenant +' vxlan'+tenant[6:]+'\n')
    time.sleep(2)
