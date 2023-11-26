console.log("---Start---");
const SIZE_LIMIT = 512000;

let hour = undefined; // :int
let minute = undefined; // :int
let firstDaylightHhMm = undefined;
let lastDaylightHhMm = undefined;
let lastHhMm = undefined;

let picturesData = {};
let metadata = {};
let sortedPictures = undefined;
let index = undefined;
let selectedHhMm15 = undefined;
let selectedPicture = undefined;

async function fetchData(sensor, year, month, day) {
    console.log(".fetchData('" + sensor + "', '" + year + "', '" + month + "', '" + day + "') - start method");
    // Construct the URL with parameters for the fetch call
    let url = "/captures.json";
    let firstParam = true;
    if (sensor !== null) {
        url += (firstParam ? "?s=" : "&s=") + sensor
        firstParam = false
    }
    if (year !== null) {
        url += (firstParam ? "?y=" : "&y=") + year
        firstParam = false
    }
    if (month !== null) {
        url += (firstParam ? "?m=" : "&m=") + month
        firstParam = false
    }
    if (day !== null) {
        url += (firstParam ? "?d=" : "&d=") + day
    }
    try {
        const response = await fetch(url);
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
            sortedPictures = Object.keys(picturesData).sort();

            console.log(".fetchData() - interpreted metadata:", metadata.sensor, metadata.year);
        } else {
            console.error(".fetchData() - Incorrect JSON format.");
        }
    } catch (error) {
        console.error(".fetchData() - An error occurred during the fetching of data from captures.json:", error.message);
    }
}

async function handlePreviousDayClick() {
    console.log(".handlePreviousDayClick() - Event 'click' on element #previous_day");
    console.log("metadata.sensor = " + metadata.sensor);
    console.log("metadata.year = " + metadata.year);
    console.log("metadata.month_day (current) = " + metadata.month_day);
    const [month, day] = metadata.month_day.split("-");
    await refreshDate(metadata.sensor, metadata.year, month, parseInt(day) - 1);
}

async function updateDateData() {
    console.log(".updateDateData()");
    document.getElementById("current_year").textContent = metadata.year;
    const [month, day] = metadata.month_day.split("-");
    document.getElementById("current_month").textContent = month;
    document.getElementById("current_day").textContent = day;
    document.getElementById("current_sensor").textContent = metadata.sensor;

    makeElementClickable(document.getElementById("previous_day"));
    //document.getElementById("previous_day").addEventListener("click", handlePreviousDayClick());
}

/**
 Reset background of top picture selector for currently selected
 */
async function unselectPictureSelector() {
    console.log(".unselectPictureSelector()");
    if (selectedHhMm15 !== undefined) {
        const hh_mm_element = document.getElementById(selectedHhMm15);
        if (selectedPicture.fSize < SIZE_LIMIT) {
            hh_mm_element.classList.remove("night-selected")
            hh_mm_element.classList.add("night")
        } else {
            hh_mm_element.classList.remove("day-selected")
            hh_mm_element.classList.add("day")
        }
        selectedHhMm15 = undefined;
    }
}

// Function to update the current_image element
async function updateCurrentImage(pictureData, hh_mm) {
    console.log(".updateCurrentImage('" + pictureData + "', '" + hh_mm + "')");
    const currentImage = pictureData.img;
    console.log("\t-> currentImage = " + currentImage);

    await unselectPictureSelector();

    // Change the src attribute of the main image
    document.getElementById("capture-img").src = "../captures/" + metadata.sensor + "/" + metadata.year + "/" + metadata.month_day + "/" + currentImage;

    const parts = currentImage.split(/[_-]|Z/g); // Split by '_', '-', and 'Z'
    hour = parseInt(parts[4], 10);
    minute = parseInt(parts[5], 10);

    selectedHhMm15 = hhMm15SelectorFor(parts[4] + "h" + parts[5]);
    selectedPicture = pictureData;
    const hh_mm_element = document.getElementById(selectedHhMm15);
    if (pictureData.fSize < SIZE_LIMIT) {
        hh_mm_element.classList.remove("night")
        hh_mm_element.classList.add("night-selected")
    } else {
        hh_mm_element.classList.remove("day")
        hh_mm_element.classList.add("day-selected")
    }

    document.getElementById("current_hh_mm").textContent = hour + ":" + minute.toString().padStart(2, '0');

    index = sortedPictures.indexOf(hh_mm);
    if (index > 0) {
        makeElementClickable(document.getElementById("previous_hh_mm"));
    } else {
        makeElementNotClickable(document.getElementById("previous_hh_mm"));
    }
    if (index < sortedPictures.length - 1) {
        makeElementClickable(document.getElementById("next_hh_mm"));
    } else {
        makeElementNotClickable(document.getElementById("next_hh_mm"));
    }

    // TODO Check consistency with metadata
    document.getElementById("error_message").textContent = metadata.error_message; // TODO Implement error message display
    if (metadata.error_message !== "") {
        alert("Error:\n" + metadata.error_message);
    }

    // await updateDateData(); // NOT TO DO WITHIN .updateCurrentImage()
}

