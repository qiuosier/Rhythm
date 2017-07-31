
# Taurus
## A Windows System Backup/Restore Application
*Last updated on January 2009*

Taurus is an C++ application for Windows Pre-installation Environment.

I always consider installing software system as a tedious subject, especially when I installing it for others. Here installing software system consist of the installations of the operating system (always Windows XP now), updates and other software for daily use, such as Microsoft Office.

Unfortunately, my parents and some of my friends are not good at using the computer. Their system often crash with virus infection or unknown reasons. Moreover, the system recovery feature of Windows XP seems much less helpful than expected. Ghost is a great tool for creating and restoring system images. However, it is not familiar with people know less about computer and English.

Taurus is developed for backing up and restoring system images. It is based on Microsoft's Windows ImageX and works with Microsoft Windows Image Format(WIM) files.

The goal of Taurus is to provide an simple and easy-to-use interface for backing up and restoring windows systems. Taurus is a Win32 program coded in C++, using the ImageX API to capture or apply images.

As we know, all data in the destination drive will lost when performing a restoration. However, ImageX will not erase the destination when applying image. In other words, no file will be delete except that the files with the same name will be replaced. A format option is provided in Taurus for those who want to perform a "clean" restoration.

Some Features:

* Back up and restore system with WIM image
* Windows Vista-like Graphical Interface
* No computer knowledge required
* Automatically search backup files in the hard disk
* Format is optional when restoring systems

Some Limitations:

* Only for windows
* Only backup the C drive
* Backup destination and filename cannot be specified
* A minimum of 512MB RAM in the computer is required