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



static const struct modversion_info ____versions[]
__used __section("__versions") = {
	{ 0x5e4bf025, "cfg80211_inform_bss_frame_data" },
	{ 0xba1b7dc1, "filp_open" },
	{ 0x9dd4105e, "free_irq" },
	{ 0xc45d298e, "is_vmalloc_addr" },
	{ 0x7c93c0c5, "usb_alloc_urb" },
	{ 0x08be25f6, "cfg80211_mgmt_tx_status_ext" },
	{ 0x54c21791, "regulatory_set_wiphy_regd_sync" },
	{ 0xdb839308, "cfg80211_rx_unexpected_4addr_frame" },
	{ 0xce6c3923, "usb_anchor_urb" },
	{ 0xa61fd7aa, "__check_object_size" },
	{ 0xd272d446, "rtnl_unlock" },
	{ 0x1abc7887, "release_firmware" },
	{ 0xd6e79690, "down_timeout" },
	{ 0xbc068716, "usb_free_urb" },
	{ 0x092a35a2, "_copy_from_user" },
	{ 0x44fe0d2f, "eth_mac_addr" },
	{ 0x7dfd5b55, "pci_enable_device" },
	{ 0x77570aa0, "skb_put" },
	{ 0xd272d446, "__rcu_read_lock" },
	{ 0x783fff37, "cfg80211_scan_done" },
	{ 0x534ed5f3, "__msecs_to_jiffies" },
	{ 0xd710adbf, "__kmalloc_noprof" },
	{ 0x8598b2ba, "consume_skb" },
	{ 0x40a621c5, "snprintf" },
	{ 0x65026e43, "complete" },
	{ 0x49733ad6, "queue_work_on" },
	{ 0x503b2d8b, "cfg80211_remain_on_channel_expired" },
	{ 0x21cb1521, "cfg80211_cac_event" },
	{ 0x23cb3eb0, "skb_dequeue" },
	{ 0x60c9c0b3, "__init_swait_queue_head" },
	{ 0xc87f4bab, "finish_wait" },
	{ 0xb0605e43, "dma_unmap_page_attrs" },
	{ 0xc36345fa, "__sw_hweight32" },
	{ 0x545aba25, "request_firmware" },
	{ 0x5eb30ee8, "usb_register_driver" },
	{ 0x40a621c5, "scnprintf" },
	{ 0xee3fc2ff, "ieee80211_amsdu_to_8023s" },
	{ 0xc24925eb, "__pci_register_driver" },
	{ 0x4073d0de, "up" },
	{ 0x12ad300e, "iounmap" },
	{ 0x506e75e8, "ieee80211_chandef_to_operating_class" },
	{ 0x55eab75f, "pci_disable_msi" },
	{ 0xa5c5afbb, "pci_request_regions" },
	{ 0xfbe7861b, "memcpy" },
	{ 0xcb8b6ec6, "kfree" },
	{ 0x2352b148, "timer_delete" },
	{ 0xfdc1d8a5, "get_userconfig_txpwr_idx" },
	{ 0xeebe9074, "cfg80211_external_auth_request" },
	{ 0x0db8d68d, "prepare_to_wait_event" },
	{ 0x9852c24a, "netdev_warn" },
	{ 0x5e505530, "kthread_should_stop" },
	{ 0x2352b148, "timer_delete_sync" },
	{ 0x16ab4215, "__wake_up" },
	{ 0x4776203a, "cfg80211_new_sta" },
	{ 0x4bc34cc3, "unregister_netdevice_queue" },
	{ 0xe1e1f979, "_raw_spin_lock_irqsave" },
	{ 0x33d46dde, "pci_ioremap_bar" },
	{ 0xa3700b72, "cfg80211_disconnected" },
	{ 0x84162d7e, "ether_setup" },
	{ 0xf2c078a6, "pci_unregister_driver" },
	{ 0x9852c24a, "netdev_err" },
	{ 0xd272d446, "__fentry__" },
	{ 0xe48388e9, "wake_up_process" },
	{ 0xe199f25f, "jiffies_to_usecs" },
	{ 0x4b132375, "dev_driver_string" },
	{ 0x5e485e38, "dev_addr_mod" },
	{ 0x91c7ef29, "eth_type_trans" },
	{ 0x5a844b26, "__x86_indirect_thunk_rax" },
	{ 0x303cd268, "dma_map_page_attrs" },
	{ 0x172a80d1, "alloc_netdev_mqs" },
	{ 0xca07a9bc, "wiphy_new_nm" },
	{ 0xe8213e80, "_printk" },
	{ 0xb31ea904, "cfg80211_ready_on_channel" },
	{ 0x5629a063, "strncasecmp" },
	{ 0xbd03ed67, "__ref_stack_chk_guard" },
	{ 0x6ac784f4, "schedule_timeout" },
	{ 0xd272d446, "schedule" },
	{ 0x28afa247, "cfg80211_classify8021d" },
	{ 0x8f3c0912, "__tracepoint_sched_set_state_tp" },
	{ 0xd272d446, "__stack_chk_fail" },
	{ 0x8ce83585, "queue_delayed_work_on" },
	{ 0xde338d9a, "_raw_spin_unlock_bh" },
	{ 0xd710adbf, "__kmalloc_large_noprof" },
	{ 0x60ee008f, "wiphy_register" },
	{ 0xf64ac983, "__copy_overflow" },
	{ 0x8dc67ef7, "usb_kill_anchored_urbs" },
	{ 0x9479a1e8, "strnlen" },
	{ 0x99de96ce, "cfg80211_put_bss" },
	{ 0x734d4262, "cfg80211_roamed" },
	{ 0x6dca6b6b, "cfg80211_ch_switch_notify" },
	{ 0x5a844b26, "__x86_indirect_thunk_rdx" },
	{ 0x57055bb8, "usb_submit_urb" },
	{ 0x68fa39a0, "skb_copy_expand" },
	{ 0xc3105e2c, "skb_queue_tail" },
	{ 0x61079369, "print_hex_dump" },
	{ 0x1f232406, "ieee80211_get_channel_khz" },
	{ 0x90a48d82, "__ubsan_handle_out_of_bounds" },
	{ 0xbd03ed67, "page_offset_base" },
	{ 0x7138ebcd, "__cfg80211_radar_event" },
	{ 0x7851be11, "get_testmode" },
	{ 0x26226372, "cfg80211_find_elem_match" },
	{ 0x9c0551c6, "tasklet_kill" },
	{ 0xf36c79f1, "pci_clear_master" },
	{ 0x7a5ffe84, "init_wait_entry" },
	{ 0x21d58255, "pci_enable_msi" },
	{ 0xfa4174ad, "_dev_err" },
	{ 0x07bc7e7e, "sort" },
	{ 0x6a72b0e5, "simple_open" },
	{ 0x77570aa0, "skb_pull" },
	{ 0x9126ce86, "request_threaded_irq" },
	{ 0x630954b9, "__write_overflow_field" },
	{ 0xd272d446, "__rcu_read_unlock" },
	{ 0x32feeafc, "mod_timer" },
	{ 0xcdec1689, "tasklet_init" },
	{ 0x4073d0de, "down" },
	{ 0xbd03ed67, "random_kmalloc_seed" },
	{ 0xd7a59a65, "vmalloc_noprof" },
	{ 0xbd4294b2, "cfg80211_michael_mic_failure" },
	{ 0xd2d74ba0, "cfg80211_cqm_pktloss_notify" },
	{ 0xbeb1d261, "destroy_workqueue" },
	{ 0xf46d5bf3, "mutex_lock" },
	{ 0x77570aa0, "skb_push" },
	{ 0xe981281f, "kmem_cache_free" },
	{ 0xe182ab80, "debugfs_remove" },
	{ 0xd768e109, "pci_read_config_word" },
	{ 0x2435d559, "strncmp" },
	{ 0x4776203a, "cfg80211_del_sta_sinfo" },
	{ 0xca60ed1e, "netif_receive_skb" },
	{ 0x6848eb64, "const_current_task" },
	{ 0xc609ff70, "strncpy" },
	{ 0x9c0551c6, "__tasklet_schedule" },
	{ 0xd3ed45de, "strcasecmp" },
	{ 0x5a844b26, "__x86_indirect_thunk_r13" },
	{ 0x6cfacb90, "wiphy_unregister" },
	{ 0xd5812452, "free_netdev" },
	{ 0x1900ba98, "wait_for_completion_interruptible" },
	{ 0xbd03ed67, "phys_base" },
	{ 0x680628e7, "ktime_get_real_ts64" },
	{ 0x7bd1523a, "cfg80211_notify_new_peer_candidate" },
	{ 0x402db74e, "memcmp" },
	{ 0x228b1f9c, "kthread_stop" },
	{ 0x173ec8da, "sscanf" },
	{ 0xc1e6c71e, "__mutex_init" },
	{ 0x894e7abe, "usb_deregister" },
	{ 0xe54e0a6b, "__fortify_panic" },
	{ 0xe199f25f, "jiffies_to_msecs" },
	{ 0x81a1a811, "_raw_spin_unlock_irqrestore" },
	{ 0x9b4b48a0, "_ctype" },
	{ 0xd5812452, "netif_tx_stop_all_queues" },
	{ 0x91f8c41a, "netif_tx_wake_queue" },
	{ 0x85acaba2, "cancel_delayed_work" },
	{ 0x7295b8c3, "ieee80211_freq_khz_to_channel" },
	{ 0x0e9cab28, "memset" },
	{ 0xfb44bbd0, "aicwf_prealloc_txq_alloc" },
	{ 0xf36c79f1, "pci_set_master" },
	{ 0xf330da6d, "kernel_read" },
	{ 0x1c9578f7, "param_ops_charp" },
	{ 0x23cb3eb0, "skb_dequeue_tail" },
	{ 0xbeb1d261, "__flush_workqueue" },
	{ 0xd272d446, "__x86_return_thunk" },
	{ 0xf35617a7, "debugfs_create_u32" },
	{ 0xdd0e0f53, "kmem_cache_alloc_noprof" },
	{ 0x092a35a2, "_copy_to_user" },
	{ 0x5403c125, "__init_waitqueue_head" },
	{ 0xca60ed1e, "netif_rx" },
	{ 0x3cc6f0d3, "__netdev_alloc_skb" },
	{ 0x65026e43, "complete_all" },
	{ 0xbc068716, "usb_unanchor_urb" },
	{ 0x7fd710be, "__kmem_cache_create_args" },
	{ 0x40c76f23, "set_testmode" },
	{ 0x1c9578f7, "param_ops_string" },
	{ 0x888b8f57, "strcmp" },
	{ 0x2806a76d, "cfg80211_ch_switch_started_notify" },
	{ 0xb0767fd1, "skb_unlink" },
	{ 0x2c3de8e5, "__dynamic_netdev_dbg" },
	{ 0x058c185a, "jiffies" },
	{ 0x02996a3c, "kthread_create_on_node" },
	{ 0x7a6661ca, "ktime_get_real_seconds" },
	{ 0xdd6830c7, "sprintf" },
	{ 0xbd03ed67, "vmemmap_base" },
	{ 0x82fd7238, "__ubsan_handle_shift_out_of_bounds" },
	{ 0x7ec472ba, "__preempt_count" },
	{ 0x63cd58f2, "cfg80211_unregister_wdev" },
	{ 0xf1a452e6, "__dev_queue_xmit" },
	{ 0x9ccf35e1, "cfg80211_probe_status" },
	{ 0xf1de9e85, "vfree" },
	{ 0x0fbdc0f7, "cfg80211_stop_iface" },
	{ 0x5f6ca7a8, "cfg80211_rx_mgmt_ext" },
	{ 0xf46d5bf3, "mutex_unlock" },
	{ 0xcf915583, "names_cachep" },
	{ 0x1c9578f7, "param_ops_bool" },
	{ 0xaa0f4c13, "pci_release_regions" },
	{ 0x3f7ce9b9, "__dma_sync_single_for_device" },
	{ 0xcbae5412, "__const_udelay" },
	{ 0xff967528, "wait_for_completion_killable_timeout" },
	{ 0xb9e023c2, "pci_write_config_byte" },
	{ 0xc1616ce7, "filp_close" },
	{ 0x957c6137, "__kmalloc_cache_noprof" },
	{ 0xbc068716, "usb_kill_urb" },
	{ 0x2d88a3ab, "cancel_work_sync" },
	{ 0x546c19d9, "validate_usercopy_range" },
	{ 0x75738bed, "__warn_printk" },
	{ 0x62306a9a, "netif_carrier_off" },
	{ 0x5a844b26, "__x86_indirect_thunk_r9" },
	{ 0x71798f7e, "delayed_work_timer_fn" },
	{ 0x7fd36f2e, "time64_to_tm" },
	{ 0xde338d9a, "_raw_spin_lock_bh" },
	{ 0x62306a9a, "netif_carrier_on" },
	{ 0x5954e9cb, "debugfs_create_file_full" },
	{ 0x146ee687, "cfg80211_chandef_create" },
	{ 0xd272d446, "rtnl_lock" },
	{ 0xee9b7bc8, "cfg80211_ft_event" },
	{ 0xf36c79f1, "pci_disable_device" },
	{ 0x37673716, "get_userconfig_txpwr_ofst" },
	{ 0x02f9bbf0, "timer_init_key" },
	{ 0x224a53e7, "get_random_bytes" },
	{ 0x5a844b26, "__x86_indirect_thunk_r12" },
	{ 0x8e3336dd, "disable_irq_nosync" },
	{ 0xdf4bee3d, "alloc_workqueue_noprof" },
	{ 0xe4de56b4, "__ubsan_handle_load_invalid_value" },
	{ 0x43a349ca, "strlen" },
	{ 0xfc6b01e9, "dev_kfree_skb_any_reason" },
	{ 0xf41e64be, "cfg80211_report_obss_beacon_khz" },
	{ 0x54c21791, "regulatory_set_wiphy_regd" },
	{ 0x1c9578f7, "param_ops_int" },
	{ 0x92f76524, "skb_append" },
	{ 0x7c07e6b1, "debugfs_create_dir" },
	{ 0xeb1741e6, "pci_write_config_word" },
	{ 0x0e95ec6a, "get_fw_path" },
	{ 0x0232ea06, "generic_file_llseek" },
	{ 0xde338d9a, "_raw_spin_unlock" },
	{ 0x437e81c7, "simple_read_from_buffer" },
	{ 0x6c65a26b, "cfg80211_connect_done" },
	{ 0x6cfacb90, "wiphy_free" },
	{ 0x67628f51, "msleep" },
	{ 0x067c4275, "cfg80211_cqm_rssi_notify" },
	{ 0x7851be11, "__SCT__might_resched" },
	{ 0x78339609, "kmalloc_caches" },
	{ 0xb2e62cba, "__trace_set_current_state" },
	{ 0x9852c24a, "netdev_info" },
	{ 0x6da5974d, "kmem_cache_destroy" },
	{ 0xc3105e2c, "skb_queue_head" },
	{ 0xaef1f20d, "system_wq" },
	{ 0x2d88a3ab, "flush_work" },
	{ 0x4f1fdcb1, "cfg80211_rx_unprot_mlme_mgmt" },
	{ 0x97a16f65, "register_netdevice" },
	{ 0x984622ae, "module_layout" },
};

