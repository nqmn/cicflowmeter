import argparse

from scapy.sendrecv import AsyncSniffer

from cicflowmeter import __version__
from cicflowmeter.flow_session import FlowSession


def create_sniffer(
    input_file, input_interface, output_mode, output, fields=None, verbose=False
):
    assert (input_file is None) ^ (input_interface is None), (
        "Either provide interface input or file input not both"
    )
    if fields is not None:
        fields = fields.split(",")

    # Pass config to FlowSession constructor
    session = FlowSession(
        output_mode=output_mode,
        output=output,
        fields=fields,
        verbose=verbose,
    )

    if input_file:
        sniffer = AsyncSniffer(
            offline=input_file,
            filter="ip and (tcp or udp or icmp)",
            prn=session.process,
            store=False,
        )
    else:
        sniffer = AsyncSniffer(
            iface=input_interface,
            filter="ip and (tcp or udp or icmp)",
            prn=session.process,
            store=False,
        )
    return sniffer, session


def main():
    parser = argparse.ArgumentParser(
        prog="cicflowmeter",
        description="CICFlowMeter Python Implementation - Network traffic flow analysis tool with support for TCP, UDP, and ICMP protocols",
        epilog="Examples:\n"
               "  cicflowmeter -f example.pcap -c flows.csv\n"
               "  cicflowmeter -i eth0 -c flows.csv -v\n"
               "  cicflowmeter -f traffic.pcap -u http://localhost:8080/flows\n"
               "  cicflowmeter -f data.pcap -c output.csv --fields src_ip,dst_ip,protocol",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # Version argument
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="show program's version number and exit"
    )

    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        "-i",
        "--interface",
        action="store",
        dest="input_interface",
        metavar="INTERFACE",
        help="capture online data from network interface (e.g., eth0, wlan0)"
    )
    input_group.add_argument(
        "-f",
        "--file",
        action="store",
        dest="input_file",
        metavar="FILE",
        help="capture offline data from PCAP file"
    )

    output_group = parser.add_mutually_exclusive_group(required=True)
    output_group.add_argument(
        "-c",
        "--csv",
        action="store_const",
        const="csv",
        dest="output_mode",
        help="output flows as CSV format"
    )
    output_group.add_argument(
        "-u",
        "--url",
        action="store_const",
        const="url",
        dest="output_mode",
        help="output flows as HTTP POST requests to URL"
    )

    parser.add_argument(
        "output",
        metavar="OUTPUT",
        help="output file name (in CSV mode) or URL (in URL mode)"
    )

    parser.add_argument(
        "--fields",
        action="store",
        dest="fields",
        metavar="FIELD_LIST",
        help="comma-separated list of fields to include in output (default: all 82 features)"
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="enable verbose output for debugging and packet processing details"
    )

    args = parser.parse_args()

    sniffer, session = create_sniffer(
        args.input_file,
        args.input_interface,
        args.output_mode,
        args.output,
        args.fields,
        args.verbose,
    )
    sniffer.start()

    try:
        sniffer.join()
    except KeyboardInterrupt:
        sniffer.stop()
    finally:
        sniffer.join()
        # Flush all flows at the end
        session.flush_flows()


if __name__ == "__main__":
    main()
