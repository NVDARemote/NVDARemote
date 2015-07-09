#NVDA Remote Access
Verzia 1.0

Práve čítate dokumentáciu k doplnku NVDA Remote Access, ktorý vám umožní pripájať sa k ďalšiemu počítaču so spusteným voľne dostupným čítačom obrazovky NVDA. Pri tom vôbec nie je dôležité či sa pripájate ku počítaču umiestnenému na vedľajšom stole, alebo k počítaču vzdialenému na druhom konci sveta. Celý proces je veľmi jednoduchý, stačí si zapamätať len niekoľko málo príkazov. Môžete sa pripojiť k niekoho iného počítaču, alebo môžete niekomu dôveryhodnému umožniť, aby sa pripojil k tomu vášmu a pomohol vám s jeho údržbou, pomohol vám pri riešení problému, alebo vás zaškolil na používanie nejakej vlastnosti alebo aplikácii bežiacej na vašom počítači.

##Pred tým než začnete

NVDA by ste mali mať nainštalovaný na oboch počítačoch a do oboch týchto inštalácií NVDA ešte potrebujete doinštalovať doplnok NVDA Remote Access.
Inštalácia ako NVDA tak aj doplnku NVDA Remote Access je úplne štandardná, stačí si z web stránky oboch projektov stiahnuť aktuálnu verziu, najprv nainštalovať NVDA a následne doplnok NVDA Remote Access. Podrobnejšie o inštalácii NVDA aj o inštalácii doplnkov sa môžete dočítať v používateľskej príručke NVDA.

##Spustenie vzdialeného pripojenia cez relay server
###Ovládaný počítač
1. Z ponuky NVDA otvorte Nástroje, Vzdialené ovládanie, Pripojiť.
2. V prvej skupine prepínačov zvoľte Klient.
3. V druhej skupine prepínačov zvoľte Povoliť ovládanie tohoto počítača.
4. Do editačného poľa hostiteľ zapíšte adresu relay servera, ku ktorému sa chystáte pripojiť (napr. nvdaremote.com).
5. Do editačného poľa Kľúč môžete vložiť vlastný kľúč alebo si potvrdením tlačidla Vygenerovať kľúč môžete nechať vygenerovať náhodný kľúč.
Tento kľúč použijú dôveryhodné osoby, ktorých poveríte, aby mohli ovládať váš počítač.
Ovládaný počítač a všetci používatelia, ktorí ho budú vzdialene ovládať musia použiť rovnaký kľúč.
6. Stlačením tlačidla OK ukončíte nastavenie, NVDA sa pripojí k relay serveru, čo indikuje pípnutím.

###Ovládajúci počítač
1. Z ponuky NVDA otvorte Nástroje, Vzdialené ovládanie, Pripojiť.
2. V prvej skupine prepínačov zvoľte Klient.
3. V druhej skupine prepínačov zvoľte Ovládať vzdialený počítač.
4. Do editačného poľa hostiteľ zapíšte adresu relay servera, ku ktorému sa chystáte pripojiť (napr. nvdaremote.com).
5. Do editačného poľa Kľúč môžete vložiť vlastný kľúč alebo si potvrdením tlačidla Vygenerovať kľúč môžete nechať vygenerovať náhodný kľúč.
Ovládaný počítač a všetci používatelia, ktorí ho budú vzdialene ovládať musia použiť rovnaký kľúč.
6. Stlačením tlačidla OK ukončíte nastavenie, NVDA sa pripojí k relay serveru, čo indikuje pípnutím.

##Priame pripojenie
Prepínač Server v prvej skupine prepínačov v dialógu Pripojiť umožňuje nastaviť priame spojenie ovládaného a ovládajúceho počítača bez nutnosti použitia relay servera.
Ak ste v prvej skupine prepínačov zvolili server, v druhej skupine vyberte režim vašeho pripojenia.
Človek, ktorý sa pripojí k vám vyberie opačné nastavenie v druhej skupine prepínačov.

Ak máte správne nastavený režim, pomocou tlačidla Zistiť verejnú adresu IP získate vašu externú adresu IP, ktorú odovzdáte tomu, kto sa k vám pripojí a zároveň zistíte, či máte správne presmerovaný port.
Ak sa počas tejto kontroly zistí, že váš port (6837) nie je dostupný, zobrazí sa varovanie.
Nastavte správne presmerovanie a skúste znovu Zistiť verejnú adresu IP.
Všimnite si: V súvislosti s procesom nastavovania presmerovania portov v tomto návode neuvádzame viacej podrobností, pretože je to rozsiahla téma. Viacej informácií o presmerovaní portov môžete získať v návode k vašemu routeru alebo DSL modemu. V niektorých prípadoch môžete pomoc s presmerovaním portov získať od svojho poskytovateľa internetu alebo správcu siete.

Do poľa kľúč vložte vymyslený kľúč, alebo použite tlačidlo Vygenerovať kľúč, ak chcete získať náhodný kľúč. Človek, ktorý sa k vám pripojí potrebuje spolu s vašou verejnou adresou IP aj tento kľúč.

