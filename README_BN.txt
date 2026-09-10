OISHI LOVE - ANDROID APK PROJECT

এই project Tkinter থেকে Android-এর জন্য Kivy-তে convert করা হয়েছে।
Design/features: Opening screen, Home, Special Message, Love Letter, Cute Zone,
Sorry, Surprise, Just Oishi, Photo Gallery, Previous/Next, enlarge photo,
heart animation, Dark Mode এবং optional Music support।

PHONE-ONLY BUILD (GitHub Actions):
1) GitHub-এ নতুন public/private repository বানাও।
2) এই folder-এর সব file/folder repository-তে upload করো।
3) .github/workflows/build-apk.yml file-টিও অবশ্যই upload হবে।
4) GitHub repository > Actions > Build Oishi APK > Run workflow চাপো।
5) Build শেষ হলে workflow run-এর নিচে Artifacts থেকে oishi-love-apk download করো।
6) ZIP extract করে APK install করো।

PHOTOS:
images folder-এর ভিতরে JPG/PNG ছবি রাখো। বর্তমানে omar.png এবং oishi.png আছে।
নতুন ছবি দিলে আবার APK build করতে হবে।

MUSIC:
music/love.wav নামে একটি WAV file রাখলে Music button কাজ করবে।

যদি GitHub Actions build error দেয়, error log-এর screenshot/text পাঠালে সেই অনুযায়ী fix করা যাবে।
