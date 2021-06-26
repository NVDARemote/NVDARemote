# NVDA Uzaktan Erişim
Sürüm 2.3

Ücretsiz NVDA ekran okuyucusunu çalıştıran başka bir bilgisayara bağlanmanıza olanak tanıyan NVDA Uzaktan Erişim eklentisine hoş geldiniz. İster aynı odada ister dünyanın öbür ucunda olun fark etmez. Bağlanmak çok basit ve hatırlanması gereken çok az komut var. Başka bir kişinin bilgisayarını yönetmek için bağlanabilir veya rutin bakım yapmak, bir sorunu teşhis etmek veya eğitim vermek için güvenilir bir kişinin sisteminize bağlanmasına izin verebilirsiniz.

## başlamadan önce

NVDA'yı her iki bilgisayara da kurmuş olmanız ve NVDA Uzaktan Erişim eklentisini edinmeniz gerekir.
Hem NVDA hem de Uzaktan Erişim eklentisinin kurulumu standarttır. Daha fazla bilgiye ihtiyacınız varsa, bu NVDA Kullanıcı Kılavuzunda bulunabilir.

## güncelleme

Eklentiyi güncellerken, NVDA "Uzak bağlantı'yı güvenli masaüstüne kurduysanız, kopyayı güvenli masaüstünde de güncellemeniz önerilir.
Bunu yapmak için önce mevcut eklentinizi güncelleyin. Ardından NVDA menüsünü, tercihleri, ayarları ve genel kategorisini açın ve "Oturum açma sırasında ve güvenli ekranlarda geçerli konfigürasyonu kullan (yönetici yetkisi gerektirir)" etiketli düğmeye basın.

## Bir geçiş sunucusu aracılığıyla uzak oturum başlatma
### Yönetilecek  bilgisayarda
1. NVDA menüsünü açın, Araçlar, Uzak bağlantı, Bağlan.
2. İlk seçim düğmelerinden istemciyi seçin.
3. İkinci radyo düğmesi grubunda Bu bilgisayarın yönetilmesine izin ver'i seçin.
4. Ana bilgisayar alanına, bağlandığınız sunucunun adresini  girin, örneğin nvdaremote.com. Belirli bir sunucu alternatif bir bağlantı noktası kullandığında, ana bilgisayarı <host>:<port> biçiminde girebilirsiniz, örneğin nvdaremote.com:1234.
5. Anahtar alanına bir anahtar girin veya sonraki anahtar oluştur düğmesine basın.
Anahtar, başkalarının bilgisayarınızı yönetmek için kullanacağı paroladır.
Yönetilen makine ve tüm bağlananların aynı anahtarı kullanması gerekir.
6. Tamam düğmesine basın. Bittiğinde, bir ses duyacak ve bağlanacaksınız.

### Yönetecek Bİlgisayarda
1. NVDA menüsünü açın, Araçlar, Uzak bağlantı, Bağlan.
2. İlk radyo düğmelerinden istemciyi seçin.
3. İkinci seçim düğmesi grubunda Başka bir bilgisayarı yönet'i seçin.
4. Ana bilgisayar alanına, bağlandığınız sunucunun adresini girin, örneğin nvdaremote.com. Belirli bir sunucu alternatif bir bağlantı noktası kullandığında, ana bilgisayarı <host>:<port> biçiminde girebilirsiniz, örneğin nvdaremote.com:1234.
5. Anahtar alanına bir anahtar girin veya sonraki anahtar oluştur düğmesine basın.
Yöneten bilgisayar ve tüm bağlandıklarının aynı anahtarı kullanması gerekir.
6. Tamam düğmesine basın. Bittiğinde, bir ses duyacak ve bağlanacaksınız.

## Doğrudan bağlantılar
Bağlan iletişim kutusundaki ilk seçim düğmelerinden sunucu seçeneği, doğrudan bağlantı kurmanıza olanak tanır.
Bunu seçtikten sonra, bağlantınızın hangi modda olacağını seçin.
Diğer kişi, tersini kullanarak size bağlanacaktır.

Mod seçildikten sonra, harici IP adresinizi almak için Harici IP Al düğmesini kullanabilirsiniz ve
bağlantı noktası (port) alanına girilen portun doğru yönlendirildiğinden  emin olun.
Portcheck, portunuzun (varsayılan olarak 6837) erişilebilir olmadığını tespit ederse, bir uyarı gösterilecektir.
Portu yönlendirin ve tekrar deneyin.
Not: bağlantı noktası yönlendirme (port forwarding) işlemi bu belgenin kapsamı dışındadır. Daha fazla talimat için lütfen yönlendiricinizle birlikte verilen bilgilere bakın.

