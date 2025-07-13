# Python CICFlowMeter with ICMP Support

> **Enhanced Fork**: This is an enhanced version of the original CICFlowMeter with comprehensive ICMP support while maintaining full backward compatibility.

---

## 🚀 **New in This Fork: ICMP Support**

- ✅ **ICMP Traffic Extraction** - Now supports ICMP packets alongside TCP/UDP
- ✅ **Original 82 Features Maintained** - No additional fields, perfect compatibility
- ✅ **3-tuple Flow Identification** - Uses `(src_ip, dst_ip, icmp_type)` for ICMP flows
- ✅ **Echo Request/Reply Pairing** - Automatically groups ping traffic as bidirectional flows
- ✅ **Protocol-Specific Timeouts** - Optimized 60s timeout for ICMP vs 240s for TCP/UDP
- ✅ **Backward Compatible** - Existing TCP/UDP functionality unchanged

### Supported Traffic Types
- **TCP flows** - Full original functionality preserved
- **UDP flows** - Full original functionality preserved
- **ICMP flows** - NEW! Echo requests/replies, unreachable, TTL exceeded, redirects, and more

---

## ⚡️ Version 0.4.2-ma

- **NEW**: Enhanced with ICMP support while maintaining the original 82 features for full compatibility.
- **NEW**: Added `--version` command line option to display version information.
- **ENHANCED**: Improved command line help with better descriptions and examples.

---

## Installation

### Option 1: From Source (Recommended)

```bash
# Clone this enhanced fork
git clone https://github.com/nqmn/cicflowmeter
cd cicflowmeter

# Install dependencies
pip install -e .

# Or using uv (if available)
uv sync
source .venv/bin/activate
```

### Option 2: Direct Installation

```bash
# Install directly from this repository
pip install git+https://github.com/nqmn/cicflowmeter.git
```

### Requirements

- Python 3.8+
- Scapy 2.5.0+
- NumPy 1.26.2+
- SciPy 1.11.4+
- Requests 2.31.0+

## Usage

### Command Line Interface

```bash
usage: cicflowmeter [-h] [--version] (-i INTERFACE | -f FILE) (-c | -u) [--fields FIELD_LIST] [-v] OUTPUT

CICFlowMeter Python Implementation - Network traffic flow analysis tool with support for TCP, UDP, and ICMP protocols

positional arguments:
  OUTPUT                output file name (in CSV mode) or URL (in URL mode)

options:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -i INTERFACE, --interface INTERFACE
                        capture online data from network interface (e.g., eth0, wlan0)
  -f FILE, --file FILE  capture offline data from PCAP file
  -c, --csv             output flows as CSV format
  -u, --url             output flows as HTTP POST requests to URL
  --fields FIELD_LIST   comma-separated list of fields to include in output (default: all 82 features)
  -v, --verbose         enable verbose output for debugging and packet processing details

Examples:
  cicflowmeter -f example.pcap -c flows.csv
  cicflowmeter -i eth0 -c flows.csv -v
  cicflowmeter -f traffic.pcap -u http://localhost:8080/flows
  cicflowmeter -f data.pcap -c output.csv --fields src_ip,dst_ip,protocol
```

### Basic Examples

**Check version:**
```bash
cicflowmeter --version
```

**Get help:**
```bash
cicflowmeter --help
```

**Process PCAP file with ICMP support:**
```bash
cicflowmeter -f example.pcap -c flows.csv
```

**Real-time capture (includes ICMP):** *(requires root permission)*
```bash
cicflowmeter -i eth0 -c flows.csv
```

**Verbose output to see packet processing:**
```bash
cicflowmeter -f example.pcap -c flows.csv -v
```

**Extract specific fields only:**
```bash
cicflowmeter -f example.pcap -c flows.csv --fields "src_ip,dst_ip,src_port,dst_port,protocol,tot_fwd_pkts,tot_bwd_pkts"
```

### Python API

```python
from cicflowmeter.sniffer import create_sniffer

# Process PCAP file
sniffer, session = create_sniffer(
    input_file="example.pcap",
    input_interface=None,
    output_mode="csv",
    output="flows.csv",
    verbose=True
)

sniffer.start()
sniffer.join()
```

## ICMP Support Details

### Supported ICMP Types
- **Echo Request/Reply (Type 8/0)** - Ping traffic with proper request/reply pairing
- **Destination Unreachable (Type 3)** - Network/host unreachable messages
- **Time Exceeded (Type 11)** - TTL exceeded messages (traceroute)
- **Redirect (Type 5)** - ICMP redirect messages
- **All other ICMP types** - Generic support for any ICMP message type

### Flow Identification
- **TCP/UDP flows**: `(src_ip, dst_ip, src_port, dst_port)`
- **ICMP flows**: `(src_ip, dst_ip, icmp_type, icmp_id)`
- **Echo pairing**: Request/reply pairs automatically grouped as bidirectional flows

### Feature Handling for ICMP
- **82 original features maintained** - No additional fields added
- **Non-applicable fields** set to -1 for ICMP flows:
  - `src_port`, `dst_port` → -1
  - TCP flags (`fin_flag_cnt`, `syn_flag_cnt`, etc.) → -1
  - TCP window sizes (`init_fwd_win_byts`, `init_bwd_win_byts`) → -1
- **Protocol-agnostic features** work normally:
  - Packet counts, byte statistics, timing features, etc.

### Sample Output

**ICMP Flow (ping):**
```csv
src_ip,dst_ip,src_port,dst_port,protocol,tot_fwd_pkts,tot_bwd_pkts,flow_duration,fin_flag_cnt
192.168.1.100,8.8.8.8,-1,-1,1,2,1,0.05,-1
```

**TCP Flow (unchanged):**
```csv
src_ip,dst_ip,src_port,dst_port,protocol,tot_fwd_pkts,tot_bwd_pkts,flow_duration,fin_flag_cnt
192.168.1.2,192.168.1.1,12345,80,6,1,0,0.0,0
```

## Examples and Testing

See the `examples/` directory for:
- Sample PCAP files with ICMP traffic
- Generated CSV outputs
- Analysis summaries

### References:

1. [UNB CICFlowMeter](https://www.unb.ca/cic/research/applications.html#CICFlowMeter) - Original CICFlowMeter
2. [Original Java Implementation](https://github.com/ahlashkari/CICFlowMeter) - Reference implementation
3. [Base Python Fork](https://github.com/hieulw/cicflowmeter) - Original Python implementation this fork is based on

## Contributing

Contributions are welcome! Please ensure:
1. Backward compatibility is maintained
2. All tests pass
3. New features include comprehensive tests
4. Documentation is updated

## License

Same as the original CICFlowMeter project.
