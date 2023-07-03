// More info about initialization & config:
// - https://revealjs.com/initialization/
// - https://revealjs.com/config/
Reveal.initialize({
    hash: true,
    width: 1280,
    height: 720,
    // Learn about plugins: https://revealjs.com/plugins/
    plugins: [ RevealMarkdown, RevealHighlight, RevealNotes, RevealMath.KaTeX ]
});

Reveal.configure({
    pdfSeparateFragments: false,
    pdfMaxPagesPerSlide: 1,
    showNotes: true,
    showNotes: 'separate-page'
});