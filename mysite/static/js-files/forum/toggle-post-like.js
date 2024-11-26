const likeDivs = document.getElementsByClassName("post")

for (const div of likeDivs) {
    const postId = div.querySelector("span[value='post-likes']").id;
    const likeUrl = `${window.location.origin}/forum-page/post/${postId}/like/`
    const likeButton = div.querySelector("span[class='like-button']");
    
    likeButton.addEventListener("click", () => {
        fetch(likeUrl)
            .then(response => response.json())
            .then(data => {
                
                document.getElementById(postId).textContent = data.likes_count;

                if (likeButton.textContent === "Like") likeButton.textContent = "Unlike";
                else likeButton.textContent = "Like";

            })
    })
}