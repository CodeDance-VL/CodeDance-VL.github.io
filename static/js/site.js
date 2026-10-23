// Configure the local MathJax bundle before its deferred script runs.
window.MathJax = {
  tex: {
    inlineMath: [["$", "$"], ["\\(", "\\)"]],
    displayMath: [["$$", "$$"], ["\\[", "\\]"]],
    processEscapes: true
  },
  svg: {
    fontCache: "local"
  },
  options: {
    enableMenu: false
  }
};
