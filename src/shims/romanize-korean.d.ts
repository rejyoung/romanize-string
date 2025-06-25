declare module "@romanize/korean" {
  interface RomanizationOptions {
    system: "RR" | "MR" | "YL";
  }
  export function romanize(hangul: string, romanizationOptions?: RomanizationOptions): string;
}
