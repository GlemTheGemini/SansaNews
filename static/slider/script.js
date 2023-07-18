    const slider = document.querySelector(".slider");
    const nextBtn = document.querySelector(".next-btn");
    const prevBtn = document.querySelector(".prev-btn");
    const slides = document.querySelectorAll(".slide");
    const slideIcons = document.querySelectorAll(".slide-icon");
    const numberOfSlides = slides.length;
    var slideNumber = 0;

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

    //image slider previous button
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

    document.addEventListener('DOMContentLoaded', function() {
      formatAllTextAndColor();
    });
    
    function formatAllTextAndColor() {
      const descripciones = document.querySelectorAll('#descripcion');
    
      descripciones.forEach(descripcion => {
        const texto = descripcion.textContent.trim();
        const bloquesTexto = texto.split(/(?<=\.\s|\uD800[\uDC00-\uDFFF]|\uD83C[\uDF00-\uDFFF]|\uD83D[\uDC00-\uDDFF]|\uD83E[\uDD00-\uDDFF])/);
    
        descripcion.innerHTML = '';
    
        let parrafoActual = null;
        bloquesTexto.forEach(bloque => {
          if (bloque !== '') {
            if (bloque.match(/[\uD800-\uDFFF]|[\uD83C-\uD83E][\uDC00-\uDFFF]/)) {
              if (parrafoActual) {
                descripcion.appendChild(parrafoActual);
              }
              parrafoActual = document.createElement('p');
              parrafoActual.innerHTML = bloque;
              descripcion.appendChild(parrafoActual);
            } else if (bloque.startsWith('. ')) {
              parrafoActual.innerHTML += bloque;
            } else {
              const updatedBloque = bloque.replace(/(@\w+|#\w+)/g, '<span class="special-char">$1</span>');
              const ocurrencias = updatedBloque.match(/(@\w+|#\w+)/g);
              if (ocurrencias) {
                if (parrafoActual) {
                  descripcion.appendChild(parrafoActual);
                }
                parrafoActual = document.createElement('p');
                ocurrencias.forEach(ocurrencia => {
                  updatedBloque = updatedBloque.replace(ocurrencia, `<span class="special-char">${ocurrencia}</span>`);
                });
                parrafoActual.innerHTML = updatedBloque;
                descripcion.appendChild(parrafoActual);
              } else {
                if (!parrafoActual) {
                  parrafoActual = document.createElement('p');
                  descripcion.appendChild(parrafoActual);
                }
                parrafoActual.innerHTML += bloque;
              }
            }
          }
        });
        if (parrafoActual) {
          descripcion.appendChild(parrafoActual);
        }
      });
    }
    //image slider autoplay
    //var playSlider;
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
      }, 10000);
    }
    repeater();*/
    /*
    //stop the image slider autoplay on mouseover
    slider.addEventListener("mouseover", () => {
      clearInterval(playSlider);
    });

    //start the image slider autoplay again on mouseout
    slider.addEventListener("mouseout", () => {
      repeater();
    });*/