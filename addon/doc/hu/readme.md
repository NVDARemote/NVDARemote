#NVDA távelérés
1.0-as verzió

Üdvözli az NVDA Távelérés Támogatása kiegészítő, amely lehetővé teszi, hogy egy másik számítógéphez kapcsolódjon az ingyenes NVDA képernyőolvasóval. Nem számít, hogy a szomszéd szobából, vagy épp a világ másik feléről. A kapcsolódás egyszerű, és csak nagyon kevés parancsot kell észben tartani hozzá. Kapcsolódhat egy másik ember számítógépéhez, vagy megengedheti egy megbízható embernek a saját rendszeréhez való kapcsolódást, akár rutinszerű karbantartás, akár egy probléma észlelése, akár csak gyakorlás céljából.

##Mielőtt elkezdené

Mindkét számítógépre telepíteni kell az NVDA-t az NVDA távelérést támogató kiegészítővel.
Az NVDA és az NVDA Távelérés Támogatása kiegészítő telepítése egyaránt az általános szabványt követi. Részletesebb információkat az NVDA felhasználói útmutatójában talál.

##Távelérés indítása közvetítő szerveren keresztül
###Vezérelt számítógép
1. Nyissa meg az NVDA menü, Eszközök, Távelérés, Kapcsolódás menüpontot.
2. Válassza  a Kliens opciót az első választógombon.
3. Válassza a Számítógépem irányítása opciót a második választógomb-csoportban.
4. A szerver szerkesztőmezőbe írja be a kapcsolódó szerver címét pl.: nvdaremote.com.
5. Írjon be egy azonosítót az Azonosító szerkesztőmezőbe, vagy használja az Azonosító generálása gombot.
Ezt az azonosítót használják a számítógépe vezérléséhez.
A vezérlőnek, és összes kliensének ugyanazt az azonosítót kell használnia.
6. Nyomja meg az Ok gombot. Egy hangjelzés figyelmeztet a kapcsolat létrejöttére.

###Vezérlő számítógép
1. Nyissa meg az NVDA menü, Eszközök, Távelérés, Kapcsolódás menüpontot.
2. Válassza  a Kliens opciót az első választógombon.
3. Válassza a Másik számítógép irányítása opciót a második választógomb-csoportban.
4. A szerver szerkesztőmezőbe írja be a kapcsolódó szerver címét pl.: nvdaremote.com.
5. Írjon be egy azonosítót az Azonosító szerkesztőmezőbe, vagy használja az Azonosító generálása gombot.
A vezérlőnek, és összes kliensének ugyanazt az azonosítót kell használnia.
6. Nyomja meg az Ok gombot. Egy hangjelzés figyelmeztet a kapcsolat létrejöttére.

##Közvetlen kapcsolódás
A Szerver opció a kapcsolódás párbeszédpanelen lehetővé teszi közvetlen kapcsolódás beállítását.
Miután ezt kiválasztotta, meg kell adni a kapcsolódás módját.
A másik félnek az ellenkező módot kell választania. Tehát egyik gépen a Számítógépem irányítása, a másikon meg a Másik számítógép irányítása opciót kell választani.

Miután ez megvan, már használhatja a Külső IP-cím lekérdezése gombot a saját külső IP-címének lekérdezésére, ill. a port ellenőrzésére.
Amennyiben az ellenőrzés során kiderül, hogy a port (6837) nem áll készen, egy figyelmeztetés fog megjelenni.
Állítsa be megfelelően a portot, és próbálja újra.
Figyelem: A port beállításának folyamata nem képezi ezen útmutató részét, a szükséges információkat máshonnan kell beszereznie. Pl. a routeréhez mellékelt instrukciókból.

Adjon meg egy azonosítót az Azonosító szerkesztőmezőbe, vagy nyomja meg az Azonosító generálása gombot. A másik félnek a kapcsolódáshoz az imént lekérdezett külső IP-címre, és erre az azonosítóra van szüksége.

Az Ok gomb lenyomása után kapcsolódni fog.
Amint a másik fél is kapcsolódik, máris használhatja az NVDA Távelérést.

