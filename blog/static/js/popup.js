//write a javascript fuction that displays a popup on a button click
const postpopup = () => {
    const popup = document.querySelector(".fixed");
    const button = document.querySelector("#delete-post");

    button.addEventListener("click", () => {
    popup.style.display = "flex";
    });
}

const categorypopup = () => { 
    const popup = document.querySelector(".fixed");
    const button = document.querySelector("#delete-category");

    button.addEventListener("click", () => {
        popup.style.display = "flex";
    });
}

