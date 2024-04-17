run_maths = function() {

  if (document.querySelector('[class*="cmath"]') !== null) {

    if (typeof (mjax_path)=='undefined') { mjax_path='https://cdn.jsdelivr.net/npm/mathjax@2'; }
    if (typeof (mjax_config)=='undefined') { mjax_config='AM_CHTML'; }

    if (typeof(window.MathJax) == 'undefined') { window.MathJax = { }; }

    if (mjax_config.toLowerCase().indexOf('tex') >= 0) {
          m = window.MathJax;
          if (typeof(m.displayAlign) == 'undefined') { m.displayAlign = 'left'; }
          if (typeof(m.tex2jax) == 'undefined') { m.tex2jax = { }; }
          if (typeof(m.tex2jax.inlineMath) == 'undefined')     { m.tex2jax.inlineMath     = [ ['##','##'], ["\\(","\\)"] ]; }
          if (typeof(m.tex2jax.displayMath) == 'undefined')    { m.tex2jax.displayMath    = [ ['$$','$$'], ["\\[","\\]"] ]; }
          if (typeof(m.tex2jax.processEscapes) == 'undefined') { m.tex2jax.processEscapes = true; }
    }

    smjax = document.createElement ('script');
    smjax.setAttribute('src',`${mjax_path}/MathJax.js?config=${mjax_config}`);
    smjax.setAttribute('async',true);
    document.getElementsByTagName('head')[0].appendChild(smjax);
  }
};

if (document.readyState === 'loading') {  window.addEventListener('DOMContentLoaded', run_maths); }
else { run_maths(); }
