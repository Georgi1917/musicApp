const musicDivs = document.querySelectorAll("div")
const playAllButton = document.getElementById("play-all")

playAllButton.addEventListener("click", () => {
    let currIndex = 0

    while (currIndex < musicDivs.length) {
        const neededSound = new Audio(musicDivs[currIndex].getAttribute("value"))

        neededSound.play()

        neededSound.addEventListener("ended", () => {
            currIndex += 1
        })
    }
})