const neededDivs = document.querySelectorAll("div")

const sound = new Audio()

var time;

for (const div of neededDivs) {
    const musicButton = div.querySelector("button")
    musicButton.addEventListener('click', playSound)

    let currDuration = div.querySelector("span[value='current-duration']")
    let songDuration = div.querySelector("span[value='song-duration']")

    function change_duration_of_song() {
        let currentDurationArray = currDuration.textContent.split(":").map(Number)
        let songDurationArray = songDuration.textContent.split(":").map(Number)
        
        if (currentDurationArray[2] === 59) {
            currentDurationArray[2] = 0
            if (currentDurationArray[1] === 59) {
                currentDurationArray[1] = 0
                currentDurationArray[0] = currentDurationArray[0] + 1
            } else {
                currentDurationArray[1] = currentDurationArray[1] + 1
            }
        } else {
            currentDurationArray[2] = currentDurationArray[2] + 1
        }

        currDuration.textContent = currentDurationArray.join(":")

        if (currDuration.textContent === songDuration.textContent) {
            musicButton.textContent = "Play"
            currDuration.textContent = "0:0:0"

            clearInterval(time)
        }
    }

    function playSound() {

        if (musicButton.textContent === "Play") {
            sound.pause()
            sound.src = div.getAttribute("value")
            sound.play()
            time = setInterval(change_duration_of_song, 1000)
            musicButton.textContent = "Stop"
        } else if (musicButton.textContent === "Stop") {
            sound.src = div.getAttribute("value")
            clearInterval(time)
            sound.pause()
            musicButton.textContent = "Play"
            currDuration.textContent = "0:0:0"
        }
        

    }
}