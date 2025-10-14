# Hub-and-spoke
- The hub-and-spoke topology is shaped like a star, with the central hub at the center and all the other devices connected to it like spokes on a wheel.
- Instead of managing each device individually, we configure and monitor everything from the hub.
- This topology is a common approach for managing network traffic in Google Cloud environments.
- There is no need for complex routing configurations between individual devices.
- The hub automatically routes traffic between spokes based on predefined rules.
- Scalability: The hub-and-spoke topology can easily accommodate future network growth by adding more spokes.

## Possible-Implementations
1. VPC Network Peering
2. Cloud VPN
3. Network Connectivity Center (NCC)
> Note: [Check the Considerations](https://cloud.google.com/network-connectivity/docs/network-connectivity-center/concepts/overview#considerations)

## Hub-Preset-Topologies
1. **Mesh:** All spokes attached to a hub can communicate with each other in one hub route table. Does not support NCC Gateway spoke type.
2. **Star:** Only designated edge and center spokes can communicate with each other, thus ensuring segmentation and connectivity separation across edge VPC networks.
3. **Hybrid inspection:** Customize traffic processing between your Interconnect and connected VPC networks using an NCC Gateway spoke. Gateway spokes protect VLAN attachments in the `gateways` group. VPC spokes and hybrid spokes can be grouped into `services`, `prod`, or `non-prod` for isolation.
 **Learn More:** [Preset connectivity topologies](https://cloud.google.com/network-connectivity/docs/network-connectivity-center/concepts/connectivity-topologies?_gl=1*11n1i8s*_ga*MTk4NjcxMjMwNi4xNzYwNDQyNzI2*_ga_WH2QY8WWF5*czE3NjA0NDI3MjUkbzEkZzEkdDE3NjA0NDMxNTUkajQ5JGwwJGgw#spoke-groups)> 
> **Note:** We can view the Network Topology in a map view using ` Network Intelligence > Network Topology.`

