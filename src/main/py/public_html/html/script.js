console.log("---Start---");
const SIZE_LIMIT = 512000;

let current_image = "XXXXXXX";
let sensorName = "-sensor-";
let year = 2099;
let month = 0;
let day = 0;
let hour = 0;
let minute = 0;


let imageData = {}
let metadata = {}

async function fetchData() {
    console.log(".fetchData() - start method")
    try {
        const response = await fetch('/captures.json');
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        if (data.pictures && data.metadata) {
            // Update imageData with data from capture.json
            imageData = data.pictures;

            // Update metadata with data from capture.json
            metadata = data.metadata;

            console.log(".fetchData() - Données mises à jour avec succès:", imageData, metadata);
        } else {
            console.error(".fetchData() - Le format JSON est incorrect.");
        }
    } catch (error) {
        console.error(".fetchData() - Une erreur s'est produite lors de la récupération des données:", error.message);
    }
}

// Function to update the current_image element
function updateCurrentImage(data) {
    console.log("---updateCurrentImage(" + data + ")---");

    const currentImage = data.img

    // Change the src attribute of the main image
    document.getElementById("capture-img").src = "../captures/tilleul/2020/12-29/" + currentImage;

    // Extract sensorName using a regular expression
    let sensorName = currentImage.match(/^(.*?)_\d{4}-\d{2}-\d{2}/)[1];

    // Extract year, month, day, hour, and minute using string splitting and parsing
    const parts = currentImage.split(/[_-]|Z/g); // Split by '_', '-', and 'Z'
    year = parseInt(parts[1], 10);
    month = parseInt(parts[2], 10);
    day = parseInt(parts[3], 10);
    hour = parseInt(parts[4], 10);
    minute = parseInt(parts[5], 10);

    document.getElementById("current-minute").textContent = minute.toString().padStart(2, '0');
    document.getElementById("current-hour").textContent = hour;
    document.getElementById("current-day").textContent = day;
    document.getElementById("current-month").textContent = month;
    document.getElementById("current-year").textContent = year;
    document.getElementById("current-sensorName").textContent = sensorName;
}

document.addEventListener("DOMContentLoaded", function () {
    console.log("DOMContentLoaded - ---DOMContentLoaded-start---");

    // Appeler la fonction fetchData pour obtenir les données au chargement de la page
    console.log("DOMContentLoaded - before fetchData call")
    fetchData();
    console.log("DOMContentLoaded - after fetchData call:", imageData, metadata);
    //delay(5000);
    /*const imageData = {
        "06h30": {fSize: 46533, img: "tilleul_2020-12-29Z06-30-08.jpg"},
        "06h45": {fSize: 46641, img: "tilleul_2020-12-29Z06-45-08.jpg"},
        "07h00": {fSize: 46604, img: "tilleul_2020-12-29Z07-00-08.jpg"},
        "07h15": {fSize: 108528, img: "tilleul_2020-12-29Z07-15-08.jpg"},
        "07h30": {fSize: 791501, img: "tilleul_2020-12-29Z07-30-08.jpg"},
        "07h45": {fSize: 1087651, img: "tilleul_2020-12-29Z07-45-08.jpg"},
        "08h00": {fSize: 1093435, img: "tilleul_2020-12-29Z08-00-08.jpg"},
        "08h15": {fSize: 1116305, img: "tilleul_2020-12-29Z08-15-08.jpg"},
        "08h30": {fSize: 1160192, img: "tilleul_2020-12-29Z08-30-08.jpg"},
        "08h45": {fSize: 1153000, img: "tilleul_2020-12-29Z08-45-08.jpg"}
    };*/

    for (let hour = 0; hour <= 23; hour++) {
        for (let minute = 0; minute < 60; minute += 15) {
            // Format the hour and minute as "HHhMM"
            const formattedHour = hour.toString().padStart(2, '0');
            const formattedMinute = minute.toString().padStart(2, '0');
            // Create the time string
            const identif = `${formattedHour}h${formattedMinute}`;
            // Now, you can use the 'identif' variable in your loop
            const data = imageData[identif];

            // Get the element by its ID
            const element = document.getElementById(identif);
            if (data) {
                // Update the displayed current_image
                console.log("DOMContentLoaded - addEventListener: '" + identif + "' -> '" + data + "'")
                element.addEventListener("click", function () {
                    updateCurrentImage(data);
                });
                // Add an event listener to each table cell

                if (data.fSize < SIZE_LIMIT) {
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
                console.log("DOMContentLoaded - No 'data' for identif '" + identif + "'.");
                document.getElementById(identif).style.backgroundColor = "DarkGray";
                document.getElementById(identif).style.cursor = "default";
                /* add "cursor: pointer;" */
            }
        }
    }
    console.log("DOMContentLoaded - ---DOMContentLoaded-end---");
});
console.log("---End---");