function grayPictureSelectorWithoutEvent() {
    console.log(".grayPictureSelectorWithoutEvent()");
    for (let hour = 0; hour <= 23; hour++) {
        for (let minute = 0; minute < 60; minute += 15) {
            // Format the hour and minute as "HHhMM"
            const formattedHour = hour.toString().padStart(2, '0');
            const formattedMinute = minute.toString().padStart(2, '0');
            // Create the time string
            const hh_mm = `${formattedHour}h${formattedMinute}`;
            // Assuming hh_mm_element is your HTML element
            const hh_mm_element = document.getElementById(hh_mm);
            // Get the event listeners for the "click" event

            const text = hh_mm_element.textContent;
            // Check if there are click event listeners
            if (text === "—") {
                document.getElementById(hh_mm).style.backgroundColor = "DarkGray";
                document.getElementById(hh_mm).style.cursor = "default";
            }
        }
    }
}

function hhMm15SelectorFor(hh_mm) {
    console.log(".hhMm15SelectorFor('" + hh_mm + "')");
    const mm = hh_mm.slice(-2);
    const mmAsInt = parseInt(mm);
    let hh_mm15;
    if (mmAsInt % 15 === 0) {
        // mmAsInt is a multiple of 15
        hh_mm15 = hh_mm;
    } else {
        // mmAsInt is not a multiple of 15
        hh_mm15 = hh_mm.substring(0, 3) + (mmAsInt - (mmAsInt % 15)).toString();
    }
    return hh_mm15
}

async function fillPictureSelectorHhMm(hh_mm, pictureData) {
    console.log(".fillPictureSelectorHhMm('" + hh_mm + "', '" + pictureData + "')");
    const mm = hh_mm.slice(-2);
    const hh_mm15 = hhMm15SelectorFor(hh_mm)

    // Get the hh_mm_element by its ID
    const hh_mm_element = document.getElementById(hh_mm15);

    hh_mm_element.textContent = mm;

    // console.log("DOMContentLoaded - addEventListener: '" + hh_mm + "' -> '" + pictureData + "'")
    hh_mm_element.addEventListener("click", function () {
        updateCurrentImage(pictureData, hh_mm);
    });
    // Add an event listener to each table cell

    if (pictureData.fSize < SIZE_LIMIT) {
        hh_mm_element.classList.add("night")
    } else {
        hh_mm_element.classList.add("day")
    }

    makeElementClickable(hh_mm_element);
}

function makeElementClickable(element) {
    console.log(".makeElementClickable(-> element.id='" + element.id + "')");
    element.style.cursor = "pointer";

    // todo Replaceable with .buttonEnabled ?
    // Add a mouseover event listener
    element.addEventListener("mouseover", function () {
        element.classList.add("hovered-cell");
    });
    // Add a mouseout event listener
    element.addEventListener("mouseout", function () {
        element.classList.remove("hovered-cell");
    });

    element.classList.remove("buttonDisabled");
    element.classList.add("buttonEnabled");
}

function makeElementNotClickable(element) {
    console.log(".makeElementNotClickable(...)");
    element.style.cursor = "default";

    // Remove mouseover event listener
    element.removeEventListener("mouseover", function () {
    });
    // Add a mouseout event listener
    element.removeEventListener("mouseout", function () {
    });

    element.classList.remove("buttonEnabled");
    element.classList.add("buttonDisabled");
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
                fillPictureSelectorHhMm(hh_mm, pictureData);
            } else {
                console.log("DOMContentLoaded - No 'pictureData' for hh_mm '" + hh_mm + "'.");
                document.getElementById(hh_mm).style.backgroundColor = "DarkGray";
                document.getElementById(hh_mm).style.cursor = "default";
            }
        }
    }
}

