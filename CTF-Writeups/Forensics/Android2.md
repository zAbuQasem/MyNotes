# Challenge: Android (2)
## Description: Can you find the password hint?

After extracting the `image_sdb.img` from the compressed file, and trying to mount the disk image, i faced the same issues as the `Android1` challenge.You can refer to `android1` writeup ([Android1](https://github.com/zAbuQasem/MyNotes/blob/main/CTF-Writeups/Forensics/Android1.md)) in order to solve the mounting issue.

![mohammedatary](https://i.imgur.com/vsVmRKP.png)

In order to solve the challenge i have to reach the `password hint` which is not an available feature in most android phones, so we have to find a place where the password hint could be specified by the user.The possible places i thought of are:
1. Lockscreen (Because of 'who is going to die to get my password' mindset)
2. Picture in the gallery (Basic behaviour from it proffesionals)

I started searching for the artifact that holds the lockscreen settings and found this file `locksettings.db` in the `system/` folder.After examining the file type it appeared to be an `sqlite3` db file.
![moiwq](https://i.imgur.com/OVm2YT1.png)
So i tried opening the file with `sqlitebrowser`it opened without any issues :)
![DEAD](https://i.imgur.com/cDmWvda.png)

I found a suspicious entity

![kontrol](https://i.imgur.com/Iq8XbiZ.png)

Then i took the column name `lock_screen_owner_info` and found this [Article](https://www.howtogeek.com/194878/how-to-display-owner-information-on-the-lock-screen-on-your-android-phone/) talking about displaying owner information on the lock screen, So this must be the place i'm looking for.
I copied the `)))(()))$$#)))` from the column, tried to submit it, and it worked!

FLAG = JUST{`)))(()))$$#)))`}

---

## Refereneces
[how-to-display-owner-information-on-the-lock-screen-on-your-android-phone](https://www.howtogeek.com/194878/how-to-display-owner-information-on-the-lock-screen-on-your-android-phone/)
