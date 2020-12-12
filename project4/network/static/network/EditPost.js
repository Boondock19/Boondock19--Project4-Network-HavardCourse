document.addEventListener("DOMContentLoaded", function () {
    edit=document.querySelectorAll(".EditPost")
    console.log("Cargo el script")
    console.log(edit)
    edit.forEach((element) => {
        element.addEventListener("click", function () {
        GetPost=element.getAttribute("data-post_id");
        EditPostBtn=document.querySelector(`#editpost-${  GetPost }`);
        console.log(GetPost)
        if (EditPostBtn.textContent == "Edit"){
            
            Contend_of_Post=document.querySelector(`#p_text_contend_${  GetPost }`)
            Texarea_of_Post=document.querySelector(`#texarea_text_contend_${  GetPost }`)
            Contend_of_Post.style.diplay="none";
            Texarea_of_Post.style.display="block";
            EditPostBtn.textContent="Save"
            EditPostBtn.setAttribute("class","btn btn-success SavePost")
        } else if (EditPostBtn.textContent == "Save") {
            EditPost(GetPost,Texarea_of_Post.value)
            EditPostBtn.textContent="Edit"
            EditPostBtn.setAttribute("class","btn btn-warning EditPost")
           }
        })
    })  
})

function EditPost(id,content) {
    form= new FormData();
    form.append("id",id);
    form.append("content",content);
    fetch("/EditPost/",{
        method:"POST",
        body:form,
    }).then((res) =>{
        document.querySelector(`#p_text_contend_${id}`).textContent=content
        document.querySelector(`#p_text_contend_${id}`).style.display="block"
        document.querySelector(`#texarea_text_contend_${id}`).style.display="none"
        document.querySelector(`#texarea_text_contend_${id}`).value =content.trim();
    })
}