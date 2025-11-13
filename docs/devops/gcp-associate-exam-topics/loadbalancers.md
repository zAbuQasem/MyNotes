# General-Notes

- **Pro Tip**: Use separate health checks for load balancing and for autohealing. Health checks for load balancing detect unresponsive instances and direct traffic away from them. Health checks for autohealing detect and recreate failed instances, so they should be less aggressive than load balancing health checks. Using the same health check for these services would remove the distinction between unresponsive instances and failed instances, causing unnecessary latency and unavailability for your users.

---
# Load-Balancers-in-Google Cloud

## HTTP(S)-Load-Balancer

- **Global Load Balancer**: Distributes HTTP and HTTPS traffic globally.
- **SSL Offloading**: Handles SSL termination to reduce load on backend instances.
- **URL Mapping**: Supports URL-based routing to different backend services.
- **Autoscaling**: Automatically scales backend services to handle traffic spikes.
- **Use Cases**: Ideal for global web applications with content delivery needs.
- [Official Documentation](https://cloud.google.com/load-balancing/docs/https)
---
## Network-Load-Balancer

- **Regional Load Balancer**: Operates at the regional level.
- **TCP/UDP Traffic**: Supports load balancing for TCP and UDP traffic.
- **High Performance**: Handles high-throughput, low-latency applications.
- **Use Cases**: Suitable for gaming servers and VoIP.
- [Official Documentation](https://cloud.google.com/load-balancing/docs/network)
---
## Internal-Load-Balancer

- **Regional Internal Load Balancer**: Designed for internal TCP/UDP traffic.
- **Private Connectivity**: Ensures traffic remains within the Google Cloud network.
- **Health Checks**: Ensures only healthy instances receive traffic.
- **Use Cases**: Suitable for internal applications or services within a VPC.
- [Official Documentation](https://cloud.google.com/load-balancing/docs/internal)
---
## External-Load-Balancer

- **Global or Regional**: Distributes traffic globally or regionally depending on configuration.
- **Protocol Support**: Supports HTTP(S), TCP/SSL Proxy, and UDP traffic.
- **DDoS Protection**: Integrates with Cloud Armor for DDoS mitigation.
- **Use Cases**: Suitable for customer-facing applications with public IPs.
- [Official Documentation](https://cloud.google.com/load-balancing/docs/external)
---
## SSL-Proxy-Load-Balancer

- **SSL Traffic**: Optimized for secure TCP traffic using SSL termination.
- **Global Distribution**: Distributes traffic globally to backend services.
- **Use Cases**: Ideal for applications requiring secure TCP connections.
- [Official Documentation](https://cloud.google.com/load-balancing/docs/ssl-proxy)
---
## TCP-Proxy-Load-Balancer

- **TCP Traffic**: Distributes non-SSL TCP traffic globally.
- **High Performance**: Provides efficient routing for latency-sensitive applications.
- **Use Cases**: Best for non-SSL, latency-sensitive workloads.
- [Official Documentation](https://cloud.google.com/load-balancing/docs/tcp-proxy)

---
# Key-Features-and-Best-Practices

- **Health Checks**:
    - Use dedicated health checks tailored for load balancing and autohealing.
    - Monitor latency, response codes, and packet loss to ensure reliability.
- **Autoscaling**:
    - Enable autoscaling to handle variable traffic patterns.
    - Define scaling policies based on CPU usage, request counts, or custom metrics.
- **Traffic Routing**:
    - Leverage URL and path-based routing for web applications.
    - Use weighted round-robin for traffic distribution.
- **Security**:
    - Enable Cloud Armor for DDoS protection and security policies.
    - Use SSL certificates to secure traffic.
- **Monitoring**:
    - Integrate with Cloud Monitoring and Logging to analyze traffic patterns and backend performance.

---

# Additional-Resources

- [Load Balancing Overview](https://cloud.google.com/load-balancing/docs/overview)
- [Health Check Configurations](https://cloud.google.com/load-balancing/docs/health-checks)
- [Autoscaling Documentation](https://cloud.google.com/compute/docs/autoscaler)