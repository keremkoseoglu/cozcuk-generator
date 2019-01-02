# Çözcük Generator

Bu program, [Çözcük](https://github.com/keremkoseoglu/cozcuk-server) oyununa bilmece
üretmek için tasarlanmıştır.

**main.py** dosyası, iki amaçla kullanılabilir.

- **generate_puzzles**: data/esanlamlilar.csv dosyasından faydalanalarak, eş anlamlı sözcükler üzerinden bilmeceler türetir ve /data/output.csv dosyasına yazar.
- **post_to_server**: data/output.csv dosyasındaki bilmeceleri Çözcük sunucusuna iletir.

Sunucuya veri gönderme işi, HTTP POST ile gerçekleşir. Bu amaçla; aşağıdaki Environment Variable'ların hazırlanması gerekir:
- **username**: Çözcük kullanıcı adı
- **password**: Çözcük şifresi
- **server**: Çözcük sunucusunun adresi