Anahtar alanına bir anahtar girin veya oluştur'a basın. Diğer kişi, bağlanmak için anahtarla birlikte harici IP'nize ihtiyaç duyacaktır. Bağlantı noktası alanına varsayılan (6837) dışında bir bağlantı noktası girdiyseniz, diğer kişinin alternatif bağlantı noktasını  şu şekilde ana bilgisayar adresine eklediğinden emin olun: &lt;external ip&gt;:&lt;port&gt;.

Tamam'a basıldığında bağlanacaksınız.
Diğer kişi bağlandığında, NVDA uzak bağlantı'yı normal şekilde kullanabilirsiniz.

## Uzak Bilgisayarı Yönetme

Bağlantı oturumu başladıktan sonra, yöneten bilgisayarın kullanıcısı uzak bilgisayarı yönetmeye başlamak için f11 tuşuna basabilir (örneğin klavye tuşlarıyla veya braille girişi ile).
NVDA uzak makine kullanılıyor dediğinde, bastığınız klavye ve braille ekran tuşları uzak makineye gönderilir. Ayrıca, yöneten makine bir braille ekranı kullanıyorsa, uzaktaki makineden gelen bilgiler bunun üzerinde gösterilecektir. Tuşları göndermeyi durdurmak ve yöneten makineye geri dönmek için tekrar f11 tuşuna basın.
Mükemmel uyumluluk için lütfen her iki makinedeki klavye düzenlerinin eşleştiğinden emin olun.

## Oturumunuzu paylaşma

Başka birinin NVDA UZAKTAN oturumunuza kolayca katılabilmesi için bir bağlantı paylaşmak için Uzak bağlantı menüsünden Bağlantıyı Kopyala'yı seçin.
Yöneten bilgisayar olarak bağlıysanız, bu bağlantı başka birinin bağlanmasına ve yönetilmesine izin verecektir.
Bunun yerine bilgisayarınızı yönetilecek şekilde ayarladıysanız, bağlantı, onu paylaştığınız kişilerin makinenizi kontrol etmesine olanak tanır.
Birçok uygulama, kullanıcıların bu bağlantıyı otomatik olarak etkinleştirmesine izin verir, ancak belirli bir uygulama içinden çalışmıyorsa, panoya kopyalanabilir ve çalıştır iletişim kutusundan çalıştırılabilir.


## Ctrl + Alt + Del komutu gönder
Tuşları yöneten bilgisayara gönderirken CTRL+Alt+del kombinasyonunu göndermek normalde mümkün değildir.
CTRL+Alt+del göndermeniz gerekiyorsa ve uzak makine güvenli masaüstündeyse bu komutu kullanın.

## Bir Bilgisayarı Katılımsız Olarak Uzaktan Yönetme

Bazen kendi bilgisayarlarınızdan birini uzaktan kontrol etmek isteyebilirsiniz. Bu, özellikle seyahat ediyorsanız ve ev bilgisayarınızı dizüstü bilgisayarınızdan kontrol etmek istiyorsanız yararlıdır. Veya dışarıda otururken evinizin bir odasındaki bilgisayarı başka bir bilgisayarla kontrol etmek isteyebilirsiniz. Biraz ileri düzeyde hazırlık bunu uygun ve mümkün kılar.

1. NVDA menüsüne girin ve Araçlar'ı ve ardından Uzak bağlantı'yı seçin. Son olarak, Seçenekler'de Enter'a basın.
2. "Başlangıçta kontrol sunucusuna otomatik olarak bağlan" yazan onay kutusunu işaretleyin.
3. uzak kontrol sunucusu  mu yoksa  Ana kontrol sunucusu  üzerinden bağlanacağınızı seçin.
4. İkinci radyo düğmesi grubunda Bu makinenin yönetilmesine izin ver'i seçin.
5. Bağlantıyı kendiniz barındırıyorsanız, yönetilen makinede port alanına (varsayılan olarak 6837) girilen porta yöneten makinelerden erişilebilmesini sağlamanız gerekecektir.
6. Uzak sunucu kullanmak istiyorsanız, hem Ana Bilgisayar hem de Anahtar alanlarını doldurun, sekmesinden Tamam'a gidin ve Enter'a basın. Bu durumda Anahtar Oluştur seçeneği kullanılamaz. Herhangi bir uzak konumdan kolayca kullanabilmeniz için hatırlayacağınız bir anahtar bulmak en iyisidir.

İleri düzey kullanım için, NVDA uzak bağlantı'yı yöneten modunda yerel veya uzak bir kontrol sunucusuna otomatik olarak bağlanacak şekilde de yapılandırabilirsiniz. Bunu istiyorsanız, ikinci seçim düğmesi grubunda Başka bir bilgisayarı yönet'i seçin.

Not: Seçenekler iletişim kutusundaki başlangıçta otomatik bağlanmayla ile ilgili seçenekler, NVDA yeniden başlatılıncaya kadar uygulanmaz.


