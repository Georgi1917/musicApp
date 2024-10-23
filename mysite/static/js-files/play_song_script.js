const neededDivs = document.querySelectorAll("div")

const sound = new Audio()

var time;

function set_button_to_normal() {
    for (const neededDiv of neededDivs) {
        const mButton = neededDiv.querySelector("button")
        let curDuration = neededDiv.querySelector("span[value='current-duration']")
        mButton.textContent = "Play"
        curDuration.textContent = "0:0:0"
    }
}

for (const div of neededDivs) {
    const musicButton = div.querySelector("button")
    const volumeCont = div.querySelector("input")
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
            set_button_to_normal()
            clearInterval(time)
            sound.src = div.getAttribute("value")
            normalize_audio(sound)
            changeVolume(sound, volumeCont)
            console.log(sound.volume)
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