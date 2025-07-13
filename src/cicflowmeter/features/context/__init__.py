from enum import Enum, auto

from scapy.packet import Packet


class PacketDirection(Enum):
    """Packet Direction creates constants for the direction of the packets.

    There are two given directions that the packets can Feature along
    the line. PacketDirection is an enumeration with the values
    forward (1) and reverse (2).
    """

    FORWARD = auto()
    REVERSE = auto()


def get_packet_flow_key(packet: Packet, direction: PacketDirection) -> tuple:
    """Creates a key signature for a packet.

    Summary:
        Creates a key signature for a packet so it can be
        assigned to a flow.

    Args:
        packet: A network packet
        direction: The direction of a packet

    Returns:
        For TCP/UDP: A tuple of (src_ip, dest_ip, src_port, dest_port)
        For ICMP: A tuple of (src_ip, dest_ip, icmp_type, icmp_id)

    """

    if "TCP" in packet:
        protocol = "TCP"
    elif "UDP" in packet:
        protocol = "UDP"
    elif "ICMP" in packet:
        protocol = "ICMP"
    else:
        raise Exception("Only TCP, UDP, and ICMP protocols are supported.")

    if protocol == "ICMP":
        # For ICMP, use (src_ip, dest_ip, icmp_type, icmp_id) as flow key
        # This groups echo request/reply pairs and other ICMP types appropriately
        icmp_type = packet["ICMP"].type
        # Only echo request/reply have ID field, others use 0
        icmp_id = getattr(packet["ICMP"], 'id', 0) if hasattr(packet["ICMP"], 'id') else 0

        if direction == PacketDirection.FORWARD:
            src_ip = packet["IP"].src
            dest_ip = packet["IP"].dst
            return src_ip, dest_ip, icmp_type, icmp_id
        else:  # REVERSE
            # For ICMP echo reply (type 0), we want to match with echo request (type 8)
            # So we swap IPs and use the request type for consistent flow grouping
            src_ip = packet["IP"].dst
            dest_ip = packet["IP"].src
            # Map echo reply (0) back to echo request (8) for flow grouping
            if icmp_type == 0:  # Echo Reply
                icmp_type = 8  # Echo Request
            return src_ip, dest_ip, icmp_type, icmp_id
    else:
        # TCP/UDP handling (existing logic)
        if direction == PacketDirection.FORWARD:
            dest_ip = packet["IP"].dst
            src_ip = packet["IP"].src
            src_port = packet[protocol].sport
            dest_port = packet[protocol].dport
            # Return the tuple in the order (src_ip, dest_ip, src_port, dest_port) for FORWARD
            return src_ip, dest_ip, src_port, dest_port
        else: # REVERSE
            dest_ip = packet["IP"].src
            src_ip = packet["IP"].dst
            src_port = packet[protocol].dport
            dest_port = packet[protocol].sport
            # Return the tuple in the order (src_ip, dest_ip, src_port, dest_port)
            # The assignments above handle the direction swapping logic.
            return src_ip, dest_ip, src_port, dest_port
