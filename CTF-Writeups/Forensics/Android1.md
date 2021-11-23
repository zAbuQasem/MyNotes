# Challenge: Android (1)
## Description: Can you unlock my phone?
### Solution
First of all let's extract the disk image `data.dd` from `Android.7z` compressed file.
```bash
7z x Android.7z
```
![img1](https://i.imgur.com/3cBNzAv.png)
Now let's mount this disk image,so we can explore the file system
```bash
sudo mount  data.dd /mnt/
```
![pain](https://i.imgur.com/TizvWuF.png)
Seems like it can't find the correct offset for the mount point, so we have to manually specify it..

We can view the disk image sector size and partitions using the `fdisk` command
```bash
fdisk -l -u=sectors data.dd
```
![lol](https://i.imgur.com/6fntJ8o.png)
We are interested in the `data.dd3` because it contains the file system

To calculate the Offset of this partition we will use this simple equation:
```txt
Sector_Size * Start = OFFSET
```
From the `fdisk` screenshot above we know that the sector size is `512 bytes` and the start of the `data.dd3` partition is `1067008`
```txt
512 * 1067008 = 546308096 (OFFSET)
```
Now let's try to mount the image again, but this time with the `offset`
```bash
sudo mount -o offset=546308096 data.dd /mnt
```
![meow](https://i.imgur.com/mz9pQ2b.png)
Nice, now we want to find the `gesture.key` file as it contain the passcode used to unlock the device.The file is usaully locate in `system/` folder
![lol2](https://i.imgur.com/rUZQv4B.png)
