/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                primary: {
                    DEFAULT: '#1e4a6e',
                    dark: '#163a57',
                    light: '#2d6a9f',
                },
                accent: {
                    DEFAULT: '#7cb342',
                    light: '#9ccc65',
                    dark: '#558b2f',
                },
                wa: {
                    dark: '#111b21',
                    panel: '#202c33',
                    chat: '#0b141a',
                    border: '#2a3942',
                    hover: '#2a3942',
                },
                text: {
                    primary: '#e9edef',
                    secondary: '#8696a0',
                }
            }
        },
    },
    plugins: [],
}
