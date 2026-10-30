// Header border on scroll, copy-email button, play videos only while visible.
(function(){
  var top=document.getElementById('top');
  addEventListener('scroll',function(){top.classList.toggle('scrolled',scrollY>8)},{passive:true});

  document.querySelectorAll('[data-copy]').forEach(function(b){
    b.addEventListener('click',function(){
      var label=b.textContent;
      navigator.clipboard.writeText(b.dataset.copy).then(function(){
        b.textContent='Copied';
        setTimeout(function(){b.textContent=label},1600);
      });
    });
  });

  var still=matchMedia('(prefers-reduced-motion: reduce)').matches;
  var videos=document.querySelectorAll('video');
  if(!videos.length||!('IntersectionObserver' in window))return;
  var io=new IntersectionObserver(function(es){es.forEach(function(e){
    if(e.isIntersecting&&!still){e.target.play().catch(function(){})}else{e.target.pause()}
  })},{threshold:.4});
  videos.forEach(function(v){if(still)v.setAttribute('controls','');io.observe(v)});
})();