##Leütések küldése
Amint a kapcsolat létrejön a vezérlő fél az F11 billentyű lenyomása után kezdheti meg küldeni a billentyűleütéseit.
Miután az NVDA bejelenti, hogy leütések küldése, a vezérlő fél által megnyomott billentyűk hatása a vezérelt fél számítógépén fog jelentkezni. Az F11 újboli lenyomása kikapcsolja a leütések küldését, és visszavált a vezérlő számítógépre.
A legjobb kompatibilitás érdekében győződjön meg róla, hogy a vezérlő és a vezérelt fél oldalán megegyezik-e a billentyűzetkiosztás.

##A Ctrl+Alt+Del átküldése
A leütések küldése keretein belül nem lehetséges a CTRL+Alt+del billentyűkombináció átküldése a többi billentyűleütéshez hasonló módon.
Amennyiben szükség lenne erre a billentyűparancsra, és a vezérelt rendszer a biztonsági képernyőn van, akkor használja ezt a menüpontot.

##Távelérés másik fél beavatkozása nélkül

Néha szükség lehet valamelyik saját számítógépének távvezérlésére. Különösen utazás közben lehet ez hasznos, amikor a laptopjáról akarja vezérelni az otthoni PC-jét, vagy éppen otthon az egyik szobából egy másik szobában lévő gépet. Néhány beállítás elvégzése után kényelmesen megoldható ez is.

1. Az NVDA menüjében válassza az Eszközök, Távelérés, Beállítások menüpontot.
2. Jelölje be az "Automatikus kapcsolódás a vezérlő szerverhez indítás után" jelölőnégyzetet.
3. Töltse ki értelemszerűen a Szerver és az Azonosító szerkesztőmezőket, majd nyomja le az Ok gombot.
4. Figyelem, az Azonosító generálása opció itt nem elérhető, olyan azonosítót adjon meg, amire biztosan emlékezni fog olyankor, amikor épp távolról akarja vezérelni saját számítógépét.

##Távoli beszéd némítása
Amennyiben nem akarja hallani a vezérelt számítógép beszédét, használja ezt az opciót, ami az NVDA menü, Eszközök, Távelérés almenüjében található.

##Távelérés befejezése
A távelérés befejezéséhez tegye a következőket:
1. A vezérlő számítógépen nyomja meg az F11 billentyűt a leütések elküldésének befejezéséhez. A "Nincs leütés küldés" üzenetet kell hallania. Amennyiben ehelyett a "leütések küldése" üzenetet hallja, nyomja meg még egyszer az F11-et.
2. Válassza az NVDA menüjében az Eszközök, Távelérés, Szétkapcsol opciót.

##Vágólap-tartalom küldése
Ez a Távelérés almenüben elérhető opció lehetővé teszi a vágólapon található szöveg küldését.
Aktiválása esetén a vágólap tartalmát átküldi a másik számítógépnek.

##Az NVDA Távelérés beállítása a Biztonsági képernyőhöz

Ahhoz, hogy az NVDA Távelérés a Biztonsági képernyőnn is működjön, be kell másolni a kiegészítőt az NVDA Biztonsági képernyőn érvényes beállításai közé.

1. Az NVDA menüjében válassza a Beállítások, majd az Általános beállítások menüpontot.
2. Navigáljon "Az aktuális beállítások használata a bejelentkező és egyéb biztonsági képernyőkön (rendszergazdai jog szükséges)" gombra, és aktiválja azt.
3. Válaszoljon igennel a megjelenő párbeszédpanelen, amely rákérdez a beállítások ill. bővítmények másolására. Amennyiben felbukkan a Windows biztonsági képernyője, tegyen ugyanígy.
4. Amikor a beállítások másolása elkészült egy üzenet jelenik meg a folyamat sikeréről, Enterrel aktiválja az üzenetpanel Ok gombját, majd egy újabb enterrel az Általános beállítások párbeszédpanelt is bezárhatja.

Ha egyszer az NVDA Távelérés Támogatása kiegészítő bekerül az NVDA Biztonsági képernyőn érvényes beállításai közé, akkor ha távelérésnél szükség lesz rá, már felolvassa a program a biztonsági képernyőt is.

##Közreműködők
Szeretnénk kiemelni az alábbi közreműködőket, akik másokkal együtt lehetővé tették, hogy az NVDA Távelérés projekt valósággá váljon.

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
