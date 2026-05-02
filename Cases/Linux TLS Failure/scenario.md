# Case: Linux Agent TLS Connection Failure

## Summary
A Linux endpoint could not connect to a management server, while other endpoints on the same subnet were connecting successfully. Initial firewall, route, and TCP connection checks did not identify an obvious local issue.

## Objective
Determine whether the issue is caused by local endpoint configuration, routing, firewall behavior, or something interfering with the TLS connection.

## Approach
Run basic local network checks, test the connection manually, then collect a packet capture during a registration attempt.

## Findings
The packet capture showed that the TCP handshake completed, but the TLS handshake did not complete successfully. This suggests that something along the network path may be inspecting, interrupting, or modifying the TLS session.

## Success Criteria
- Confirm whether TCP connectivity succeeds
- Determine whether TLS negotiation completes
- Identify whether evidence points to endpoint configuration or network-path interference
- Provide enough evidence for escalation to the network/security team