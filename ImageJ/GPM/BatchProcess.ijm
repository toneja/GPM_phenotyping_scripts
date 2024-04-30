// Macro to batch process a folder of images one at a time
inputFolder = getArgument();

// Get a list of files in the input folder
list = getFileList(inputFolder);

// Process each image file in the folder
for (i = 0; i < list.length; i++) {
    if (endsWith(list[i], ".tif") || endsWith(list[i], ".jpg")) {
        // Open the image
        open(inputFolder + "/" + list[i]);
        
        // Execute our main macro
        runMacro("../GPM/AnalyzeSporesAndGermlings.ijm");
        
        // Close the image
        close();
    }
}
