const potrace = require('potrace');
const fs = require('fs');

const imagePath = 'C:/Users/rishi/.gemini/antigravity-ide/brain/58c5b061-3e8d-4aa2-bb14-777755c86d3f/media__1780124376173.jpg';

const params = {
  threshold: 110,
  turdsize: 15,
  optTolerance: 0.2
};

potrace.trace(imagePath, params, (err, svg) => {
  if (err) {
    console.error(err);
    process.exit(1);
  }
  fs.writeFileSync('t:/Vaastu Next/lotus.svg', svg);
  console.log('SVG generated successfully!');
});
