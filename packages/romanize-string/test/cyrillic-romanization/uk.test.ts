import { romanizeCyrillic } from "../../src/transliterators/cyrillic-romanization";
import { describe, it, expect } from "vitest";

/**
 * Adapted from cyrillic-to-translit-js
 * Original author: Aleksandr Filatov
 * License: MIT
 * https://github.com/greybax/cyrillic-to-translit-js
 */

describe("Ukrainian transliteration", () => {
    it("matches https://pasport.org.ua/vazhlivo/transliteratsiya", () => {
        const t = (s: string) => romanizeCyrillic(s, "uk");

        expect(t("алушта")).toBe("alushta");
        expect(t("андрій")).toBe("andrii");
        expect(t("борщагівка")).toBe("borshchahivka");
        expect(t("борисенко")).toBe("borysenko");
        expect(t("вінниця")).toBe("vinnytsia");
        expect(t("володимир")).toBe("volodymyr");
        expect(t("гадяч")).toBe("hadiach");
        expect(t("богдан")).toBe("bohdan");
        expect(t("згурський")).toBe("zghurskyi");
        expect(t("ґалаґан")).toBe("galagan");
        expect(t("ґорґани")).toBe("gorgany");
        expect(t("донецьк")).toBe("donetsk");
        expect(t("дмитро")).toBe("dmytro");
        expect(t("рівне")).toBe("rivne");
        expect(t("олег")).toBe("oleh");
        expect(t("есмань")).toBe("esman");
        expect(t("єнакієве")).toBe("yenakiieve");
        expect(t("гаєвич")).toBe("haievych");
        expect(t("короп'є")).toBe("koropie");
        expect(t("житомир")).toBe("zhytomyr");
        expect(t("жанна")).toBe("zhanna");
        expect(t("жежелів")).toBe("zhezheliv");
        expect(t("закарпаття")).toBe("zakarpattia");
        expect(t("казимирчук")).toBe("kazymyrchuk");
        expect(t("іванків")).toBe("ivankiv");
        expect(t("іващенко")).toBe("ivashchenko");
        expect(t("їжакевич")).toBe("yizhakevych");
        expect(t("кадиївка")).toBe("kadyivka");
        expect(t("мар'їне")).toBe("marine");
        expect(t("йосипівка")).toBe("yosypivka");
        expect(t("стрий")).toBe("stryi");
        expect(t("олексій")).toBe("oleksii");
        expect(t("київ")).toBe("kyiv");
        expect(t("коваленко")).toBe("kovalenko");
        expect(t("лебедин")).toBe("lebedyn");
        expect(t("леонід")).toBe("leonid");
        expect(t("миколаїв")).toBe("mykolaiv");
        expect(t("маринич")).toBe("marynych");
        expect(t("ніжин")).toBe("nizhyn");
        expect(t("наталія")).toBe("nataliia");
        expect(t("одеса")).toBe("odesa");
        expect(t("онищенко")).toBe("onyshchenko");
        expect(t("полтава")).toBe("poltava");
        expect(t("петро")).toBe("petro");
        expect(t("решетилівка")).toBe("reshetylivka");
        expect(t("рибчинський")).toBe("rybchynskyi");
        expect(t("суми")).toBe("sumy");
        expect(t("соломія")).toBe("solomiia");
        expect(t("тернопіль")).toBe("ternopil");
        expect(t("троць")).toBe("trots");
        expect(t("ужгород")).toBe("uzhhorod");
        expect(t("уляна")).toBe("uliana");
        expect(t("фастів")).toBe("fastiv");
        expect(t("філіпчук")).toBe("filipchuk");
        expect(t("харків")).toBe("kharkiv");
        expect(t("христина")).toBe("khrystyna");
        expect(t("біла церква")).toBe("bila tserkva");
        expect(t("стеценко")).toBe("stetsenko");
        expect(t("чернівці")).toBe("chernivtsi");
        expect(t("шевченко")).toBe("shevchenko");
        expect(t("шостка")).toBe("shostka");
        expect(t("кишеньки")).toBe("kyshenky");
        expect(t("щербухи")).toBe("shcherbukhy");
        expect(t("гоща")).toBe("hoshcha");
        expect(t("гаращенко")).toBe("harashchenko");
        expect(t("юрій")).toBe("yurii");
        expect(t("корюківка")).toBe("koriukivka");
        expect(t("яготин")).toBe("yahotyn");
        expect(t("ярошенко")).toBe("yaroshenko");
        expect(t("костянтин")).toBe("kostiantyn");
        expect(t("знам'янка")).toBe("znamianka");
        expect(t("феодосія")).toBe("feodosiia");
        expect(t("згорани")).toBe("zghorany");
        expect(t("розгон")).toBe("rozghon");
    });

    it("handles apostrophes (U+0027)", () => {
        const t = (s: string) => romanizeCyrillic(s, "uk");

        expect(t("короп'є")).toBe("koropie");
        expect(t("мар'їне")).toBe("marine");
        expect(t("знам'янка")).toBe("znamianka");
    });

    it("handles apostrophes (U+2019)", () => {
        const t = (s: string) => romanizeCyrillic(s, "uk");

        expect(t("короп’є")).toBe("koropie");
        expect(t("мар’їне")).toBe("marine");
        expect(t("знам’янка")).toBe("znamianka");
    });

    it("handles apostrophes (U+02BC)", () => {
        const t = (s: string) => romanizeCyrillic(s, "uk");

        expect(t("коропʼє")).toBe("koropie");
        expect(t("марʼїне")).toBe("marine");
        expect(t("знамʼянка")).toBe("znamianka");
    });
});
