# Changelog

## [0.4.2-ma] - 2025-07-13
### Added
- **Version Command**: Added `--version` command line option to display version information
- **Enhanced Help**: Improved command line help with detailed descriptions, examples, and better formatting
- **Program Description**: Added comprehensive program description and usage examples in help text

### Enhanced
- **Argument Parser**: Enhanced argument parser with better metavar names and detailed help descriptions
- **User Experience**: Improved command line interface with clearer option descriptions and examples

## [0.4.2] - 2025-07-13
### Added
- **ICMP Support**: Comprehensive ICMP (Internet Control Message Protocol) traffic extraction and flow analysis
- **3-tuple Flow Identification**: Uses `(src_ip, dst_ip, icmp_type)` for basic ICMP flows and `(src_ip, dst_ip, icmp_type, icmp_id)` for echo packets
- **Echo Request/Reply Pairing**: Automatic bidirectional flow grouping for ping traffic
- **Protocol-Specific Timeouts**: Optimized 60-second timeout for ICMP flows vs 240 seconds for TCP/UDP
- **Comprehensive ICMP Type Support**: Echo Request/Reply (8/0), Destination Unreachable (3), Time Exceeded (11), Redirect (5), and generic support for all ICMP types

### Changed
- **BPF Filter**: Updated from `"ip and (tcp or udp)"` to `"ip and (tcp or udp or icmp)"` to capture ICMP packets
- **Flow Key Generation**: Extended `get_packet_flow_key()` to handle ICMP protocol alongside TCP/UDP
- **Feature Extraction**: Modified flag counting and payload extraction to handle ICMP packets appropriately
- **Flow Session**: Updated packet filtering and timeout handling for mixed protocol traffic

### Enhanced
- **Backward Compatibility**: All existing TCP/UDP functionality preserved unchanged
- **CSV Output**: Maintains original 82 features with ICMP-specific fields set to -1 for non-applicable values (ports, TCP flags, window sizes)
- **Memory Optimization**: Shorter ICMP timeouts reduce memory footprint for short-lived flows
- **Error Handling**: Robust null value handling for ICMP packets without optional fields

### Testing
- **Unit Tests**: 13 comprehensive tests covering ICMP echo, unreachable, TTL exceeded, redirect, and flow key generation
- **Integration Tests**: End-to-end pipeline validation with synthetic PCAP files
- **Backward Compatibility**: Verification that existing TCP/UDP processing remains unchanged

## [0.4.1] - 2025-07-12
### Added
- Initial ICMP support framework
- Basic ICMP packet recognition and flow creation

## [0.4.0] - 2025-06-08
### Changed
- Fork from [Base Python Fork](https://github.com/hieulw/cicflowmeter)
- Major refactor: Now uses a custom FlowSession and the prn callback of AsyncSniffer for all flow processing, instead of relying on Scapy's DefaultSession/session system.
- All flow logic, feature extraction, and output are now fully managed by the project code, not by Scapy internals.
- The process method always returns None, preventing unwanted packet printing by Scapy.
- Logging is robust: only shows debug output if -v is set.
- All flows are always flushed at the end, even for small pcaps.

### Notes
- This project is a CICFlowMeter-like tool (see https://www.unb.ca/cic/research/applications.html#CICFlowMeter), not Cisco NetFlow. It extracts custom flow features as in the original Java CICFlowMeter.
- The refactor does not change the set of features/fields extracted, only how packets are routed to your logic.
