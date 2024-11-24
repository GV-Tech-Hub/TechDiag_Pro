PassMark ® Software MemTest86™
Copyright (C) 2013-2024 PassMark Software
All Rights Reserved
https://www.memtest86.com

Overview
========================================
PassMark's MemTest86 is a standalone memory testing software for x86 and ARM computers.
MemTest86 boots from a USB flash drive and tests the RAM in your computer for 
faults using a series of comprehensive algorithms and test patterns.
<For more details see the MemTest86 User Guide>


Requirements
========================================
- UEFI-capable x86 (x86/x64) or ARM64 (aarch64) compatible System (Mac and PC)
- USB Flash drive (>= 1GB capacity)


Creating a bootable USB drive
========================================

For Windows:

 - Plug in your USB drive.
 - Launch the included ImageUSB application.
 - Select your USB drive from the list (Step 1).
 - Select 'Write image to USB drive' (Step 2)
 - If it is not already selected, select the included image file (Step 3).
 - Click 'Write' (Step 4).

After accepting a few more prompts this should give you a working
bootable USB drive.

For Linux:

1) Insert a USB drive into a USB slot.
2) Determine which device the USB drive is assigned as (eg. /dev/sdc) by opening the Terminal and typing the following command:

lsblk -p -o NAME,VENDOR,MODEL,SIZE,TYPE,SERIAL

3) As root, use the 'dd' command to write the image to the USB drive. For example,

sudo dd if=memtest86-usb.img of=<dev> conv=fsync status=progress

where <dev> is the device the USB key is assigned to obtained from the previous command. Use the base device (ie. /dev/sdc) not a partition designation (ie. /dev/sdc1).

**Warning** all data on the USB key will be lost. 
**FINAL Warning** Make sure that the device used in the dd command above is correct!!!

For Mac:

1) Insert a USB drive into a USB slot.
2) Determine which device the USB drive is assigned as by opening the Terminal and typing the following command:
 
diskutil list

3) Unmount all volumes on the USB drive by typing the following command: 

diskutil unmountDisk [device name]

4) As root, use the 'dd' command to write the image to the USB drive. For example,

sudo dd if=memtest86-usb.img of=<dev> conv=sync

where <dev> is the device the USB key is assigned to obtained from the previous command. Use the base device (ie. /dev/disk1) not a partition designation (ie. /dev/disk1s1).

**Warning** all data on the USB key will be lost. 
**FINAL Warning** Make sure that the device used in the dd command above is correct!!!


Booting the MemTest86 USB drive
========================================
To start MemTest86 insert the USB flash drive into the appropriate drive and 
restart your computer. The UEFI BIOS must be configured to boot from the device 
that MemTest86 is installed on. Most systems have an optional boot menu 
that is enabled by pressing a key at startup (often ESC, F9, F11 or F12).

If available use the boot menu to select the correct drive.
Please consult your motherboard documentation for details.

On a Mac, to boot from USB, you need to hold down the ALT / Option key on the Mac keyboard 
while powering on the machine.

On newer Macs (from 2018) with the Apple T2 Security Chip, you may need to change the SecureBoot settings
for MemTest86 to boot. Please see the following page for instructions:
https://support.apple.com/en-us/HT208330

Reclaiming disk space from the USB drive
========================================
You may have noticed that the MemTest86 USB drive you have created may have lost some 
disk space and normal formatting will not recover the lost space. 
For example, this can happen when a UFD contains multiple partitions, such as the
MemTest86 image. Formatting will not span across multiple partitions/volume. 
To erase the partition records and reclaim the whole disk, you will need to 
zero the MBR.

WARNING: THIS PROCESS WILL COMPLETELY DELETE THE DATA ON THE DRIVE

For Windows:

1. Insert UFD.
2. Launch imageUSB and select the appropriate UFD. (Be careful and select the correct drive!).
3. Choose the Zero UFD option & Run.
4. Drive MBR is now Zeroed. You will need to reinsert the drive for Windows to recognize it 
   and prompt for formatting before you can use it again. A normal format will now recover 
   the full capacity of the USB drive.

For Linux/Mac:

1) Insert the USB drive into a USB slot.
2) Determine which device the USB drive is assigned as (eg. /dev/sdc on Linux, /dev/disk1 on Mac).
3) As root, use the 'dd' command to erase the partition table of the USB drive. For example,

dd if=/dev/zero of=<dev> bs=512 count=1

where <dev> is the device the USB key is assigned to. Use the base device (ie. /dev/sdc) not a partition designation (ie. /dev/sdc1).


Documentation
=============
All the documentation is included in the MemTest86 User Guide PDF. It can be found under the
'help' folder in the USB flash drive. 


Support
=======
For technical support, questions, suggestions, please check the User Guide or 
visit our web page at https://www.memtest86.com


Ordering / Registration
=======================
All the details are in our sales information page
https://www.memtest86.com/pricing.html


Enjoy..
The PassMark Development team