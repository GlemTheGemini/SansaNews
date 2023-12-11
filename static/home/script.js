
$(document).ready(function() {
  var $cell = $('.card');

  //open and close card when clicked on card
  $cell.find('.js-expander').click(function () {
    
    var $thisCell = $(this).closest('.card');

    if ($thisCell.hasClass('is-collapsed')) {
      $cell.not($thisCell).removeClass('is-expanded').addClass('is-collapsed').addClass('is-inactive');
      $thisCell.removeClass('is-collapsed').addClass('is-expanded');

      if ($cell.not($thisCell).hasClass('is-inactive')) {
        //do nothing
      } else {
        $cell.not($thisCell).addClass('is-inactive');
      }

    } else {
      $thisCell.removeClass('is-expanded').addClass('is-collapsed');
      $cell.not($thisCell).removeClass('is-inactive');
    }
  });

  //close card when click on cross
  $cell.find('.js-collapser').click(function () {

    var $thisCell = $(this).closest('.card');

    $thisCell.removeClass('is-expanded').addClass('is-collapsed');
    $cell.not($thisCell).removeClass('is-inactive');

  });
});


const slider = document.querySelector(".slider");
const nextBtn = document.querySelector(".next-btn");
const prevBtn = document.querySelector(".prev-btn");
const slides = document.querySelectorAll(".slide");
const slideIcons = document.querySelectorAll(".slide-icon");
const numberOfSlides = slides.length;
var slideNumber = 0;
var playSlider;
const caracteres = document.addEventListener('DOMContentLoaded', function() {
  separateParagraphs();
  formatSpecialChars();
});
//image slider next button
nextBtn.addEventListener("click", () => {
  slides.forEach((slide) => {
    slide.classList.remove("active");
  });
  slideIcons.forEach((slideIcon) => {
    slideIcon.classList.remove("active");
  });
  slideNumber++;
  if(slideNumber > (numberOfSlides - 1)){
    slideNumber = 0;
  }
  slides[slideNumber].classList.add("active");
  slideIcons[slideNumber].classList.add("active");
});


//image slider previous button (no utilizado)
/*
prevBtn.addEventListener("click", () => {
  slides.forEach((slide) => {
    slide.classList.remove("active");
  });
  slideIcons.forEach((slideIcon) => {
    slideIcon.classList.remove("active");
  });
  slideNumber--;
  if(slideNumber < 0){
    slideNumber = numberOfSlides - 1;
  }
  slides[slideNumber].classList.add("active");
  slideIcons[slideNumber].classList.add("active");
});
*/

function separateParagraphs() {
  const descripciones = document.querySelectorAll('#descripcion');

  descripciones.forEach(descripcion => {
    const texto = descripcion.textContent.trim();
    const parrafos = texto.split('. ');

    descripcion.innerHTML = '';

    parrafos.forEach(parrafo => {
      const p = document.createElement('p');
      p.innerHTML = parrafo;
      descripcion.appendChild(p);
    });
  });
}

function formatSpecialChars() {
  const parrafos = document.querySelectorAll('#descripcion p');

  parrafos.forEach(parrafo => {
    const texto = parrafo.innerHTML;
    const updatedTexto = texto.replace(/(@[\w\u00C0-\u017F._]+)/g, '<span class="special-char">$1</span>')
                              .replace(/(#[\w\u00C0-\u017F]+)/g, '<span class="special-char">$1</span>');
    parrafo.innerHTML = updatedTexto;
  });
}


//image slider autoplay (no se utiliza)
/*
var repeater = () => {
  playSlider = setInterval(function(){
    slides.forEach((slide) => {
      slide.classList.remove("active");
    });
    slideIcons.forEach((slideIcon) => {
      slideIcon.classList.remove("active");
    });
    slideNumber++;
    if(slideNumber > (numberOfSlides - 1)){
      slideNumber = 0;
    }
    slides[slideNumber].classList.add("active");
    slideIcons[slideNumber].classList.add("active");
  }, 6000);
}
repeater();

*/
