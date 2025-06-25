declare module "arabic-transliterate" {
  export default function arabictransliterate(
    input: string,
    direction: "latin2arabic" | "arabic2latin",
    language: "Arabic",
  ): string;
}
