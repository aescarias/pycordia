document.querySelectorAll("pre>code").forEach(elem => {
    let lines = elem.textContent.split("\n");
    if (lines[0] === '') lines.shift()

    let matches;
    let indentation = (matches = /^[\s\t]+/.exec(lines[0])) !== null ? matches[0] : null;
    if (indentation) {
        lines = lines.map(line => {
            line = line.replace(indentation, '')
            return line.replace(/\t/g, '    ')
        })

        elem.textContent = lines.join("\n").trim()
    }
})

hljs.highlightAll()
