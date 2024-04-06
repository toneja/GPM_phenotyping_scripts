// Options
var cropRadius = 600
var thresholdCeiling = 240
var thresholdMethod = "raw"
var useBlur = true

// Open image stack from arguments if available
var closeWindow = false;
if (lengthOf(getArgument()) > 0) {
	// Open the virtual stack of images
	open(getArgument(), "virtual");
	closeWindow = true;
}

// Crop image stack to thresholdCeiling * 2 diameter circle in center of image
r = cropRadius;
x = (getWidth() / 2) - r;
y = (getHeight() / 2) - r;
setTool("oval");
makeOval(x, y, r * 2, r * 2);
run("Crop");
// saveAs("tif", "GPM/images/" + getTitle());

// Subtract background from image stack
run("Subtract Background...", "rolling=10 light stack");

// Set thresholds
if (thresholdMethod == "raw") {
	setThreshold(0, thresholdCeiling, "raw");
} else {
	setAutoThreshold("thresholdMethod stack");
}

// Blur image to reduce breaking up of germination tubes
if (useBlur) {
	run("Gaussian Blur...", "sigma=1 stack");
}

// Generate a binary image from our image stack
run("Convert to Mask", "method=thresholdMethod background=Light");

// Remove some of the small speckles
run("Despeckle", "stack");
run("Fill Holes", "stack");
saveAs("tif", "GPM/images/" + getTitle());

// Generate ROIs
run("Set Measurements...", "area centroid perimeter fit shape feret's stack redirect=None decimal=3");
run("Analyze Particles...", "size=60-600 circularity=0.00-1.00 show=Overlay display exclude include add stack");
roiManager("Show None");
saveAs("Results", "GPM/results/Results_" + File.getNameWithoutExtension(getTitle()) + ".csv");

// Close ImageJ window when running in batches
if (closeWindow) {
	run("Quit");
}
