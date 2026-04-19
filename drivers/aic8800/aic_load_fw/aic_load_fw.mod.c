#include <linux/module.h>
#include <linux/export-internal.h>
#include <linux/compiler.h>

MODULE_INFO(name, KBUILD_MODNAME);

__visible struct module __this_module
__section(".gnu.linkonce.this_module") = {
	.name = KBUILD_MODNAME,
	.init = init_module,
#ifdef CONFIG_MODULE_UNLOAD
	.exit = cleanup_module,
#endif
	.arch = MODULE_ARCH_INIT,
};

KSYMTAB_FUNC(get_fw_path, "", "");
KSYMTAB_FUNC(get_testmode, "", "");
KSYMTAB_FUNC(set_testmode, "", "");
KSYMTAB_FUNC(get_hardware_info, "", "");
KSYMTAB_FUNC(get_userconfig_xtal_cap, "", "");
KSYMTAB_FUNC(get_userconfig_txpwr_idx, "", "");
KSYMTAB_FUNC(get_userconfig_txpwr_ofst, "", "");
KSYMTAB_FUNC(aicwf_prealloc_txq_alloc, "", "");

SYMBOL_CRC(get_fw_path, 0x0e95ec6a, "");
SYMBOL_CRC(get_testmode, 0x7851be11, "");
SYMBOL_CRC(set_testmode, 0x40c76f23, "");
SYMBOL_CRC(get_hardware_info, 0x7851be11, "");
SYMBOL_CRC(get_userconfig_xtal_cap, 0x4c5b3f5d, "");
SYMBOL_CRC(get_userconfig_txpwr_idx, 0xfdc1d8a5, "");
SYMBOL_CRC(get_userconfig_txpwr_ofst, 0x37673716, "");
SYMBOL_CRC(aicwf_prealloc_txq_alloc, 0xfb44bbd0, "");

