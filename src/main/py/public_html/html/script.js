console.log("---Start---");
const SIZE_LIMIT = 512000;

let current_image = "XXXXXXX";
let sensorName = "-sensor-";
let year = 2099;
let month = 0;
let day = 0;
let hour = 0;
let minute = 0;

let picturesData = {};
let metadata = {};

async function fetchData() {
    console.log(".fetchData() - start method");
    try {
        const response = await fetch('/captures.json');
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        if (data.pictures && data.metadata) {
            // Update picturesData with data from capture.json
            picturesData = data.pictures;
            // Update metadata with data from capture.json
            metadata = data.metadata;
            console.log(".fetchData() - Data updated successfully:", picturesData, metadata);

            sensorName = metadata.sensor
            // FIXME string>int year = metadata.year
            // TODO month = f( metadata.month_day )
            // TODO day = f( metadata.month_day )
            console.log(".fetchData() - interpreted metadata:", sensorName, year);
        } else {
            console.error(".fetchData() - Incorrect JSON format.");
        }
    } catch (error) {
        console.error(".fetchData() - An error occurred during the fetching of data from captures.json:", error.message);
    }
}

// Function to update the current_image element
function updateCurrentImage(pictureData) {
    const currentImage = pictureData.img;
    console.log(".updateCurrentImage('" + currentImage + "')");

    // Change the src attribute of the main image
    document.getElementById("capture-img").src = "../captures/" + metadata.sensor + "/" + metadata.year + "/" + metadata.month_day + "/" + currentImage;

    // Extract sensorName using a regular expression
    let sensorName = currentImage.match(/^(.*?)_\d{4}-\d{2}-\d{2}/)[1];

    // Extract year, month, day, hour, and minute using string splitting and parsing
    const parts = currentImage.split(/[_-]|Z/g); // Split by '_', '-', and 'Z'
    year = parseInt(parts[1], 10);
    month = parseInt(parts[2], 10);
    day = parseInt(parts[3], 10);
    hour = parseInt(parts[4], 10);
    minute = parseInt(parts[5], 10);

    document.getElementById("current_hh_mm").textContent = hour + ":" + minute.toString().padStart(2, '0');
    document.getElementById("current_day").textContent = day;
    document.getElementById("current_month").textContent = month;
    document.getElementById("current_year").textContent = year;
    document.getElementById("current_sensorName").textContent = sensorName;

    // TODO Check consistency with metadata
    document.getElementById("error_message").textContent = metadata.error_message; // TODO Implement error message display
}

function grayPictureSelectorWithoutEvent() {
    for (let hour = 0; hour <= 23; hour++) {
        for (let minute = 0; minute < 60; minute += 15) {
            // Format the hour and minute as "HHhMM"
            const formattedHour = hour.toString().padStart(2, '0');
            const formattedMinute = minute.toString().padStart(2, '0');
            // Create the time string
            const hh_mm = `${formattedHour}h${formattedMinute}`;
            console.log("Checking if element '" + hh_mm + "' has listeners...");
            // Assuming hh_mm_element is your HTML element
            const hh_mm_element = document.getElementById(hh_mm);
            // Get the event listeners for the "click" event

            const text = hh_mm_element.textContent
            console.log("content is '" + text + "'")

            const clickListeners = hh_mm_element.onclick;
            // Check if there are click event listeners
            if (text === "-") {
                console.log("Element '" + hh_mm + "' has a single 'dash' as text content.");
                document.getElementById(hh_mm).style.backgroundColor = "DarkGray";
                document.getElementById(hh_mm).style.cursor = "default";
            } else {
                console.log("Element '" + hh_mm + "' has text content = '" + text + "'.");
            }
        }
    }
}

function updatePictureSelector(hh_mm, pictureData) {
    const mm = hh_mm.slice(-2)
    const mmAsInt = parseInt(mm)
    let hh_mm15
    if (mmAsInt % 15 === 0) {
        // mmAsInt is a multiple of 15
        hh_mm15 = hh_mm
    } else {
        // mmAsInt is not a multiple of 15
        hh_mm15 = hh_mm.substring(0, 3) + (mmAsInt - (mmAsInt % 15)).toString()
    }

    // Get the hh_mm_element by its ID
    const hh_mm_element = document.getElementById(hh_mm15);

    hh_mm_element.textContent = mm

    // Update the displayed current_image
    console.log("DOMContentLoaded - addEventListener: '" + hh_mm + "' -> '" + pictureData + "'")
    hh_mm_element.addEventListener("click", function () {
        updateCurrentImage(pictureData);
    });
    // Add an event listener to each table cell

    if (pictureData.fSize < SIZE_LIMIT) {
        //hh_mm_element.style.backgroundColor = rgba(173, 216, 230, 0.5);
        hh_mm_element.style.backgroundColor = "LightBlue";
    } else {
        hh_mm_element.style.backgroundColor = "Khaki";
    }
    hh_mm_element.style.cursor = "pointer";

    // Add a mouseover event listener
    hh_mm_element.addEventListener("mouseover", function () {
        hh_mm_element.classList.add("hovered-cell");
    });
    // Add a mouseout event listener
    hh_mm_element.addEventListener("mouseout", function () {
        hh_mm_element.classList.remove("hovered-cell");
    });

    /*
    * cell:hover {
background-color: lightblue
    * */
}

function fillPictureSelector_deprecated() {
    for (let hour = 0; hour <= 23; hour++) {
        for (let minute = 0; minute < 60; minute += 15) {
            // Format the hour and minute as "HHhMM"
            const formattedHour = hour.toString().padStart(2, '0');
            const formattedMinute = minute.toString().padStart(2, '0');
            // Create the time string
            const hh_mm = `${formattedHour}h${formattedMinute}`;
            // Now, you can use the 'hh_mm' variable in your loop
            const pictureData = picturesData[hh_mm];

            if (pictureData) {
                updatePictureSelector(hh_mm, pictureData)
            } else {
                console.log("DOMContentLoaded - No 'pictureData' for hh_mm '" + hh_mm + "'.");
                document.getElementById(hh_mm).style.backgroundColor = "DarkGray";
                document.getElementById(hh_mm).style.cursor = "default";
            }
        }
    }
}

function fillPictureSelector() {
    // Iterate through each element inside "pictures"
    for (const element_hh_mm in picturesData) { // rely on
        if (picturesData.hasOwnProperty(element_hh_mm)) {
            let pictureData = {};
            pictureData.img = undefined;
            pictureData.fSize = undefined;
            pictureData = picturesData[element_hh_mm];
            console.log(`Element ${element_hh_mm}:`, pictureData);
            // Your logic for each element goes here

            updatePictureSelector(element_hh_mm, pictureData)
        }
    }

    grayPictureSelectorWithoutEvent()
}

document.addEventListener("DOMContentLoaded", async function () {
    console.log("DOMContentLoaded - ---DOMContentLoaded-start---");

    // Call fetchData function to get data after page loaded:
    await fetchData(); // Wait for fetchData to complete
    console.log("DOMContentLoaded - after fetchData call:", picturesData, metadata);
    const picturesFolder = "captures/" + metadata.sensor + "/"
    console.log("DOMContentLoaded - picturesFolder =", picturesFolder);

    fillPictureSelector()

    console.log("DOMContentLoaded - ---DOMContentLoaded-end---");
});

console.log("---End---");
