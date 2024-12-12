const playAllButton = document.getElementById("play-all");

var changeTime;

const allAudioFiles = []
const newAudio = new Audio()
let currAudioIndex = 0

for (const d of neededDivs) {
    
    allAudioFiles.push(d)
    
}

function change_duration_for_current_song(currentDuration, totalDuration, volumeControl) {
    let currDurationArray = currentDuration.textContent.split(":").map(Number)
        
    if (currDurationArray[2] === 59) {
        currDurationArray[2] = 0
        if (currDurationArray[1] === 59) {
            currDurationArray[1] = 0
            currDurationArray[0] = currDurationArray[0] + 1
        } else {
            currDurationArray[1] = currDurationArray[1] + 1
        }
    } else {
        currDurationArray[2] = currDurationArray[2] + 1
    }

    currentDuration.textContent = currDurationArray.join(":")

    if (currentDuration.textContent === totalDuration.textContent) {
        currentDuration.textContent = "0:0:0"
        volumeControl.disabled = true
        volumeControl.value = 0.5

        clearInterval(changeTime)
    }
}

function loadTrack(index) {
    
    newAudio.src = allAudioFiles[index].getAttribute("value");

    index + 1 >= allAudioFiles.length ? currAudioIndex = 0 : currAudioIndex++; 

}

function playNextTrack() {

    const currDiv = allAudioFiles[currAudioIndex]

    const currDuration = currDiv.querySelector("span[value='current-duration']")
    const totalDuration = currDiv.querySelector("span[value='song-duration']")
    const volumeControl = currDiv.querySelector("input")
    volumeControl.disabled = false

    loadTrack(currAudioIndex)
    normalize_audio(newAudio, volumeControl.value)
    changeVolume(newAudio, volumeControl)

    changeTime = setInterval(change_duration_for_current_song, 1000, ...[currDuration, totalDuration, volumeControl])

    newAudio.play()
    
}

playAllButton.addEventListener("click", () => {

    if (playAllButton.textContent == "Play Playlist") {
        newAudio.addEventListener("ended", playNextTrack)
        playNextTrack();
        playAllButton.textContent = "Stop Playlist"
    } else {
        newAudio.pause()
        clearInterval(changeTime)
        allAudioFiles[currAudioIndex === 0 ? allAudioFiles.length - 1 : currAudioIndex - 1].querySelector("span[value='current-duration']").textContent = "0:0:0"
        allAudioFiles[currAudioIndex === 0 ? allAudioFiles.length - 1 : currAudioIndex - 1].querySelector("input").disabled = true
        allAudioFiles[currAudioIndex === 0 ? allAudioFiles.length - 1 : currAudioIndex - 1].querySelector("input").value = 0.5
        currAudioIndex = 0
        playAllButton.textContent = "Play Playlist"
    }
    
})