Hneď ako stlačíte tlačidlo OK, spustíte pripojenie.
Potom, čo sa pripojí váš partner, môžete vzdialené ovládanie NVDA remote začať používať rovnako ako v prípade spojenia cez relay server.

##Odosielanie klávesov
Keď sú oba počítače úspešne spojené, stlačením F11 na ovládajúcom počítači je možné spustiť odosielanie klávesov na ovládaný počítač.
Keď NVDA oznámi Odosielanie klávesov spustené, všetky klávesy, ktoré stlačíte sa odošlú na ovládaný počítač. Opätovným stlačením F11 zastavíte odosielanie klávesov a vrátite ovládanie späť na ovládajúci počítač, čo NVDA oznámi hláskov Odosielanie klávesov zastavené. 
Na zachovanie kompatibility je odporúčané, aby ste na oboch počítačoch mali nastavené rovnaké rozloženie klávesov.

##Odoslať klávesy ctrl+alt+del
Keď je spustené odosielanie klávesov, štandardným spôsobom nie je možné  z ovládaného počítača odoslať kombináciu klávesov ctrl+alt+del.
Ak potrebujete odoslať túto kombináciu klávesov a na vzdialenom počítači je zobrazená zabezpečená obrazovka, použite túto možnosť z ponuky NVDA, Vzdialené ovládanie..

##Vzdialené ovládanie počítača bez obsluhy

Niekedy by ste mohli chcieť vzdialene ovládať váš vlastný počítač. Predovšetkým to môže byť užitočné ak ste na cestách a chcete sa z notebooku pripojiť k stolnému počítaču doma. Alebo ak ste doma, môžete z počítača v jednej izbe ovládať počítač v inej izbe. Takéto použitie je s doplnkom NVDA remote možné a praktické, stačí prejsť na počítači, ktorý si želáte ovládať bez ďalšej obsluhy jednoduchou prípravou.

1. V ponuke NVDA nájdite podponuku Nástroje, Vzdialené ovládanie a tam potvrďte položku Možnosti.
2. Zaškrtnite políčko Pri spustení sa automaticky pripojiť k riadiacemu serveru.
3. Vyplňte editačné polia Hostiteľ a Kľúč, prejdite na tlačidlo OK a stlačte enter.
4. Prosím všimnite si: V tejto situácii nie je k dispozícii tlačidlo Vygenerovať kľúč. Mali by ste zadať svoj vlastný vymyslený kľúč, ktorý budete vedieť použiť len vy na ovládanie vašeho vzdialeného počítača bez obsluhy.

##Stlmenie reči na vzdialenom počítači
Ak nechcete na vzdialenom počítači počuť reč hlasového výstupu počas jeho ovládania, prejdite v ponuke NVDA do podponuky Nástroje, Vzdialené ovládanie a potvrďte položku Stlmiť reč na vzdialenom počítači.

##Ukončenie ovládania vzdialeného počítača

Ovládanie vzdialeného počítača ukončíte nasledovným spôsobom:

1. Na ovládajúcom počítači stláčajte kláves F11 až kým NVDA neoznámi Odosielanie klávesov zastavené.
2. V ponuke NVDA nájdite podponuku Nástroje, Vzdialené ovládanie a tam zvoľte položku Odpojiť.

##Odoslať text schránky
Položka Odoslať text schránky v podponuke Vzdialené ovládanie umožní odoslanie aktuálneho textu v schránke windows na vašom počítači.
Po potvrdení tejto položky bude text zo schránky windows odoslaný do schránky všetkých pripojených počítačov.

##Nastavenie doplnku NVDA remote na použitie na zabezpečených obrazovkách windows

Aby doplnok NVDA Remote správne fungoval aj v čase, keď sa na vzdialenom počítači zobrazuje zabezpečená obrazovka windows, musí byť nainštalovaný na takéto použitie.

1. Z ponuky NVDA zvoľte Možnosti a v podponuke Možnosti položku Všeobecné nastavenia.
2. Prejdite na tlačidlo použiť aktuálne nastavenia NVDA na prihlasovacej a zabezpečených obrazovkách (vyžaduje administrátorské práva) a stlačte kláves enter.
3. Na otázky súvisiace s kopírovaním nastavení a doplnkov odpovedzte áno a tak isto odpovedzte áno ak sa objaví obrazovka na prepnutie užívateľského účtu (UAC).
4. Keď kopírovanie nastavení skončí, stlačením klávesu enter sa zbavíte informačnej správy s tlačidlom OK, dialóg Všeobecné nastavenia ukončite prejdením na tlačidla OK a potvrdením tlačidla enter.

Keď je doplnok NVDA remote takto pripravený na použitie na zabezpečenej obrazovke windows, počas vzdialeného ovládania vašeho počítača bude na ovládajúcom počítači prístupná aj zabezpečená obrazovka hneď, ako sa zobrazí.

##Prispievatelia
Radi by sme osobitne poďakovali nasledovným dobrovoľníkom, ktorím sme spolu s ostatnými vďační za to, že je doplnok NVDA Remote skutočne na svete:

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