static const struct modversion_info ____versions[]
__used __section("__versions") = {
	{ 0xba1b7dc1, "filp_open" },
	{ 0x7c93c0c5, "usb_alloc_urb" },
	{ 0xce6c3923, "usb_anchor_urb" },
	{ 0xbc068716, "usb_free_urb" },
	{ 0x77570aa0, "skb_put" },
	{ 0x534ed5f3, "__msecs_to_jiffies" },
	{ 0xd710adbf, "__kmalloc_noprof" },
	{ 0x8598b2ba, "consume_skb" },
	{ 0x40a621c5, "snprintf" },
	{ 0x65026e43, "complete" },
	{ 0x49733ad6, "queue_work_on" },
	{ 0x60c9c0b3, "__init_swait_queue_head" },
	{ 0xc87f4bab, "finish_wait" },
	{ 0x5eb30ee8, "usb_register_driver" },
	{ 0xb2fa43dd, "kernel_sigaction" },
	{ 0xfbe7861b, "memcpy" },
	{ 0xcb8b6ec6, "kfree" },
	{ 0x0db8d68d, "prepare_to_wait_event" },
	{ 0x5e505530, "kthread_should_stop" },
	{ 0x16ab4215, "__wake_up" },
	{ 0xe1e1f979, "_raw_spin_lock_irqsave" },
	{ 0xde338d9a, "_raw_spin_lock" },
	{ 0xd272d446, "__fentry__" },
	{ 0xe48388e9, "wake_up_process" },
	{ 0x5a844b26, "__x86_indirect_thunk_rax" },
	{ 0xe8213e80, "_printk" },
	{ 0xbd03ed67, "__ref_stack_chk_guard" },
	{ 0xd272d446, "schedule" },
	{ 0x6ac784f4, "schedule_timeout" },
	{ 0x8f3c0912, "__tracepoint_sched_set_state_tp" },
	{ 0xd272d446, "__stack_chk_fail" },
	{ 0xde338d9a, "_raw_spin_unlock_bh" },
	{ 0x8dc67ef7, "usb_kill_anchored_urbs" },
	{ 0x9479a1e8, "strnlen" },
	{ 0x5a844b26, "__x86_indirect_thunk_rdx" },
	{ 0x57055bb8, "usb_submit_urb" },
	{ 0x90a48d82, "__ubsan_handle_out_of_bounds" },
	{ 0x7a5ffe84, "init_wait_entry" },
	{ 0x77570aa0, "skb_pull" },
	{ 0xbd03ed67, "random_kmalloc_seed" },
	{ 0xd7a59a65, "vmalloc_noprof" },
	{ 0xe981281f, "kmem_cache_free" },
	{ 0x6848eb64, "const_current_task" },
	{ 0x5a844b26, "__x86_indirect_thunk_r13" },
	{ 0x1900ba98, "wait_for_completion_interruptible" },
	{ 0x228b1f9c, "kthread_stop" },
	{ 0x894e7abe, "usb_deregister" },
	{ 0xe54e0a6b, "__fortify_panic" },
	{ 0x81a1a811, "_raw_spin_unlock_irqrestore" },
	{ 0x0e9cab28, "memset" },
	{ 0xf330da6d, "kernel_read" },
	{ 0x23cb3eb0, "skb_dequeue_tail" },
	{ 0xd272d446, "__x86_return_thunk" },
	{ 0xdd0e0f53, "kmem_cache_alloc_noprof" },
	{ 0x5403c125, "__init_waitqueue_head" },
	{ 0x3cc6f0d3, "__netdev_alloc_skb" },
	{ 0x65026e43, "complete_all" },
	{ 0xbc068716, "usb_unanchor_urb" },
	{ 0x1c9578f7, "param_ops_string" },
	{ 0x888b8f57, "strcmp" },
	{ 0xb0767fd1, "skb_unlink" },
	{ 0x02996a3c, "kthread_create_on_node" },
	{ 0x7ec472ba, "__preempt_count" },
	{ 0xf1de9e85, "vfree" },
	{ 0xcf915583, "names_cachep" },
	{ 0xcbae5412, "__const_udelay" },
	{ 0xff967528, "wait_for_completion_killable_timeout" },
	{ 0xc1616ce7, "filp_close" },
	{ 0x957c6137, "__kmalloc_cache_noprof" },
	{ 0xbc068716, "usb_kill_urb" },
	{ 0x2d88a3ab, "cancel_work_sync" },
	{ 0x75738bed, "__warn_printk" },
	{ 0x5a844b26, "__x86_indirect_thunk_r9" },
	{ 0xde338d9a, "_raw_spin_lock_bh" },
	{ 0x95427a88, "send_sig" },
	{ 0xe4de56b4, "__ubsan_handle_load_invalid_value" },
	{ 0x43a349ca, "strlen" },
	{ 0xfc6b01e9, "dev_kfree_skb_any_reason" },
	{ 0x1c9578f7, "param_ops_int" },
	{ 0xde338d9a, "_raw_spin_unlock" },
	{ 0x67628f51, "msleep" },
	{ 0x7851be11, "__SCT__might_resched" },
	{ 0x78339609, "kmalloc_caches" },
	{ 0xb2e62cba, "__trace_set_current_state" },
	{ 0xaef1f20d, "system_wq" },
	{ 0x984622ae, "module_layout" },
};

