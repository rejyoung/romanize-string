declare module "cyrillic-to-translit-js" {
    interface CyrillicToTranslitInstance {
        transform(input: string, spaceReplacement?: string): string;
        reverse(input: string, spaceReplacement?: string): string;
    }

    export default function cyrillicToTranslit(config?: {
        preset: "ru" | "uk" | "mn";
    }): CyrillicToTranslitInstance;
}
