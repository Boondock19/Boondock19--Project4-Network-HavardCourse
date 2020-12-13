document.addEventListener("DOMContentLoaded", function () {
like=document.querySelectorAll(".Likebtn")
like.forEach(element => {
    element.addEventListener("click", function () {
        GetPost=element.getAttribute("data-post_id");
        console.log(GetPost)
        Post_Liked=element.getAttribute("data-Liked")
        console.log(Post_Liked)
        Postbtn=document.querySelector(`#like-btn-${GetPost}`);
        CountLikes=document.querySelector(`#like-count-${GetPost}`);
        var Count=Number(CountLikes.textContent);
        console.log(Count)
        Liked(GetPost,Post_Liked)
        
       })

    })
});



function Liked (id,Liked) {
    form = new FormData();
    form.append("id",id);
    form.append("Liked",Liked);
    fetch("/Liked/", {
        method:"POST",
        body:form,
    })
    .then((res) => res.json())
    .then((res) => {
        if (res.Liked=="yes") {
            btn=document.querySelector(`#like-btn-${id}`)
            btn.setAttribute("data-Liked","yes")
            document.querySelector(`#like-btn-${id}`).textContent="Dislike";
            document.querySelector(`#like-count-${id}`).textContent=res.CountLiked

        } else if (res.Liked=="no") {
            btn=document.querySelector(`#like-btn-${id}`)
            btn.setAttribute("data-Liked","no")
            document.querySelector(`#like-btn-${id}`).textContent="Like";
            document.querySelector(`#like-count-${id}`).textContent=res.CountLiked 
        }
    })

}