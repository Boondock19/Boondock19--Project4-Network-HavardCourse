
console.log("ESTA VAINA SI CARGA ALO?")
followButton=document.querySelector("#followButton");
followButton.addEventListener("click", function () {
    OwnerOfProfile=followButton.getAttribute("data-ownerofprofile");
    follows=followButton.textContent.trim();
    console.log(OwnerOfProfile)
    console.log(follows)
    form = new FormData();
    form.append("follows",follows);
    fetch(`${OwnerOfProfile}`, {
        method: "POST",
        body: form,
      })
        .then((res) => res.json())
        .then((res) => {
          console.log("Entro en la promesa")
          followButton.textContent = res.follows;
          document.querySelector(
            "#followerscount"
          ).textContent = ` ${res.followerscount}`;
          console.log("leyo toda la promesa")
        });
});

console.log("LEYO TODO, TODO BIEN EN CASA?")
