A ddfilesorter egy sokoldalú, grafikus felülettel rendelkező fájlrendszerező alkalmazás, amely lehetővé teszi a fájlok rendszerezését kiterjesztés, dátum, méret vagy fájlnév alapján. A program fő célja, hogy automatizálja a fájlok mozgatását egy bemeneti mappából egy kimeneti mappába, a felhasználó által megadott szabályok szerint.

Általános működés
Az alkalmazás Tkinter és ttk (Theme Ttk) modulokat használ a grafikus felhasználói felület (GUI) felépítéséhez. Amikor elindítod, egyetlen ablak jelenik meg, amelyben a következő főbb funkciók találhatók:

Bemeneti és kimeneti könyvtár beállítása: Az ablak tetején két beviteli mező és a hozzájuk tartozó "Választás" gombok találhatók, amelyekkel megadhatod a forrás- és a célmappát. A program alapvetően a bemeneti mappában lévő összes fájlt rendezi, és áthelyezi a kimeneti mappába.

Konfigurációs fájl: Az alkalmazás automatikusan menti az utoljára megadott beállításokat egy config.json nevű fájlba. Amikor újra megnyitod a programot, ezeket az értékeket automatikusan betölti, így nem kell újra beírnod őket.

Lapok: A program egy lapozható (notebook) felületet használ, ahol négy különböző rendezési módszer közül választhatsz. Mindegyik lap a saját rendezési logikáját tartalmazza.

"Rendezés" gomb: Az ablak jobb alsó sarkában lévő gomb a kiválasztott lapon lévő beállítások alapján indítja el a rendezési folyamatot.

Lapok és rendezési módszerek
Az alkalmazás négy különböző lapot kínál a fájlok rendszerezésére:

1. Rendezés kiterjesztés szerint
Ez a lap a fájlok kiterjesztése alapján rendezi azokat.

Funkció: Egy beviteli mezőbe írhatod be a kiterjesztéseket, vesszővel elválasztva.

Csoportosítás: Lehetőséged van kiterjesztéseket csoportosítani zárójelekkel. Például az (jpg, png) megadása esetén az összes .jpg és .png kiterjesztésű fájl egyetlen, jpg_png nevű mappába kerül.

"Egyéb" kategória: A * karakterrel megadhatsz egy "egyéb" kategóriát. Ha egy fájl kiterjesztése nem egyezik a korábban felsoroltakkal, az ebbe a mappába kerül.

Logika: A program sorban halad a megadott feltételeken. Egy fájl csak egyszer kerül áthelyezésre.

2. Rendezés dátum szerint
Ez a lap a fájlok létrehozási vagy módosítási dátuma alapján rendszerezi azokat.

Funkció: Egy kapcsolóval (rádiógombbal) választhatsz a létrehozási és a módosítási dátum között. Egy beviteli mezőben adhatsz meg dátumokat vagy dátumintervallumokat, például:

2025.01.01: Fájlok, amelyek dátuma pontosan ezen a napon van.

2025.02.01-2025.03.01: Fájlok, amelyek dátuma a megadott intervallumon belül esik. A kezdő dátum beleértendő, a záró dátum pedig nem.

2025.04.01-: Fájlok, amelyek dátuma egyenlő vagy nagyobb a megadott dátumnál.

-2025.08.01: Fájlok, amelyek dátuma kisebb a megadott dátumnál.

Logika: A program sorban halad a feltételeken, és az elsőnek megfelelő mappába helyezi a fájlt.

3. Rendezés méret szerint
Ez a lap a fájlok mérete alapján végzi el a rendszerezést.

Funkció: Egy kapcsolóval kiválaszthatod a mértékegységet: KB, MB vagy GB. A beviteli mezőben megadhatsz méreteket vagy méretintervallumokat, például:

-500: Fájlok, amelyek mérete kisebb, mint 500 KB (vagy a kiválasztott mértékegység).

500-1000: Fájlok, amelyek mérete 500 és 1000 között van.

1000-: Fájlok, amelyek mérete nagyobb vagy egyenlő, mint 1000.

Logika: A program itt is sorban halad a feltételeken, és az elsőnek megfelelő mappába helyezi a fájlt.

4. Rendezés fájlnév szerint
Ez a lap a fájlok nevére vonatkozó szabályok alapján rendezi a fájlokat.

Funkció: Egy jelölőnégyzet (checkbox) segítségével beállíthatod, hogy a keresés kisbetű/nagybetű érzékeny legyen-e. A beviteli mezőben a * (csillag) és ! (felkiáltójel) karakterekkel adhatsz meg szabályokat:

abc*: A fájlnév "abc"-vel kezdődik.

!abc*: A fájlnév nem "abc"-vel kezdődik.

*abc*: A fájlnév tartalmazza az "abc" szövegrészt.

!*abc*: A fájlnév nem tartalmazza az "abc" szövegrészt.

*abc: A fájlnév "abc"-vel végződik.

!*abc: A fájlnév nem "abc"-vel végződik.

Logika: A program sorrendben dolgozza fel a megadott mintákat, és a fájlokat az elsőnek megfelelő szabály alapján helyezi el.

Rendezési folyamat
Miután megnyomod a "Rendezés" gombot, a program a következő lépéseket hajtja végre:

Validálja a megadott beállításokat (pl. létezik-e a bemeneti/kimeneti mappa, érvényes-e a megadott formátum).

Létrehozza a szükséges almappákat a kimeneti könyvtárban a rendezési szabályoknak megfelelően.

Végigmegy az összes fájlon a bemeneti mappában, és az aktuális lapon kiválasztott szabályok alapján áthelyezi azokat a megfelelő célmappába.

A művelet végén kitörli az összes üres mappát a kimeneti könyvtárból.

Egy felugró üzenetben tájékoztat a folyamat befejezéséről és az áthelyezett fájlok számáról.

Az alkalmazás rugalmas, és a különböző rendezési logikák együttesen biztosítják, hogy szinte bármilyen mappaszerkezetet könnyedén létrehozhass, mindezt automatizáltan, a korábbi beállítások mentésével és betöltésével.