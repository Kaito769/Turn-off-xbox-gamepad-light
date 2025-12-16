# Turn Off Xbox Gamepad Light (Windows)

A simple, lightweight tool to completely turn off the LED of your Xbox Controller (Series X/S, One) on Windows.

![Xbox LED Off](https://img.shields.io/badge/Xbox_LED-OFF-green) ![Platform](https://img.shields.io/badge/Platform-Windows-blue)

## 🇺🇸 English Description

### Problem
On Windows, the default XInput driver does not allow users to control the Xbox Controller's Guide Button LED. It is permanently set to a bright white light.

### Solution
This tool uses a clever workaround involving Steam's driver infrastructure to temporarily bypass this limitation.
1. It saves a system setting to turn off the LED (0.0 brightness).
2. It briefly launches Steam in the background (silent mode) to apply this setting to the controller.
3. It closes Steam immediately after the setting is applied.
4. **Result:** The light stays OFF until you unplug the controller, with no background apps running!

### Requirements
- **Steam** must be installed on your computer.
  - *Why?* Because Windows blocks LED control. Steam is the only "driver" that can legitimately change it. This tool automates the process of using Steam as a "confugrator".

### How to Use
1. Download `XboxLedOff.exe` from the **Releases** page.
2. Run the program.
3. Click **"TURN OFF LED"**.
4. Wait a few seconds for the process to complete.
5. Done! The program will exit and the light will stay off.

*Note: To turn the light back on, simply unplug and replug your controller.*

---

## 🇹🇷 Türkçe Açıklama

### Sorun
Windows üzerinde varsayılan sürücüler, Xbox kontrolcüsünün ışığını kapatmanıza izin vermez. Işık sürekli yanar ve gece oyun oynarken rahatsız edici olabilir.

### Çözüm
Bu araç, Steam'in sürücü altyapısını kullanarak bu engeli aşan basit bir yöntem kullanır.
1. Sisteme "Işığı Kapat" (0.0 parlaklık) komutunu kaydeder.
2. Bu ayarın kontrolcüye iletilmesi için Steam'i arkaplanda (sessizce) saniyeliğine açar.
3. Ayar uygulandığı an Steam'i kapatır.
4. **Sonuç:** Işık kapanır ve arkada hiçbir program açık kalmaz!

### Gereksinimler
- Bilgisayarınızda **Steam** yüklü olmalıdır.
  - *Neden?* Çünkü Windows ışık kontrolünü engeller. Bunu yapabilen tek güvenli araç Steam'dir. Bu program, Steam'i sadece bir "aracı" olarak kullanıp kontrolcünün ışığını kapatır.

### Nasıl Kullanılır?
1. **Releases** kısmından `XboxLedOff.exe` dosyasını indirin.
2. Programı çalıştırın.
3. **"LED'İ KAPAT"** butonuna basın.
4. İşlem bitene kadar birkaç saniye bekleyin.
5. Bitti! Program kapanacak ve ışığınız sönük kalacaktır.

*Not: Işığı geri açmak için kontrolcüyü (USB) çıkarıp takmanız yeterlidir.*
