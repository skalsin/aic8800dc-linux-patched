savedcmd_aic_load_fw/aic_load_fw.o := ld -m elf_x86_64 -z noexecstack --no-warn-rwx-segments   -r -o aic_load_fw/aic_load_fw.o @aic_load_fw/aic_load_fw.mod 
