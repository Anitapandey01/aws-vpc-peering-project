# AWS VPC Peering: Private Network Connectivity

**Project:** EWB VPC Peering  
**Focus:** Amazon VPC, IPv4 CIDR planning, route tables, security groups, EC2, bastion access, and connectivity validation.

## Overview

This project documents a two-VPC AWS network in which private EC2 workloads communicate using private IPv4 addresses over a VPC peering connection. A bastion host in VPC A is the administration entry point. App-A and App-B must not have public IPv4 addresses.

> **Cost and evidence note:** This repository is a project scaffold and implementation guide; it does not create AWS resources automatically. AWS EC2, EBS, and public IPv4 resources may incur charges. Do not launch resources unless your lab account explicitly provides no-cost access or you have checked the current price and budget. Do not claim tests passed until you run them and save your own evidence.

## Architecture

Open [`docs/architecture.svg`](docs/architecture.svg) for the network diagram.

## Address plan

| Resource | VPC/subnet | IPv4 CIDR / address |
|---|---|---|
| `ewb-vpc-a` | VPC A | `10.10.0.0/16` |
| `ewb-a-public` | VPC A public subnet | `10.10.1.0/24` |
| `ewb-a-private` | VPC A private subnet | `10.10.2.0/24` |
| `ewb-vpc-b` | VPC B | `10.20.0.0/16` |
| `ewb-b-private` | VPC B private subnet | `10.20.1.0/24` |
| `ewb-bastion` | Public subnet A | `10.10.1.10` + public IPv4 |
| `ewb-app-a` | Private subnet A | `10.10.2.10`, no public IPv4 |
| `ewb-app-b` | Private subnet B | `10.20.1.10`, no public IPv4 |

The VPC CIDRs do not overlap. The `/24` subnet ranges are contained within their parent VPC CIDRs.

## Route-table design

Keep AWS-created `local` routes. Add the following routes after the peering connection is **Active**:

| Route table | Destination | Target |
|---|---|---|
| `ewb-rt-a-public` | `0.0.0.0/0` | Internet gateway `ewb-igw-a` |
| `ewb-rt-a-public` | `10.20.0.0/16` | Peering connection `pcx-...` |
| `ewb-rt-a-private` | `10.20.0.0/16` | Peering connection `pcx-...` |
| `ewb-rt-b-private` | `10.10.0.0/16` | Peering connection `pcx-...` |

The public route table needs the VPC B route because the bastion initiates SSH to App-B through `ProxyJump`. VPC B's private route table needs the return route to VPC A. VPC peering is not transitive and does not let VPC B use VPC A's internet gateway.

## Security-group rules

Use the actual current public IPv4 address of your administration computer, followed by `/32`, for bastion SSH. Do not use `0.0.0.0/0` for SSH.

| Security group | Inbound rule | Source |
|---|---|---|
| `ewb-sg-bastion` | TCP 22 | Your current public IPv4 `/32` |
| `ewb-sg-app-a` | TCP 22 | `10.10.1.10/32` |
| `ewb-sg-app-a` | ICMP Echo Request | `10.20.1.10/32` |
| `ewb-sg-app-b` | TCP 22 | `10.10.1.10/32` |
| `ewb-sg-app-b` | ICMP Echo Request | `10.10.2.10/32` |

For this beginner lab, default allow-all outbound rules and default network ACLs are assumed. Keep App-A and App-B private (no public IPv4 address).

## Build procedure

1. In one AWS account and one Region, create VPC A (`10.10.0.0/16`) and VPC B (`10.20.0.0/16`).
2. Create the subnets in the address plan. Disable automatic public IPv4 assignment on private subnets.
3. Create and attach `ewb-igw-a` to VPC A.
4. Create the three route tables and explicitly associate each subnet with the correct table.
5. Create the security groups using the rules above.
6. Create an EC2 key pair and store the private key securely on your own computer. Never commit it to GitHub.
7. Launch Amazon Linux instances: bastion in the public subnet, App-A in VPC A private subnet, App-B in VPC B private subnet. Assign the planned private IPs if available; otherwise update all rules and documentation to match actual IPs.
8. Create a VPC peering request from VPC A to VPC B, accept it, and wait for **Active** status.
9. Add the peering routes in both VPCs and the public route table as listed above.
10. Connect to the bastion, then use SSH `ProxyJump` to reach the private instances.
11. Run and capture the validation tests below. Record actual resource IDs in `docs/resource-inventory.md`.
12. Clean up resources when finished to avoid ongoing charges.

## Validation plan

Run these tests only after your resources are ready. Replace addresses with the actual private IPs if you changed them.

| Test | Command/action | Expected result |
|---|---|---|
| Baseline | From App-A, ping App-B before peering routes | No replies |
| Forward path | From App-A: `ping -c 4 10.20.1.10` | Replies if routes, host firewall and ICMP rules are correct |
| Reverse path | From App-B: `ping -c 4 10.10.2.10` | Replies if routes, host firewall and ICMP rules are correct |
| Private SSH | From your laptop: `ssh ewb-app-b` with `ProxyJump` configured | Shell on App-B via bastion |
| Isolation | Confirm App-A and App-B have no public IPv4 addresses | No public IPv4 on either private workload |
| Controlled failure | Temporarily remove only App-B's inbound ICMP Echo Request rule, repeat ping, then restore it | Ping should fail while rule is absent and work again after restoration |

The expected results are acceptance criteria, not pre-recorded test outcomes. Add your own screenshots to `evidence/` after running the lab.

## GitHub submission checklist

- [ ] Replace the name/batch placeholders in `docs/resource-inventory.md`.
- [ ] Add your own architecture/resource screenshots to `evidence/`.
- [ ] Record actual VPC, subnet, route table, instance and peering IDs.
- [ ] Record actual ping/SSH outputs; do not invent results.
- [ ] Remove account IDs, public IPs if you do not want them public, and other sensitive details from screenshots.
- [ ] Confirm no `.pem` key, credentials, tokens, or passwords are included.
- [ ] Explain the forward route, return route, and why active peering alone is insufficient.

## Cleanup

Save evidence first. Terminate the three lab instances, remove any lab EBS volumes/snapshots and Elastic IPs, delete the peering connection and peering routes, delete the lab security groups after network interfaces are gone, then remove subnets, custom route tables, internet gateway, and both VPCs. Check billing after cleanup; usage reporting can lag.