static const u32 ____version_ext_crcs[]
__used __section("__version_ext_crcs") = {
	0x5e4bf025,
	0xba1b7dc1,
	0x9dd4105e,
	0xc45d298e,
	0x7c93c0c5,
	0x08be25f6,
	0x54c21791,
	0xdb839308,
	0xce6c3923,
	0xa61fd7aa,
	0xd272d446,
	0x1abc7887,
	0xd6e79690,
	0xbc068716,
	0x092a35a2,
	0x44fe0d2f,
	0x7dfd5b55,
	0x77570aa0,
	0xd272d446,
	0x783fff37,
	0x534ed5f3,
	0xd710adbf,
	0x8598b2ba,
	0x40a621c5,
	0x65026e43,
	0x49733ad6,
	0x503b2d8b,
	0x21cb1521,
	0x23cb3eb0,
	0x60c9c0b3,
	0xc87f4bab,
	0xb0605e43,
	0xc36345fa,
	0x545aba25,
	0x5eb30ee8,
	0x40a621c5,
	0xee3fc2ff,
	0xc24925eb,
	0x4073d0de,
	0x12ad300e,
	0x506e75e8,
	0x55eab75f,
	0xa5c5afbb,
	0xfbe7861b,
	0xcb8b6ec6,
	0x2352b148,
	0xfdc1d8a5,
	0xeebe9074,
	0x0db8d68d,
	0x9852c24a,
	0x5e505530,
	0x2352b148,
	0x16ab4215,
	0x4776203a,
	0x4bc34cc3,
	0xe1e1f979,
	0x33d46dde,
	0xa3700b72,
	0x84162d7e,
	0xf2c078a6,
	0x9852c24a,
	0xd272d446,
	0xe48388e9,
	0xe199f25f,
	0x4b132375,
	0x5e485e38,
	0x91c7ef29,
	0x5a844b26,
	0x303cd268,
	0x172a80d1,
	0xca07a9bc,
	0xe8213e80,
	0xb31ea904,
	0x5629a063,
	0xbd03ed67,
	0x6ac784f4,
	0xd272d446,
	0x28afa247,
	0x8f3c0912,
	0xd272d446,
	0x8ce83585,
	0xde338d9a,
	0xd710adbf,
	0x60ee008f,
	0xf64ac983,
	0x8dc67ef7,
	0x9479a1e8,
	0x99de96ce,
	0x734d4262,
	0x6dca6b6b,
	0x5a844b26,
	0x57055bb8,
	0x68fa39a0,
	0xc3105e2c,
	0x61079369,
	0x1f232406,
	0x90a48d82,
	0xbd03ed67,
	0x7138ebcd,
	0x7851be11,
	0x26226372,
	0x9c0551c6,
	0xf36c79f1,
	0x7a5ffe84,
	0x21d58255,
	0xfa4174ad,
	0x07bc7e7e,
	0x6a72b0e5,
	0x77570aa0,
	0x9126ce86,
	0x630954b9,
	0xd272d446,
	0x32feeafc,
	0xcdec1689,
	0x4073d0de,
	0xbd03ed67,
	0xd7a59a65,
	0xbd4294b2,
	0xd2d74ba0,
	0xbeb1d261,
	0xf46d5bf3,
	0x77570aa0,
	0xe981281f,
	0xe182ab80,
	0xd768e109,
	0x2435d559,
	0x4776203a,
	0xca60ed1e,
	0x6848eb64,
	0xc609ff70,
	0x9c0551c6,
	0xd3ed45de,
	0x5a844b26,
	0x6cfacb90,
	0xd5812452,
	0x1900ba98,
	0xbd03ed67,
	0x680628e7,
	0x7bd1523a,
	0x402db74e,
	0x228b1f9c,
	0x173ec8da,
	0xc1e6c71e,
	0x894e7abe,
	0xe54e0a6b,
	0xe199f25f,
	0x81a1a811,
	0x9b4b48a0,
	0xd5812452,
	0x91f8c41a,
	0x85acaba2,
	0x7295b8c3,
	0x0e9cab28,
	0xfb44bbd0,
	0xf36c79f1,
	0xf330da6d,
	0x1c9578f7,
	0x23cb3eb0,
	0xbeb1d261,
	0xd272d446,
	0xf35617a7,
	0xdd0e0f53,
	0x092a35a2,
	0x5403c125,
	0xca60ed1e,
	0x3cc6f0d3,
	0x65026e43,
	0xbc068716,
	0x7fd710be,
	0x40c76f23,
	0x1c9578f7,
	0x888b8f57,
	0x2806a76d,
	0xb0767fd1,
	0x2c3de8e5,
	0x058c185a,
	0x02996a3c,
	0x7a6661ca,
	0xdd6830c7,
	0xbd03ed67,
	0x82fd7238,
	0x7ec472ba,
	0x63cd58f2,
	0xf1a452e6,
	0x9ccf35e1,
	0xf1de9e85,
	0x0fbdc0f7,
	0x5f6ca7a8,
	0xf46d5bf3,
	0xcf915583,
	0x1c9578f7,
	0xaa0f4c13,
	0x3f7ce9b9,
	0xcbae5412,
	0xff967528,
	0xb9e023c2,
	0xc1616ce7,
	0x957c6137,
	0xbc068716,
	0x2d88a3ab,
	0x546c19d9,
	0x75738bed,
	0x62306a9a,
	0x5a844b26,
	0x71798f7e,
	0x7fd36f2e,
	0xde338d9a,
	0x62306a9a,
	0x5954e9cb,
	0x146ee687,
	0xd272d446,
	0xee9b7bc8,
	0xf36c79f1,
	0x37673716,
	0x02f9bbf0,
	0x224a53e7,
	0x5a844b26,
	0x8e3336dd,
	0xdf4bee3d,
	0xe4de56b4,
	0x43a349ca,
	0xfc6b01e9,
	0xf41e64be,
	0x54c21791,
	0x1c9578f7,
	0x92f76524,
	0x7c07e6b1,
	0xeb1741e6,
	0x0e95ec6a,
	0x0232ea06,
	0xde338d9a,
	0x437e81c7,
	0x6c65a26b,
	0x6cfacb90,
	0x67628f51,
	0x067c4275,
	0x7851be11,
	0x78339609,
	0xb2e62cba,
	0x9852c24a,
	0x6da5974d,
	0xc3105e2c,
	0xaef1f20d,
	0x2d88a3ab,
	0x4f1fdcb1,
	0x97a16f65,
	0x984622ae,
};
static const char ____version_ext_names[]
__used __section("__version_ext_names") =
	"cfg80211_inform_bss_frame_data\0"
	"filp_open\0"
	"free_irq\0"
	"is_vmalloc_addr\0"
	"usb_alloc_urb\0"
	"cfg80211_mgmt_tx_status_ext\0"
	"regulatory_set_wiphy_regd_sync\0"
	"cfg80211_rx_unexpected_4addr_frame\0"
	"usb_anchor_urb\0"
	"__check_object_size\0"
	"rtnl_unlock\0"
	"release_firmware\0"
	"down_timeout\0"
	"usb_free_urb\0"
	"_copy_from_user\0"
	"eth_mac_addr\0"
	"pci_enable_device\0"
	"skb_put\0"
	"__rcu_read_lock\0"
	"cfg80211_scan_done\0"
	"__msecs_to_jiffies\0"
	"__kmalloc_noprof\0"
	"consume_skb\0"
	"snprintf\0"
	"complete\0"
	"queue_work_on\0"
	"cfg80211_remain_on_channel_expired\0"
	"cfg80211_cac_event\0"
	"skb_dequeue\0"
	"__init_swait_queue_head\0"
	"finish_wait\0"
	"dma_unmap_page_attrs\0"
	"__sw_hweight32\0"
	"request_firmware\0"
	"usb_register_driver\0"
	"scnprintf\0"
	"ieee80211_amsdu_to_8023s\0"
	"__pci_register_driver\0"
	"up\0"
	"iounmap\0"
	"ieee80211_chandef_to_operating_class\0"
	"pci_disable_msi\0"
	"pci_request_regions\0"
	"memcpy\0"
	"kfree\0"
	"timer_delete\0"
	"get_userconfig_txpwr_idx\0"
	"cfg80211_external_auth_request\0"
	"prepare_to_wait_event\0"
	"netdev_warn\0"
	"kthread_should_stop\0"
	"timer_delete_sync\0"
	"__wake_up\0"
	"cfg80211_new_sta\0"
	"unregister_netdevice_queue\0"
	"_raw_spin_lock_irqsave\0"
	"pci_ioremap_bar\0"
	"cfg80211_disconnected\0"
	"ether_setup\0"
	"pci_unregister_driver\0"
	"netdev_err\0"
	"__fentry__\0"
	"wake_up_process\0"
	"jiffies_to_usecs\0"
	"dev_driver_string\0"
	"dev_addr_mod\0"
	"eth_type_trans\0"
	"__x86_indirect_thunk_rax\0"
	"dma_map_page_attrs\0"
	"alloc_netdev_mqs\0"
	"wiphy_new_nm\0"
	"_printk\0"
	"cfg80211_ready_on_channel\0"
	"strncasecmp\0"
	"__ref_stack_chk_guard\0"
	"schedule_timeout\0"
	"schedule\0"
	"cfg80211_classify8021d\0"
	"__tracepoint_sched_set_state_tp\0"
	"__stack_chk_fail\0"
	"queue_delayed_work_on\0"
	"_raw_spin_unlock_bh\0"
	"__kmalloc_large_noprof\0"
	"wiphy_register\0"
	"__copy_overflow\0"
	"usb_kill_anchored_urbs\0"
	"strnlen\0"
	"cfg80211_put_bss\0"
	"cfg80211_roamed\0"
	"cfg80211_ch_switch_notify\0"
	"__x86_indirect_thunk_rdx\0"
	"usb_submit_urb\0"
	"skb_copy_expand\0"
	"skb_queue_tail\0"
	"print_hex_dump\0"
	"ieee80211_get_channel_khz\0"
	"__ubsan_handle_out_of_bounds\0"
	"page_offset_base\0"
	"__cfg80211_radar_event\0"
	"get_testmode\0"
	"cfg80211_find_elem_match\0"
	"tasklet_kill\0"
	"pci_clear_master\0"
	"init_wait_entry\0"
	"pci_enable_msi\0"
	"_dev_err\0"
	"sort\0"
	"simple_open\0"
	"skb_pull\0"
	"request_threaded_irq\0"
	"__write_overflow_field\0"
	"__rcu_read_unlock\0"
	"mod_timer\0"
	"tasklet_init\0"
	"down\0"
	"random_kmalloc_seed\0"
	"vmalloc_noprof\0"
	"cfg80211_michael_mic_failure\0"
	"cfg80211_cqm_pktloss_notify\0"
	"destroy_workqueue\0"
	"mutex_lock\0"
	"skb_push\0"
	"kmem_cache_free\0"
	"debugfs_remove\0"
	"pci_read_config_word\0"
	"strncmp\0"
	"cfg80211_del_sta_sinfo\0"
	"netif_receive_skb\0"
	"const_current_task\0"
	"strncpy\0"
	"__tasklet_schedule\0"
	"strcasecmp\0"
	"__x86_indirect_thunk_r13\0"
	"wiphy_unregister\0"
	"free_netdev\0"
	"wait_for_completion_interruptible\0"
	"phys_base\0"
	"ktime_get_real_ts64\0"
	"cfg80211_notify_new_peer_candidate\0"
	"memcmp\0"
	"kthread_stop\0"
	"sscanf\0"
	"__mutex_init\0"
	"usb_deregister\0"
	"__fortify_panic\0"
	"jiffies_to_msecs\0"
	"_raw_spin_unlock_irqrestore\0"
	"_ctype\0"
	"netif_tx_stop_all_queues\0"
	"netif_tx_wake_queue\0"
	"cancel_delayed_work\0"
	"ieee80211_freq_khz_to_channel\0"
	"memset\0"
	"aicwf_prealloc_txq_alloc\0"
	"pci_set_master\0"
	"kernel_read\0"
	"param_ops_charp\0"
	"skb_dequeue_tail\0"
	"__flush_workqueue\0"
	"__x86_return_thunk\0"
	"debugfs_create_u32\0"
	"kmem_cache_alloc_noprof\0"
	"_copy_to_user\0"
	"__init_waitqueue_head\0"
	"netif_rx\0"
	"__netdev_alloc_skb\0"
	"complete_all\0"
	"usb_unanchor_urb\0"
	"__kmem_cache_create_args\0"
	"set_testmode\0"
	"param_ops_string\0"
	"strcmp\0"
	"cfg80211_ch_switch_started_notify\0"
	"skb_unlink\0"
	"__dynamic_netdev_dbg\0"
	"jiffies\0"
	"kthread_create_on_node\0"
	"ktime_get_real_seconds\0"
	"sprintf\0"
	"vmemmap_base\0"
	"__ubsan_handle_shift_out_of_bounds\0"
	"__preempt_count\0"
	"cfg80211_unregister_wdev\0"
	"__dev_queue_xmit\0"
	"cfg80211_probe_status\0"
	"vfree\0"
	"cfg80211_stop_iface\0"
	"cfg80211_rx_mgmt_ext\0"
	"mutex_unlock\0"
	"names_cachep\0"
	"param_ops_bool\0"
	"pci_release_regions\0"
	"__dma_sync_single_for_device\0"
	"__const_udelay\0"
	"wait_for_completion_killable_timeout\0"
	"pci_write_config_byte\0"
	"filp_close\0"
	"__kmalloc_cache_noprof\0"
	"usb_kill_urb\0"
	"cancel_work_sync\0"
	"validate_usercopy_range\0"
	"__warn_printk\0"
	"netif_carrier_off\0"
	"__x86_indirect_thunk_r9\0"
	"delayed_work_timer_fn\0"
	"time64_to_tm\0"
	"_raw_spin_lock_bh\0"
	"netif_carrier_on\0"
	"debugfs_create_file_full\0"
	"cfg80211_chandef_create\0"
	"rtnl_lock\0"
	"cfg80211_ft_event\0"
	"pci_disable_device\0"
	"get_userconfig_txpwr_ofst\0"
	"timer_init_key\0"
	"get_random_bytes\0"
	"__x86_indirect_thunk_r12\0"
	"disable_irq_nosync\0"
	"alloc_workqueue_noprof\0"
	"__ubsan_handle_load_invalid_value\0"
	"strlen\0"
	"dev_kfree_skb_any_reason\0"
	"cfg80211_report_obss_beacon_khz\0"
	"regulatory_set_wiphy_regd\0"
	"param_ops_int\0"
	"skb_append\0"
	"debugfs_create_dir\0"
	"pci_write_config_word\0"
	"get_fw_path\0"
	"generic_file_llseek\0"
	"_raw_spin_unlock\0"
	"simple_read_from_buffer\0"
	"cfg80211_connect_done\0"
	"wiphy_free\0"
	"msleep\0"
	"cfg80211_cqm_rssi_notify\0"
	"__SCT__might_resched\0"
	"kmalloc_caches\0"
	"__trace_set_current_state\0"
	"netdev_info\0"
	"kmem_cache_destroy\0"
	"skb_queue_head\0"
	"system_wq\0"
	"flush_work\0"
	"cfg80211_rx_unprot_mlme_mgmt\0"
	"register_netdevice\0"
	"module_layout\0"
;

MODULE_INFO(depends, "cfg80211,aic_load_fw");

MODULE_ALIAS("usb:vA69Cp8801d*dc*dsc*dp*icFFiscFFipFFin*");
MODULE_ALIAS("usb:vA69Cp88DCd*dc*dsc*dp*icFFiscFFipFFin*");
MODULE_ALIAS("usb:vA69Cp88DDd*dc*dsc*dp*ic*isc*ip*in*");
MODULE_ALIAS("usb:v368Bp88DFd*dc*dsc*dp*ic*isc*ip*in*");
MODULE_ALIAS("usb:v2357p0147d*dc*dsc*dp*ic*isc*ip*in*");
MODULE_ALIAS("usb:v3625p0110d*dc*dsc*dp*ic*isc*ip*in*");
MODULE_ALIAS("usb:v2C4Ep0114d*dc*dsc*dp*ic*isc*ip*in*");

MODULE_INFO(srcversion, "E8A8DF432CD5DF0C3908D1A");
