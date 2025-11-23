# Reverse-Engineering

to configure ltrace you can change the conf file in `/etc/ltrace.conf`

add this `int memcmp(addr, addr, int, addr)` so ltrace can print out what `memcmp` is comparing with

