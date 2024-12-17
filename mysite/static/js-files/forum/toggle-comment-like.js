const commentDivs = document.getElementsByClassName("comment")

for (const commentDiv of commentDivs) {
    const commentLikes = commentDiv.querySelector("span[value='comment_likes']")
    const likeCommentButton = commentDiv.querySelector("span[class='like-comment']")
    const likeCommentUrl = `${window.location.origin}/forum-page/post/${document.querySelector("span[value='post-likes']").id}/like/${commentLikes.id}/`

    likeCommentButton.addEventListener("click", () => {
        fetch(likeCommentUrl)
            .then(response => response.json())
            .then(data => {

                if (data.status === 403) {

                    window.location.href = data.redirect_url;

                } else {

                    commentDiv.querySelector("span[value='comment_likes']").textContent = data.likes_count
                
                    if (likeCommentButton.textContent == "Like") likeCommentButton.textContent = "Unlike"
                    else likeCommentButton.textContent = "Like"
                    
                }

            })
    })
}