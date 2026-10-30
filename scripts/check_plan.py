#!/usr/bin/env python3
"""Validate the project's planned IPv4 CIDRs and subnet containment.

This local script does not connect to AWS or create resources.
Run: python scripts/check_plan.py
"""
from ipaddress import ip_network

vpc_a = ip_network("10.10.0.0/16")
vpc_b = ip_network("10.20.0.0/16")
subnets = {
    "ewb-a-public": ip_network("10.10.1.0/24"),
    "ewb-a-private": ip_network("10.10.2.0/24"),
    "ewb-b-private": ip_network("10.20.1.0/24"),
}

assert not vpc_a.overlaps(vpc_b), "VPC CIDRs overlap"
assert all(subnets["ewb-a-public"].subnet_of(vpc_a) for _ in [0])
assert subnets["ewb-a-private"].subnet_of(vpc_a)
assert subnets["ewb-b-private"].subnet_of(vpc_b)

subnet_values = list(subnets.values())
for i, first in enumerate(subnet_values):
    for second in subnet_values[i + 1:]:
        assert not first.overlaps(second), f"Subnet CIDRs overlap: {first} and {second}"

print("PASS: VPC CIDRs do not overlap.")
print("PASS: Every subnet is contained within its intended VPC.")
print("PASS: Subnet CIDRs do not overlap.")
print("Note: This validates the written IP plan only; it does not test AWS connectivity.")
