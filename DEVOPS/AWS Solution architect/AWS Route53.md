# Navigation
- [**Amazon-Route53**](#Amazon-Route53)
- [**CNAME-vs-ALIAS**](#CNAME-vs-ALIAS)
- [**Routing-policies**](#Routing-policies)
	- [Simple](#Simple)
	- [Weighted](#Weighted)
	- [Latency-based](#Latency-based)
	- [Geolocation](#Geolocation)
	- [Geoproximity](#Geoproximity)
	- [Multi-Value](#Multi-Value)
	- [Traffic-flow](#Traffic-flow)
# Amazon-Route53
- A highly available, scalable, fully managed and Authoritative DNS  
- Authoritative = the customer (you) can update the DNS records  
- Route 53 is also a Domain Registrar  
- Ability to check the health of your resources  
- The only AWS service which provides 100% availability SLA
# CNAME-vs-ALIAS
- **CNAME**:  
	- Points a hostname to any *other hostname*. (app.mydomain.com => blabla.anything.com)  
	- ONLY FOR NON ROOT DOMAIN (aka.something.mydomain.com)  
- **Alias**:  
	- Points a hostname to an *AWS Resource* (app.mydomain.com => blabla.amazonaws.com)  
	- Works for ROOT DOMAIN and NON ROOT DOMAIN (aka mydomain.com)  
	- Automatically recognizes changes in the resource's ip
	- Unlike **CNAME**, it can b used for the top node of  a DNS namespaces (Zone Apex)
	- Free of charge  
	- Native health check

# Routing-policies
## Simple
- Route traffic to a single resource
- Can specify multiple values in the same record
- If multiple values are returned, a random one is chosen by the client  
- When Alias enabled, specify only one AWS resource  
- Can’t be associated with Health Checks
## Weighted
- Control the percentage of requests that go to each specific resource
- DNS records must have the same name and type
- Can be associated with health checks
> **Note**: If all records have weight of 0, then all records will be returned equally

## Latency-based
- Redirect to the resource that has the least latency close to us
- Latency is based on traffic between users and aws regions
- Can be associated with Health Checks (has a failover capability)
## Geolocation
- Based on user location
- Should create a **default** record (in case there's no match on location)
- Ca be associated with health checks
## Geoproximity
- Route traffic to your resources based on the geographic location of users and resources  
- Ability to shift more traffic to resources based on the defined bias  
- **To change the size of the geographic region, specify bias values**:  
	- To expand (1 to 99) – more traffic to the resource  
	- To shrink (-1 to -99) – less traffic to the resource  
- **Resources can be**:  
	- AWS resources (specify AWS region)  
	- Non-AWS resources (specify Latitude and Longitude)  
- You must use Route 53 **Traffic Flow** to use this feature
## Multi-Value
Use when routing traffic to multiple resources  
- Route 53 return multiple values/resources  
- Can be associated with Health Checks (return only values for healthy resources)  
- Up to 8 healthy records are returned for each Multi-Value query  
- Multi-Value is not a substitute for having an **ELB**
## Traffic-flow
- Simplify the process of creating and maintaining records in large and complex configurations  
- Visual editor to manage complex routing decision trees  
- Configurations can be saved as **Traffic Flow Policy**