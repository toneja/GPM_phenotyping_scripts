// Open image stack from arguments if available
var closeWindow = false;
if (lengthOf(getArgument()) > 0) {
	// Open the virtual stack of images
	open(getArgument(), "virtual");
	closeWindow = true;
}

// Crop image stack to 1500px diameter circle in center of image
r = 750;
x = (getWidth() / 2) - r;
y = (getHeight() / 2) - r;
setTool("oval");
makeOval(x, y, r * 2, r * 2);
run("Crop");
saveAs("tif", "GPM/images/" + getTitle());

// Subtract background from image stack
run("Subtract Background...", "rolling=10 light stack");

// Generate a binary image from our image stack
setAutoThreshold("Default");
setThreshold(0, 240);
setOption("BlackBackground", false);
run("Convert to Mask", "method=Default background=Light");
run("Fill Holes", "stack");
saveAs("tif", "GPM/images/" + getTitle());

// Generate ROIs
run("Set Measurements...", "area centroid perimeter fit shape feret's stack redirect=None decimal=3");
run("Analyze Particles...", "size=100-600 circularity=0.00-0.97 show=Overlay display exclude include add stack");
roiManager("Show None");
saveAs("Results", "GPM/results/Results_" + File.getNameWithoutExtension(getTitle()) + ".csv");

// Close ImageJ window when running in batches
if (closeWindow) {
	run("Quit");
}
