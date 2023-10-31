console.log("---Start---");
const SIZE_LIMIT = 512000;

let current_image = "XXXXXXX";
let sensorName = "-sensor-";
let year = 2099;
let month = 0;
let day = 0;
let hour = 0;
let minute = 0;

document.addEventListener("DOMContentLoaded", function () {
    console.log("---DOMContentLoaded-start---");

    const imageData = {
        "00h00": {fSize: 46661, img: "tilleul_2020-12-29Z00-00-08.jpg"},
        "00h15": {fSize: 46673, img: "tilleul_2020-12-29Z00-15-08.jpg"},
        "00h30": {fSize: 46603, img: "tilleul_2020-12-29Z00-30-08.jpg"},
        "00h45": {fSize: 46601, img: "tilleul_2020-12-29Z00-45-08.jpg"},
        "01h00": {fSize: 46731, img: "tilleul_2020-12-29Z01-00-08.jpg"},
        "01h15": {fSize: 46766, img: "tilleul_2020-12-29Z01-15-08.jpg"},
        "01h30": {fSize: 46678, img: "tilleul_2020-12-29Z01-30-08.jpg"},
        "01h45": {fSize: 46473, img: "tilleul_2020-12-29Z01-45-08.jpg"},
        "02h00": {fSize: 46595, img: "tilleul_2020-12-29Z02-00-08.jpg"},
        "02h15": {fSize: 46652, img: "tilleul_2020-12-29Z02-15-08.jpg"},
        "02h30": {fSize: 46627, img: "tilleul_2020-12-29Z02-30-08.jpg"},
        "02h45": {fSize: 46534, img: "tilleul_2020-12-29Z02-45-08.jpg"},
        "03h00": {fSize: 46610, img: "tilleul_2020-12-29Z03-00-09.jpg"},
        "03h15": {fSize: 46596, img: "tilleul_2020-12-29Z03-15-08.jpg"},
        "03h30": {fSize: 46689, img: "tilleul_2020-12-29Z03-30-08.jpg"},
        "03h45": {fSize: 46683, img: "tilleul_2020-12-29Z03-45-08.jpg"},
        "04h00": {fSize: 46603, img: "tilleul_2020-12-29Z04-00-08.jpg"},
        "04h15": {fSize: 46516, img: "tilleul_2020-12-29Z04-15-09.jpg"},
        "04h30": {fSize: 46585, img: "tilleul_2020-12-29Z04-30-08.jpg"},
        "04h45": {fSize: 46519, img: "tilleul_2020-12-29Z04-45-08.jpg"},
        "05h00": {fSize: 46648, img: "tilleul_2020-12-29Z05-00-08.jpg"},
        "05h15": {fSize: 46638, img: "tilleul_2020-12-29Z05-15-08.jpg"},
        "05h30": {fSize: 46593, img: "tilleul_2020-12-29Z05-30-08.jpg"},
        "05h45": {fSize: 46661, img: "tilleul_2020-12-29Z05-45-08.jpg"},
        "06h00": {fSize: 46631, img: "tilleul_2020-12-29Z06-00-08.jpg"},
        "06h15": {fSize: 46609, img: "tilleul_2020-12-29Z06-15-09.jpg"},
        "06h30": {fSize: 46533, img: "tilleul_2020-12-29Z06-30-08.jpg"},
        "06h45": {fSize: 46641, img: "tilleul_2020-12-29Z06-45-08.jpg"},
        "07h00": {fSize: 46604, img: "tilleul_2020-12-29Z07-00-08.jpg"},
        "07h15": {fSize: 108528, img: "tilleul_2020-12-29Z07-15-08.jpg"},
        "07h30": {fSize: 791501, img: "tilleul_2020-12-29Z07-30-08.jpg"},
        "07h45": {fSize: 1087651, img: "tilleul_2020-12-29Z07-45-08.jpg"},
        "08h00": {fSize: 1093435, img: "tilleul_2020-12-29Z08-00-08.jpg"},
        "08h15": {fSize: 1116305, img: "tilleul_2020-12-29Z08-15-08.jpg"},
        "08h30": {fSize: 1160192, img: "tilleul_2020-12-29Z08-30-08.jpg"},
        "08h45": {fSize: 1153000, img: "tilleul_2020-12-29Z08-45-08.jpg"},
        "09h00": {fSize: 1116201, img: "tilleul_2020-12-29Z09-00-08.jpg"},
        "09h15": {fSize: 1186726, img: "tilleul_2020-12-29Z09-15-08.jpg"},
        "09h30": {fSize: 1119104, img: "tilleul_2020-12-29Z09-30-08.jpg"},
        "09h45": {fSize: 1109490, img: "tilleul_2020-12-29Z09-45-08.jpg"},
        "10h00": {fSize: 1143556, img: "tilleul_2020-12-29Z10-00-08.jpg"},
        "10h15": {fSize: 1162086, img: "tilleul_2020-12-29Z10-15-11.jpg"},
        "10h30": {fSize: 1179178, img: "tilleul_2020-12-29Z10-30-09.jpg"},
        "10h45": {fSize: 1170136, img: "tilleul_2020-12-29Z10-45-09.jpg"},
        "11h00": {fSize: 1138029, img: "tilleul_2020-12-29Z11-00-08.jpg"},
        "11h15": {fSize: 1187628, img: "tilleul_2020-12-29Z11-15-08.jpg"},
        "11h30": {fSize: 1142732, img: "tilleul_2020-12-29Z11-30-08.jpg"},
        "11h45": {fSize: 1195062, img: "tilleul_2020-12-29Z11-45-08.jpg"},
        "12h00": {fSize: 1113049, img: "tilleul_2020-12-29Z12-00-08.jpg"},
        "12h15": {fSize: 1147729, img: "tilleul_2020-12-29Z12-15-08.jpg"},
        "12h30": {fSize: 1048152, img: "tilleul_2020-12-29Z12-30-08.jpg"},
        "12h45": {fSize: 1007747, img: "tilleul_2020-12-29Z12-45-08.jpg"},
        "13h00": {fSize: 1116413, img: "tilleul_2020-12-29Z13-00-08.jpg"},
        "13h15": {fSize: 1160091, img: "tilleul_2020-12-29Z13-15-08.jpg"},
        "13h30": {fSize: 1114134, img: "tilleul_2020-12-29Z13-30-08.jpg"},
        "13h45": {fSize: 1131524, img: "tilleul_2020-12-29Z13-45-08.jpg"},
        "14h00": {fSize: 1101222, img: "tilleul_2020-12-29Z14-00-08.jpg"},
        "14h15": {fSize: 1057128, img: "tilleul_2020-12-29Z14-15-08.jpg"},
        "14h30": {fSize: 926505, img: "tilleul_2020-12-29Z14-30-09.jpg"},
        "14h45": {fSize: 917604, img: "tilleul_2020-12-29Z14-45-08.jpg"},
        "15h00": {fSize: 947831, img: "tilleul_2020-12-29Z15-00-09.jpg"},
        "15h15": {fSize: 923159, img: "tilleul_2020-12-29Z15-15-08.jpg"},
        "15h30": {fSize: 1067316, img: "tilleul_2020-12-29Z15-30-08.jpg"},
        "15h45": {fSize: 1048425, img: "tilleul_2020-12-29Z15-45-08.jpg"},
        "16h00": {fSize: 1074060, img: "tilleul_2020-12-29Z16-00-08.jpg"},
        "16h15": {fSize: 1063189, img: "tilleul_2020-12-29Z16-15-08.jpg"},
        "16h30": {fSize: 881359, img: "tilleul_2020-12-29Z16-30-08.jpg"},
        "16h45": {fSize: 135116, img: "tilleul_2020-12-29Z16-45-08.jpg"},
        "17h00": {fSize: 51957, img: "tilleul_2020-12-29Z17-00-08.jpg"},
        "17h15": {fSize: 51516, img: "tilleul_2020-12-29Z17-15-08.jpg"},
        "17h30": {fSize: 51687, img: "tilleul_2020-12-29Z17-30-08.jpg"},
        "17h45": {fSize: 51324, img: "tilleul_2020-12-29Z17-45-08.jpg"},
        "18h00": {fSize: 51538, img: "tilleul_2020-12-29Z18-00-08.jpg"}/*,
                "18h15": {fSize: 51325, img: "tilleul_2020-12-29Z18-15-08.jpg"},
                "18h30": {fSize: 52295, img: "tilleul_2020-12-29Z18-30-08.jpg"},
                "18h45": {fSize: 52862, img: "tilleul_2020-12-29Z18-45-08.jpg"},
                "19h00": {fSize: 52527, img: "tilleul_2020-12-29Z19-00-08.jpg"},
                "19h15": {fSize: 52930, img: "tilleul_2020-12-29Z19-15-08.jpg"},
                "19h30": {fSize: 53194, img: "tilleul_2020-12-29Z19-30-08.jpg"},
                "19h45": {fSize: 52433, img: "tilleul_2020-12-29Z19-45-08.jpg"},
                "20h00": {fSize: 46629, img: "tilleul_2020-12-29Z20-00-09.jpg"},
                "20h15": {fSize: 53649, img: "tilleul_2020-12-29Z20-15-08.jpg"},
                "20h30": {fSize: 52832, img: "tilleul_2020-12-29Z20-30-08.jpg"},
                "20h45": {fSize: 52934, img: "tilleul_2020-12-29Z20-45-08.jpg"},
                "21h00": {fSize: 52507, img: "tilleul_2020-12-29Z21-00-08.jpg"},
                "21h15": {fSize: 52917, img: "tilleul_2020-12-29Z21-15-08.jpg"},
                "21h30": {fSize: 52495, img: "tilleul_2020-12-29Z21-30-09.jpg"},
                "21h45": {fSize: 52760, img: "tilleul_2020-12-29Z21-45-08.jpg"},
                "22h00": {fSize: 52590, img: "tilleul_2020-12-29Z22-00-11.jpg"},
                "22h15": {fSize: 52538, img: "tilleul_2020-12-29Z22-15-08.jpg"},
                "22h30": {fSize: 52606, img: "tilleul_2020-12-29Z22-30-08.jpg"},
                "22h45": {fSize: 52790, img: "tilleul_2020-12-29Z22-45-11.jpg"},
                "23h00": {fSize: 52672, img: "tilleul_2020-12-29Z23-00-08.jpg"},
                "23h15": {fSize: 52675, img: "tilleul_2020-12-29Z23-15-08.jpg"},
                "23h30": {fSize: 52871, img: "tilleul_2020-12-29Z23-30-08.jpg"},
                "23h45": {fSize: 52755, img: "tilleul_2020-12-29Z23-45-08.jpg"} */
    };

    // Function to update the current_image element
    function updateCurrentImage(data) {
        console.log("---updateCurrentImage(" + data + ")---");
        const fSize = data.fSize;
        //console.log("fSize: " + fSize);

        const currentImage = data.img

        // Change the src attribute of the main image
        document.getElementById("capture-img").src = "capture/tilleul/2020/12-29/" + currentImage;

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
                console.log("addEventListener: '" + identif + "' -> '" + data + "'")
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
                console.log("No 'data' for identif '" + identif + "'.");
                document.getElementById(identif).style.backgroundColor = "DarkGray";
                document.getElementById(identif).style.cursor = "default";
                /* add "cursor: pointer;" */
            }
        }
    }
    console.log("---DOMContentLoaded-end---");
});
console.log("---End---");
