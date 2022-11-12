// buttons
var sliderControl = document.querySelector(".slider-control");

// slides informations
var slides = document.querySelectorAll(".slide"),
  slidesLength = slides.length;

// slides array
var slidesArr = [].slice.call(slides);

// reverse array sorting
slidesArr = slidesArr.reverse();

// slide current
var slideCurrent = 0;

sliderControl.addEventListener("click", function (e) {
  target = e.target;

  // get next button
  if (target.classList.contains("next")) {
    (next = e.target),
      (prev = next.previousElementSibling),
      (nextSlide = slidesArr[slideCurrent + 1]),
      (slide = slidesArr[slideCurrent]);

    slide.classList.add("slide-on");
    slide.classList.remove("text-on");
    nextSlide.classList.add("text-on");

    slideCurrent += 1;

    if (slideCurrent > 0) {
      prev.classList.remove("disabled");
    }

    if (slideCurrent === slidesLength - 1) {
      next.classList.add("disabled");
    }
  }

  // get prev button
  if (target.classList.contains("prev")) {
    slideCurrent -= 1;

    (prev = e.target),
      (next = prev.nextElementSibling),
      (prevSlide = slidesArr[slideCurrent + 1]),
      (slide = slidesArr[slideCurrent]);

    prevSlide.classList.remove("text-on");
    slide.classList.remove("slide-on");
    slide.classList.add("text-on");

    if (slideCurrent === slidesLength - 2) {
      next.classList.remove("disabled");
    }

    if (slideCurrent === 0) {
      prev.classList.add("disabled");
    }
  }
});

balapaCop("Image Slider", "#999");