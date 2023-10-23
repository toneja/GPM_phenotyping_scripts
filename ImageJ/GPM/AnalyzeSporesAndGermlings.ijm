// Open image stack from arguments if available
var closeWindow = false;
if (lengthOf(getArgument()) > 0) {
	// Open the virtual stack of images
	open(getArgument(), "virtual");
	closeWindow = true;
}

// Crop image stack to 1000x1000 in center of image
size = 1000;
makeRectangle(getWidth()/2-size/2, getHeight()/2-size/2, size, size);
run("Crop");
saveAs("tif", "GPM/images/" + getTitle());

// Subtract background from image stack
run("Subtract Background...", "rolling=10 light stack");
// Blur image to reduce breaking up of germination tubes
run("Gaussian Blur...", "sigma=1 stack");
// normalize contrast 
run("Enhance Contrast...", "saturated=0.50 normalize process_all use");

// Generate a binary image from our image stack
setAutoThreshold("MaxEntropy stack");
run("Convert to Mask", "method=MaxEntropy background=Light");
// Remove some of the small speckles
run("Despeckle", "stack");
saveAs("tif", "GPM/images/" + getTitle());

// Generate ROIs
run("Set Measurements...", "area centroid perimeter fit shape feret's stack redirect=None decimal=3");
run("Analyze Particles...", "size=40-600 circularity=0.00-1.00 show=Overlay display exclude include add stack");
roiManager("Show None");
saveAs("Results", "GPM/results/Results_" + File.getNameWithoutExtension(getTitle()) + ".csv");

// Close ImageJ window when running in batches
if (closeWindow) {
	run("Quit");
}
