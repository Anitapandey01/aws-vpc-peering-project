# Security and routing notes

## Why both directions need routes

A sends a packet to B using the route for `10.20.0.0/16` through the peering connection. B must also have a route for `10.10.0.0/16` through that same peering connection so the reply can return. A one-way route is not sufficient.

## Why App-B sees the bastion as the SSH source

With SSH `ProxyJump`, the laptop connects to the bastion, and the bastion opens a separate TCP connection to App-B. App-B therefore sees the bastion's private IP (`10.10.1.10`) as the source for that SSH connection.

## Why Active peering alone is insufficient

Peering creates the VPC-to-VPC link. Route tables must direct packets to the peer, security groups must allow the traffic, and host firewalls must permit it. A missing return route or inbound ICMP rule can still cause ping to fail.

## Why VPC B does not gain internet access

VPC peering is not a transit gateway and does not forward VPC A's internet-gateway access to VPC B. The lab intentionally gives VPC B no internet gateway and no NAT gateway.

## Security reminders

- Allow SSH to the bastion only from your own current public IPv4 `/32`.
- Allow SSH to private hosts only from the bastion private IP `/32`.
- Never expose SSH to `0.0.0.0/0`.
- Never commit `.pem` files, passwords, AWS access keys, or tokens.
- Use default network ACLs for this beginner lab unless you are prepared to configure return traffic.