static const u32 ____version_ext_crcs[]
__used __section("__version_ext_crcs") = {
	0xba1b7dc1,
	0x7c93c0c5,
	0xce6c3923,
	0xbc068716,
	0x77570aa0,
	0x534ed5f3,
	0xd710adbf,
	0x8598b2ba,
	0x40a621c5,
	0x65026e43,
	0x49733ad6,
	0x60c9c0b3,
	0xc87f4bab,
	0x5eb30ee8,
	0xb2fa43dd,
	0xfbe7861b,
	0xcb8b6ec6,
	0x0db8d68d,
	0x5e505530,
	0x16ab4215,
	0xe1e1f979,
	0xde338d9a,
	0xd272d446,
	0xe48388e9,
	0x5a844b26,
	0xe8213e80,
	0xbd03ed67,
	0xd272d446,
	0x6ac784f4,
	0x8f3c0912,
	0xd272d446,
	0xde338d9a,
	0x8dc67ef7,
	0x9479a1e8,
	0x5a844b26,
	0x57055bb8,
	0x90a48d82,
	0x7a5ffe84,
	0x77570aa0,
	0xbd03ed67,
	0xd7a59a65,
	0xe981281f,
	0x6848eb64,
	0x5a844b26,
	0x1900ba98,
	0x228b1f9c,
	0x894e7abe,
	0xe54e0a6b,
	0x81a1a811,
	0x0e9cab28,
	0xf330da6d,
	0x23cb3eb0,
	0xd272d446,
	0xdd0e0f53,
	0x5403c125,
	0x3cc6f0d3,
	0x65026e43,
	0xbc068716,
	0x1c9578f7,
	0x888b8f57,
	0xb0767fd1,
	0x02996a3c,
	0x7ec472ba,
	0xf1de9e85,
	0xcf915583,
	0xcbae5412,
	0xff967528,
	0xc1616ce7,
	0x957c6137,
	0xbc068716,
	0x2d88a3ab,
	0x75738bed,
	0x5a844b26,
	0xde338d9a,
	0x95427a88,
	0xe4de56b4,
	0x43a349ca,
	0xfc6b01e9,
	0x1c9578f7,
	0xde338d9a,
	0x67628f51,
	0x7851be11,
	0x78339609,
	0xb2e62cba,
	0xaef1f20d,
	0x984622ae,
};
static const char ____version_ext_names[]
__used __section("__version_ext_names") =
	"filp_open\0"
	"usb_alloc_urb\0"
	"usb_anchor_urb\0"
	"usb_free_urb\0"
	"skb_put\0"
	"__msecs_to_jiffies\0"
	"__kmalloc_noprof\0"
	"consume_skb\0"
	"snprintf\0"
	"complete\0"
	"queue_work_on\0"
	"__init_swait_queue_head\0"
	"finish_wait\0"
	"usb_register_driver\0"
	"kernel_sigaction\0"
	"memcpy\0"
	"kfree\0"
	"prepare_to_wait_event\0"
	"kthread_should_stop\0"
	"__wake_up\0"
	"_raw_spin_lock_irqsave\0"
	"_raw_spin_lock\0"
	"__fentry__\0"
	"wake_up_process\0"
	"__x86_indirect_thunk_rax\0"
	"_printk\0"
	"__ref_stack_chk_guard\0"
	"schedule\0"
	"schedule_timeout\0"
	"__tracepoint_sched_set_state_tp\0"
	"__stack_chk_fail\0"
	"_raw_spin_unlock_bh\0"
	"usb_kill_anchored_urbs\0"
	"strnlen\0"
	"__x86_indirect_thunk_rdx\0"
	"usb_submit_urb\0"
	"__ubsan_handle_out_of_bounds\0"
	"init_wait_entry\0"
	"skb_pull\0"
	"random_kmalloc_seed\0"
	"vmalloc_noprof\0"
	"kmem_cache_free\0"
	"const_current_task\0"
	"__x86_indirect_thunk_r13\0"
	"wait_for_completion_interruptible\0"
	"kthread_stop\0"
	"usb_deregister\0"
	"__fortify_panic\0"
	"_raw_spin_unlock_irqrestore\0"
	"memset\0"
	"kernel_read\0"
	"skb_dequeue_tail\0"
	"__x86_return_thunk\0"
	"kmem_cache_alloc_noprof\0"
	"__init_waitqueue_head\0"
	"__netdev_alloc_skb\0"
	"complete_all\0"
	"usb_unanchor_urb\0"
	"param_ops_string\0"
	"strcmp\0"
	"skb_unlink\0"
	"kthread_create_on_node\0"
	"__preempt_count\0"
	"vfree\0"
	"names_cachep\0"
	"__const_udelay\0"
	"wait_for_completion_killable_timeout\0"
	"filp_close\0"
	"__kmalloc_cache_noprof\0"
	"usb_kill_urb\0"
	"cancel_work_sync\0"
	"__warn_printk\0"
	"__x86_indirect_thunk_r9\0"
	"_raw_spin_lock_bh\0"
	"send_sig\0"
	"__ubsan_handle_load_invalid_value\0"
	"strlen\0"
	"dev_kfree_skb_any_reason\0"
	"param_ops_int\0"
	"_raw_spin_unlock\0"
	"msleep\0"
	"__SCT__might_resched\0"
	"kmalloc_caches\0"
	"__trace_set_current_state\0"
	"system_wq\0"
	"module_layout\0"
;

MODULE_INFO(depends, "");

MODULE_ALIAS("usb:vA69Cp8800d*dc*dsc*dp*ic*isc*ip*in*");
MODULE_ALIAS("usb:vA69Cp8801d*dc*dsc*dp*ic*isc*ip*in*");

MODULE_INFO(srcversion, "30DC7BD0E0C5F7E3874F435");
