// Enhance contrast for inconsistent images
run("Enhance Contrast...", "saturated=0.35 normalize");

// Crop image to 1000x1000 in center of image
size = 1000;
makeRectangle(getWidth()/2-size/2, getHeight()/2-size/2, size, size);
run("Crop");

// Subtract background from image
run("Subtract Background...", "rolling=10 light");

// Set thresholds
setAutoThreshold("MaxEntropy");
// setThreshold(0, 240, "raw");

// Generate a binary image from our image
run("Convert to Mask", "background=Light");

// Remove some of the small speckles
run("Despeckle");

// Try to fill in some of the gaps
run("Fill Holes");

// Save final manipulated image
saveAs("tif", "GPM/images/" + getTitle());

// Generate ROIs
run("Set Measurements...", "area centroid perimeter fit shape feret's redirect=None decimal=3");
run("Analyze Particles...", "size=50-500 circularity=0.00-1.00 show=Overlay exclude include add");
roiManager("Show None");
saveAs("Results", "GPM/results/" + File.getNameWithoutExtension(getTitle()) + ".csv");
