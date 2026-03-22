import time
from scapy.all import sniff, IP, TCP
import database
import notifications

skanowane_porty = {}
PROG_ALARMU = 5 

syn_tracker = {}
SYN_LIMIT = 50
SYN_WINDOW = 2.0

def process_packet(packet):
    # Sprawdzamy, czy to pakiet internetowy (IP) i transportowy (TCP)
    if IP in packet and TCP in packet:
        ip_src = packet[IP].src
        port_dst = packet[TCP].dport
        flagi_tcp = packet[TCP].flags
        
        # --- 1. DETEKCJA SKANOWANIA PORTÓW ---
        if ip_src not in skanowane_porty:
            skanowane_porty[ip_src] = set()
            
        skanowane_porty[ip_src].add(port_dst)
        
        if len(skanowane_porty[ip_src]) > PROG_ALARMU:
            print(f"\n[!] Wykryto skanowanie portów z {ip_src}")
            szczegoly = f"Zeskanowano m.in.: {list(skanowane_porty[ip_src])[:5]}"
            
            database.log_alert(ip_src, "Port Scan", szczegoly)
            notifications.send_discord_alert(ip_src, "Port Scan", szczegoly)
            skanowane_porty[ip_src].clear()

        # --- 2. DETEKCJA SYN FLOOD (DoS) ---
        if flagi_tcp == 'S':
            obecny_czas = time.time()
            
            if ip_src not in syn_tracker:
                syn_tracker[ip_src] = []
                
            syn_tracker[ip_src].append(obecny_czas)
            
            # Usuwamy pakiety spoza naszego 2-sekundowego okna
            syn_tracker[ip_src] = [t for t in syn_tracker[ip_src] if obecny_czas - t <= SYN_WINDOW]
            
            if len(syn_tracker[ip_src]) > SYN_LIMIT:
                print(f"\n[!!!] Atak SYN Flood (DoS) z {ip_src}!")
                szczegoly_dos = f"Ilość SYN: {len(syn_tracker[ip_src])} w {SYN_WINDOW}s"
                
                database.log_alert(ip_src, "SYN Flood (DoS)", szczegoly_dos)
                notifications.send_discord_alert(ip_src, "SYN Flood (DoS)", szczegoly_dos)
                syn_tracker[ip_src].clear()

if __name__ == "__main__":
    database.init_db()
    print("NIDS Engine v4.0 nasłuchuje...")
    sniff(filter="tcp and not port 22", prn=process_packet, store=False)
