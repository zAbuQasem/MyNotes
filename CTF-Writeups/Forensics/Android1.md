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
Nice, now after successfully mounting the image, we have to get the `gesture.key` file  from the `system/` folder as it contain the pattern used to unlock the device.
```bash
cp /system/gesture.key ~/Desktop/JustCTF/Android_1
```
Pattern lock data is kept in gesture.key and the lock sequence is encrypted with a SHA1 hashing algorithm.Since SHA1 is a one-way algorithm there is no reverse function to convert hash to original sequence. To restore the code the attacker will need to create a table of sequences with hash strings. The best way here could be to have a dictionary to recover the pattern.

Fortunately there is a tool on github for that.
```bash 
git clone https://github.com/sch3m4/androidpatternlock
cd androidpatternlock
```
By running the tool with the `gesture.key` we will crack the hash and obtain the pattern sequence!
```bash
python aplc.py ~/Desktop/JustCTF/Android_1/gesture.key
```
![Mohammadflailah](https://i.imgur.com/5XDftxs.png)
![loll](https://i.imgur.com/73NLxBt.png)

FLAG = JUST{157489623}
---
## References
- [getting-started-android-forensics](https://resources.infosecinstitute.com/topic/getting-started-android-forensics/)
- [password-and-pattern-lock-protection](https://www.forensicfocus.com/articles/android-forensics-study-of-password-and-pattern-lock-protection/)
- [how-to-recover-rest-android-pattern-lock-with-gesture-key](https://www.hackeracademy.org/how-to-recover-rest-android-pattern-lock-with-gesture-key/)
