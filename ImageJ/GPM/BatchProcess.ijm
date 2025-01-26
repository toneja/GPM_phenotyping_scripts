// Macro to batch process a folder of images one at a time
inputFolder = getArgument();
if (indexOf(inputFolder, "UVC") != -1) {
    assayType = "UVC";
} else {
    assayType = "fungicide";
}

// Get a list of files in the input folder
list = getFileList(inputFolder);

// Process each image file in the folder
for (i = 0; i < list.length; i++) {
    if (endsWith(list[i], ".jpg")) {
        // Open the image
        open(inputFolder + "/" + list[i]);

        // Execute our main macro
        runMacro("../GPM/AnalyzeSporesAndGermlings.ijm", assayType);

        // Close the image
        close();
    }
}

// Exit ImageJ
run("Quit");
