//jquery for toggle dropdown menus
$(document).ready(function(){
    //toggle sub-menus
    $(".sub-btn").click(function(){
      $(this).next(".sub-menu").slideToggle();
    });

    function closeMenuOnMouseLeave() {
        $(".sub-menu").slideUp();
    }

    // Detectar si el menú está desplegado y cerrarlo cuando se quita el mouse de encima
    $(".sub-menu").mouseleave(function(){
      if ($(this).is(":visible")) {
        closeMenuOnMouseLeave();
      }
    });

    //toggle more-menus
    $(".more-btn").click(function(){
      $(this).next(".more-menu").slideToggle();
    });
});

  //javascript for the responsive navigation menu
  var menu = document.querySelector(".menu");
  var menuBtn = document.querySelector(".menu-btn");
  var closeBtn = document.querySelector(".close-btn");

  menuBtn.addEventListener("click", () => {
    menu.classList.add("active");
  });

  closeBtn.addEventListener("click", () => {
    menu.classList.remove("active");
  });

  //javascript for the navigation bar effects on scroll
  window.addEventListener("scroll", function(){
    var header = document.querySelector("header");
    header.classList.toggle("sticky", window.scrollY > 0);
  });