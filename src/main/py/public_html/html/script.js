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

document.addEventListener("DOMContentLoaded", async function () {
    console.log("DOMContentLoaded - ---DOMContentLoaded-start---");

    // Appeler la fonction fetchData pour obtenir les données au chargement de la page
    console.log("DOMContentLoaded - before fetchData call");
    await fetchData(); // Wait for fetchData to complete
    console.log("DOMContentLoaded - after fetchData call:", picturesData, metadata);
    const picturesFolder = "captures/" + metadata.sensor + "/"
    console.log("DOMContentLoaded - picturesFolder =", picturesFolder);

    for (let hour = 0; hour <= 23; hour++) {
        for (let minute = 0; minute < 60; minute += 15) {
            // Format the hour and minute as "HHhMM"
            const formattedHour = hour.toString().padStart(2, '0');
            const formattedMinute = minute.toString().padStart(2, '0');
            // Create the time string
            const identif = `${formattedHour}h${formattedMinute}`;
            // Now, you can use the 'identif' variable in your loop
            const picturedata = picturesData[identif];

            // Get the element by its ID
            const element = document.getElementById(identif);
            if (picturedata) {
                // Update the displayed current_image
                console.log("DOMContentLoaded - addEventListener: '" + identif + "' -> '" + picturedata + "'")
                element.addEventListener("click", function () {
                    updateCurrentImage(picturedata);
                });
                // Add an event listener to each table cell

                if (picturedata.fSize < SIZE_LIMIT) {
                    //element.style.backgroundColor = rgba(173, 216, 230, 0.5);
                    element.style.backgroundColor = "LightBlue";
                } else {
                    element.style.backgroundColor = "Khaki";
                }
                element.style.cursor = "pointer";

                // Add a mouseover event listener
                element.addEventListener("mouseover", function () {
                    element.classList.add("hovered-cell");
                });
                // Add a mouseout event listener
                element.addEventListener("mouseout", function () {
                    element.classList.remove("hovered-cell");
                });

                /*
                * cell:hover {
background-color: lightblue
                * */

            } else {
                console.log("DOMContentLoaded - No 'picturedata' for identif '" + identif + "'.");
                document.getElementById(identif).style.backgroundColor = "DarkGray";
                document.getElementById(identif).style.cursor = "default";
                /* add "cursor: pointer;" */
            }
        }
    }

    console.log("DOMContentLoaded - ---DOMContentLoaded-end---");
});

console.log("---End---");
