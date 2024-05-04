const open_slide_menu = document.getElementById('open-slide-menu')
const btn_close = document.querySelector('.btn-close')
const main_menu = document.getElementById('main-menu')
const side_menu = document.getElementById('side-menu')
const sub_menu =  document.querySelector('.sub-menu')
const main = document.querySelector('.main')
const navbar_nav = document.getElementById('navbar-nav')

open_slide_menu.addEventListener('click', () => {
    // side_menu.style.width = '250px'
    // main.style.marginLeft = '250px'
    // navbar_nav.style.marginLeft = '250px'

    side_menu.classList.toggle('slide-nav-active')
    main.classList.toggle('main-active')
})

// btn_close.addEventListener('click', () => {
//     side_menu.style.width = '50px'
//     main.style.marginLeft = '0'
//     navbar_nav.style.marginLeft = '0'
// })

main_menu.addEventListener('click', () => {
    // sub_menu.style.display = 'block'
    sub_menu.classList.toggle('sub-menu-active')
})

// const toggleSlideMenu = () => {
//     side_menu.classList.toggle('small-slide-menu')
// }
