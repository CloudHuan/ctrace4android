adb push busybox /data/local/tmp
adb shell chmod 755 /data/local/tmp/busybox
adb push fps.sh /data/local/tmp
adb shell sh /data/local/tmp/fps.sh -w com.arashivision.insta360air/com.arashivision.insta360air.ui.home.MainActivity -f /sdcard/fps.csv
adb pull /sdcard/fps.csv ./