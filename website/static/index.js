function removeNote(noteId){
    fetch('/delete-note',{
        method: 'POST',
        body: JSON.stringify({ noteId: noteId})
    }).then((data) =>{
        window.location.href = "/"
    })}

const btn = document.querySelector('button.mobile-menu-button');
const menu = document.querySelector('.mobile-menu');
btn.addEventListener('click', () => {menu.classList.toggle("hidden");});