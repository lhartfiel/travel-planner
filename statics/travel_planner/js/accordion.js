let accordionLink = document.querySelectorAll('.cnt__accord-link');

if(accordionLink.length > 0) {
    accordionLink.forEach( (link) => {
        link.addEventListener('click', function(){
            console.log(link.parentElement.classList)
            if(link.parentNode.classList.contains('item-cnt')) {
                link.parentElement.parentElement.classList.toggle('active');
            } else {
                link.parentElement.classList.toggle('active');
            }
        })
    })
}