# Tenant-as-a-Service
Configuration of virtualized multi-tenant data center environment using EVPN-MPBGP

------------------------------------READ ME------------------------------------------
---------------------------TaaS: Tenant-as-a-Service---------------------------------
---------------------------------------by--------------------------------------------
--------------------------------Sandeep Kundala--------------------------------------

Topology



                               +------+
                               |AS 100|
                      +--------|      |------+
                      |        |  C1  |      |
                      |        +------+      |
                      |                      |  
                 +---------+             +--------+
                 | SP1     |             | SP2    |
                 +-+-+-+-+-+             +-+-+-+-++
                   | | |                   | | |
                   | | |                   | | |
                   | | +------------+      | | |
          +--------+ +-+            |      | | |
          |   +----------------------------+ | | 
          |   |        |  +------------------+ | 
          |   |        |  |         |  +-------+   
          |   |        |  |         |  |           
        +-+---+-+   +--+--+-+     +-+--+--+     
        | L1    |   | L2    |     | L3    |     
        |AS 200 |   |AS 200 |     |AS 200 |
        +-------+   +-------+     +-------+
        / |  | \     / |  | \     /  |  |  \
      H1 H2  H3 H4  H5 H6 H7 H8  H9 H10 H11 H12


Procedure:
The program utilizes RND-LAB environment designed by students of NCSU which uses Quaga, FRR and Docker.
The program and the input text file tenantinput.txt should be placed inside the rnd_lab folder/directory.
For successful run of the program:
 1. Make the connectivity matrix for the topology.
 2. give the command ./rnd_lab.bash so that the containers are created.
 3. give router ids to all the routers.
 4. configure OSPF in all the routers such that the networks south of core and north of leaves are advertised.
 5. enable bgp peering and l2vpn evpn peering.
 6. advertise prefixes of the server networks in bgp.
 7. run the python program: python TaaS.py
   