## Uzak Bilgisayardaki Konuşmayı Susturma
Uzak bilgisayarın konuşmasını veya NVDA'ya özgü sesleri duymak istemiyorsanız, NVDA menüsüne, Araçlar'a ve Uzak bağlantı'ya gidip "uzaktakini sustur"  üzerinde Enter'a basmanız yeterlidir. Lütfen bu seçeneğin, yöneten makine tuşları gönderirken kontrol ekranına uzaktan braille çıkışını devre dışı bırakmayacağını unutmayın.


## Uzak Bağlantı Oturumunu Sonlandırma

Uzak oturumu sonlandırmak için aşağıdakileri yapın:

1. Yöneten bilgisayarda, uzaktaki makineyi kontrol etmeyi durdurmak için F11 tuşuna basın. Şu mesajı duymanız veya okumanız gerekir: "Yerel makine kullanılıyor." Bunun yerine uzaktaki makineyi kontrol ettiğinize dair bir mesaj duyar veya okursanız, bir kez daha F11 tuşuna basın.

2. NVDA menüsüne, ardından Araçlar, Uzak bağlantı'ya girin ve Bağlantıyı Kes üzerinde Enter'a basın.

## Pano İçeriğini Gönderme
Uzak Bağlantı altındaki Pano içeriğini gönder seçeneği panonuzdaki metni diğer bilgisayarınkine göndermenizi sağlar.
etkinleştirildiğinde, panodaki herhangi bir metin diğer bilgisayarlarınkine de aktarılacaktır.

## NVDA Uzak Bağlantı'yı Güvenli Masaüstünde Çalışması İçin Yapılandırma

NVDA Remote'un güvenli masaüstünde çalışması için, eklentinin güvenli masaüstünde çalışan NVDA'ya yüklenmiş olması gerekir.

1. NVDA menüsünden Tercihler'i ve ardından Ayarlar'a girin  ve genel kategorisine seçin.

2. Oturum açma sırasında ve güvenli ekranlarda geçerli konfigürasyonu kullan (yönetici yetkisi gerektirir) düğmesine gidin ve Enter'a basın.

3. Ayarlarınızı kopyalamaya ve eklentileri kopyalamaya ilişkin istemlere Evet yanıtını verin ve görüntülenebilecek Kullanıcı Hesabı Denetimi istemini onaylayın.
4. Ayarlar kopyalandığında, kapatmak için Tamam düğmesine basın. İletişim kutusundan çıkmak için tab tuşuyla Tamam'a gelin ve bir kez daha Enter'a  basın.

NVDA Uzak Bağlantı, güvenli masaüstüne kurulduğunda, şu anda bir uzak oturumda yönetiliyorsanız,
geçiş yaptığınızda güvenli masaüstüne konuşma ve braille erişiminiz olacaktır.

## Katkılar
NVDA Uzak Bağlantı projesini hayata geçirmeye yardımcı olan diğerlerinin yanı sıra aşağıdaki katkıda bulunanlara teşekkür etmek isteriz.

* Hai Nguyen Ly
* Chris Westbrook
* Thomas Huebner
* John F Crosotn III
* Darrell Shandrow
* D Williams
* Matthew McCubbin
* Jason Meddaugh
* ABDULAZIZ ALSHMASI.
* Tyler W Kavanaugh
* Casey Mathews
* Babbage B.V.
* Leonard de Ruijter
* NV Access
* Reef Turner

## Değişim Günlüğü

### Sürüm 2.3
* Python 3'e taşındı
* Bırakılan Python 2 desteği
* NVDA 2019.3'te değiştirilen API'yi karşılamak için güncelleme şunları içerir:
  - Speech refactor
  - Braille ekranlarında yapılan değişiklikler

### Sürüm 2.2

* IPv6 Desteği
* Yeni NVDA 2018.3 ve eski sürümler için destek
* Modele özgü Braille ekran hareketleri için destek

### Version 2.1

* Fixed connection not saving when allowing this machine to be controlled
* Added a script to push the clipboard with ctrl+shift+NVDA+c
* Braille input now works in browse mode
* Support model specific braille display gestures
* The beeps generated by NVDA Remote no longer block NVDA

### Version 2.0

* Support for remote Braille
* Support for nvdaremote:// links
* Centered Dialogs to conform with the rest of NVDA
* Fixed portcheck to point at a domain we control, portcheck.nvdaremote.com
* Support automatically connecting to a control server in master mode
* Fixed rendering error in documentation
* Update to protocol version 2, which includes an origin field in every remote message
* Significant code cleanup allowing easier modifications in future

## Altering NVDA Remote

You may clone this repo to make alteration to NVDA Remote.

### 3rd Party dependencies

These can be installed with pip:
- Markdown
- scons
- python-gettext

### To package the add-on for distribution:

1. Open a command line, change to the root of this repo
1. Run the **scons** command. The created add-on, if there were no errors, is placed in the current directory.

