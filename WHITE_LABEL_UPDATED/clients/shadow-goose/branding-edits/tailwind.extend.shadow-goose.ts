export const shadowGooseTailwindExtend = {
  theme: {
    extend: {
      colors: {
        sg: {
          primary: "#1A1A1A",
          secondary: "#FFFFFF",
          accent: "#FF6600",
          background: "#F5F5F5",
        },
      },
      fontFamily: {
        heading: ["Poppins", "ui-sans-serif", "system-ui"],
        body: ["Open Sans", "ui-sans-serif", "system-ui"],
      },
    },
  },
} as const;
