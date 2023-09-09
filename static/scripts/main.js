const skillItems = document.querySelectorAll('.skill-item');
skillItems.forEach((item) => {
    const skillInfoBarInput = item.querySelector('.skill-info-bar-input');
    skillInfoBarInput.addEventListener('input', () => {
        const skillInfoBarValue = item.querySelector('.skill-info-bar-value');
        skillInfoBarValue.innerHTML = "+" + skillInfoBarInput.value + "min";
        skillInfoBarValue.style.transform = "translateX(" + (3.33 * skillInfoBarInput.value - 150) + "%)";
    });
    const skillProgressBar = item.querySelector('.skill-progress-bar');
    const progressPercentage = skillProgressBar.style.width.replace('%', '') / 100;
    const percentageColor = getPercentageColor(progressPercentage);
    skillProgressBar.style.backgroundColor = percentageColor;
});

const skillContainer = document.querySelector('.skill-container');
skillContainer.style.height = skillContainer.offsetHeight + 60 + "px";

function getRgb(color) {
  let [r, g, b] = color.replace('rgb(', '')
    .replace(')', '')
    .split(',')
    .map(str => Number(str));;
  return {
    r,
    g,
    b
  }
}

function colorInterpolate(colorA, colorB, intval) {
  const rgbA = getRgb(colorA),
    rgbB = getRgb(colorB);
  const colorVal = (prop) =>
    Math.round(rgbA[prop] * (1 - intval) + rgbB[prop] * intval);
  return {
    r: colorVal('r'),
    g: colorVal('g'),
    b: colorVal('b'),
  }
}

function getPercentageColor(progression) {
  const color1 = 'rgb(233, 196, 106)';
  const color2 = 'rgb(231, 111, 81)';

  const rgbNew = colorInterpolate(
    color1,
    color2, progression
  );

  return `rgb( ${rgbNew.r}, ${rgbNew.g}, ${rgbNew.b})`;
}