async function fillPicturesSelector() {
    console.log(".fillPicturesSelector()");
    // Iterate through each element inside "pictures"
    for (const element_hh_mm in picturesData) { // rely on
        //if (picturesData.hasOwnProperty(element_hh_mm)) {
            let pictureData = {};
            pictureData.img = undefined;
            pictureData.fSize = undefined;
            pictureData = picturesData[element_hh_mm];
            console.log(`Element ${element_hh_mm}:`, pictureData);
            await fillPictureSelectorHhMm(element_hh_mm, pictureData);
            if ((firstDaylightHhMm === undefined) && pictureData.fSize > SIZE_LIMIT) {
                firstDaylightHhMm = element_hh_mm;
                const firstDaylightElement = document.getElementById("firstDaylight");
                firstDaylightElement.addEventListener("click", function () {
                    updateCurrentImage(pictureData, element_hh_mm);
                });
                makeElementClickable(firstDaylightElement);
            }
            if (pictureData.fSize > SIZE_LIMIT) {
                lastDaylightHhMm = element_hh_mm;
                const LastDaylightElement = document.getElementById("LastDaylight");
                LastDaylightElement.addEventListener("click", function () {
                    updateCurrentImage(pictureData, element_hh_mm);
                });
                makeElementClickable(LastDaylightElement);
            }
        //}
        lastHhMm = element_hh_mm;
    }
    grayPictureSelectorWithoutEvent()
}

async function previousHhMm() {
    console.log(".previousHhMm()");
    const previousKey = index > 0 ?
        sortedPictures[index - 1] : sortedPictures[0];
    await updateCurrentImage(picturesData[previousKey], previousKey);
}

async function nextHhMm() {
    console.log(".nextHhMm()");
    const nextKey = index < sortedPictures.length - 1 ?
        sortedPictures[index + 1] : sortedPictures[sortedPictures.length - 1];
    await updateCurrentImage(picturesData[nextKey], nextKey);
}

async function clearData() {
    console.log(".clearData()")
    hour = undefined; // :int
    minute = undefined; // :int
    firstDaylightHhMm = undefined;
    lastDaylightHhMm = undefined;
    lastHhMm = undefined;

    picturesData = {};
    metadata = {};
    sortedPictures = undefined;
    index = undefined;
    await unselectPictureSelector();
    selectedPicture = undefined;

    // Reset content of Top Picture Selector
    for (let hour = 0; hour <= 23; hour++) {
        for (let minute = 0; minute < 60; minute += 15) {
            // Format the hour and minute as "HHhMM"
            const formattedHour = hour.toString().padStart(2, '0');
            const formattedMinute = minute.toString().padStart(2, '0');
            // Create the time string
            const hh_mm = `${formattedHour}h${formattedMinute}`;
            document.getElementById(hh_mm).textContent = "—"
        }
    }
}

async function refresh() {
    console.log(".refresh()");
    const sensor = metadata.sensor;
    const year = metadata.year;
    const [month, day] = metadata.month_day.split("-");

    await refreshDate(sensor, year, month, day);
}

async function refreshDate(sensor, year, month, day) {
    console.log(".refreshDate('" + sensor + "', '" + year + "', '" + month + "', '" + day + "')");
    await clearData();
    // Call fetchData function to get data after page loaded:
    await fetchData(sensor, year, month, day); // Wait for fetchData to complete
    console.log("\tafter fetchData call:", picturesData, metadata);
    const picturesFolder = "captures/" + metadata.sensor + "/";
    console.log("\tpicturesFolder =", picturesFolder);

    await fillPicturesSelector();
    console.log("picturesData = " + picturesData);
    if (lastDaylightHhMm !== undefined) {
        console.log("lastDaylightHhMm = " + lastDaylightHhMm);
        const pictureData = picturesData[lastDaylightHhMm];
        console.log("pictureData = ", pictureData)
        await updateCurrentImage(pictureData, lastDaylightHhMm);
    } else if (lastHhMm !== undefined) {
        const pictureData = picturesData[lastHhMm];
        await updateCurrentImage(pictureData, lastHhMm);
    } else {
        document.getElementById("error_message").textContent = "No pictures for this date!";
    }

    await updateDateData();
}

document.addEventListener("DOMContentLoaded", async function () {
    console.log("DOMContentLoaded - ---DOMContentLoaded-start---");
    // Get the current URL
    const currentUrl = new URL(window.location.href);
    // Extract parameters using URLSearchParams
    const paramSensor = currentUrl.searchParams.get("s");
    const paramYear = currentUrl.searchParams.get("y");
    const paramMonth = currentUrl.searchParams.get("m");
    const paramDay = currentUrl.searchParams.get("d");

    await refreshDate(paramSensor, paramYear, paramMonth, paramDay);

    console.log("DOMContentLoaded - ---DOMContentLoaded-end---");
});

console.log("---End---");
