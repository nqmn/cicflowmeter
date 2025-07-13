# ICMP Support in CICFlowMeter

## Overview

This enhanced version of CICFlowMeter now supports ICMP (Internet Control Message Protocol) traffic extraction from .pcap files, in addition to the existing TCP and UDP support. The implementation maintains full backward compatibility while adding comprehensive ICMP flow analysis capabilities.

## Features

### ICMP Flow Identification
- **3-tuple flow identification**: Uses `(src_ip, dst_ip, icmp_type)` for basic ICMP flows
- **4-tuple for echo packets**: Uses `(src_ip, dst_ip, icmp_type, icmp_id)` for ping traffic
- **Bidirectional flow support**: Echo request/reply pairs are automatically grouped into single flows
- **Protocol-specific timeouts**: ICMP flows use shorter timeout (60s) compared to TCP/UDP (240s)

### Supported ICMP Types
- **Echo Request/Reply (Type 8/0)**: Ping traffic with proper request/reply pairing
- **Destination Unreachable (Type 3)**: Network/host unreachable messages
- **Time Exceeded (Type 11)**: TTL exceeded messages (traceroute)
- **Redirect (Type 5)**: ICMP redirect messages
- **All other ICMP types**: Generic support for any ICMP message type

### Feature Count Maintained

✅ **Original 82 features preserved** - No additional fields added to maintain compatibility

### Modified Fields for ICMP

For ICMP flows, the following fields are set to -1 to indicate they are not applicable:

- `src_port`, `dst_port`: Not applicable for ICMP
- `init_fwd_win_byts`, `init_bwd_win_byts`: TCP window sizes
- All TCP flag counts: `fin_flag_cnt`, `syn_flag_cnt`, `rst_flag_cnt`, etc.

## Usage

### Command Line
The usage remains exactly the same as before, with new version and help options:

```bash
# Check version
cicflowmeter --version

# Get detailed help
cicflowmeter --help

# Process PCAP file with ICMP support
cicflowmeter -f example.pcap -c flows.csv

# Real-time capture (includes ICMP)
cicflowmeter -i eth0 -c flows.csv
```

### Python API
```python
from cicflowmeter.sniffer import create_sniffer

# Create sniffer with ICMP support
sniffer, session = create_sniffer(
    input_file="example.pcap",
    input_interface=None,
    output_mode="csv",
    output="flows.csv"
)

sniffer.start()
sniffer.join()
```

## Implementation Details

### Flow Key Generation
- **TCP/UDP**: `(src_ip, dst_ip, src_port, dst_port)`
- **ICMP Echo**: `(src_ip, dst_ip, icmp_type=8, icmp_id)`
- **Other ICMP**: `(src_ip, dst_ip, icmp_type, 0)`

### Echo Request/Reply Pairing
Echo replies (type 0) are automatically mapped to echo requests (type 8) for flow grouping:
- Request: `192.168.1.100 -> 8.8.8.8, type=8, id=1234`
- Reply: `8.8.8.8 -> 192.168.1.100, type=0, id=1234`
- Both packets belong to the same flow with key: `(192.168.1.100, 8.8.8.8, 8, 1234)`

### Timeout Handling
- **ICMP flows**: 60-second timeout (configurable via `ICMP_EXPIRED_UPDATE`)
- **TCP/UDP flows**: 240-second timeout (unchanged)
- **Duration thresholds**: ICMP flows are collected after 30 seconds vs 90 seconds for TCP/UDP

## Testing

### Unit Tests
Comprehensive test suite covering:
- ICMP echo request/reply flows
- Various ICMP message types (unreachable, TTL exceeded, redirect)
- Flow key generation and bidirectional pairing
- Backward compatibility with TCP/UDP flows

### Integration Tests
- End-to-end pipeline testing with real PCAP files
- CSV output validation
- Performance benchmarking

### Running Tests
```bash
# Run all ICMP tests
python -m pytest tests/test_features.py -k icmp -v

# Run integration test
python test_icmp_integration.py

# Run all tests
python -m pytest tests/ -v
```

## Backward Compatibility

✅ **Fully backward compatible**:
- Existing TCP/UDP processing unchanged
- All existing CSV fields preserved
- Same command-line interface
- Same Python API
- Existing ML pipelines continue to work

## Performance

- **Memory usage**: Minimal increase due to additional ICMP fields
- **Processing speed**: Similar performance to TCP/UDP processing
- **Flow timeout**: Optimized shorter timeouts for ICMP reduce memory usage

## Example Output

### ICMP Echo Flow
```csv
src_ip,dst_ip,src_port,dst_port,protocol,tot_fwd_pkts,tot_bwd_pkts,flow_duration,fin_flag_cnt
192.168.1.100,8.8.8.8,-1,-1,1,2,1,0.05,-1
```

### TCP Flow (unchanged)
```csv
src_ip,dst_ip,src_port,dst_port,protocol,tot_fwd_pkts,tot_bwd_pkts,flow_duration,fin_flag_cnt
192.168.1.2,192.168.1.1,12345,80,6,1,0,0.0,0
```

## Configuration

### Constants (in `constants.py`)
```python
EXPIRED_UPDATE = 240        # TCP/UDP timeout (seconds)
ICMP_EXPIRED_UPDATE = 60    # ICMP timeout (seconds)
```

### Customization
You can modify the ICMP timeout by changing `ICMP_EXPIRED_UPDATE` in `src/cicflowmeter/constants.py`.

## Troubleshooting

### Common Issues
1. **No ICMP flows detected**: Ensure your PCAP contains ICMP packets and the filter includes ICMP
2. **Missing ICMP fields**: Update to the latest version and check CSV headers
3. **Performance issues**: Consider adjusting `ICMP_EXPIRED_UPDATE` for your use case

### Debug Mode
Enable verbose logging to see packet processing:
```bash
cicflowmeter -f example.pcap -c flows.csv -v
```

## Contributing

When contributing ICMP-related features:
1. Maintain backward compatibility
2. Add comprehensive tests
3. Update documentation
4. Follow the existing code style
5. Test with various ICMP packet types

## License

Same as the original CICFlowMeter project.
