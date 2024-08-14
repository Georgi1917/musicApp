const musicDivs = document.querySelectorAll("div")
const playAllButton = document.getElementById("play-all")

var t;

playAllButton.addEventListener("click", () => {
    let currIndex = 0
    const neededAudio = new Audio()

    function change_duration(pDuration, tDuration) {
        let presentDurationArray = pDuration.textContent.split(":").map(Number)
        let totalDurationArray = tDuration.textContent.split(":").map(Number)
        
        if (presentDurationArray[2] === 59) {
            presentDurationArray[2] = 0
            if (presentDurationArray[1] === 59) {
                presentDurationArray[1] = 0
                presentDurationArray[0] = presentDurationArray[0] + 1
            } else {
                presentDurationArray[1] = presentDurationArray[1] + 1
            }
        } else {
            presentDurationArray[2] = presentDurationArray[2] + 1
        }

        pDuration.textContent = presentDurationArray.join(":")

        if (pDuration.textContent === tDuration.textContent) {
            pDuration.textContent = "0:0:0"

            clearInterval(t)
        }
    }

    function playNext() {
        if (currIndex < musicDivs.length) {
            const currentDiv = musicDivs[currIndex]
            const presentDuration = currentDiv.querySelector("span[value='current-duration']")
            const totalDuration = currentDiv.querySelector("span[value='song-duration']")
            neededAudio.src = currentDiv.getAttribute("value")

            if (playAllButton.textContent === "Play Playlist") {
                neededAudio.pause()
                neededAudio.play();
                t = setInterval(change_duration, 1000, pDuration=presentDuration, tDuration=totalDuration)
                playAllButton.textContent = "Stop Playlist"
                currIndex++;
            }
        }
    }

    neededAudio.addEventListener("ended", playNext);

    playNext();
})